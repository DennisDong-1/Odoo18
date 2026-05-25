# -*- coding: utf-8 -*-
from odoo import fields


class BookingAvailabilityService:
    """Domain-agnostic availability checks for booking resources."""

    def __init__(self, env):
        self.env = env

    def check_resource_available(
        self,
        resource,
        start,
        end,
        exclude_booking=None,
    ):
        """Return True if no non-cancelled booking overlaps [start, end] on resource."""
        if not resource or not start or not end:
            return False
        if fields.Datetime.to_datetime(end) <= fields.Datetime.to_datetime(start):
            return False

        domain = self._overlap_domain(resource, start, end, exclude_booking)
        return not self.env['booking.booking'].search_count(domain)

    def _overlap_domain(self, resource, start, end, exclude_booking=None):
        domain = [
            ('resource_id', '=', resource.id),
            ('state', '!=', 'cancelled'),
            ('start_datetime', '<', end),
            ('end_datetime', '>', start),
        ]
        if exclude_booking and exclude_booking.id:
            domain.append(('id', '!=', exclude_booking.id))
        return domain

    def find_conflicting_bookings(self, resource, start, end, exclude_booking=None):
        domain = self._overlap_domain(resource, start, end, exclude_booking)
        return self.env['booking.booking'].search(domain)
