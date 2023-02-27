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

from odoo import api, models, fields, http, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
from xlrd import open_workbook
from xlrd.book import Book
from xlrd.sheet import Sheet
import odoo.addons.decimal_precision as dp
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
        return iter(self.header)

    def next(self):
        if self.row >= self.rows:
            raise StopIteration
        r = self.data.row(self.row + 3)
        self.row += 1
        return {self.header[n]: r[n].value for n in range(len(self.header))}


class CavarosaDeliveryCostImport(models.TransientModel):
    _name = 'cavarosa.delivery.cost.import'

    # postcode_id = fields.Many2one(comodel_name="delivery.carrier",string="Postcode",help="Delivery options for customers that have these pricelists.")

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
                    # 'zip_from': (ws).zip_from,
                    # 'zip_to': (ws).zip_to,
                })
                _logger.warning('hej %s' % Iterator(ws))
                for r in ws:
                    cost.env['delivery.grid.line'].create({
                        'name': '%s - 1-3 kli' % int(r.get('postnummer')),
                        'type': 'quantity',
                        'operator': '<=',
                        'max_value': 3.0,
                        'price_type': 'fixed',
                        'list_price': r.get('pris 1-3 kli'),
                        'standard_price': 0.0,
                        'grid_id': pricelist.id,
                    })
                    cost.env['delivery.grid.line'].create({
                        'name': '%s - 4-6 kli' % int(r.get('postnummer')),
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

    cavarosa_box = fields.Boolean(string="Cavarosa Box", help="Check this field if the Carrier Type is a Cavarosa Box.")
    normal_price = fields.Float(string='Normal Price',
                                help="Keep empty if the pricing depends on the advanced pricing per destination")
    pricelist_ids = fields.Many2many(comodel_name="product.pricelist", string="Pricelists",
                                     help="Delivery options for customers that have these pricelists.")
    postcode_ids = fields.Many2many(comodel_name="delivery.carrier.postcode", string="Postcode",
                                    help="Delivery options for customers that have these pricelists.")

    # def check_postcode(self, postcode):
    #    _logger.warn('check_postcode was called!!!')
    #         # mailing_lists = []
    #         # for mailing_list in request.env['mail.mass_mailing.list'].sudo().search([('website_published', '=', True),('country_ids','in',request.env.user.partner_id.commercial_partner_id.country_id.id)]):
    #         #     mailing_lists.append({
    #         #         'name': mailing_list.name,
    #         #         'id': mailing_list.id,
    #         #         'subscribed': request.env['mail.mass_mailing.contact'].sudo().search_count([('email', '=', email), ('list_id', '=', mailing_list.id)]) > 0,
    #         #     })
    #         # return mailing_lists

    #         postcode = self.env['delivery.carrier.postcode'].search([('postcode_ids','in',self.env.user.partner_id.commercial_partner_id.zip)])
    #         if postcode:
    #             if self.name == "Hemleverans":
    #                 self.active = True
    #         else:
    #             self.active = False

    # TODO: SUper for this function! fix it!
    # def _match_address(self, partner):

    #     res = super(delivery_carrier,self)._match_address(partner)

    #     postcode = self.env['delivery.carrier.postcode'].search([('name','=',self.env.user.partner_id.commercial_partner_id.zip)])
    #     _logger.warn('sandra %s' % self.env.user.partner_id.commercial_partner_id.zip)
    #     # hur kan vi lösa aktive problem eller vi bygger en sök fun
    #     if not self.env.user.partner_id.commercial_partner_id.zip in self.postcode_ids.mapped('name'):

    #     return res

    def _data_input(self):
        for pickup in self:
            if pickup.pickup_location:
                pickup.data_input = '<select id="carrier_data" class="selectpicker" data-style="btn-primary"><option value="1">Choose location</option>%s</select>' % \
                                    '\n'.join(['<option value="%s">%s</option>' % (p.id, p.name) for p in
                                               pickup.env['res.partner'].search([('pickup_location', '=', True)])])

    data_input = fields.Text(compute="_data_input", )

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


class delivery_carrier_postcode(models.Model):
    _name = "delivery.carrier.postcode"

    name = fields.Char(string="Postcode")


class delivery_grid(models.Model):
    _name = "delivery.grid"
    _description = "Delivery Grid"

    name = fields.Char(string='Grid Name', required=True)
    sequence = fields.Integer(string='Sequence',
                              help="Gives the sequence order when displaying a list of delivery grid.")
    carrier_id = fields.Many2one('delivery.carrier', 'Carrier', ondelete='cascade')
    country_ids = fields.Many2many('res.country', 'delivery_grid_country_rel', 'grid_id', 'country_id', 'Countries')
    state_ids = fields.Many2many('res.country.state', 'delivery_grid_state_rel', 'grid_id', 'state_id', 'States')
    zip_from = fields.Char(string='Start Zip', size=12)
    zip_to = fields.Char(string='To Zip', size=12)
    line_ids = fields.One2many('delivery.grid.line', 'grid_id', 'Grid Line', copy=True)
    active = fields.Boolean(string='Active', help="If the active field is set to False, it will allow you to hide the "
                                                  "delivery grid without removing it.")

    _defaults = {
        'active': lambda *a: 1,
        'sequence': lambda *a: 1,
    }
    _order = 'sequence'

    def get_price(self, cr, uid, id, order, dt, context=None):
        total = 0
        weight = 0
        volume = 0
        quantity = 0
        total_delivery = 0.0
        product_uom_obj = self.pool.get('product.uom')
        for line in order.order_line:
            if line.state == 'cancel':
                continue
            if line.is_delivery:
                total_delivery += line.price_subtotal + self.pool['sale.order']._amount_line_tax(cr, uid, line,
                                                                                                 context=context)
            if not line.product_id or line.is_delivery:
                continue
            q = product_uom_obj._compute_qty(cr, uid, line.product_uom.id, line.product_uom_qty,
                                             line.product_id.uom_id.id)
            weight += (line.product_id.weight or 0.0) * q
            volume += (line.product_id.volume or 0.0) * q
            quantity += q
        total = (order.amount_total or 0.0) - total_delivery

        ctx = context.copy()
        ctx['date'] = order.date_order
        total = self.pool['res.currency'].compute(cr, uid, order.currency_id.id, order.company_id.currency_id.id, total,
                                                  context=ctx)
        return self.get_price_from_picking(cr, uid, id, total, weight, volume, quantity, context=context)

    def get_price_from_picking(self, cr, uid, id, total, weight, volume, quantity, context=None):
        grid = self.browse(cr, uid, id, context=context)
        price = 0.0
        ok = False
        price_dict = {'price': total, 'volume': volume, 'weight': weight, 'wv': volume * weight, 'quantity': quantity}
        for line in grid.line_ids:
            test = eval(line.type + line.operator + str(line.max_value), price_dict)
            if test:
                if line.price_type == 'variable':
                    price = line.list_price * price_dict[line.variable_factor]
                else:
                    price = line.list_price
                ok = True
                break
        if not ok:
            raise osv.except_osv(_("Unable to fetch delivery method!"), _("Selected product in the delivery method "
                                                                          "doesn't fulfill any of the delivery grid("
                                                                          "s) criteria."))

        return price


class delivery_grid_line(models.Model):
    _name = "delivery.grid.line"
    _description = "Delivery Grid Line"
    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', help="Gives the sequence order when calculating delivery grid.")
    grid_id = fields.Many2one('delivery.grid', 'Grid', ondelete='cascade')
    # types = fields.selection([('weight','Weight'),('volume','Volume'),\
    #                               ('wv','Weight * Volume'), ('price','Price'), ('quantity','Quantity')],\
    #                               'Variable', required=True)
    operator = fields.Selection([('==', '='), ('<=', '<='), ('<', '<'), ('>=', '>='), ('>', '>')], 'Operator',
                                required=True)
    max_value = fields.Float('Maximum Value', required=True)
    price_type = fields.Selection([('fixed', 'Fixed'), ('variable', 'Variable')], 'Price Type', required=True)
    variable_factor = fields.Selection(
        [('weight', 'Weight'), ('volume', 'Volume'), ('wv', 'Weight * Volume'), ('price', 'Price'),
         ('quantity', 'Quantity')], 'Variable Factor', required=True)
    list_price = fields.Float(string='Sale Price', digits_compute=dp.get_precision('Product Price'), required=True)
    standard_price = fields.Float(string='Cost Price', digits_compute=dp.get_precision('Product Price'), required=True)

    _defaults = {
        'sequence': lambda *args: 10,
        'type': lambda *args: 'weight',
        'operator': lambda *args: '<=',
        'price_type': lambda *args: 'fixed',
        'variable_factor': lambda *args: 'weight',
    }
    _order = 'list_price'


# class PostcodeController(http.Controller):

#    @http.route('/shop/payment')
#    def check_postcode(self):
#        _logger.warn('check_postcode was called')

# class ImportController(http.Controller):

#     @http.route('/base_import/set_file', methods=['POST'])
#     def set_file(self, file, import_id, jsonp='callback'):
#         import_id = int(import_id)

#         written = request.env['base_import.import'].browse(import_id).write({
#             'file': file.read(),
#             'file_name': file.filename,
#             'file_type': file.content_type,
#         })

#         return 'window.top.%s(%s)' % (misc.html_escape(jsonp), json.dumps({'result': written}))
