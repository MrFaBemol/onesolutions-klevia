{
    'name': "Klevia Sale Module",
    'category': "Sales",
    'version': "17.0.1.0.0",
    'installable': True,

    'license': "AGPL-3",
    'author': "OneSolutions Klevia SA - Gautier Casabona",
    'website': "https://www.onesolutions.ch",

    'depends': ['sale_management'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        'views/sale_order.xml',
        'reports/sale_order.xml'
    ],

    'qweb': [],
}
