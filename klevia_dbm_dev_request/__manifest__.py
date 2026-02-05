{
    'name': "Klevia - Database Manager (Dev Request)",
    'category': "Technical",
    'version': "19.0.1.0.2",
    'installable': True,
    'sequence': 1,

    'license': "OPL-1",
    'author': "OneSolutions - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['klevia_dbm_base'],
    'auto_install': True,
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Views
        'views/dbm_request.xml',

        # Reports

        # Wizards

        # Security
        'security/ir.model.access.csv',

        # Menus

        # Data
        'data/dbm_request_stage.xml',
        'data/ir_ui_menu.xml'

    ],

    'qweb': [],
}
