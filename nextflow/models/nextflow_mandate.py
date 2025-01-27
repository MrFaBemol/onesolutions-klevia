from odoo import fields, models


class NextflowMandate(models.Model):
    _name = "nextflow.mandate"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "NextFlow Mandate"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
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

    partner_id = fields.Many2one("res.partner", string="Client", ondelete="set null")
    url = fields.Char(required=True)
    subscription_code = fields.Char()
    show_subscription_code = fields.Boolean()

    user_id = fields.Many2one("res.users", string="Responsible", ondelete="restrict")
    date_from = fields.Date()
    date_to = fields.Date()
    tag_ids = fields.Many2many("nextflow.mandate.tag", string="Tags")

    note = fields.Html(string="Internal Notes")



    # --------------------------------------------
    #                   ACTIONS
    # --------------------------------------------

    def action_open_link(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.url,
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


    def action_show_subscription_code(self):
        self.show_subscription_code = True

    def action_hide_subscription_code(self):
        self.show_subscription_code = False
