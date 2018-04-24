# c5t_sms_gateway
Openerp odoo  Tested with openerp 7 Saas-3 
Uses a smartphone with smsgateway ultimate to send sms from openerp objects. The sending to the mobile phone is made with http requests

    Utilise un telephone portable avec l'appli smsgateway ultimate pour envoyer des sms. la communication avec le mobile se fait en requete http

    needs requests package: sudo pip install requests

    sample of use:
        phone = ['0607080910','0102030405']
        message = "test sms"
        self.pool.get('sms.gateway').send_message(cr, uid,phone,message)
