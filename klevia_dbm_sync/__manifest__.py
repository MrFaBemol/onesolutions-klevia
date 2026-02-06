{
    'name': "Klevia - Database Manager Sync",
    'category': "Technical",
    'version': "19.0.1.0.5",
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
        'data/ir_config_parameter.xml',

        # Views
        'views/dbm_instance.xml',
        'views/dbm_instance_user.xml',

        # Reports

        # Wizards

        # Security
        'security/ir.model.access.csv',

        # Menus

    ],

    'qweb': [],
}
