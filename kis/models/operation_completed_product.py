from odoo import fields, models, api


class OperationCompletedProduct(models.Model):
    _name = 'operation.completed.product'
    _description = 'Готовая продукция'

    operation_id = fields.Many2one('operation', string='Операция')
    user_id = fields.Many2one('res.users', 'Пользователь', default=lambda self: self.env.user)
    date = fields.Datetime(string='Дата', default=lambda _: fields.datetime.now())
    quantity = fields.Integer(string='Количество')
    state = fields.Selection(selection=[
        ('valid', 'Годные'),
        ('not_valid', 'Условно-годные'),
        ('scrap', 'Не годные')
    ], string='Статус', default='valid')
