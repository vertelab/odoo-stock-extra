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

    creditcard = fields.Boolean('Credit card',oldname='x_creditcard')
    expected_delivery_date = fields.Date('Expected Delivery Date',oldname='x_expected_delivery_date')
    export_shipping = fields.Boolean('Foreign shipping',oldname='x_export_shipping')
    picking_user = fields.Char('Old picking user',oldname='x_pickin_user')
    user_id = fields.Many2one(string='Picking user',comodel_name='res.users')
    pickup_time = fields.Datetime('Pickup time',oldname='x_pickup_time')
    prio = fields.Boolean('Prio',oldname='x_prio')
    pure_cell = fields.Boolean('Cell',oldname='x_pure_cell')
    ready4picking = fields.Boolean('Ready for picking',oldname='x_ready4picking')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
