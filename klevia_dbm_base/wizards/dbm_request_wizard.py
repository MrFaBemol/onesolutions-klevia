from odoo import api, fields, models, _
from odoo.exceptions import UserError


class DbmRequestWizard(models.TransientModel):
    _name = "dbm.request.wizard"
    _description = "Create Request Wizard"

    instance_id = fields.Many2one("dbm.instance", required=True)

    name = fields.Char(required=True)
    request_type = fields.Selection(
        selection=[
            ("install", "Installation"),
            ("upgrade", "Upgrade / Migration"),
            ("other", "Other"),
        ],
        required=True,
        default="other",
    )

    user_id = fields.Many2one("res.users", string="Assigned To", required=True)
    version_id = fields.Many2one("dbm.version", string="Target Odoo Version")
    description = fields.Text(required=True)

    def action_confirm(self):
        self.ensure_one()
        if not self.instance_id:
            raise UserError(_("No instance provided."))

        req = self.env["dbm.request"].create({
            "instance_id": self.instance_id.id,
            "name": self.name,
            "request_type": self.request_type,
            "user_id": self.user_id.id,
            "version_id": self.version_id.id or False,
            "description": self.description,
        })

        # Flag instance
        if self.request_type == "install":
            self.instance_id.to_install = True
        elif self.request_type == "upgrade":
            self.instance_id.to_upgrade = True

        # Optional: schedule activity for assignee (simple)
        # req.activity_schedule(
        #     "mail.mail_activity_data_todo",
        #     user_id=self.user_id.id,
        #     summary=dict(self._fields["request_type"].selection).get(self.request_type),
        #     note=self.description,
        # )

        return {"type": "ir.actions.act_window_close"}
