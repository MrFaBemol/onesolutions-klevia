from odoo import fields, models


class DbmHosting(models.Model):
    _name = "dbm.hosting"
    _inherit = ["protected.record.mixin"]
    _description = "Hosting"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
    code = fields.Char(
        help="Technical code (e.g. odoo_com, odoo_sh, on_prem). Useful for logic.",
        index=True,
    )

    category_id = fields.Many2one("dbm.category", required=True, ondelete="cascade")

    is_on_premise = fields.Boolean(
        string="On-Premise",
        help="If enabled, instances on this hosting can store SSH/VPN details.",
        default=False,
    )
