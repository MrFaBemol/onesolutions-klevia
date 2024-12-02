from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class DbmHosting(models.Model):
    _name = "dbm.hosting"
    _description = "dbm.hosting"


    name = fields.Char(required=True)
    category_id = fields.Many2one("dbm.category", required=True, ondelete="cascade")

