from odoo import models, fields
from odoo import api
from odoo.exceptions import UserError


class DbmInstanceUser(models.Model):
    _name = "dbm.instance.user"
    _description = "DBM Instance User"
    _order = "active_on_db desc, remote_user_id, name"

    _dbm_instance_user_uniq = models.Constraint(
        "unique(instance_id, remote_user_id)",
        "This user already exists for this instance.",
    )

    instance_id = fields.Many2one("dbm.instance", required=True, ondelete="cascade")
    remote_user_id = fields.Integer(required=True)
    name = fields.Char(required=True)
    login = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    active_on_db = fields.Boolean(default=True)
    partner_id = fields.Many2one("res.partner", ondelete="set null")



