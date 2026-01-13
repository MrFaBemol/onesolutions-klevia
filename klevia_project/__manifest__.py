{
    'name': "Klevia Project",
    'category': "Project",
    'version': "19.0.1.0.2",
    'installable': True,

    'license': "OPL-1",
    'author': "OneSolutions SA - Gautier Casabona",
    'website': "https://www.onesolutions.io",

    'depends': ['hr_timesheet', 'project'],
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
