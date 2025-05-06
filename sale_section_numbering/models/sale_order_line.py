from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    section_number = fields.Integer(
        string='Section number',
        required=False)

    @api.model
    def create(self, values):
        # Add code here
        line = super(SaleOrderLine, self).create(values)
        if line.order_id and line.display_type == 'line_section':
            if line.order_id.first_section_number is not None:
                line.section_number = line.order_id.first_section_number
                line.order_id.first_section_number += 1

        return line
