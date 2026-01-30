from odoo import models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


# self.env.user._bus_send('simple_notification', {
#     'type': 'success',
#     'message': success_message,
# })


class DbmInstance(models.Model):
    _inherit = "dbm.instance"

    def action_open_connect_as(self):
        self.ensure_one()
        return {
            "name": _("Connect As"),
            "type": 'ir.actions.act_window',
            "res_model": 'dbm.instance.user',
            "domain": [('instance_id', '=', self.id)],
            "views": [[False, "list"]],
            "target": 'new',
            "context": {
                **self.env.context,
            },
        }
