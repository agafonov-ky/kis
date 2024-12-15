from odoo import fields, models, api


class Product(models.Model):
    _name = 'product'
    _description = 'Продукт'

    name = fields.Char(string='Наименование')
