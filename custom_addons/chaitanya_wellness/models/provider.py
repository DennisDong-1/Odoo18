from odoo import fields, models


class ChaitanyaWellnessProvider(models.Model):
    _name = 'chaitanya.wellness.provider'
    _description = 'Therapist / Provider'
    _order = 'name'

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    bio = fields.Html(translate=True, string='Profile')
    partner_id = fields.Many2one('res.partner', string='Linked contact')
    service_ids = fields.Many2many(
        'chaitanya.wellness.service',
        'chaitanya_wellness_provider_service_rel',
        'provider_id',
        'service_id',
        string = 'Services offered',
    )
    working_day_ids = fields.One2many(
        'chaitanya.wellness.working_day',
        'provider_id', # child model, inverse field
        string='Working hours',
    )