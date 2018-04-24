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


    def _check_status_code(self, status_code):
        """
        Take the status code and throw an exception if the server didn't return 200 or 201 code
        @param status_code: status code returned by the server
        @return: True or raise an exception
        """
        message_by_code = {204: 'No content',
                           400: 'Bad Request',
                           401: 'Unauthorized',
                           404: 'Not Found',
                           405: 'Method Not Allowed',
                           500: 'Internal Server Error',}

        error_label = ('This call to sms Gateway failed and '
                       'returned an HTTP status of %d. That means: %s.')
        if status_code in (200, 201):
            return True
        if status_code in message_by_code:
            raise osv.except_osv(_('Warning!'), _(error_label % (status_code, message_by_code[status_code]), status_code))
        else:
            raise osv.except_osv(_('Warning!'), _(("This call to PrestaShop Web Services returned an unexpected HTTP status of: %d")  % (status_code,)))


    def get_phone_formatted(self,phone_number):
        """
        Format phone number and check if len okay after format
        :param phone_number: str phone number
        :return: formatted phone or False
        """
        if not phone_number or not str(phone_number):
            return False
        phone_formatted = str(phone_number).replace('.','').replace('-','').replace('_','').strip()
        return len(phone_formatted) == 10 and phone_formatted.isdigit() and phone_formatted or False


    def send_message(self,cr,uid,phone_numbers,message,context=None):
        """
        Check params and send message via the smartphone gateway
        :param cr: the current row, from the database cursor,
        :param uid: the current user’s ID for security checks,
        :param phone_numbers: tuple list or simple phone numbers
        :param message: the message to send
        :param context: A standard dictionary
        :return:
        """
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
                self._check_status_code(r.status_code)
            except:
                raise osv.except_osv(_('Warning!'),_('smthing went wrong while joining the gateway'))

        if invalid_phones:
            err_str = 'Some phone number are invalid :' + ' / '.join(str(p) for p in invalid_phones)
            raise osv.except_osv(_('Warning!'), _(err_str))
