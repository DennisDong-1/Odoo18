{
    'name': 'Extending Website',
    'version': '1.0',
    'category': 'Website/Website',
    'category': 'Custom',
    'summary': 'Custom website extensions and snippets',
    'description': 'A custom module to extend the website with new building blocks.',
    'depends': ['website'],
    'data': [
        'views/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'extending_website/static/src/snippets/s_intro_custom/s_intro_custom.scss',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
