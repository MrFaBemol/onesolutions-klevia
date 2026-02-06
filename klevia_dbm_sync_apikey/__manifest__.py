{
    'name': "Klevia - Database Manager Generate API Key for Sync",
    'category': "Technical",
    'version': "19.0.1.0.3",
    'installable': True,
    'sequence': 1,

    'license': "OPL-1",
    'author': "OneSolutions - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['klevia_dbm_sync'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Views
        'views/dbm_instance.xml',

        # Reports

        # Wizards

        # Security
        'security/ir.model.access.csv',

        # Menus

        # Data

    ],

    'qweb': [],
}
