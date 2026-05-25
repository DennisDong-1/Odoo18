# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request
from datetime import datetime, timedelta

class BookingPortalController(http.Controller):

    @http.route('/booking', type='http', auth='public', website=True)
    def booking_index(self, **kwargs):
        """Render page listing all active Booking Types."""
        booking_types = request.env['booking.type'].search([('active', '=', True)])
        return request.render('booking_core.portal_booking_types', {
            'booking_types': booking_types,
        })

    @http.route('/booking/new', type='http', auth='public', website=True)
    def booking_new(self, type_id=None, error=None, **kwargs):
        """Render the simple booking form."""
        if not type_id:
            return request.redirect('/booking')
        
        booking_type = request.env['booking.type'].browse(int(type_id))
        if not booking_type.exists():
            return request.redirect('/booking')

        # Filter active resources matching this booking type
        resources = request.env['booking.resource'].search([
            ('booking_type_id', '=', booking_type.id),
            ('active', '=', True)
        ])

        # Suggest tomorrow morning 10:00 AM to 11:00 AM as a default window
        default_start = datetime.now() + timedelta(days=1)
        default_start = default_start.replace(hour=10, minute=0, second=0, microsecond=0)
        default_end = default_start + timedelta(hours=1.0) # Simple 1-hour default slot

        return request.render('booking_core.portal_booking_form', {
            'booking_type': booking_type,
            'resources': resources,
            'default_start': default_start.strftime('%Y-%m-%dT%H:%M'),
            'default_end': default_end.strftime('%Y-%m-%dT%H:%M'),
            'error': error,
            'submitted_vals': kwargs,
        })

    @http.route('/booking/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def booking_create(self, **post):
        """Handle booking submission and run overlap validation."""
        type_id = post.get('booking_type_id')
        resource_id = post.get('resource_id')
        partner_name = post.get('partner_name')
        partner_email = post.get('partner_email')
        start_str = post.get('start_datetime')
        end_str = post.get('end_datetime')
        notes = post.get('notes')

        if not all([type_id, resource_id, partner_name, partner_email, start_str, end_str]):
            return request.redirect(f'/booking/new?type_id={type_id}&error=All fields are required.')

        try:
            start_dt = datetime.strptime(start_str, '%Y-%m-%dT%H:%M')
            end_dt = datetime.strptime(end_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return request.redirect(f'/booking/new?type_id={type_id}&error=Invalid dates.')

        if end_dt <= start_dt:
            return request.redirect(f'/booking/new?type_id={type_id}&error=End time must be after start time.')

        # Find or create res.partner by email address
        partner = request.env['res.partner'].sudo().search([('email', '=', partner_email)], limit=1)
        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': partner_name,
                'email': partner_email,
            })

        resource = request.env['booking.resource'].sudo().browse(int(resource_id))
        
        # Check slot availability
        from odoo.addons.booking_core.services.availability import BookingAvailabilityService
        service = BookingAvailabilityService(request.env)

        if not service.check_resource_available(resource, start_dt, end_dt):
            return request.render('booking_core.portal_booking_form', {
                'booking_type': request.env['booking.type'].browse(int(type_id)),
                'resources': request.env['booking.resource'].search([
                    ('booking_type_id', '=', int(type_id)),
                    ('active', '=', True)
                ]),
                'error': 'The selected resource is already booked for this slot. Please choose another time.',
                'submitted_vals': post,
                'default_start': start_str,
                'default_end': end_str,
            })

        # Save booking in pending state
        booking = request.env['booking.booking'].sudo().create({
            'partner_id': partner.id,
            'booking_type_id': int(type_id),
            'resource_id': resource.id,
            'start_datetime': start_dt,
            'end_datetime': end_dt,
            'notes': notes,
            'state': 'pending',
        })

        return request.redirect(f'/booking/success?booking_id={booking.id}')

    @http.route('/booking/success', type='http', auth='public', website=True)
    def booking_success(self, booking_id=None, **kwargs):
        """Render success receipt screen."""
        if not booking_id:
            return request.redirect('/booking')
        
        booking = request.env['booking.booking'].sudo().browse(int(booking_id))
        if not booking.exists():
            return request.redirect('/booking')

        return request.render('booking_core.portal_booking_success', {
            'booking': booking,
        })
