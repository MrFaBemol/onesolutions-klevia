from odoo import api, fields, models
from odoo.fields import Command


class UpdateLineTaxes(models.TransientModel):
    _name = 'update.line.taxes'
    _description = 'UpdateLineTaxes'

    name = fields.Char()
    
    tax_ids = fields.Many2many(
        comodel_name='account.tax',domain="[('type_tax_use', '=', 'sale')]",
        string='Taxes')

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale order',
        required=False)

    sale_order_line_ids = fields.One2many(
        comodel_name='update.line.taxes.line',
        inverse_name='update_line_taxes_id',
        string='Lines',
        required=False)

    def action_update_taxes(self):
        for rec in self:
            for line in rec.sale_order_line_ids:
                if line.is_update_tax:
                    line.sale_order_line_id.write({'tax_id': [(6, 0, rec.tax_ids.ids)]})



    @api.model
    def default_get(self, fields):
        defaults = super(UpdateLineTaxes,self).default_get(fields)
        sale_order_id = self.env.context.get('default_sale_order_id')
        if sale_order_id:
            sale_order = self.env['sale.order'].browse(sale_order_id)
            lines = [{
                'sale_order_line_id': line.id,
                'order_id':line.order_id,
                'tax_id':line.tax_id,
                'product_id': line.product_id.id,
                'price_unit': line.price_unit,
                'is_update_tax': False  # Default unchecked
            } for line in sale_order.order_line]

            defaults.update({
                'sale_order_id': sale_order_id,
                'sale_order_line_ids': [(0, 0, line) for line in lines]
            })

        return defaults

    # @api.depends('sale_order_id')  # Trigger when sale_order_id changes
    # def _compute_sale_order_lines(self):
    #     for rec in self:
    #         if rec.sale_order_id:
    #             # Search for sale order lines related to the sale_order_id
    #             sale_order_lines = self.env['sale.order.line'].search([('order_id', '=', rec.sale_order_id.id)])
    #             # Set the value for sale_order_line_ids
    #             rec.sale_order_line_ids = sale_order_lines
    #
    #
    # def _inverse_sale_order_lines(self):
    #     pass



class UpdateLineTaxesLine(models.TransientModel):
    _name = 'update.line.taxes.line'
    _description = 'Wizard Sale Order Lines'

    update_line_taxes_id = fields.Many2one('update.line.taxes', ondelete="cascade")
    sale_order_line_id = fields.Many2one('sale.order.line', string="Description")
    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Order',
        required=False)
    product_id = fields.Many2one('product.product', string="Product", readonly=True)
    price_unit = fields.Float(string="Unit Price", readonly=True)
    is_update_tax = fields.Boolean(string="Update Taxes",readonly=False)
    tax_id = fields.Many2many(
        comodel_name='account.tax',
        string='Tax_id')
