import json
from .rest_client import RestClient


class RegistryProxy(object):

    def __init__(self, base_url, public_key):
        self.PublicKey = public_key
        self.client = RestClient(base_url)

    def voucher_create(self, source_id, nonce, payload):
        request_payload = json.dumps({'SourceId': source_id,
                                      'Nonce': nonce,
                                      'Payload': payload})

        return self.client.voucher_create(request_payload)

    def voucher_verify(self, payload):
        request_payload = json.dumps({'Payload': payload})
        print(request_payload)

        return self.client.voucher_verify(request_payload)
