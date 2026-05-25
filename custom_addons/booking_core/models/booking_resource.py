# -*- coding: utf-8 -*-
from odoo import fields, models


class BookingResource(models.Model):
    _name = 'booking.resource'
    _description = 'Booking Resource'
    _order = 'name'

    name = fields.Char(required=True, translate=True, string='Resource ( Service )')
    active = fields.Boolean(default=True)
    booking_type_id = fields.Many2one(
        'booking.type',
        string='Booking Type',
        ondelete='restrict',
    )
    # capacity = fields.Integer(
    #     string='Capacity the service can accomodate',
    #     default=1,
    #     help='Number of parallel bookings allowed. MVP overlap logic assumes 1.',
    # )
    # calendar_id = fields.Many2one(
    #     'resource.calendar',
    #     string='Working Hours',
    #     help='Optional working-time calendar for availability checks later.',
    # )

    booking_ids = fields.One2many(
        'booking.booking',
        'resource_id',
        string='Bookings',
    )
