from odoo import fields, models


class DbmServer(models.Model):
    _name = "dbm.server"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Database Server"

    name = fields.Char(required=True, tracking=True)

    category_id = fields.Many2one("dbm.category", required=True, ondelete="restrict", tracking=True)
    hosting_id = fields.Many2one(
        "dbm.hosting",
        required=True,
        ondelete="restrict",
        domain="[('category_id', '=', category_id)]",
        tracking=True,
    )

    notes = fields.Text(string="Technical Notes")
