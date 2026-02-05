from odoo import api, fields, models, _
from odoo.exceptions import UserError


class DbmRequestWizard(models.TransientModel):
    _inherit = "dbm.request.wizard"
    _description = "Create Request Wizard"

    request_type = fields.Selection(
        selection_add=[("dev", "Development")],
        ondelete={"dev": "cascade"},
        default='dev',
    )
