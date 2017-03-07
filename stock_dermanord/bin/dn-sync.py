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

try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing, pip install odoorpc')

#TODO: Make database a parameter. Add a sequence to servers to avoid hard coding. Make mail adress in bash script configurable.
params = odoorpc.session.get('payroll')
odoo = odoorpc.ODOO(params.get('host'),port=params.get('port'))
odoo.login(params.get('database'),params.get('user'),params.get('passwd'))

msg = ""
for server_id in range(1, 3):
    sync_id = odoo.env['base.synchro'].create({
        'server_url': server_id,
        'user_id': odoo.env.uid,
    })
    res = {}
    try:
        res = odoo.env['base.synchro'].browse(sync_id).upload_download_multi_thread()
    except:
        pass
    if res.get('views', [[0]])[0][0] != odoo.env.ref('base_synchro.view_base_synchro_finish').id:
        msg += "Sync failed on server %s." % server_id
        exit(msg)
    else:
        msg += "Synced server %s.\n" % server_id
