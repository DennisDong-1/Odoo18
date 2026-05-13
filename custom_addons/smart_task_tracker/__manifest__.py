{
    'name': 'Smart Task Tracker',
    'author': 'Dennis Dong',
    'category': 'Custom',
    'version': '1.0',
    'license': 'LGPL-3',
    'summary': 'Track tasks and productivity',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/task_views.xml',
    ],
    'installable': True,
    'application': True
}