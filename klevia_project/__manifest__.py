{
    'name': "Klevia Project",
    'category': "Project",
    'version': "18.0.1.0.0",
    'installable': True,

    'license': "OPL-1",
    'author': "OneSolutions SA - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['hr_timesheet'],
    "assets": {
        "web.assets_backend": [],
    },

    'data': [
        # Security
        # 'security/ir.model.access.csv',

        # Views
        'views/account_analytic_line.xml',
        'views/project_task.xml',

        # Reports
    ],

    'qweb': [],
}
