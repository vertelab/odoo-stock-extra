# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo import http
from odoo.http import request
from odoo.tools import safe_eval as eval
import traceback

from odoo.modules.registry import Registry

import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    float_format_field = fields.Float(string='Float Format', compute='_compute_float_format_field', help="Used to format floats supplied in context ({'float_format_field': 23.5})")

    def _compute_float_format_field(self):
        for item in self:
            item.float_format_field = item.env.context.get('float_format_field', 0.0)

    def _get_delivery_slip_name(self):
        return _('%s Delivery Slip.pdf') % object.name

    def get_original_quantities(self):
        """Returns a dict describing the originally ordered quantities."""
        res = {}
        for line in self.move_lines:
            res[line.id] = {
                'qty':  line.product_qty or 0.0,
                'name': line.product_id.display_name,
            }
        return res

    # ~ float_format_field = fields.Float(string='Float Format', compute='_compute_float_format_field', help="Used to format floats supplied in context ({'float_format_field': 23.5})")
    
    # ~ @api.one
    # ~ def _compute_float_format_field(self):
        # ~ self.float_format_field = self.env.context.get('float_format_field', 0.0)

    # ~ @api.multi
    # ~ def _get_delivery_slip_name(self):
        # ~ return _('%s Delivery Slip.pdf') % object.name
    
    # ~ @api.multi
    # ~ def get_original_quantities(self):
        # ~ """Returns a dict describing the originally ordered quantities."""
        # ~ res = {} 
        # ~ for line in self.move_lines:
            # ~ res[line.id] = {
                # ~ 'qty': line.procurement_id and line.procurement_id.product_qty or 0.0,
                # ~ 'name': line.product.display_name,
            # ~ }
        # ~ return res
