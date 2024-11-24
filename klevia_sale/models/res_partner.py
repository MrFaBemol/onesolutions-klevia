from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    arr_history_line_ids = fields.One2many("res.partner.arr.history.line", "partner_id")
    arr_history_amount_total = fields.Float(compute='_compute_arr_history_amount_total', store=True, tracking=True, string="Historic ARR (total)")

    @api.depends('arr_history_line_ids.amount')
    def _compute_arr_history_amount_total(self):
        for partner in self:
            partner.arr_history_amount_total = sum(partner.arr_history_line_ids.mapped('amount'))
