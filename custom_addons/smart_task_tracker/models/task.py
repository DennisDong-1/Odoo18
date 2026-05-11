from odoo import models, fields
# from datetime import datetime

class SmartTask(models.Model):
    _name = 'smart.task'    
    _description = 'Smart Task'

    name = fields.Char(required=True)
    description = fields.Text()
    user_id = fields.Many2one('res.users', string="Assigned To") #creates a relationship - each task belongs to ONE user, 'res.users' - Odoo's built in users table
    deadline = fields.Date()

    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'high')
    ], default = 'medium')

    state = fields.Selection([
        ('todo', 'To Do'),
        ('in_progress', 'In Progess'),
        ('done', 'Done')
    ], default='todo')

    time_spent = fields.Float(
        string="Time Spent (Hours)",
        readonly = True
        )
    
    start_time = fields.Datetime(
        readonly = True
    )

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