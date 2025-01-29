from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class NextflowMandateActivity(models.Model):
    _name = "nextflow.mandate.activity"
    _description = "nextflow.mandate.activity"


    name = fields.Char()
    odoo_id = fields.Integer()
    odoo_state = fields.Selection(
        selection=[
            ('overdue', 'Overdue'),
            ('today', 'Today'),
            ('planned', 'Planned'),
            ('done', 'Done'),
        ]
    )
