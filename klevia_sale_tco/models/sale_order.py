from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    must_include_tco = fields.Boolean(string="Include TCO")
    must_include_odoo_cost = fields.Boolean(string="Include Odoo infos")

    # --------------------------------------------
    #                All Odoo fields
    # --------------------------------------------

    odoo_currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.EUR', raise_if_not_found=False))

    odoo_hosting_cost = fields.Monetary(string="Hosting (Monthly)", currency_field='odoo_currency_id', compute="_compute_odoo_hosting_cost")
    odoo_hosting_cost_yearly = fields.Monetary(string="Hosting (Yearly)", currency_field='odoo_currency_id', compute="_compute_odoo_hosting_cost")
    odoo_hosting_type = fields.Selection(
        selection=[
            ('saas', "SaaS (Odoo.com)"),
            ('sh', 'Odoo.SH'),
            ('on_premise', "On Premise"),
        ],
        string="Hosting Type",
        default='saas',
        required=True,
        readonly=False,
        store=True,
        compute='_compute_odoo_hosting_type',
    )
    odoo_sh_worker = fields.Integer(default=1, string="# Workers")
    odoo_sh_staging = fields.Integer(default=1, string="# Staging")
    odoo_sh_storage = fields.Integer(default=15, string="# Gb")

    odoo_license_cost_year_1 = fields.Monetary(string="Licenses (Year 1)", currency_field='odoo_currency_id', compute="_compute_odoo_license_cost")
    odoo_license_cost_year_2 = fields.Monetary(string="Licenses (Year 2)", currency_field='odoo_currency_id', compute="_compute_odoo_license_cost")
    odoo_license_type = fields.Selection(
        selection=[
            ('free', '1 App free'),
            ('standard', 'Standard'),
            ('custom', 'Custom'),
        ],
        string="License Type",
        default='standard',
        required=True,
        readonly=False,
        store=True,
        compute='_compute_odoo_license_type',
    )
    odoo_license_count = fields.Integer(compute="_compute_odoo_license_count")
    odoo_license_customer = fields.Integer(default=1)
    odoo_license_include_onesolutions = fields.Boolean(default=True, string="OneSolutions License")

    odoo_need_payroll = fields.Boolean(string="Payroll")
    odoo_need_studio = fields.Boolean(string="Studio")
    odoo_multi_company = fields.Boolean(string="Multi Company")
    odoo_external_api = fields.Boolean(string="External API")
    odoo_need_development = fields.Boolean(string="Development")

    odoo_configuration_warning = fields.Char(compute="_compute_odoo_configuration_warning")


    @api.depends('odoo_license_type', 'odoo_hosting_type', 'odoo_need_payroll', 'odoo_need_studio', 'odoo_need_development', 'odoo_multi_company', 'odoo_external_api')
    def _compute_odoo_configuration_warning(self):
        for order in self:
            warning = ""

            order.odoo_configuration_warning = False

    @api.depends('odoo_license_type', 'odoo_need_development')
    def _compute_odoo_hosting_type(self):
        for order in self:
            if order.odoo_need_development and order.odoo_hosting_type == 'saas':
                order.odoo_hosting_type = 'sh'

            if order.odoo_license_type == 'free':
                order.odoo_hosting_type = 'saas'

    @api.depends('odoo_hosting_type', 'odoo_sh_worker', 'odoo_sh_storage', 'odoo_sh_staging')
    def _compute_odoo_hosting_cost(self):
        HOSTING_PRICES = self._get_hosting_prices()
        free_hosting_order = self.filtered(lambda o: o.odoo_hosting_type in ['saas', 'on_premise']) # On premise is virtually free for TCO
        free_hosting_order.odoo_hosting_cost = 0.0
        free_hosting_order.odoo_hosting_cost_yearly = 0.0
        for order in (self - free_hosting_order):
            order.odoo_hosting_cost = HOSTING_PRICES['worker'] * self.odoo_sh_worker + HOSTING_PRICES['staging'] * self.odoo_sh_staging + HOSTING_PRICES['storage'] * self.odoo_sh_storage
            order.odoo_hosting_cost_yearly =  order.odoo_hosting_cost * 12


    @api.depends('odoo_need_studio', 'odoo_need_development', 'odoo_multi_company', 'odoo_external_api', 'odoo_hosting_type')
    def _compute_odoo_license_type(self):
        for order in self:
            if order.odoo_hosting_type == 'on_premise' or any(
                    [
                        order.odoo_need_studio,
                        order.odoo_need_development,
                        order.odoo_multi_company,
                        order.odoo_external_api,
                    ]
            ):
                order.odoo_license_type = 'custom'
            else:
                order.odoo_license_type = 'standard'


    @api.depends('odoo_license_customer', 'odoo_license_include_onesolutions')
    def _compute_odoo_license_count(self):
        for order in self:
            order.odoo_license_count = order.odoo_license_customer + (1 if order.odoo_license_include_onesolutions else 0)

    @api.depends('odoo_license_type', 'odoo_license_count')
    def _compute_odoo_license_cost(self):
        LICENSE_PRICES = self._get_license_prices()
        for order in self:
            prices = LICENSE_PRICES[order.odoo_license_type]
            order.odoo_license_cost_year_1 = prices[1] * order.odoo_license_count * 12
            order.odoo_license_cost_year_2 = prices[2] * order.odoo_license_count * 12



    # --------------------------------------------
    #                   ONCHANGE
    # --------------------------------------------

    @api.onchange('odoo_license_type')
    def _onchange_odoo_license_type(self):
        if self.odoo_need_payroll and self.odoo_license_type == 'free':
            raise UserError(_("Payroll is not available with a free license. Choose 'Standard' instead."))
        if self.odoo_license_type != 'custom':
            self.odoo_need_studio = False
            self.odoo_need_development = False
            self.odoo_multi_company = False
            self.odoo_external_api = False



    # --------------------------------------------
    #                   MISC
    # --------------------------------------------

    def _get_formatted_licence_prices(self):
        """ Used in report to display prices with correct formatting (aka 2 decimal) """
        self.ensure_one()
        licence_prices = self._get_license_prices().get(self.odoo_license_type)
        return {
            1: "%.2f €" % licence_prices[1],
            2: "%.2f €" % licence_prices[2],
            'total_1': "%.2f €" % self.odoo_license_cost_year_1,
            'total_2': "%.2f €" % self.odoo_license_cost_year_2,
        }


    def _get_formatted_sh_prices(self):
        """ Used in report to display prices with correct formatting (aka 2 decimal) """
        self.ensure_one()
        hosting_prices = self._get_hosting_prices()
        hosting_prices |= {
            'storage_month': "%.2f €" % (self.odoo_sh_storage * hosting_prices.get('storage')),
            'total_month': "%.2f €" % self.odoo_hosting_cost ,
            'total_year': "%.2f €" % self.odoo_hosting_cost_yearly ,
        }
        return hosting_prices

    @api.model
    def _get_license_prices(self):
        return {
            'free': {
                1: 0,
                2: 0,
            },
            'standard': {
                1: 19.90,
                2: 24.90,
            },
            'custom': {
                1: 29.90,
                2: 37.40,
            }
        }


    @api.model
    def _get_hosting_prices(self):
        """ Prices are in euros and if paid annually"""
        return {
            'worker': 48,       # / unit
            'staging': 12,      # / unit
            'storage': 0.16,    # / Gb
        }
