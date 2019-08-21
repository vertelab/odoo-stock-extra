# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2019 Vertel AB (<http://vertel.se>).
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

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    float_format_field = fields.Float(string='Float Format', compute='_compute_float_format_field', help="Used to format floats supplied in context ({'float_format_field': 23.5})")
    
    @api.one
    def _compute_float_format_field(self):
        self.float_format_field = self.env.context.get('float_format_field', 0.0)

    @api.multi
    def _get_delivery_slip_name(self):
        return _('%s Delivery Slip.pdf') % object.name
    
    @api.multi
    def get_original_quantities(self):
        """Returns a dict describing the originally ordered quantities."""
        res = {}
        
        def get_product(product):
            """Returns the dict for the given product from res. Creates it if it doesn't exist yet."""
            if product.id not in res:
                res[product.id] = {
                    'qty': 0.0,
                    'name': product.display_name,
                }
            return res[product.id]
        
        for order in self.env['sale.order'].search([('procurement_group_id', '=', self.group_id.id)]):
            for line in order.order_line:
                product = line.product_id
                qty = line.product_uom._compute_qty_obj(line.product_uom, line.product_uom_qty, product.uom_id)
                product_dict = get_product(product)
                product_dict['qty'] = product_dict['qty'] + qty
                # Handle kit products
                if product.iskit or product.is_offer:
                    bom = product.bom_ids.filtered(lambda r: r.product_id == product) or product.bom_ids.filtered(lambda r: not r.product_id)
                    if bom:
                        bom = bom[0]
                        for bom_line in bom.bom_line_ids:
                            product_dict = get_product(bom_line.product_id)
                            product_dict['qty'] = product_dict['qty'] + qty * bom_line.product_qty
        return res
        
            
            
