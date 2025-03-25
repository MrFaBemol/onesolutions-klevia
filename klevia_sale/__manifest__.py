{
    'name': "Klevia Sale Module",
    'category': "Sales",
    'version': "18.0.1.0.3",
    'installable': True,

    'license': "OPL-1",
    'author': "OneSolutions Klevia SA - Gautier Casabona",
    'website': "https://www.onesolutions.ch",

    'depends': ['sale_management', 'sale_subscription'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/res_partner.xml',
        'views/sale_order.xml',

        # Reports
        'reports/sale_order.xml'
    ],

    'qweb': [],
}
