import hashlib
import hmac
import random
import time

from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)


class twoctwop_redirectapi:
    def __init__(self, merchant_id, secret_key, request_uri):
        self.request_uri = request_uri
        self.secret_key = secret_key
        self.data = {
            'merchant_id': merchant_id,
            'order_id': int(round(time.time()*1000)),
            'version': '8.5'
        }

    def request(self):
        # mandatory_fields = ['payment_description', 'order_id', 'amount']
        # for f in mandatory_fields:
        #     if f not in self.data:
        #         raise Exception('Missing mandatory value {}'.format(f))

        self.data['hash_value'] = self._get_request_hash()
        print(self.data)

        # generate form id
        form_id = ''
        chars = 'bcdfghjklmnpqrstvwxyz'
        for i in range(0, 20):
            form_id = '{}{}'.format(
                form_id, chars[random.randint(0, len(chars) - 1)])

        # generate html
        html = []
        html.append('<form id="{}" action="{}" method="post">'.format(
            form_id, self.request_uri))
        for key in ['version', 'merchant_id', 'currency', 'result_url_1', 'hash_value']:
            html.append(
                '<input type="hidden" name="{}" value="{}" />'.format(key, self.data[key]))
        # html.append('Product info: <input type="text" name="payment_description" value="{}" readonly/><br/>'.format(
        #     self.data['payment_description']))
        # html.append('Order No: <input type="text" name="order_id" value="{}" readonly/><br/>'.format(
        #     self.data['order_id']))
        # html.append('Amount: <input type="text" name="amount" value="{:.2f}" readonly/><br/>'.format(
        #     int(self.data['amount'])/100))
        html.append('<input type="submit" value="Pay now">')
        html.append('</form>')
        # html.append(
        #     '<script>document.forms.{}.submit()</script>'.format(form_id))
        return ''.join(html)

    def test_request(self):
        pass

        # form_id = ''

    # def set_transaction_information(self, description, currency, amount):

    def _get_currency_code_from_id(self, id):
        return {
            '702': 'SGD',
            '104': 'MMK',
            '360': 'IDR',
            '764': 'THB',
            '608': 'PHP',
            '344': 'HKD',
            '458': 'MYR',
            '704': 'VND'
        }[str(id)]

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

    def _get_request_hash(self):
        # $version.$merchant_id.$payment_description.$order_id.$currency.$amount.$result_url_1
        fields = ['version', 'merchant_id', 'payment_description',
                  'order_id', 'currency', 'amount', 'result_url_1']

        hash_str = ''
        for f in fields:
            if f in self.data:
                hash_str = '{}{}'.format(hash_str, self.data[f])
        print(hash_str)
        hash = hmac.new(bytes(self.secret_key, 'latin-1'), bytes(hash_str, 'latin-1'),
                        hashlib.sha256).hexdigest()
        # hash = hmac.new(bytes(self.secret_key, 'latin-1'), hash_str.encode('utf-8'),
        #                 hashlib.sha256).hexdigest()

        return hash.upper()

    def _validate_response_hash(self, request):
        pass


# class PaymentAPI(Resource):
#     def get(self):
#         client = twoctwop_redirectapi(
#             'JT04', 'QnmrnH6QE23N', 'https://demo2.2c2p.com/2C2PFrontEnd/RedirectV3/payment')

#         client.test_request()
#         client.request()
#         return {"Position": 1231101}


# class PaymentServer(object):
#     def __init__(self):
#         self.globalData = 'hello'


# paymentServer = PaymentServer()


@app.route('/')
def home():
    return "Hello, World"


@app.route('/payment')
def payment():
    client = twoctwop_redirectapi(
        'JT04', 'QnmrnH6QE23N', 'https://demo2.2c2p.com/2C2PFrontEnd/RedirectV3/payment')

    client.data['amount'] = ('000000000000{}'.format(10700))[-12:]
    client.data['currency'] = client._get_currency_id_from_code('THB')
    client.data['payment_description'] = 'First time test 2c2p'
    client.data['result_url_1'] = 'http://127.0.0.1:5000/payment-result'

    return client.request()


@app.route('/payment-result', methods=['POST'])
def payment_result():
    return "Hello"
    # data = request.json()
    # return jsonify(data)


if __name__ == "__main__":

    # api = Api(app)
    # api.add_resource(PaymentAPI, '/')
    app.run(debug=True)
