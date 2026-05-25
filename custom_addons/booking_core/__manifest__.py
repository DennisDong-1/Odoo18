{
    'name': 'Generic Booking',
    'version': '18.0.1.0.0',
    'category': 'Services',
    'summary': 'Generic booking system for everything',
    'author': 'Dennis Dong',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'resource', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/booking_sequence.xml',
        'views/booking_type_views.xml',
        'views/booking_resource_views.xml',
        'views/booking_booking_views.xml',
        'views/booking_portal_templates.xml', # QWeb templates view
        'views/booking_portal_form_templates.xml',
        'views/booking_portal_success_templates.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
}
