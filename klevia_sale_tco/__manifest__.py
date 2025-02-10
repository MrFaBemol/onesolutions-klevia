{
    'name': "Klevia Sale - TCO calculator (for Odoo)",
    'category': "Sales",
    'version': "18.0.0.0.1",
    'installable': True,
    'sequence': 1,

    'license': "OPL-1",
    'author': "OneSolutions SA - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['sale_management'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Reports
        'reports/sale_order.xml',

        # Views
        'views/sale_order.xml',
    ],

    'qweb': [],
}
