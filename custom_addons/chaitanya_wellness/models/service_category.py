from odoo import fields, models


class ChaitanyaWellnessServiceCategory(models.Model):
    _name = 'chaitanya.wellness.service.category'   #technical name, is turned into a DB table (chaitanya_wellness_service_category)
    _description = 'Service Category'
    _order = 'sequence, name'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    description = fields.Html(translate=True)
    website_published = fields.Boolean(
        string='Published on website',
        default=True,
    )

    # Extending
    service_ids = fields.One2many(
        'chaitanya.wellness.service',
        'category_id',
        string = "Services")
    service_count = fields.Integer(compute="_compute_service_count", )

    def _compute_service_count(self):
        Service = self.env['chaitanya.wellness.service']
        grouped = Service.read_group(   #DB style aggregation
            [('category_id', 'in', self.ids)],
            ['category_id'],
            ['category_id'],
        )
        counts = {
            g['category_id'][0]: g['category_id_count']
            for g in grouped
            if g['category_id']
        }

        for rec in self:
            rec.service_count = counts.get(rec.id, 0)