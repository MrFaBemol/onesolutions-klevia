from odoo import models, fields


class DbmRequestLine(models.Model):
    _name = "dbm.request.line"
    _description = "DBM Development Estimation Line"
    _order = "id asc"

    request_id = fields.Many2one(
        "dbm.request",
        required=True,
        ondelete="cascade",
    )

    line_type = fields.Selection(
        selection=[
            ("model", "Data Model"),
            ("logic", "Business Logic"),
            ("view", "Views"),
            ("security", "Security"),
            ("report", "Reports"),
            ("owl", "OWL / JS"),
        ],
        required=True,
    )

    description = fields.Char(required=True)
    time_estimated = fields.Float(string="Estimated Time (h)", required=True)
