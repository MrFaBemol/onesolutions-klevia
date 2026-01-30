from odoo import api, fields, models, Command, _
from odoo.exceptions import ValidationError


class DbmInstance(models.Model):
    _name = "dbm.instance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Instance"
    _rec_names_search = ['name', 'technical_name', 'partner_id']

    active = fields.Boolean(default=True, tracking=True)

    # -------------------------
    # Favorites (per user)
    # -------------------------
    favorite_user_ids = fields.Many2many(
        "res.users",
        "dbm_instance_favorite_user_rel",
        "instance_id",
        "user_id",
        string="Favorite Users",
        copy=False,
    )

    is_favorite = fields.Boolean(
        compute="_compute_is_favorite",
        readonly=False,
        search="_search_is_favorite",
        compute_sudo=True,
    )

    @api.model
    def _search_is_favorite(self, operator, value):
        if operator != "in":
            return NotImplemented
        return [("favorite_user_ids", "in", [self.env.uid])]

    def _compute_is_favorite(self):
        user = self.env.user
        # We store favorites on the instance itself (favorite_user_ids).
        for rec in self:
            rec.is_favorite = user in rec.favorite_user_ids

    def _set_favorite_user_ids(self, is_favorite):
        self_sudo = self.sudo()
        for rec in self_sudo:
            if is_favorite:
                rec.favorite_user_ids = [Command.link(self.env.uid)]
            else:
                rec.favorite_user_ids = [Command.unlink(self.env.uid)]

    # -------------------------
    # Core fields
    # -------------------------
    name = fields.Char(required=True, string="Access URL", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Customer", ondelete="set null", tracking=True)

    category_id = fields.Many2one(
        "dbm.category",
        required=True,
        ondelete="restrict",
        tracking=True,
        default=lambda self: self.env.ref('klevia_dbm_base.dbm_category_odoo', raise_if_not_found=False),
    )
    hosting_id = fields.Many2one(
        "dbm.hosting",
        required=True,
        ondelete="restrict",
        domain="[('category_id', '=', category_id)]",
        tracking=True,
    )
    server_id = fields.Many2one(
        "dbm.server",
        ondelete="restrict",
        domain="[('hosting_id', '=', hosting_id)]",
        tracking=True,
    )

    technical_name = fields.Char(
        string="Technical Name",
        tracking=True,
        index=True,
        help="Used to generate conventions (e.g. GitHub repo).",
    )

    stage_id = fields.Many2one(
        "dbm.instance.stage",
        string="Status",
        required=True,
        tracking=True,
        default=lambda self: self._default_stage_id(),
        ondelete="restrict",
    )
    stage_color = fields.Selection(related="stage_id.decoration_type")

    version_id = fields.Many2one(
        "dbm.version",
        string="Version",
        tracking=True,
        ondelete="restrict",
    )

    license_type = fields.Selection(
        selection=[
            ("standard", "Standard"),
            ("custom", "Custom"),
        ],
        default="standard",
        tracking=True,
    )

    subscription_code = fields.Char(string="Subscription Code", tracking=True)

    is_odoo_sh = fields.Boolean(string="Odoo.SH Instance", compute="_compute_is_odoo_sh")
    odoo_sh_url = fields.Char(string="Odoo.SH URL", tracking=True)
    github_url = fields.Char(string="GitHub URL", tracking=True)

    tag_ids = fields.Many2many(
        "dbm.tag",
        "dbm_instance_tag_rel",
        "instance_id",
        "tag_id",
        string="Tags",
    )

    responsible_id = fields.Many2one(
        "res.users",
        string="Technical Responsible",
        tracking=True,
        ondelete="set null",
    )

    company_id = fields.Many2one("res.company", string="Company", tracking=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one(related="company_id.currency_id")

    technical_notes = fields.Text(string="Technical Notes")

    # -------------------------
    # Flags (installation / upgrade)
    # -------------------------
    to_install = fields.Boolean(default=False, tracking=True)
    to_upgrade = fields.Boolean(default=False, tracking=True)

    # -------------------------
    # On-premise SSH/VPN info
    # -------------------------
    is_on_premise = fields.Boolean(related="hosting_id.is_on_premise")

    ssh_host = fields.Char(string="SSH Host")
    ssh_port = fields.Integer(string="SSH Port", default=22)
    ssh_user = fields.Char(string="SSH User")
    ssh_notes = fields.Text(string="SSH Notes")

    vpn_required = fields.Boolean(string="VPN Required", default=False)
    vpn_profile_file = fields.Binary(string="VPN Profile",help="Attach a VPN profile (e.g. .ovpn).")
    vpn_profile_file_name = fields.Char(string="Name of VPN profile")


    @api.depends('hosting_id')
    def _compute_is_odoo_sh(self):
        odoo_sh_hosting = self.env.ref('klevia_dbm_base.dbm_hosting_odoo_sh', raise_if_not_found=False)
        for instance in self:
            instance.is_odoo_sh = instance.hosting_id == odoo_sh_hosting

    # -------------------------
    # Defaults / onchange
    # -------------------------
    @api.model
    def _default_stage_id(self):
        stage = self.env["dbm.instance.stage"].search([("active", "=", True)], order="sequence, id", limit=1)
        return stage.id

    @api.onchange("category_id")
    def _onchange_category_id(self):
        self.hosting_id = False
        self.server_id = False

    @api.onchange("hosting_id")
    def _onchange_hosting_id(self):
        self.server_id = False

    @api.onchange('technical_name', 'hosting_id')
    def _onchange_technical_name(self):
        if not self.technical_name:
            return
        odoo_com_hosting = self.env.ref('klevia_dbm_base.dbm_hosting_odoo_com', raise_if_not_found=False)
        odoo_sh_hosting = self.env.ref('klevia_dbm_base.dbm_hosting_odoo_sh', raise_if_not_found=False)
        if odoo_com_hosting and self.hosting_id != odoo_com_hosting:
            self.github_url = f"https://github.com/onesolutions-klevia-clients/{self.technical_name}"
        if odoo_sh_hosting and self.hosting_id == odoo_sh_hosting:
            self.odoo_sh_url = f"https://www.odoo.sh/project/{self.technical_name}"


    # -------------------------
    # Constraints / helpers
    # -------------------------
    @api.constrains("name")
    def _check_url(self):
        for rec in self:
            if rec.name and not (rec.name.startswith("http://") or rec.name.startswith("https://")):
                raise ValidationError(_("Access URL must start with http:// or https://"))


    def get_clean_url(self):
        self.ensure_one()
        if self.name[-1] == "/":
            self.name = self.name[:-1]
        return self.name

    # -------------------------
    # CRUD
    # -------------------------


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Default GitHub URL convention (only if empty)
            if not vals.get("github_url") and vals.get("technical_name") and vals.get("hosting_id"):
                hosting = self.env["dbm.hosting"].browse(vals["hosting_id"])
                if hosting and hosting.code and hosting.code != "odoo_com":
                    vals["github_url"] = f"https://github.com/onesolutions-klevia-clients/{vals['technical_name']}"
        return super().create(vals_list)

    def write(self, vals):
        if "is_favorite" in vals:
            self._set_favorite_user_ids(vals.pop("is_favorite"))
        return super().write(vals)

    def name_get(self):
        res = []
        for rec in self:
            parts = []
            if rec.partner_id:
                parts.append(rec.partner_id.name)
            if rec.technical_name:
                parts.append(rec.technical_name)
            if not parts:
                parts.append(rec.name or _("Instance"))
            res.append((rec.id, " - ".join(parts)))
        return res

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = ["|", "|",
                      ("partner_id.name", operator, name),
                      ("name", operator, name),
                      ("technical_name", operator, name)]
        recs = self.search(domain + args, limit=limit)
        return recs.name_get()

    # -------------------------
    # Actions (URL + request flows)
    # -------------------------
    def action_open_link(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": self.name,
            "target": "new",
        }


    def action_open_sh_project(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": self.odoo_sh_url,
            "target": "new",
        }

    def action_open_github(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": self.github_url,
            "target": "new",
        }

    def action_toggle_favorite(self):
        self.is_favorite = not self.is_favorite

    def action_archive(self):
        for rec in self:
            rec.active = False

    def action_unarchive(self):
        for rec in self:
            rec.active = True


    def action_open_request_wizard(self):
        self.ensure_one()
        ctx = dict(self.env.context or {})
        ctx.update({
            "default_instance_id": self.id,
            "default_user_id": self.responsible_id.id or False,
            "default_version_id": self.version_id.id or False,
        })
        return {
            "type": "ir.actions.act_window",
            "name": _("Create Request"),
            "res_model": "dbm.request.wizard",
            "view_mode": "form",
            "target": "new",
            "context": ctx,
        }

    def action_mark_installed(self):
        for rec in self:
            rec.to_install = False

    def action_mark_upgraded(self):
        for rec in self:
            rec.to_upgrade = False
