from odoo import api, fields, models, _


class DbmRequest(models.Model):
    _name = "dbm.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Request"
    _order = "priority desc, create_date desc"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True, tracking=True)

    request_type = fields.Selection(
        selection=[
            ("install", "Installation"),
            ("upgrade", "Upgrade / Migration"),
            ("other", "Other"),
        ],
        required=True,
        default="other",
        tracking=True,
    )

    instance_id = fields.Many2one(
        "dbm.instance",
        string="Instance",
        required=True,
        ondelete="cascade",
        tracking=True,
    )
    instance_partner_id = fields.Many2one(related="instance_id.partner_id", store=True)

    user_id = fields.Many2one(
        "res.users",
        string="Assigned To",
        required=True,
        tracking=True,
        default=lambda self: self.env.user,
    )

    description = fields.Text(tracking=True)
    priority = fields.Selection([
        ('0', 'Low priority'),
        ('1', 'Medium priority'),
        ('2', 'High priority'),
        ('3', 'Urgent'),
    ], default='0', index=True, string="Priority", tracking=True)
    date_deadline = fields.Date(tracking=True)

    version_id = fields.Many2one(
        "dbm.version",
        string="Target Odoo Version",
        ondelete="restrict",
        tracking=True,
    )

    stage_id = fields.Many2one(
        "dbm.request.stage",
        string="Stage",
        required=True,
        default=lambda self: self._default_stage_id(),
        tracking=True,
        ondelete="restrict",
        group_expand="_group_expand_stage_id"
    )

    @api.model
    def _default_stage_id(self):
        stage = self.env["dbm.request.stage"].search([("active", "=", True)], order="sequence, id", limit=1)
        return stage.id

    @api.model
    def _group_expand_stage_id(self, stages, domain):
        return self.env["dbm.request.stage"].search([("active", "=", True)], order="sequence, id")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.name == _("Request"):
                rec.name = f"{rec.instance_id.display_name} - {dict(self._fields['request_type'].selection).get(rec.request_type)}"
        return records
