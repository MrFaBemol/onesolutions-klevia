from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    is_checked = fields.Boolean(string='Page break', required=False)

