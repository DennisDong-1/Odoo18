# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.booking_core.services.availability import BookingAvailabilityService


class BookingBooking(models.Model):
    _name = 'booking.booking'
    _description = 'Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_datetime desc, id desc'

    name = fields.Char(
        string='Reference',
        copy=False,
        readonly=True,
        default='/',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer Name',
        required=True,
        tracking=True,
    )
    booking_type_id = fields.Many2one(
        'booking.type',
        string='Booking Type',
        required=True,
        ondelete='restrict',
        tracking=True,
    )
    resource_id = fields.Many2one(
        'booking.resource',
        string='Resource',
        required=True,
        ondelete='restrict',
        tracking=True,
        domain="[('booking_type_id', '=', booking_type_id)]",
    )
    start_datetime = fields.Datetime(required=True, tracking=True)
    end_datetime = fields.Datetime(required=True, tracking=True)
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        required=True,
        tracking=True,
        copy=False,
    )
    notes = fields.Text()

    @api.onchange('booking_type_id')
    def _onchange_booking_type_id(self):
        if self.resource_id and self.resource_id.booking_type_id != self.booking_type_id:
            self.resource_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') in (False, '/'):
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('booking.booking') or '/'
                )
        return super().create(vals_list)

    @api.constrains('resource_id', 'start_datetime', 'end_datetime', 'state')
    def _check_no_overlapping_booking(self):
        service = BookingAvailabilityService(self.env)
        for booking in self:
            if booking.state == 'cancelled':
                continue
            if not booking._has_valid_interval():
                raise ValidationError(_('End time must be after start time.'))
            if not service.check_resource_available(
                booking.resource_id,
                booking.start_datetime,
                booking.end_datetime,
                exclude_booking=booking,
            ):
                raise ValidationError(_(
                    'This resource is already booked for the selected time slot. '
                    'Please choose another time or resource.'
                ))

    def _has_valid_interval(self):
        self.ensure_one()
        return (
            self.start_datetime
            and self.end_datetime
            and self.end_datetime > self.start_datetime
        )

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
            self.write({'state': 'done'})

    def action_cancel(self):
            self.write({'state': 'cancelled'})

    def action_draft(self):
            self.write({'state': 'draft'})

