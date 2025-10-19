from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = "crm.lead"

    partner_id = fields.Many2one(string="Customer")
    main_contact_id = fields.Many2one("res.partner", string="Contact ", domain="[('parent_id', '=', partner_id)]")

    odoo_consultant_id = fields.Many2one("res.users")
    onedrive_folder_url = fields.Char(string="OneDrive Folder")
