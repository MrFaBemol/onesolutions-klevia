from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import requests
import json
import logging
_logger = logging.getLogger(__name__)


# self.env.user._bus_send('simple_notification', {
#     'type': 'success',
#     'message': success_message,
# })


class DbmInstance(models.Model):
    _inherit = "dbm.instance"

    def action_generate_api_key(self):
        self.ensure_one()
        result = self._generate_api_key()
        self.api_password = result.get('api_key')
        self.api_dbname = result.get('dbname')

    def _generate_api_key(self):
        endpoint_url = f"{self.get_clean_url()}/onesolutions/api/key"
        login = self.api_username
        secret = self.env['ir.config_parameter'].sudo().get_param('klevia_dbm_sync.secret')
        if not secret:
            raise UserError(_("Please set a secret in the system parameters (klevia_dbm_sync.secret)"))
        payload = {
            "login": login,
            "secret": secret,
        }

        try:
            response = requests.post(
                endpoint_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
        except requests.exceptions.RequestException as e:
            raise UserError(_("Failed to call the endpoint, please check that the os_sync module is installed on the database\n\n%s", e))

        if response.status_code != 200:
            raise UserError(_("Invalid response, status code : %s", response.status_code))

        try:
            data = response.json()
        except Exception:
            raise UserError(_("Invalid JSON response: %s", response.text))

        result = data.get('result')
        if not result.get('api_key'):
            raise UserError(_("No API key returned"))
        if not result.get('dbname'):
            raise UserError(_("No DB name returned"))

        return result

