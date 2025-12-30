from odoo import fields, models


class DbmInstanceStage(models.Model):
    _name = "dbm.instance.stage"
    _inherit = ["protected.record.mixin"]
    _description = "Instance Stage"
    _order = "sequence, id"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True, translate=False)
    sequence = fields.Integer(default=10)
    fold = fields.Boolean(string="Folded in Kanban", default=False)
    decoration_type = fields.Selection(
        string="Color",
        selection=[
            ("success", "Green"),
            ("danger", "Red"),
            ("warning", "Yellow"),
            ("info", "Blue"),
            ("muted", "Grey"),
        ],
        default="muted",
    )

