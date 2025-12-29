{
    'name': "Klevia - CRM odoo specific",
    'category': "CRM",
    'version': "19.0.0.0.2",
    'installable': True,
    'sequence': 1,

    'license': "OPL-1",
    'author': "OneSolutions - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['klevia_crm'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        'data/mail_template.xml',
        'views/crm_lead.xml',
    ],

    'qweb': [],
}
