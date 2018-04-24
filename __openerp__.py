# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#
#    Author: crobert@caillot.fr
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
{
    "name": "SMS gateway",
    "version": "1.0",
    "depends": [],
    "author": "crobert@caillot.fr",
    "category": "other",
    "description": """
    Uses a smartpphone with smsgateway ultimate to send sms from openerp objects. The sending to the mobile phone is made with http requests

    Utilise un telephone portable avec l'appli smsgateway ultimate pour envoyer des sms. la communication avec le mobile se fait en requete http

    needs requests package: sudo pip install requests

    sample of use:
        phone = ['0607080910','0102030405']
        message = "test sms"
        self.pool.get('sms.gateway').send_message(cr, uid,phone,message)
    """,
    "init_xml": [],
    'data': [
         'sms.xml',
        # 'security/ir.model.access.csv'
                   ],
    'installable': True,
    'active': False,
}