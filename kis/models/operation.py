import random

import requests

from odoo import fields, models, api


class Operation(models.Model):
    _name = 'operation'
    _description = 'Операция'

    name = fields.Char(string='Наименование')
    product_id = fields.Many2one(comodel_name='product', string='Продукт')
    priority = fields.Integer(string='Приоритет')
    work_center = fields.Many2one(comodel_name='work.center', string='Рабочий центр')
    quantity = fields.Integer(string='Количество')
    type = fields.Many2one(comodel_name='operation.type', string='Тип проверки')
    sample_quantity = fields.Integer(string='Выборка', compute='_compute_sample_otk')
    date_get_in_work = fields.Datetime(string='Время получения в работу')
    date_start_plan = fields.Datetime(string='Начало план')
    date_end_plan = fields.Datetime(string='Окончание план')
    date_start_fact = fields.Datetime(string='Начало факт')
    date_end_fact = fields.Datetime(string='Окончание факт')
    comment = fields.Char(string='Комментарий')
    manufacturing_type = fields.Selection(selection=[
        ('manufacturing', 'Производство'),
        ('other', 'Другое'),
    ], string='Тип', default='other')

    state = fields.Selection(selection=[
        ('draft', 'Черновик'),
        ('in_process', 'В процессе'),
        ('done', 'Выполнено'),
        ('cancelled', 'Отменено'),
    ], string='Статус', default='draft')
    time_ids = fields.One2many(comodel_name='operation.time', inverse_name='operation_id', string='История выполнения')
    completed_product_ids = fields.One2many(comodel_name='operation.completed.product', inverse_name='operation_id',
                                            string='Проверенная продукция')

    def create_operation(self):

        cookies = COOKIES

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            # 'Cookie': '_ym_uid=1687759526803437176; cids=1; session_id=df92a0a72b5c62c90b6d9731c6e61c41f6b7e22d; _ym_d=1723039502',
            'Origin': 'https://ri.forban.tech',
            'Referer': 'https://ri.forban.tech/web',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'id': 7,
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'model': 'mrp.workorder',
                'method': 'web_search_read',
                'args': [],
                'kwargs': {
                    'limit': 80,
                    'offset': 0,
                    'order': '',
                    'count_limit': 10001,
                    'context': {
                        'lang': 'ru_RU',
                        'tz': 'Europe/Moscow',
                        'uid': 2,
                        'allowed_company_ids': [
                            1,
                        ],
                        'bin_size': True,
                        'params': {
                            'action': 234,
                            'model': 'mrp.workorder',
                            'view_type': 'list',
                            'cids': 1,
                            'menu_id': 198,
                        },
                    },
                    'domain': [
                        '&',
                        [
                            'production_id.state',
                            'in',
                            [
                                'plan',
                                'in_progress',
                                'to_close',
                                'closed',
                            ],
                        ],
                        [
                            'sample_otk_id',
                            '!=',
                            False,
                        ],
                    ],
                    'fields': [
                        'index',
                        'name',
                        'resource_id',
                        'quantity',
                        'product_id'
                    ],
                },
            },
        }

        response = requests.post(
            'https://ri.forban.tech/web/dataset/call_kw/mrp.workorder/web_search_read',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )
        if response.status_code == 200:
            for _ in range(random.randint(1,5)):
                record = random.choice(response.json()['result']['records'])
                product_id = self.env['product'].search([('name', '=', record['product_id'][1])], limit=1)
                if not product_id:
                    product_id = self.env['product'].create({
                        'name': record['product_id'][1]
                    })

                operation_type_ids = self.env['operation.type'].search([])

                work_center_ids = self.env['work.center'].search([])

                operation_id = self.env['operation'].create({
                    'name': record['name'],
                    'work_center': random.choice(work_center_ids).id,
                    'quantity': record['quantity'],
                    'product_id': product_id.id,
                    'priority': random.choice([50, 100, 150]),
                    'type': random.choice(operation_type_ids).id,
                    'manufacturing_type': 'manufacturing',
                    'date_get_in_work': fields.datetime.now()
                })

    def action_set_state_in_process(self):
        for record in self:
            record.update({
                'state': 'in_process',
                'date_start_fact': fields.datetime.now()
            })
            record.time_ids.create({
                'user_id': self.env.user.id,
                'time_start': fields.datetime.now(),
                'operation_id': record.id,
            })

    def action_set_state_done(self):
        for record in self:
            record.update({
                'state': 'done',
                'date_end_fact': fields.datetime.now()
            })
            for item in record.time_ids:
                if not item.time_end:
                    item.update({
                        'time_end': fields.datetime.now()
                    })

    def action_set_state_cancelled(self):
        for record in self:
            record.update({
                'state': 'cancelled'
            })

    @api.depends('type', 'quantity')
    def _compute_sample_otk(self):
        for record in self:
            record.sample_quantity = 0
            sample_line_ids = record.type.line_ids.sorted(lambda x: x.total_complete_products)
            if sample_line_ids:
                min_sample = sample_line_ids[0]
                max_sample = sample_line_ids[-1]

                if 0 < record.quantity < min_sample.total_complete_products:
                    if record.quantity < min_sample.sample:
                        record.sample_quantity = record.quantity
                    else:
                        record.sample_quantity = min_sample.sample
                elif record.quantity >= max_sample.total_complete_products:
                    if max_sample.uom == 'unit':
                        record.sample_quantity = max_sample.sample
                    else:
                        record.sample_quantity = record.quantity / 100 * max_sample.sample
                else:
                    for index, item in enumerate(sample_line_ids):
                        if item.total_complete_products <= record.quantity < sample_line_ids[index + 1].total_complete_products:
                            if item.uom == 'unit':
                                record.sample_quantity = item.sample
                            else:
                                record.sample_quantity = record.quantity / 100 * item.sample
                            break
