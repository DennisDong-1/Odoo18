from odoo import models, fields, api


class smart_task(models.Model):
    _name = 'smart.task'    
    _description = 'Smart Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, string="Task Name")
    description = fields.Text()
    user_id = fields.Many2one(  #creates a relationship - each task belongs to ONE user, 'res.users' - Odoo's built in users table
        'res.users',
        string="Assigned To",
        tracking=True,
        default=lambda self: self.env.user)
    deadline = fields.Date()

    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default = 'medium', tracking=True)

    state = fields.Selection([
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], default='todo', tracking=True)

    time_spent = fields.Float(
        string="Time Spent (Hours)",
        readonly = True
        )
    
    start_time = fields.Datetime(
        readonly = True
    )

    progress = fields.Integer(
        string="Progress",
        compute="_compute_progress",
        store=True
    )

    @api.depends('state')
    def _compute_progress(self):
        for record in self:
            if record.state == 'todo':
                record.progress = 0
            elif record.state == 'in_progress':
                record.progress = 50
            elif record.state == 'done':
                record.progress = 100

    def action_start_task(self):
        for record in self:
            record.state = 'in_progress'
            record.start_time = fields.Datetime.now()


    def action_complete_task(self):
        for record in self:
            
            if record.start_time:
                end_time = fields.Datetime.now()

                duration = (
                    end_time - record.start_time
                ).total_seconds() / 3600

                record.time_spent += duration

            record.state = 'done'