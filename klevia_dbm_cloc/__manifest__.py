{
    'name': "Klevia - Database Manager CLOC",
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
        # Data

        # Views
        'views/dbm_instance.xml',
        'views/dbm_cloc_pricing.xml',

        # Reports

        # Wizards

        # Security
        'security/ir.model.access.csv',

        # Menus
        'data/ir_ui_menu.xml',

    ],

    'qweb': [],
}
