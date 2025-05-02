{
    'name': "Klevia Sale",
    'category': "Sales",
    'version': "18.0.1.0.6",
    'installable': True,

    'license': "OPL-1",
    'author': "OneSolutions SA - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['sale_subscription', 'crm'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/crm_lead.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/utm_source.xml',
        'views/sale_order_template.xml',

        # Reports
        'reports/sale_order.xml'
    ],

    'qweb': [],
}
