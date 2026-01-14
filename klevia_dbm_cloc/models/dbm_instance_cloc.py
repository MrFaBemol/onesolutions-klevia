from odoo import fields, models

class DbmInstanceCloc(models.Model):
    _name = "dbm.instance.cloc"
    _description = "Instance CLOC"

    instance_id = fields.Many2one("dbm.instance", required=True, ondelete="cascade", readonly=True)
    module_name = fields.Char(required=True, readonly=True)
    loc = fields.Integer(string="Lines of Code", required=True, readonly=True)
    include_in_cloc = fields.Boolean(default=True, string="Include")

