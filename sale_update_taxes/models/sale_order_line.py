from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'SaleOrderLine'
    is_update_tax = fields.Boolean(string='Update', required=False)
