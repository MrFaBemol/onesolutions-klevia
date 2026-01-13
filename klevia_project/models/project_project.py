from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = "project.project"

    def get_template_tasks(self):
        res = super().get_template_tasks()
        print("=====================================================")
        print(res)
        print("=====================================================")
        res = self.env['project.task'].search_read(
            [('id', '=', 4), ('is_template', '=', True)],
            ['id', 'name'],
        )
        print("=====================================================")
        print(res)
        print("=====================================================")
        return res
