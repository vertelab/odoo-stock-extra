# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Portal Purchase Stock',
    'version': '0.1',
    'category': 'Tools',
    'complexity': 'easy',
    'summary': 'Purchase menu and rights for suppliers',
    'description': """
        
TODO: Move edi_gs1 support into its own module.

This module adds purchase menu for suppliers
============================================

This module installs automatically when you install portal, purchase and 
stock. For suppliers that you have invited using for example Send RFQ or
a self made template (see URL-examples furher) have a menu consisting
of Purchase order and Delivery. (Other modules can add more menus, for 
example mail and sale).

* URL for signup for a new supplier who gets a Purchase Order for the first time:
http://localhost:8069/web/signup?redirect=%2Fweb%23action%3Dmail.action_mail_redirect%26model%3Dpurchase.order%26id%3D<purchase id>&token=<token>&db=<database>

* URL for existing user, arbitary model and resource id:
http://localhost:8069/web?db=<database>#action=mail.action_mail_redirect&login=<user%40domain.com>&res_id=<id>&model=<model>

* add "Manage Lots / Serial Numbers" for suppliers that do picking with lots / serial numbers, 
you can add this in your "Template User" before you invite your supplier.

    """,
    'author': 'Vertel AB',
    'depends': ['sale','purchase','stock','portal','procurement', 'edi_gs1'],
    'data': [
        'portal_purchase_view.xml',
        'security/ir.model.access.csv',
        'security/portal_security.xml',
    ],
    'installable': True,
    'auto_install': False,
    'category': 'Hidden',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
