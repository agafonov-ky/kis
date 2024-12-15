from odoo import fields, models, api


class OperationType(models.Model):
    _name = 'operation.type'
    _description = 'Тип операции'

    name = fields.Char(string='Наименование')
    comment = fields.Char(string='Комментарий')
    line_ids = fields.One2many(comodel_name='operation.type.line', inverse_name='operation_type_id', string='Выборки')