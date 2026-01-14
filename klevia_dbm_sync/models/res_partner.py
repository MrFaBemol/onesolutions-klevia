from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)



class ResPartner(models.Model):
    _inherit = "res.partner"

    dbm_instance_user_ids = fields.One2many("dbm.instance.user", "partner_id")
    dbm_instance_ids = fields.Many2many("dbm.instance", compute="_compute_dbm_instance_ids")

    @api.depends('dbm_instance_user_ids')
    def _compute_dbm_instance_ids(self):
        for partner in self:
            partner.dbm_instance_ids = partner.dbm_instance_user_ids.instance_id

