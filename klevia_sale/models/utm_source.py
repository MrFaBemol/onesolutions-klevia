from odoo import fields, models


class UtmSource(models.Model):
    _inherit = "utm.source"
    _order = "sequence"

    active = fields.Boolean(default=True)
    sequence = fields.Integer('Sequence', default=100)
    color = fields.Selection(
        selection=[
            ('grey', 'Grey'),
            ("green", "Green"),
            ("yellow", "Yellow"),
            ("red", "Red"),
            ("blue", "Blue"),
        ],
        default='grey',
        required=True,
    )

