{
    'name': "Klevia Sale Module",
    'category': "Sales",
    'version': "17.0.1.0.2",
    'installable': True,

    'license': "AGPL-3",
    'author': "OneSolutions Klevia SA - Gautier Casabona",
    'website': "https://www.onesolutions.ch",

    'depends': ['sale_management'],
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
