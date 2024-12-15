from odoo import fields, models, api


class OperationTypeLine(models.Model):
    _name = 'operation.type.line'
    _description = 'Позиция выборки'

    operation_type_id = fields.Many2one(comodel_name='operation.type', string='Тип операции')
    total_complete_products = fields.Integer(string='Количество более')
    sample = fields.Integer(string='Выборка')
    uom = fields.Selection(selection=[
        ('unit', 'Штуки'),
        ('percentage', 'Проценты')
    ], string='Ед. измерения', default='unit')
