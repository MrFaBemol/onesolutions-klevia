from odoo import api,fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    include_sow = fields.Boolean(string="Include Statement of Work")
    statement_of_work = fields.Html(string="Statement of Work")
    partner_arr_history_amount_total = fields.Float(related="partner_id.arr_history_amount_total")

    def action_pdf_preview(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': "/report/pdf/sale.report_saleorder/%s" % self.id,
            'target': 'new'
        }

    @api.depends('sale_order_template_id')
    def _compute_payment_term_id(self):
        super()._compute_payment_term_id()
        for order in self.filtered('sale_order_template_id'):
            if order.sale_order_template_id.payment_term_id:
                order.payment_term_id = order.sale_order_template_id.payment_term_id
