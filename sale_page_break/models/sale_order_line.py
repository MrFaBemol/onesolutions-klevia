from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_checked = fields.Boolean(string='Is_checked', required=False)