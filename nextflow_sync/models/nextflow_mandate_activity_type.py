from odoo import api, fields, models, _


class NextflowMandateActivityType(models.Model):
    _name = "nextflow.mandate.activity.type"
    _description = "nextflow.mandate.activity.type"

    name = fields.Char()
    odoo_id = fields.Integer()
    mandate_id = fields.Many2one("nextflow.mandate")


