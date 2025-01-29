
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from otools_rpc.external_api import Environment
from loguru import logger as loguru_logger
import re
import logging
_logger = logging.getLogger(__name__)


class NextflowMandate(models.Model):
    _inherit = "nextflow.mandate"

    _sql_constraints = [
        ('check_sync_interval_value', 'CHECK(sync_interval_value > 0)', 'The frequency value for synchronization should be higher than 0.'),
    ]

    activate_sync = fields.Boolean()
    user_login = fields.Char()
    user_password = fields.Char(string="Password / API Key")
    database_name = fields.Char(compute="_compute_database_name", readonly=False, store=True, copy=False)
    credentials_state = fields.Selection(
        selection=[
            ('0_to_confirm', 'To confirm'),
            ('1_valid', 'Valid'),
            ('2_invalid', 'Invalid'),
        ],
        default='0_to_confirm',
        compute='_compute_credentials_state',
        readonly=False,
        store=True,
    )
    my_activity_action_odoo_id = fields.Integer(readonly=True)

    sync_interval_value = fields.Integer(default=4)
    sync_interval_unit = fields.Selection(
        selection=[
            ('minutes', 'Minutes'),
            ('hours', 'Hours'),
            ('days', 'Days'),
        ],
        default='hours',
    )
    next_sync = fields.Datetime(default=fields.Datetime.now, copy=False)
    last_sync = fields.Datetime(readonly=True, copy=False)
    mandate_lang_code = fields.Char(default='fr_CH', string='Language Code')


    # --- Activities

    available_activity_type_ids = fields.One2many("nextflow.mandate.activity.type", "mandate_id")

    inbox_type_ids = fields.Many2many("nextflow.mandate.activity.type", 'inbox_type_rel', string="Inbox", domain="[('id', 'in', available_activity_type_ids)]", copy=False)
    payroll_type_ids = fields.Many2many("nextflow.mandate.activity.type", 'payroll_type_rel', string="Payroll", domain="[('id', 'in', available_activity_type_ids)]", copy=False)
    accounting_type_ids = fields.Many2many("nextflow.mandate.activity.type", 'accounting_type_rel', string="Accounting", domain="[('id', 'in', available_activity_type_ids)]", copy=False)
    vat_type_ids = fields.Many2many("nextflow.mandate.activity.type", 'vat_type_rel', string="VAT", domain="[('id', 'in', available_activity_type_ids)]", copy=False)

    total_count = fields.Integer(readonly=True, copy=False)
    inbox_count = fields.Integer(readonly=True, copy=False)
    payroll_count = fields.Integer(readonly=True, copy=False)
    accounting_count = fields.Integer(readonly=True, copy=False)
    vat_count =fields.Integer(readonly=True, copy=False)



    @api.depends('url')
    def _compute_database_name(self):
        pattern = r'^(https?://)?(([^/]+\.)?nextflow\.ch)/?$'
        for mandate in self:
            match = re.match(pattern, mandate.url or "")
            mandate.database_name = match.group(2) if match else ""

    @api.depends('user_login', 'user_password', 'database_name', 'url')
    def _compute_credentials_state(self):
        for mandate in self:
            mandate.credentials_state = '0_to_confirm'

    # --------------------------------------------
    #                   MISC
    # --------------------------------------------

    def _get_env(self, update_state=False):
        self.ensure_one()
        if not all([self.url, self.user_login, self.user_password, self.database_name]):
            raise UserError(_('URL, username, password and database name are required to test credentials.'))

        # Patch for otools_rpc 0.5.2 to be removed when library is updated
        if "FTRACE" in loguru_logger._core.levels:
            del loguru_logger._core.levels["FTRACE"]

        env = Environment(
            url=self.url,
            db=self.database_name,
            username=self.user_login,
            password=self.user_password,
        )

        is_connected = env.user is not None and env.user.get('id')
        if update_state:
            self.credentials_state = '1_valid' if is_connected else '2_invalid'
        else:
            if not is_connected:
                raise UserError(_("Couldn't get an environment, please check credentials and logs."))

        return env.with_context(lang=self.mandate_lang_code)

    def _action_synchronize_activities(self):
        """ This actually synchronizes count for each activity category, not really activities """
        env = self._get_env()

        # I'll comment a bit to not be confused between env and id / odoo_id
        # Get the odoo ids (in the mandate database) of all used activity types.
        all_activity_types = self.inbox_type_ids | self.payroll_type_ids | self.accounting_type_ids | self.vat_type_ids
        odoo_type_ids = all_activity_types.mapped('odoo_id')

        # Ask for all overdue / today activities
        today = fields.Date.today()
        date_str = f"{today.year}-{today.month}-{today.day}"
        all_activities = env['mail.activity'].search_read([("date_deadline", "<=", date_str), ('activity_type_id', 'in', odoo_type_ids)], ['date_deadline', 'activity_type_id'])


        # Map odoo mandate type to count to get better performance after
        type_to_activity_count = defaultdict(int)
        for activity in all_activities:
            type_to_activity_count[activity.activity_type_id.id] += 1

        # Finally add up all activity by categories
        for category in ['inbox', 'payroll', 'accounting', 'vat']:
            category_count = 0
            for odoo_type in self[category + '_type_ids']:
                category_count += type_to_activity_count[odoo_type.odoo_id]
            self[category + '_count'] = category_count

        self.total_count = len(all_activities)

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success",
                "message": _("Synchronization done !"),
                "next": {"type": "ir.actions.act_window_close"},
                "sticky": False,
            }
        }




        # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------

    def action_test_credentials(self):
        env = self._get_env(update_state=True)

        if self.credentials_state == '1_valid':
            note_type = "success"
            note_message = _("All good !")
            self.my_activity_action_odoo_id = env.ref('mail.mail_activity_action_my').id
        else:
            note_type = "danger"
            note_message = _("Invalid credentials.")

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": note_type,
                "message": note_message,
                "next": {"type": "ir.actions.act_window_close"},
                "sticky": False,
            }
        }


    def action_synchronize_activity_types(self, env = None):
        env = env or self._get_env()

        existing_type_ids = self.available_activity_type_ids.mapped('odoo_id')
        mandate_activity_type_ids = env['mail.activity.type'].search_read([], fields=['name'])

        new_vals_list = [
            {
                'mandate_id': self.id,
                'odoo_id': activity_type.id,
                'name': activity_type.name,
            }
            for activity_type in mandate_activity_type_ids.filtered(lambda t: t.id not in existing_type_ids)
        ]
        self.env['nextflow.mandate.activity.type'].sudo().create(new_vals_list)

        deleted_ids = list(set(existing_type_ids) - set(mandate_activity_type_ids.ids))
        self.available_activity_type_ids.filtered_domain([('odoo_id', 'in', deleted_ids)]).sudo().unlink()


    def action_synchronize_activities(self):
        return self._action_synchronize_activities()


    def action_open_activities(self):
        self.ensure_one()
        if not all([self.url, self.credentials_state == '1_valid']):
            raise UserError(_('URL and valid credentials are required to access activities.'))
        if not self.my_activity_action_odoo_id:
            raise UserError(_('My activity odoo action id is required.'))

        base_url = self.url[:-1] if self.url[-1] == "/" else self.url
        full_url = base_url + f"/odoo/action-{self.my_activity_action_odoo_id}"
        return {
            'type': 'ir.actions.act_url',
            'url': full_url,
            'target': 'new',
        }
