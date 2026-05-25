# -*- coding: utf-8 -*-
from odoo import fields, models


class BookingType(models.Model):
    _name = 'booking.type'
    _description = 'Booking Type'
    _order = 'name'

    name = fields.Char(required=True, translate=True, string='Booking Type')
    active = fields.Boolean(default=True)
    # duration_hours = fields.Float(
    #     string='Default Duration (hours)',
    #     help='Default slot length for this booking type.',
    # )
    # color = fields.Integer(string='Color Index')
    # website_published = fields.Boolean(
    #     string='Published on Website',
    #     default=False,
    # )

    resource_ids = fields.One2many(
        'booking.resource',
        'booking_type_id',
        string='Resources',
    )
    booking_ids = fields.One2many(
        'booking.booking',
        'booking_type_id',
        string='Bookings',
    )
