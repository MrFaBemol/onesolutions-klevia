from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    include_sow = fields.Boolean(string="Include Statement of Work")
    statement_of_work = fields.Html(string="Statement of Work")

    def action_pdf_preview(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': "/report/pdf/sale.report_saleorder/%s" % self.id,
            'target': 'new'
        }
