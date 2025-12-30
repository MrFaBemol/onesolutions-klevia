from odoo import fields, models


class DbmRequestStage(models.Model):
    _name = "dbm.request.stage"
    _inherit = ["protected.record.mixin"]
    _description = "Request Stage"
    _order = "sequence, id"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    fold = fields.Boolean(default=False)

