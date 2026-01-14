from odoo import api, fields, models, _
from odoo.exceptions import UserError

from otools_rpc.external_api import Environment
from loguru import logger as loguru_logger


class DbmInstance(models.Model):
    _inherit = "dbm.instance"

    remote_user_ids = fields.One2many("dbm.instance.user", "instance_id", string="Users")

    # --------------------------------------------------
    # RPC connection fields
    # --------------------------------------------------

    api_dbname = fields.Char(string="Database Name", tracking=True)
    api_username = fields.Char(string="RPC Username", tracking=True)
    api_password = fields.Char(string="RPC Password", tracking=False)
    api_last_test_date = fields.Datetime(string="Last Connection Test", readonly=True)
    api_last_test_success = fields.Boolean(string="Last Connection OK", readonly=True)

    # --------------------------------------------------
    # RPC helpers
    # --------------------------------------------------

    def _get_api_environment(self):
        """
        Returns an otools_rpc Environment instance.
        Raises UserError if configuration is incomplete.
        """
        self.ensure_one()

        missing = []
        if not self.name:
            missing.append(_("RPC URL"))
        if not self.api_dbname:
            missing.append(_("Database Name"))
        if not self.api_username:
            missing.append(_("Username"))
        if not self.api_password:
            missing.append(_("Password"))

        if missing:
            raise UserError(
                _("Missing RPC configuration:\n- %s") % "\n- ".join(missing)
            )

        # Patch for otools_rpc 0.5.2 to be removed when library is updated
        if "FTRACE" in loguru_logger._core.levels:
            del loguru_logger._core.levels["FTRACE"]

        return Environment(
            self.name,
            self.api_username,
            self.api_password,
            self.api_dbname,
            cache_no_expiration=True,
        )

    # --------------------------------------------------
    # Actions
    # --------------------------------------------------

    def action_test_api_connection(self):
        self.ensure_one()

        try:
            env = self._get_api_environment()
            is_connected = env.user is not None and env.user.get('id')
            if not is_connected:
                raise UserError(_("Couldn't get an environment, please check credentials and logs."))

            self.write({
                "api_last_test_date": fields.Datetime.now(),
                "api_last_test_success": True,
            })

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Connection successful"),
                    "type": "success",
                    "sticky": False,
                }
            }

        except Exception as e:
            self.write({
                "api_last_test_date": fields.Datetime.now(),
                "api_last_test_success": False,
            })

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Connection failed"),
                    "message": str(e),
                    "type": "danger",
                    "sticky": False,
                }
            }

    def action_sync_users(self):
        for instance in self:
            instance._action_sync_users()

    def _action_sync_users(self):
        self.ensure_one()
        env = self._get_api_environment()

        try:
            remote_users = env["res.users"].search_read(
                [("active", "=", True)],
                ["id", "name", "login", "email", "phone"]
            )
        except Exception as e:
            raise UserError(_("Failed to fetch users: %s") % e)

        InstanceUser = self.env["dbm.instance.user"]

        existing_users = self.remote_user_ids
        existing_by_remote_id = {u.remote_user_id: u for u in existing_users}

        remote_ids = set()

        for ru in remote_users:
            remote_ids.add(ru.id)

            vals = {
                "instance_id": self.id,
                "remote_user_id": ru.id,
                "name": ru.name,
                "login": ru.login,
                "email": ru.email,
                "phone": ru.phone,
                "active_on_db": True,
            }

            if ru.id in existing_by_remote_id:
                existing_by_remote_id[ru.id].write(vals)
            else:
                InstanceUser.create(vals)

        # Users that existed before but are no longer returned by the remote API
        users_to_deactivate = existing_users.filtered(
            lambda u: u.remote_user_id not in remote_ids
        )
        users_to_deactivate.write({"active_on_db": False})

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Users synchronized"),
                "message": _(
                    "%s active users, %s deactivated."
                ) % (len(remote_ids), len(users_to_deactivate)),
                "type": "success",
            }
        }


    def action_create_users_in_crm(self):
        for instance in self:
            instance._action_create_users_in_crm()

    def _action_create_users_in_crm(self):
        self.ensure_one()

        Partner = self.env["res.partner"]
        created = 0
        linked = 0

        for remote_user in self.remote_user_ids.filtered(lambda u: u.email and not u.partner_id):
            partner = Partner.search([("email", "=", remote_user.email)], limit=1)

            if not partner:
                partner = Partner.create({
                    "name": remote_user.name,
                    "email": remote_user.email,
                    "phone": remote_user.phone,
                    "type": "contact",
                    "parent_id": self.partner_id.id
                })
                created += 1
            else:
                linked += 1

            remote_user.partner_id = partner.id

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("CRM synchronization completed"),
                "message": _(
                    "%s contacts created, %s linked."
                ) % (created, linked),
                "type": "success",
            }
        }
