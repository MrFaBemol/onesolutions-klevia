from random import randint
from odoo import api, fields, models


class NextflowMandateTag(models.Model):
    _name = "nextflow.mandate.tag"
    _description = "nextflow.mandate.tag"

    @api.model
    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char()
    color = fields.Integer(default=_get_default_color)
