{
    'name': "Klevia - CRM",
    'category': "CRM",
    'version': "18.0.0.0.1",
    'installable': True,
    'sequence': 1,

    'license': "OPL-1",
    'author': "OneSolutions - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['crm'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        'views/crm_lead.xml',
    ],

    'qweb': [],
}
