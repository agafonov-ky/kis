from odoo import fields, models, api


class OperationTime(models.Model):
    _name = 'operation.time'
    _description = 'История выполнения'

    operation_id = fields.Many2one('operation', string='Операция')
    user_id = fields.Many2one('res.users', 'Пользователь', default=lambda self: self.env.user)
    duration = fields.Float('Длительность', compute='_compute_duration')
    time_start = fields.Datetime('Дата и время начала')
    time_end = fields.Datetime('Дата и время окончания')

    @api.depends('time_end', 'time_start')
    def _compute_duration(self):
        for record in self:
            if record.time_start and record.time_end:
                record.duration = (record.time_end - record.time_start).total_seconds() / 60
            else:
                record.duration = 0
