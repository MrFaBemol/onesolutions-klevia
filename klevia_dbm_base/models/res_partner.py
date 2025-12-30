from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    database_ids = fields.One2many("dbm.instance", "partner_id", string="Databases")
