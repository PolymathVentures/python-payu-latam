import unittest
from payu import PayU, ImproperlyConfigured
from helpers import generate_reference_code

class PayUTestCase(unittest.TestCase):

    def _make_one(self):
        # test credentials
        # http://developers.payulatam.com/en/sdk/sandbox.html
        conf = dict(merchant_id = "500238",
                    api_login = "11959c415b33d0c",
                    api_key = "6u39nqhq8ftd0hlvnjfs66eh8c",
                    account_id = "500538",
                    verify_ssl =  False # payu sandbox cert is not trusted
        )
        return PayU(**conf)

    def test_configure(self):
        conf = dict(api_key=1,
                    api_login=2,
                    account_id=3,
                    merchant_id=4,
                    test=True,
                    payment_url='ham',
                    query_url='cheese')

        payu = PayU(**conf)

        assert payu.config['API_KEY'] == 1
        assert payu.config['API_LOGIN'] == 2
        assert payu.config['ACCOUNT_ID'] == 3
        assert payu.config['MERCHANT_ID'] == 4
        assert payu.config['TEST'] == True

        payu2 = PayU()
        payu2.configure(**conf)

        assert payu2.config['API_KEY'] == 1
        assert payu2.config['API_LOGIN'] == 2
        assert payu2.config['ACCOUNT_ID'] == 3
        assert payu2.config['MERCHANT_ID'] == 4
        assert payu2.config['TEST'] == True

    def test_tokenization(self):

        payu = self._make_one()
        cc_data = {
            "payerId": "12",
            "name": "Doughnut Jimmy",
            "paymentMethod": "VISA",
            "number": "4111111111111111",
            "expirationDate": "2017/01"
        }

        expected_resp = {
            'code': 'SUCCESS',
            'creditCardToken': {'creationDate': None,
                                'creditCardTokenId': 'ef2d19b7-18e4-4406-aaa1-acfb6a57967a',
                                'errorDescription': None,
                                'expirationDate': None,
                                'identificationNumber': None,
                                'maskedNumber': '411111******1111',
                                'name': 'Doughnut Jimmy',
                                'number': None,
                                'payerId': '12',
                                'paymentMethod': 'VISA'},
            'error': None}

        resp = payu.tokenize(cc_data)
        self.assertEqual(resp.json(), expected_resp)

        incomplete_cc_data = {
            "paymentMethod": "VISA",
            "number": "4111111111111111",
            "expirationDate": "2017/01"
        }

        with self.assertRaisesRegex(ImproperlyConfigured, 'Missing attributes: payerId, name'):
            resp = payu.tokenize(incomplete_cc_data)

    def test_build_signature(self):
        payu = self._make_one()
        order = {
            'referenceCode': 'payment_test_80k9j1n7dg',
            'value': '1000',
            'currency': 'COP'
        }

        signature = payu.build_signature(order)
        assert signature == '1811d58e896b1c89a9332ac0951f10ea'

    def test_build_order(self):
        payu = self._make_one()
        ref = 'payment_test_80k9j1n7dg'
        order_data = {
            'referenceCode': ref,
            'value': '1000',
            'currency': 'COP',
            'description': "payment test"
        }
        order = payu.build_order(order_data)
        assert order['accountId'] == payu.config['ACCOUNT_ID']
        assert order['referenceCode'] == ref
        assert order['description'] == 'payment test'
        assert order['signature'] == '1811d58e896b1c89a9332ac0951f10ea'
        assert order['additionalValues']['TX_VALUE']['value'] == '1000'
        assert order['additionalValues']['TX_VALUE']['currency'] == 'COP'
        assert order['language'] == 'es'

    def test_build_transaction(self):
        payu = self._make_one()

        ref = 'payment_test_80k9j1n7dg'
        order_data = {
            'referenceCode': ref,
            'value': '1000',
            'currency': 'COP',
            'description': "payment test"
        }
        order = payu.build_order(order_data)

        cc_data = {
            "payerId": "12",
            "name": "Doughnut Jimmy",
            "paymentMethod": "VISA",
            "number": "4111111111111111",
            "expirationDate": "2017/01"
        }
        cc_token = payu.tokenize(cc_data)
        token = cc_token.json()['creditCardToken']['creditCardTokenId']
        transaction = payu.build_transaction(
            order=order,
            payment_method='VISA',
            payment_country='CO',
            credit_card_token = token,
            additional_data = {
                "deviceSessionId": "vghs6tvkcle931686k1900o6e1",
                "ipAddress": "127.0.0.1",
                "cookie": "pt1t38347bs6jc9ruv2ecpv7o2",
                "userAgent": "Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0"
            })

        expected_result = {
            "order": {
                "accountId": "500538",
                "referenceCode": 'payment_test_80k9j1n7dg',
                "description": "payment test",
                "language": "es",
                "signature": '1811d58e896b1c89a9332ac0951f10ea',
                "additionalValues": {
                    "TX_VALUE": {
                        "value": '1000',
                        "currency": 'COP'
                    }
                },
            },
            "creditCardTokenId": "ef2d19b7-18e4-4406-aaa1-acfb6a57967a",
            "type": "AUTHORIZATION_AND_CAPTURE",
            "paymentMethod": "VISA",
            "paymentCountry": "CO",
            "deviceSessionId": "vghs6tvkcle931686k1900o6e1",
            "ipAddress": "127.0.0.1",
            "cookie": "pt1t38347bs6jc9ruv2ecpv7o2",
            "userAgent": "Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0"
        }

        assert expected_result == transaction


    def test_submit_transaction(self):
        payu = self._make_one()

        ref = generate_reference_code()
        order_data = {
            'referenceCode': ref,
            'value': '1000',
            'currency': 'COP',
            'description': "payment test"
        }
        transaction = payu.build_transaction(
            order=payu.build_order(order_data),
            payment_method='VISA',
            payment_country='CO',
            credit_card_token = 'ef2d19b7-18e4-4406-aaa1-acfb6a57967a',
            additional_data = {
                "deviceSessionId": "vghs6tvkcle931686k1900o6e1",
                "ipAddress": "127.0.0.1",
                "cookie": "pt1t38347bs6jc9ruv2ecpv7o2",
                "userAgent": "Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0"
            })

        resp = payu.submit_transaction(transaction)
        assert resp.json()['code'] == 'SUCCESS'
