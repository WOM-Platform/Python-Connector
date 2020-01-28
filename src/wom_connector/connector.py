import uuid
import json
from .registry_proxy import RegistryProxy
from .crypto import Crypto



from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key


class Connector:

    def __init__(self, base_url, ID, registry_pubk, instrument_privk, instrument_privk_password=None):
        self.registry_proxy = RegistryProxy(base_url, self.__load_public_key(registry_pubk, "Registry Public Key"))
        self.ID = ID
        self.instrument_privk = self.__load_private_key(instrument_privk, instrument_privk_password, "Instrument Private Key")

    def __check_not_none(self, value, tag):
        if value is None:
            raise ValueError("Parameter {0} has an incorrect value" % tag)

    @staticmethod
    def __load_public_key(public_key_str, tag):
        public_key = load_pem_public_key(public_key_str, default_backend())
        if not isinstance(public_key, RSAPublicKey):
            raise TypeError("{0} is not a public RSA key" % tag)

        return public_key

    @staticmethod
    def __load_private_key(private_key_str, password, tag):
        private_key = load_pem_private_key(private_key_str, password, default_backend())
        if not isinstance(private_key, RSAPrivateKey):
            raise TypeError("{0} is not a private RSA key" % tag)

        return private_key

    @staticmethod
    def __generate_nonce(nonce = None):
        return uuid.uuid4().int if nonce is None else nonce

    def request_vouchers(self, vouchers, nonce = None, password = None):

        if vouchers is None \
                or not isinstance(vouchers, list) \
                or len(vouchers) == 0:
            raise ValueError("Voucher list is not valid or empty")

        effective_nonce = self.__generate_nonce(nonce)

        vouchers_create_payload = Crypto.Encrypt(json.dumps({'SourceId': self.ID,
                                                   'Nonce': effective_nonce,
                                                   'Password': password,
                                                   'Vouchers': vouchers}),
                                                 receiver_public_key=self.registry_proxy.PublicKey)
        self.registry_proxy.voucher_create(source_id=self.ID,
                                           nonce=effective_nonce,
                                           payload=vouchers_create_payload)
