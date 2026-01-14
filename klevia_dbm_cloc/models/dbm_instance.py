from odoo import api, fields, models, _
from odoo.exceptions import UserError
from ast import literal_eval


class DbmInstance(models.Model):
    _inherit = "dbm.instance"

    cloc_line_ids = fields.One2many("dbm.instance.cloc", "instance_id")

    cloc_total = fields.Integer(compute="_compute_cloc_total", store=True, readonly=False, tracking=True)
    cloc_cost_estimated = fields.Monetary(
        compute="_compute_cloc_cost",
        currency_field="company_currency",
        string="Estimated Maintenance Cost",
        store=False,
    )


    @api.depends('cloc_line_ids.loc', 'cloc_line_ids.include_in_cloc')
    def _compute_cloc_total(self):
        for instance in self:
            instance.cloc_total = sum(instance.cloc_line_ids.filtered(lambda l: l.include_in_cloc).mapped('loc'))

    @api.depends('cloc_total')
    def _compute_cloc_cost(self):
        pricing = self.env["dbm.cloc.pricing"].search([], order="max_loc asc")

        for instance in self:
            total_loc = instance.cloc_total
            remaining = total_loc
            cost = 0.0
            previous_max = 0

            for tier in pricing:
                if remaining <= 0:
                    break

                tier_range = tier.max_loc - previous_max
                qty = min(remaining, tier_range)

                cost += qty * tier.price_per_loc
                remaining -= qty
                previous_max = tier.max_loc

            instance.cloc_cost_estimated = cost


    # =========================================================
    #                         ACTIONS
    # =========================================================

    def action_recompute_cloc_cost(self):
        self._compute_cloc_cost()

    def action_sync_cloc(self):
        for instance in self:
            instance._action_sync_cloc()

    def _action_sync_cloc(self):
        self.ensure_one()

        if not self.technical_name:
            raise UserError(_("Technical name is required to compute CLOC inclusion rules."))

        env = self._get_api_environment()

        param = env["ir.config_parameter"].search_read([('key', '=', 'publisher_warranty.cloc')], ["value"])
        if not param:
            raise UserError(_("No CLOC information found on this database."))

        try:
            data = literal_eval(param.value)
        except Exception:
            raise UserError(_("Invalid CLOC format."))

        modules = data.get("modules", {})

        # Nettoyage complet : snapshot strict
        self.cloc_line_ids.unlink()

        Cloc = self.env["dbm.instance.cloc"]
        tech_name = self.technical_name.lower()

        for module_name, loc in modules.items():
            module_name_lc = module_name.lower()
            include = (
                    module_name_lc.startswith(tech_name)
                    or module_name_lc == "odoo/studio"
            )

            Cloc.create({
                "instance_id": self.id,
                "module_name": module_name,
                "loc": loc,
                "include_in_cloc": include,
            })

