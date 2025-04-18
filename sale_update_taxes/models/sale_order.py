from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_tax_update_wizard(self):
        sale_order_lines = [{
            'sale_order_line_id': line.id,
            'order_id': line.order_id.id,
            'tax_ids': [(6, 0, line.tax_id.ids)],
            'product_id': line.product_id.id,
            'price_unit': line.price_unit,
            'is_update_tax': False
        } for line in self.order_line if line.display_type not in ['line_section', 'line_note']]
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'update.line.taxes.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': dict(default_sale_order_line_ids=[(0, 0, line) for line in sale_order_lines])
        }
