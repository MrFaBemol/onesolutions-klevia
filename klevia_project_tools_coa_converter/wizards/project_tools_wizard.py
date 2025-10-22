from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class ProjectToolsWizard(models.TransientModel):
    _inherit = "project.tools.wizard"

    def open_coa_converter(self):
        return {
            "name": _("Chart of accounts converter"),
            "type": 'ir.actions.act_window',
            "res_model": 'project.tools.coa.converter.wizard',
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
            },
        }
