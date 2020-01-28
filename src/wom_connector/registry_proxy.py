
class RegistryProxy(object):

    def __init__(self, base_url, public_key):
        self.base_url = base_url
        self.PublicKey = public_key

    def voucher_create(self, source_id, nonce, payload):
        # TODO!
        pass
