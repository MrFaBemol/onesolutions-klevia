from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class DbmServer(models.Model):
    _name = "dbm.server"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Database Server"

    name = fields.Char(required=True)
    category_id = fields.Many2one("dbm.category", required=True, ondelete="restrict")
    hosting_id = fields.Many2one("dbm.hosting", required=True, ondelete="restrict", domain="[('category_id', '=', category_id)]")

