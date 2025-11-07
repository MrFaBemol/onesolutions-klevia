from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class SaleOrderOption(models.Model):
    _inherit = "sale.order.option"

    total_price = fields.Float(digits='Product Price', compute='_compute_total_price', store=True, readonly=False)

    @api.depends('quantity', 'price_unit')
    def _compute_total_price(self):
        for option in self:
            option.total_price = option.price_unit * option.quantity
