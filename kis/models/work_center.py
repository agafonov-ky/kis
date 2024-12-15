from odoo import fields, models, api


class WorkCenter(models.Model):
    _name = 'work.center'
    _description = 'Рабочий центр'

    name = fields.Char(string='Наименование')
