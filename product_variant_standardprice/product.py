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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class product_product(models.Model):
    _inherit = 'product.product'

    standard_price = fields.Float(digits_compute=dp.get_precision('Product Price'), help="", groups="base.group_user", string="Cost Price")


class stock_history(models.Model):
    _inherit = 'stock.history'

    product_inventory_value = fields.Float(compute='_get_product_inventory_value', string='Inventory Value', readonly=True)

    @api.multi
    @api.depends('price_unit_on_quant', 'quantity')
    def _get_product_inventory_value(self):
        for line in self:
            line.product_inventory_value = line.price_unit_on_quant * line.quantity

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(stock_history, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        if 'product_inventory_value' in fields:
            group_lines = {}
            for line in res:
                domain = line.get('__domain', domain)
                group_lines.setdefault(str(domain), self.search_read(domain, ['product_inventory_value']))

            for line in res:
                if line.get('__domain'):
                    line['product_inventory_value'] = 0.0
                    for r in group_lines[str(line['__domain'])]:
                        line['product_inventory_value'] += r['product_inventory_value']
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
