from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_page_break = fields.Boolean(string='Page break', required=False,store=True)

