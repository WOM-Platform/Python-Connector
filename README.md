# WOM Connector for Python

Python connector library for the [WOM platform](https://wom.social).
[Get it on PyPI](https://pypi.org/project/wom-connector/).

This library can be used to interact with the WOM platform as a _Point of Service_ or as an _Instrument_.

## Examples

### Point of sale

As a Point of Sale, you can create new “payment requests” for users/customers.
A payment request can be customized with a given filter (which determines the kind of WOM vouchers you want to accept) and an amount of required vouchers.
Once a request has been created, you will obtain a _one-time code&nbsp;(OTC)_ and a _password_ that you will provide to your user (as a link or a QR&nbsp;code) in order for them to process the payment.

You can provide an _Ack URL_ to the payment request, which is an HTTP end-point that will receive an HTTP request from the WOM&nbsp;Registry as soon as the payment is performed.
Also, you can provide a _Pocket Ack URL_, which will be invoked by the user's WOM&nbsp;Pocket application when the payment is confirmed.
This latter URL can be a Web URL (opened in a Web browser) or a inter-application deep link.

In order to use the WOM Platform as a Point of Sale, you will need to register as a Merchant and create a Point of Sale, which will provide you with the POS ID and its private key.

```python
privk = open("keys/pos1.pem", "rb")

# This will create a filter for 'H' (health) vouchers, in a given geographic region, not older than 2 weeks
filter = Filter.create(aim='H', left_top_bound=[46.0, -17.0], right_bottom_bound=[12.0, 160.0], max_age=14)

pos = POS(domain='wom.social', # This is set to wom.social if you're using the platform
          pos_id='5e74205c5f21bb265a2d26d8', # POS ID
          pos_privk=privk.read())

otc, password = pos.request_payment(amount=100,
                                    pocket_ack_url='https://example.org',
                                    filter=filter,
                                    pos_ack_url='https://example.org',
                                    persistent=False,
                                    nonce=None,
                                    password=None)
```
