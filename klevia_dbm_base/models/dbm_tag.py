from odoo import fields, models


class DbmTag(models.Model):
    _name = "dbm.tag"
    _description = "Instance Tag"
    _order = "name, id"

    name = fields.Char(required=True)
    color = fields.Integer(default=0)

    _dbm_tag_name_uniq = models.Constraint(
        'unique(name)',
        'This tag already exists.',
    )
