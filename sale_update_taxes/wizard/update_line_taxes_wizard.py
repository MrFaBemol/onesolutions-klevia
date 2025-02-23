from odoo import api, fields, models


class UpdateLineTaxesWizard(models.TransientModel):
    _name = 'update.line.taxes.wizard'
    _description = 'UpdateLineTaxes'

    tax_ids = fields.Many2many(
        comodel_name='account.tax', domain="[('type_tax_use', '=', 'sale')]",
        string='Taxes')

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale order',
    )

    sale_order_line_ids = fields.One2many(
        comodel_name='update.line.taxes.wizard.line',
        inverse_name='update_line_taxes_id',
        string='Lines',
        required=False)

    def action_update_taxes(self):
        self.ensure_one()
        self.sale_order_line_ids.filtered('is_update_tax').sale_order_line_id.tax_id = self.tax_ids.ids


class UpdateLineTaxesWizardLine(models.TransientModel):
    _name = 'update.line.taxes.wizard.line'
    _description = 'Wizard Sale Order Lines'

    update_line_taxes_id = fields.Many2one('update.line.taxes.wizard', ondelete="cascade")
    sale_order_line_id = fields.Many2one('sale.order.line', string="Description")
    order_id = fields.Many2one(related='sale_order_line_id.order_id', readonly=True)
    product_id = fields.Many2one(related='sale_order_line_id.product_id', readonly=True)
    price_unit = fields.Float(related='sale_order_line_id.price_unit', readonly=True)
    is_update_tax = fields.Boolean(string="Update Taxes", readonly=False)
    tax_ids = fields.Many2many(related='sale_order_line_id.tax_id', readonly=True)
