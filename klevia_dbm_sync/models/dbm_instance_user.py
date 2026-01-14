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




    # from passlib.context import CryptContext
    # from odoo import models, api
    #
    # pwd_context = CryptContext(
    #     schemes=["pbkdf2_sha512"],
    #     deprecated="auto",
    # )
    #
    # def check_api_key(self, user_id, api_key_plain):
    #     user = self.env['res.users'].browse(user_id)
    #     if not user.exists():
    #         return False
    #
    #     api_keys = self.env['res.users.apikeys'].search([
    #         ('user_id', '=', user.id),
    #         ('active', '=', True),
    #     ])
    #
    #     for key in api_keys:
    #         if pwd_context.verify(api_key_plain, key.key):
    #             return True
    #
    #     return False


