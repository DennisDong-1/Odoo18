{
    'name':'Chaitanya Wellness',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Spa and wellness booking for Chaitanya',
    'author': 'Dennis Dong',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/service_category_data.xml',
        'views/service_category_views.xml',
        'views/service_views.xml',
        'views/provider_views.xml',
        'views/menus.xml',
    ],
    'application': True,
    'installable': True,
}