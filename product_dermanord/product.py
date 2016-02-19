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

import logging
_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit="product.template"
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
    
 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
