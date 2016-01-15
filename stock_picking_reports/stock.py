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


class stock_picking(models.Model):
    _inherit = "stock.picking"

    move_source_location = fields.Char(compute="_move_source_location",string="Move location",help="Source location from move.reserved_quant_ids (stock.quant)",store=True)
    @api.one
    def _move_source_location(self):
        self.move_source_location = ','.join([q.location_id._name_get(q.location_id) for q in move.reserved_quant_ids])



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
