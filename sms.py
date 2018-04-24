# -*- coding: utf-8 -*-
# OpenERP, Open Source Management Solution
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

__author__ = 'crobert@caillot.fr'

import requests
from openerp.tools.translate import _
from openerp.osv import osv, fields


sender = ". CAILLOT"

class sms_gateway(osv.Model):

    _name = 'sms.gateway'

    # Format phone number and check if len okay after format
    def get_phone_formatted(self,phone_number):
        if not phone_number or not str(phone_number):
            return False
        phone_formatted = str(phone_number).replace('.','').replace('-','').replace('_','').strip()
        return len(phone_formatted) == 10 and phone_formatted.isdigit() and phone_formatted or False


    # take a tuple or list or unique number and a message to send
    def send_message(self,cr,uid,phone_numbers,message,context=None):

        # We control everything
        if not message:
            raise osv.except_osv(_('Warning!'), _('No message was provided'))
        ip_sms_gateway = self.pool['ir.config_parameter'].get_param(cr, uid, "sms_gateway_ip:port(ex:1.0.0.152:45091)", context=context)

        if not ip_sms_gateway:
            raise osv.except_osv(_('Warning!'), _('No ip for gateway was found in ir.config_parameter'))
        invalid_phones = []
        if type(phone_numbers) not in (tuple,list):
            phone_numbers = [phone_numbers]
        if not phone_numbers:
            raise osv.except_osv(_('Warning!'), _('No phone number'))
        message += sender

        # we try to send the message
        for phone in phone_numbers:
            phone_formatted = self.get_phone_formatted(phone)
            if not phone_formatted:
                invalid_phones.append(phone)
                continue
            try:
                # http://192.168.1.66:58432/send.html?smsto=06XXXXXX&smsbody=tets&smstype=sms
                requetesms = 'http://' + ip_sms_gateway + '/send.html?' + 'smsto=' + phone_formatted + '&smsbody=' + message + '&smstype=sms'
                r = requests.get(requetesms)
                r.status_code
            except:
                raise osv.except_osv(_('Warning!'),_('smthing went wrong while joining the gateway'))

        if invalid_phones:
            err_str = 'Some phone number are invalid :' + ' / '.join(str(p) for p in invalid_phones)
            raise osv.except_osv(_('Warning!'), _(err_str))
