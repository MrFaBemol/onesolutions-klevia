from odoo import fields, models, _
from odoo.exceptions import ValidationError


class DbmCategory(models.Model):
    _name = "dbm.category"
    _inherit = ["mail.thread", "mail.activity.mixin", "protected.record.mixin"]
    _description = "Database Category"

    name = fields.Char(required=True, tracking=True)
    hosting_ids = fields.One2many("dbm.hosting", "category_id", string="Available Hostings")
    company_id = fields.Many2one("res.company", string="Company")
