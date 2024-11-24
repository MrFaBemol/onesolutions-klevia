from odoo import fields, models


class ResPartnerARRHistoryLine(models.Model):
    _name = "res.partner.arr.history.line"
    _description = "res.partner.arr.history.line"

    name = fields.Char()
    amount = fields.Float()
    partner_id = fields.Many2one("res.partner")
