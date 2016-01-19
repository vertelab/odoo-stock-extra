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


#~ class stock_picking(models.Model):
    #~ _inherit = "stock.picking"



class stock_move(models.Model):
    _inherit = "stock.move"
#    _order = 'date_expected desc, quant_source_location, id'  quant_source_location not stored
    quant_source_location = fields.Char(compute="_quant_source_location",string="Source location",help="Source location from move.reserved_quant_ids (stock.quant)",store=False) # can't trigger changes in stock.quant for store
    @api.one
#    @api.onchange('reserved_quant_ids','state')
    def _quant_source_location(self):
        if self.reserved_quant_ids:
            self.quant_source_location = ','.join([q.location_id.name for q in self.reserved_quant_ids])
        elif self.picking_id.pack_operation_ids:
            self.quant_source_location = _('(transfered)')            
        else:
            self.quant_source_location = self.location_id.name + _(' (not reserved)')
        #~ self.quant_source_location = 'Quant:' + ','.join([q.location_id._name_get(q.location_id) for q in self.reserved_quant_ids])



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
