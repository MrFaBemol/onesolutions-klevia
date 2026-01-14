{
    'name': "Klevia - Database Manager Sync",
    'category': "Technical",
    'version': "19.0.1.0.1",
    'installable': True,
    'sequence': 1,

    'license': "OPL-1",
    'author': "OneSolutions - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['klevia_dbm_base'],
    'external_dependencies': {
        'python': ['otools_rpc'],
        # 'apt': {
        #     'zeep': 'python3-zeep',
        # },
    },
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Data

        # Views
        'views/dbm_instance.xml',

        # Reports

        # Wizards

        # Security
        'security/ir.model.access.csv',

        # Menus

    ],

    'qweb': [],
}
