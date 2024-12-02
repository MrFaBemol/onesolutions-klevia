from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class DbmDatabase(models.Model):
    _name = "dbm.database"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Database"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True, string="URL")
    state = fields.Selection(
        selection=[
            ('0_setup', 'Setup'),
            ('10_in_use', 'In Use'),
            ('20_offline', 'Offline'),
            ('30_archived', 'Archived'),
        ],
        default='0_setup',
        tracking=True,
    )
    partner_id = fields.Many2one("res.partner", string="Contact", ondelete="set null")
    company_id = fields.Many2one("res.company", string="Company")
    category_company_id = fields.Many2one(related="category_id.company_id", string="Category company")

    category_id = fields.Many2one("dbm.category", required=True, ondelete="restrict")
    hosting_id = fields.Many2one("dbm.hosting", required=True, ondelete="restrict", domain="[('category_id', '=', category_id)]")
    server_id = fields.Many2one("dbm.server", required=True, ondelete="restrict", domain="[('hosting_id', '=', hosting_id)]")

    dummy_field = fields.Char()

    @api.onchange('category_id')
    def _onchange_category_id(self):
        self.hosting_id = False
        self.company_id = self.category_id.company_id or self.company_id

    @api.onchange('hosting_id')
    def _onchange_hosting_id(self):
        self.server_id = False


    # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------

    def action_open_link(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.name,
            'target': 'new',
        }

    def action_archive(self):
        self.active = False
        self.state = '30_archived'

    def action_unarchive(self):
        self.active = True
        self.state = '20_offline'

    def action_confirm_setup(self):
        self.state = '10_in_use'

    def action_take_offline(self):
        self.state = '20_offline'

    def action_take_online(self):
        self.state = '10_in_use'

    def action_reset_setup(self):
        self.state = '0_setup'