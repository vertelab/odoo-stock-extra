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
        for line in self.move_lines:
            res[line.id] = {
                'qty': line.procurement_id and line.procurement_id.product_qty or 0.0,
                # ~ 'name': line.product.display_name,
            }
        return res
