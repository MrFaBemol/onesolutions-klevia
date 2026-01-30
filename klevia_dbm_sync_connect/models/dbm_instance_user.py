from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import json


class DbmInstanceUser(models.Model):
    _inherit = "dbm.instance.user"

    def action_connect_as(self):
        self.ensure_one()
        secret = self.env['ir.config_parameter'].sudo().get_param('klevia_dbm_sync.secret')
        if not secret:
            raise UserError(_("Please set a secret in the system parameters (klevia_dbm_sync.secret)"))

        clean_url = self.instance_id.get_clean_url()
        token_endpoint_url = f"{clean_url}/onesolutions/api/connect/token"
        payload = {
            "uid": self.remote_user_id,
            "secret": secret,
            "emitter": self.env.user.login,
        }

        try:
            response = requests.post(
                token_endpoint_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
        except requests.exceptions.RequestException as e:
            raise UserError(_("Failed to call the endpoint, please check that the os_sync_connect module is installed on the database\n\n%s", e))

        if response.status_code != 200:
            raise UserError(_("Invalid response, status code : %s \n\nPlease check that the os_sync_connect module is installed on the database", response.status_code))

        try:
            data = response.json()
        except Exception:
            raise UserError(_("Invalid JSON response: %s", response.text))

        result = data.get('result')
        if not result.get('access_token'):
            raise UserError(_("No access token returned"))


        connect_url = f"{clean_url}/onesolutions/api/connect/{result.get('access_token')}"
        return {
            'type': 'ir.actions.act_url',
            'url': connect_url,
            'target': 'new',
        }



