from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    add_page_break_after = fields.Boolean(string='Page break', required=False, store=True)
