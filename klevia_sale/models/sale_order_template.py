from odoo import api, fields, models


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Payment terms')
