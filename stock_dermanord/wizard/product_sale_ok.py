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

from openerp.exceptions import except_orm, Warning, RedirectWarning,MissingError
from openerp import models, fields, api, _
from cStringIO import StringIO
import base64

import logging
_logger = logging.getLogger(__name__)

try:
    import unicodecsv as csv
except:
    _logger.info("No module named unicodecsv. sudo pip install unicodecsv")

class stock_picking_wizard(models.TransientModel):
    _name = 'product.sale_ok.wizard'
    _description = 'Update Sale ok'

    data = fields.Binary(string='CSV File', required=True)
    message = fields.Text(string='Message')

    @api.multi
    def update_values(self):
        d = csv.DictReader(StringIO(base64.b64decode(self.data)))
        message = ''
        for r in d:
            try:
                template = self.env['ir.model.data'].xmlid_to_object(r['id'])
                template.website_published = r['website_published'] == 'True'
                sale_ok = 'true' if r['website_published'] == 'True' else 'false'
                self.env.cr.execute("UPDATE product_template SET sale_ok = %s WHERE id = %s", (sale_ok, template.id))
                if template.product_variant_ids:
                    template.product_variant_ids.with_context({'supress_checks': True}).write({'sale_ok': r['sale_ok'] == 'True'})
            except:
                message += "Couldn't update product %s." % r.get('id')
        if message:
            self.message = message
            action = self.env['ir.actions.act_window'].for_xml_id('stock_dermanord', 'action_product_sale_ok_wizard_form')
            action['res_id'] = self.id
            return action
