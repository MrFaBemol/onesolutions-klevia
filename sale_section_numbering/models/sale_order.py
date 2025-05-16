from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    add_section_number = fields.Boolean(
        string='Section numbers',
        default=True)
    section_start_number = fields.Integer(
        string='First number')

    
    