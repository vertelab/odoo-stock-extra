# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2017- Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, models, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from xlrd import open_workbook
from xlrd.book import Book
from xlrd.sheet import Sheet
import os
import base64
import logging
_logger = logging.getLogger(__name__)


class Iterator(object):
    def __init__(self, data):
        self.row = 0
        self.data = data
        self.rows = data.nrows - 3
        self.header = [c.value.lower() for c in data.row(0)]
        self.zip_from = data.row(1)[1].value
        self.zip_to = data.row(data.nrows - 1)[1].value

    def __iter__(self):
        return self

    def next(self):
        if self.row >= self.rows:
            raise StopIteration
        r = self.data.row(self.row + 3)
        self.row += 1
        return {self.header[n]: r[n].value for n in range(len(self.header))}


class CavarosaDeliveryCostImport(models.TransientModel):
    _name = 'cavarosa.delivery.cost.import'

    data = fields.Binary(string='File')
    @api.model
    def _active_id(self):
        return self.env['delivery.carrier'].browse(self._context.get('active_id', []))
    carrier_id = fields.Many2one(comodel_name='delivery.carrier', default=_active_id)

    def import_costs(self):
        for cost in self:
            if cost.data:
                wb = open_workbook(file_contents=base64.b64decode(self.data))
                ws = wb.sheet_by_index(0)
                if len(cost.carrier_id.pricelist_ids) > 0:
                    for grid in cost.carrier_id.pricelist_ids:
                        cost.env['delivery.grid.line'].search([('grid_id', '=', grid.id)]).unlink()
                        grid.unlink()
                pricelist = cost.env['delivery.grid'].create({
                    'carrier_id': cost.carrier_id.id,
                    'name': 'Home Delivery',
                    'country_ids': [(4, cost.env.ref('base.se').id, 0)],
                    'zip_from': str(int(Iterator(ws).zip_from)),
                    'zip_to': str(int(Iterator(ws).zip_to)),
                })
                for r in Iterator(ws):
                    cost.env['delivery.grid.line'].create({
                        'name': '%s - 1-3 kli' %int(r.get('postnummer')),
                        'type': 'quantity',
                        'operator': '<=',
                        'max_value': 3.0,
                        'price_type': 'fixed',
                        'list_price': r.get('pris 1-3 kli'),
                        'standard_price': 0.0,
                        'grid_id': pricelist.id,
                    })
                    cost.env['delivery.grid.line'].create({
                        'name': '%s - 4-6 kli' %int(r.get('postnummer')),
                        'type': 'quantity',
                        'operator': '>=',
                        'max_value': 4.0,
                        'price_type': 'fixed',
                        'list_price': r.get('pris 4-6 kli'),
                        'standard_price': 0.0,
                        'grid_id': pricelist.id,
                    })


class delivery_carrier(models.Model):
    _inherit = 'delivery.carrier'

    cavarosa_box = fields.Boolean(string="Cavarosa Box",help="Check this field if the Carrier Type is a Cavarosa Box.")
    #~ @api.one
    #~ def _data_input(self):
        #~ if self.pickup_location:
            #~ self.data_input = '<select id="carrier_data" class="selectpicker" data-style="btn-primary"><option value="1">Choose location</option>%s</select>' % \
                              #~ '\n'.join(['<option value="%s">%s</option>' % (p.id,p.name) for p in self.env['res.partner'].search([('pickup_location','=',True)])])
    #~ data_input = fields.Text(compute="_data_input",)

    def _carrier_data(self):
        for carry in self:
            if carry.cavarosa_box:
                carry.carrier_data = '<input name="carrier_data" type="text" class="form-control carrier_input" placeholder="Box number..."/>'
            else:
                super(delivery_carrier, carry)._carrier_data()

    @api.model
    def lookup_carrier(self, carrier_id, carrier_data, order):
        carrier = self.env['delivery.carrier'].browse(int(carrier_id))
        if carrier and carrier.cavarosa_box:
            order.cavarosa_box = carrier_data
            order.partner_shipping_id = carrier.partner_id.id
        else:
            super(delivery_carrier, self).lookup_carrier(carrier_id, carrier_data, order)
