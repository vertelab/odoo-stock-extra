# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2016- Vertel AB (<http://vertel.se>).
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

import openerp.exceptions
from openerp import models, fields, api, _
import erppeek


import logging
_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit="product.template"

    #~ @api.one
    #~ def _tariff(self):
        #~ if(self.env.ref('base.us').id == self.partner_id.country_id.id):
            #~ self.tariff = self.ustariff
        #~ else:
            #~ self.tariff = self.intrastat_id


    #~ tariff = fields.Char(string='Tariff', compute='_tariff')
    ustariff = fields.Char(string='US Tariff',oldname='x_ustariff')
    iskit = fields.Boolean(string='Is Kit',oldname='x_iskit')

    #orderpoint_ids
    @api.one
    def _cost_price(self):
        self.cost_price = 0.38 * self.list_price
    cost_price = fields.Float(compute="_cost_price")
    @api.one
    def _variants(self):
        self.variants = ','.join([p.default_code or p.name or '' for p in self.product_variant_ids])
    variants = fields.Char(compute="_variants")
    @api.one
    def _taxes(self):
        self.taxes_view = ','.join([t.description for t in self.taxes_id])
        self.supplier_taxes_view = ','.join([t.description for t in self.supplier_taxes_id])
    taxes_view = fields.Char(compute="_taxes")
    supplier_taxes_view = fields.Char(compute="_taxes")
    #~ orderpoints = fields.One2many(related='product_variant_ids.orderpoint_ids')
    #~ @api.one
    #~ def _stock(self):
        #~ self.orderpoints = ','.join([o.name or '' for o in [v.orderpoint_ids or [] for v in self.product_variant_ids]])
    #~ orderpoints = fields.Char(compute='_stock')



class product_attribute_value(models.Model):
    _inherit = "product.attribute.value"


    def get_param(self,param,value):
        if not self.env['ir.config_parameter'].get_param(param):
            self.env['ir.config_parameter'].set_param(param,value)
            return value
        else:
            return self.env['ir.config_parameter'].get_param(param)

    @api.one
    def get_remote_price(self):
        tmpl_id = self.env.context.get('active_id')
        if not tmpl_id:
            return None
        tmpl = self.env['product.template'].browse(tmpl_id)
        base_variant = tmpl.product_variant_ids.sorted(lambda v: v.name)[0]
        this_variant = self.env['product.product'].search([('product_tmpl_id','=',tmpl_id),('id','in',[p.id for p in self.product_ids])])[0]

        client = erppeek.Client(self.get_param('host6','')+':'+'8069',self.get_param('host6db',''), 'admin',self.get_param('host6pw',''))
        if not client:
            raise Warning(_('Create parameter for host6/host6db/host6pw'))

        price_remote_ids = client.model('product.product').search([('default_code','=',this_variant.default_code)])
        if len(price_remote_ids) == 0:
            raise Warning(_('Missing remote product %s (%s)') % (this_variant.default_code,this_variant))
        price_remote = client.model('product.product').browse(price_remote_ids[0])
        _logger.info('Get remote price (remote=%s tmpl=%s)' % (price_remote.list_price,tmpl.lst_price))
        price = self.env['product.attribute.price'].search(['&',('product_tmpl_id','=',tmpl_id),('value_id','=',self.id)])
        if not price:
            self.env['product.attribute.price'].create({
                'product_tmpl_id': tmpl_id,
                'value_id': self.id,
                'price_extra': price_remote.list_price - tmpl.lst_price,
                    })
        else:
            price.write({'price_extra':price_remote.list_price - tmpl.lst_price })

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    @api.one
    def _tariff(self):
        if self.product_id:
            if self.env.ref('base.us').id == self.invoice_id.partner_shipping_id.country_id.id:
                self.tariff = self.product_id.ustariff
            else:
                self.tariff = self.product_id.intrastat_id.name

    tariff = fields.Char(string='Tariff', compute='_tariff')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
