import uuid
import json
from .registry_proxy import RegistryProxy
from .voucher import Voucher
from .voucher import VoucherEncoder
from .crypto import Crypto
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key


class Connector:

    def __init__(self, base_url, ID, registry_pubk, instrument_privk, instrument_privk_password=None):
        self.__registry_proxy = RegistryProxy(base_url, self.__load_public_key(registry_pubk, "Registry Public Key"))
        self.ID = ID
        self.__instrument_privk = self.__load_private_key(instrument_privk, instrument_privk_password,
                                                          "Instrument Private Key")

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
    def __generate_nonce(nonce=None):
        return base64.b64encode(uuid.uuid4().bytes).decode('utf-8') if nonce is None else nonce

    def request_vouchers(self, vouchers, nonce=None, password=None):

        response_data = self.__voucher_create(vouchers, nonce, password)
        self.__voucher_verify(response_data['Otc'])

        return response_data['Otc'], response_data['Password']

    def __voucher_create(self, vouchers, nonce=None, password=None):

        # check arguments
        if vouchers is None \
                or not isinstance(vouchers, list) \
                or len(vouchers) == 0:
            raise ValueError("Voucher list is not valid or empty")

        if not isinstance(vouchers[0], Voucher) \
                and not isinstance(vouchers[0], dict):
            raise ValueError("Vouchers has to be instances of Voucher or dictionaries")

        # generate a valid nonce if there is no one
        effective_nonce = self.__generate_nonce(nonce)

        payload = json.dumps({'SourceId': self.ID,
                              'Nonce': effective_nonce,
                              'Password': password,
                              'Vouchers': vouchers}, cls=VoucherEncoder if isinstance(vouchers[0], Voucher) else None)

        # encrypt inner payload
        vouchers_create_payload = Crypto.encrypt(payload,
                                                 public_key=self.__registry_proxy.PublicKey)

        # make registry request
        json_response = self.__registry_proxy.voucher_create(source_id=self.ID,
                                                             nonce=effective_nonce,
                                                             payload=vouchers_create_payload.decode('utf-8'))

        # decode registry response
        response = Crypto.decrypt(json_response['payload'], private_key=self.__instrument_privk)

        return json.loads(response.decode('utf-8'))

    def __voucher_verify(self, otc):

        encrypted_otc = Crypto.encrypt(json.dumps({'Otc': otc}), public_key=self.__registry_proxy.PublicKey)
        self.__registry_proxy.voucher_verify(encrypted_otc.decode('utf-8'))
