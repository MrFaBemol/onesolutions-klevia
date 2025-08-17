from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    
    
    effective_time = fields.Float()
    add_commuting = fields.Boolean()

    @api.onchange('effective_time')
    def _onchange_effective_time(self):
        if self.effective_time:
            self.unit_amount = self.effective_time


