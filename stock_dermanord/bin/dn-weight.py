#!/usr/bin/python
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

import erppeek
db_new = erppeek.Client.from_config('eightzero')
db_old = erppeek.Client.from_config('sixone')

for p in db_old.model('product.product').read(db_old.model('product.product').search(['&', ('sale_ok', '=', True), ('default_code', '!=', '')]), ['default_code', 'volume', 'weight', 'weight_net']):
    product = db_new.model('product.product').search([('default_code', '=', p['default_code'])])
    if not product:
        product = db_new.model('product.product').search(['&', ('default_code', '=', p['default_code']), ('active', '=', False)])
    if len(product) == 1:
        print 'Found product: %s' %product[0]
        product_id = product[0]
        db_new.model('product.product').write(product_id, {'volume': p.get('volume'), 'weight': p.get('weight'), 'weight_net': p.get('weight_net'),})
    else:
        print 'Det gick helvete: %s :: %s' %(p.get('default_code'), product)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
