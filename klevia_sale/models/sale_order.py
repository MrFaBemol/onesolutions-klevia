from odoo import api,fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    include_sow = fields.Boolean(string="Include Statement of Work")
    statement_of_work = fields.Html(string="Statement of Work")
    partner_arr_history_amount_total = fields.Float(related="partner_id.arr_history_amount_total")

    total_hours = fields.Integer(
        string="Total hours",
        compute="_compute_total_hours_days",
        store=True,
    )
    total_days = fields.Float(
        string="Total days",
        compute="_compute_total_hours_days",
        store=True,
    )

    @api.depends('order_line.product_uom_qty', 'order_line.product_uom')
    def _compute_total_hours_days(self):
        uom_hour = self.env.ref('uom.product_uom_hour')
        uom_categ_wtime = self.env.ref('uom.uom_categ_wtime')

        for order in self:
            total = 0.0
            for line in order.order_line:
                if line.product_uom.category_id == uom_categ_wtime:
                    # conversion automatique vers heures
                    qty_in_hours = line.product_uom._compute_quantity(line.product_uom_qty, uom_hour)
                    total += qty_in_hours
            order.total_hours = total
            order.total_days = round((total / 8) * 4) / 4

    def action_pdf_preview(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': "/report/pdf/sale.report_saleorder/%s" % self.id,
            'target': 'new'
        }

    @api.depends('sale_order_template_id')
    def _compute_payment_term_id(self):
        res = super()._compute_payment_term_id()
        for order in self.filtered('sale_order_template_id'):
            if order.sale_order_template_id.payment_term_id:
                order.payment_term_id = order.sale_order_template_id.payment_term_id
        return res
