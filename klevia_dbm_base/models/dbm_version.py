from odoo import fields, models, _
from odoo.exceptions import ValidationError


class DbmVersion(models.Model):
    _name = "dbm.version"
    _inherit = ["protected.record.mixin"]
    _description = "Instance Version"
    _order = "name desc, id desc"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True, index=True)  # ex: 18.0, 18.3, 19.0

    _dbm_version_name_uniq = models.Constraint(
        'unique(name)',
        'This version already exists.',
    )
