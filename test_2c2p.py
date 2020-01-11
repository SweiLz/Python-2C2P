import hashlib
import hmac
import random
import time
import json

from flask import Flask, url_for, render_template, redirect, request, jsonify
from forms import PaymentInfoForm
app = Flask(__name__)


class Payment2C2P():
    def __init__(self, merchant_id, secret_key, request_uri):
        self.request_uri = request_uri
        self.secret_key = secret_key
        self.data = {
            'merchant_id': merchant_id,
            'order_id': str(int(round(time.time()*1000))),
            'version': '8.5',
            'result_url_1': 'http://127.0.0.1:5000/payment-complete'
        }

    def setTransaction(self, payment_description, currency, amount, order_id):
        self.data['payment_description'] = payment_description
        self.data['currency'] = str(self._get_currency_id_from_code(currency))
        self.data['amount'] = '{:012}'.format(amount)
        self.data['order_id'] = '{:05}'.format(order_id)

        return self.data

    def request(self):
        mandatory_fields = ['payment_description',
                            'order_id', 'amount', 'currency']
        for f in mandatory_fields:
            if f not in self.data:
                raise Exception('Missing mandatory value {}'.format(f))

        self.data['hash_value'] = self._get_request_hash()

        form_id = ''
        chars = 'bcdfghjklmnpqrstvwxyz'
        for i in range(0, 20):
            form_id = '%s%s' % (
                form_id, chars[random.randint(0, len(chars) - 1)])

        html = []
        html.append('<form id="{}" action="{}" method="post">'.format(
            form_id, self.request_uri))
        for key in self.data:
            html.append('<input type="hidden" name="%s" value="%s" />' %
                        (key, self.data[key]))
        html.append('<input type="submit" value="Pay now">')
        html.append('</form>')
        html.append('<script>document.forms.%s.submit()</script>' % form_id)
        return ''.join(html)

    def _get_request_hash(self):
        fields = ['version', 'merchant_id', 'payment_description',
                  'order_id', 'currency', 'amount', 'result_url_1']

        hash_str = ''
        for f in fields:
            if f in self.data:
                hash_str = '{}{}'.format(hash_str, self.data[f])
        print(hash_str)
        hash_val = hmac.new(bytes(self.secret_key, 'utf-8'),
                            bytes(hash_str, 'utf-8'), hashlib.sha256).hexdigest()
        return hash_val

    def _validate_response_hash(self):

        # rdata = json.dumps("version=8.5&request_timestamp=2020-01-11+16%3A17%3A14&merchant_id=JT04&currency=764&order_id=1578734226319&amount=000000120000&invoice_no=&transaction_ref=1578734226319&approval_code=479135&eci=05&transaction_datetime=2020-01-11+16%3A18%3A17&payment_channel=001&payment_status=000&channel_response_code=00&channel_response_desc=success&masked_pan=411111XXXXXX1111&stored_card_unique_id=&backend_invoice=&paid_channel=&paid_agent=&recurring_unique_id=&ippPeriod=&ippInterestType=&ippInterestRate=&ippMerchantAbsorbRate=&payment_scheme=VI&process_by=VI&sub_merchant_list=&user_defined_1=&user_defined_2=&user_defined_3=&user_defined_4=&user_defined_5=&browser_info=Type%3DChrome79%2CName%3DChrome%2CVer%3D79.0&mcp=&mcp_amount=&mcp_currency=&mcp_exchange_rate=&hash_value=F1247BF43E9E5BAA72BD145BE082110ED280042620889964D369FD367827AADA")

        fields = [
            'version', 'request_timestamp', 'merchant_id', 'currency', 'order_id',
            'amount', 'invoice_no',  'transaction_ref',
            'approval_code', 'eci', 'transaction_datetime', 'payment_channel',
            'payment_status', 'channel_response_code', 'channel_response_desc',
            'masked_pan', 'stored_card_unique_id', 'backend_invoice',
            'paid_channel', 'paid_agent', 'recurring_unique_id',
            'ippPeriod', 'ippInterestType', 'ippInterestRate',
            'ippMerchantAbsorbRate', 'payment_scheme', 'process_by',
            'sub_merchant_list',
            'user_defined_1',
            'user_defined_2', 'user_defined_3', 'user_defined_4', 'user_defined_5',
            'browser_info', 'mcp', 'mcp_amount', 'mpc_currency', 'mcp_exchange_rate'
        ]

        hash_str = ''
        for f in fields:
            if f in request.POST:
                hash_str = '{}{}'.format(hash_str, request.POST[f])
        print(hash_str)
        hash_val = hmac.new(bytes(self.secret_key, 'utf-8'),
                            bytes(hash_str, 'utf-8'), hashlib.sha256).hexdigest()
        return hash_val

    def _get_currency_id_from_code(self, code):
        return {
            'SGD': 702,
            'MMK': 104,
            'IDR': 360,
            'THB': 764,
            'PHP': 608,
            'HKD': 344,
            'MYR': 458,
            'VND': 704
        }[code.upper()]


payment2C2P = Payment2C2P(
    'JT04', 'QnmrnH6QE23N', 'https://demo2.2c2p.com/2C2PFrontEnd/RedirectV3/payment')


@app.route('/', methods=('GET', 'POST'))
def hello_world():
    form = PaymentInfoForm(request.form)
    if request.method == 'POST':
        if form.is_submitted():
            print("Form successfully submitted")
        if form.validate_on_submit():
            id = payment2C2P.data['order_id']
            # message = json.
            # print(form.json())
            # print(form.description.data)
            # "Hello World"  #
            return redirect(url_for('payment', desc=form.description.data, curr=form.currency.data, amount=form.amount.data, order_id=id), code=307)
        else:
            print(form.errors)
    return render_template('index.html', form=form, template='form-template')


@app.route('/payment', methods=('GET', 'POST'))
def payment():
    if request.method == 'POST':
        desc = request.args.get('desc')
        curr = request.args.get('curr')
        amount = int(float(request.args.get('amount'))*100)
        order_id = int(request.args.get('order_id'))
        payment2C2P.setTransaction(desc, curr, amount, order_id)
        return payment2C2P.request()
    return "OK"


@app.route('/payment-complete', methods=('GET', 'POST'))
def success():
    # print(request.)
    return render_template('success.html', template='success-template')


if __name__ == "__main__":
    app.config['SECRET_KEY'] = "powerful secretkey"
    app.run(debug=True)


# Test Card
'''
Card brand 	Card no / Account information 	Expiry date 	security code

Visa 	    4111-1111-1111-1111 	12/2020 	123

MasterCard 	5555-5555-5555-4444 	12/2020 	123

JCB 	    3566-1111-1111-1113 	12/2020 	123

Amex 	    3782-8224-6310-005 	12/2020 	1234

China Union Pay  	6250-9470-0000-0014 Mobile phone number: 11112222
Dynamic Verification Code: 111111 	12/2033 	123

Alipay 	Username: sandbox_domestic@alipay.com
Password: 111111
Payment password: 111111 	  	

WeChat Pay 	Test User Account: 2604462170
Login Password: WXufo666
Pay Password: 139713 	  	 
'''
