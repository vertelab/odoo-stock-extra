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

from openerp import api, models, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import logging
_logger = logging.getLogger(__name__)


class sale_order(models.Model):
    _inherit = 'sale.order'

    cavarosa_box = fields.Char(string='Cavarosa Box')

    @api.model
    def _prepare_procurement_group(self, order):
        vals = super(sale_order, self)._prepare_procurement_group(order)
        vals['cavarosa_box'] = order.cavarosa_box
        return vals


class procurement_group(models.Model):
    _inherit = 'procurement.group'

    cavarosa_box = fields.Char(string='Cavarosa Box')


class procurement_order(models.Model):
    _inherit = 'procurement.order'

    @api.model
    def _run_move_create(self, procurement):
        vals = super(procurement_order, self)._run_move_create(procurement)
        vals['cavarosa_box'] = procurement.group_id.cavarosa_box
        return vals


class stock_move(models.Model):
    _inherit = 'stock.move'

    cavarosa_box = fields.Char(string='Cavarosa Box')


class stock_pack_operation(models.Model):
    _inherit = 'stock.pack.operation'

    cavarosa_box = fields.Char(string='Cavarosa Box')
