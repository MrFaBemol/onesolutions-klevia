from odoo import fields, models

class DbmClocPricing(models.Model):
    _name = "dbm.cloc.pricing"
    _description = "CLOC Pricing Tier"
    _order = "max_loc asc"

    max_loc = fields.Integer(string="Up to LOC", required=True)
    price_per_loc = fields.Float(string="Price per LOC", required=True)
