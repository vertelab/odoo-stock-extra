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

# sudo pip install -U erppeek
# http://wirtel.be/posts/2014/06/13/using_erppeek_to_discuss_with_openerp/
# http://erppeek.readthedocs.org/

import erppeek

local_server = 'localhost'
local_user = 'admin'
local_passwd = 'sommar2016'
local_database = 'stable_migrated06mar16'
local_port = 9069

client = erppeek.Client('http://%s:%s' % (local_server,local_port),local_database,local_user,local_passwd)

name = client.model('product.product').read([('default_code', '=', '1002-00100')], 'name')[0]
price = client.model('product.product').read([('default_code', '=', '1002-00100')], 'qty_available')[0]

print('%s\t\tPrice: %s' %(name, price))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
