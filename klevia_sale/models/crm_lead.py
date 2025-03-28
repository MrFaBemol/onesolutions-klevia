from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    source_color = fields.Selection(related='source_id.color')
