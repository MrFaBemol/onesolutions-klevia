from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    include_sow = fields.Boolean(string="Include Statement of Work")
    statement_of_work = fields.Html(string="Statement of Work")

