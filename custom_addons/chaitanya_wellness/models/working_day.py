# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ChaitanyaWellnessWorkingDay(models.Model):
    _name = 'chaitanya.wellness.working_day'
    _description = 'Provider Working Day'
    _order = 'provider_id, weekday'

    provider_id = fields.Many2one(
        'chaitanya.wellness.provider',
        required=True,
        ondelete='cascade',
    )
    weekday = fields.Selection(
        selection=[
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
            ('6', 'Sunday'),
        ],
        required=True,
        string='Weekday',
    )
    start_time = fields.Float(
        required=True,
        help='24h format, e.g. 9.5 = 09:30',
    )
    end_time = fields.Float(
        required=True,
        help='24h format, e.g. 17.0 = 17:00',
    )

    @api.constrains('start_time', 'end_time')
    def _check_times(self):
        for rec in self:
            if rec.end_time <= rec.start_time:
                day_label = dict(rec._fields['weekday'].selection).get(rec.weekday, '')
                raise ValidationError(
                    _('End time must be after start time for %(provider)s on %(day)s.')
                    % {'provider': rec.provider_id.name, 'day': day_label}
                )
