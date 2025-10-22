from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    section_id = fields.Many2one(compute="_compute_section_id")

    @api.depends('sequence')
    def _compute_section_id(self):
        for line in self:
            line.section_id = line.order_id.order_line.filtered(lambda l: l.sequence < line.sequence and l.display_type == 'line_section')[:-1]
