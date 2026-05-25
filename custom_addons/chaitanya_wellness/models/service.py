# -*- coding: utf-8 -*-
from odoo import fields, models


class ChaitanyaWellnessService(models.Model):
    _name = 'chaitanya.wellness.service'
    _description = 'Chaitanya Wellness Services'
    _order = 'category_id, sequence, name'

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    website_published = fields.Boolean(
        string='Published on website',
        default=True,
    )
    category_id = fields.Many2one(
        'chaitanya.wellness.service.category',
        string='Category',
        ondelete='restrict',
    )

    duration_minutes = fields.Integer(default=60, required=True)
    slot_step_minutes = fields.Integer(default=15)
    price = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    description = fields.Html(
        string='These are the available services.',
        translate=True,
    )
    benefits = fields.Html(translate=True)

    provider_ids = fields.Many2many(
        'chaitanya.wellness.provider',
        'chaitanya_wellness_provider_service_rel',
        'service_id',
        'provider_id',
        string='Therapists',
    )
