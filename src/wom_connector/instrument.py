import uuid
import json

from .wom_logger import WOMLogger
from .registry_proxy import RegistryProxy
from .voucher import Voucher
from .voucher import VoucherEncoder
from .crypto import Crypto
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class Instrument:

    def __init__(self, domain: str, instrument_id: int, instrument_privk: bytes, instrument_privk_password: str=None):
        """
        Create an instance of an WOM Instrument able to generate vouchers.

        Keys should be loaded using:
            privk = open("keys/instrument1.pem", "rb")
        and provided as:
            privk.read()

        :rtype: Instrument
        :param domain: str: Domain of the Registry (e.g., wom.social).
        :param instrument_id: int: Unique instrument ID, assigned by the WOM platform.
        :param instrument_privk: bytes: Instrument private key in bytes format.
        :param instrument_privk_password: bytes: Optional password for Instrument private key (Default value = None).

        """

        self.__registry_proxy = RegistryProxy(domain)
        self.ID = instrument_id
        self.__instrument_privk = self.__load_private_key(instrument_privk, instrument_privk_password, "Instrument Private Key")
        self.__logger = WOMLogger("Instrument")

    @staticmethod
    def __load_private_key(private_key_str, password, tag):
        private_key = load_pem_private_key(private_key_str, password, default_backend())
        if not isinstance(private_key, RSAPrivateKey):
            raise TypeError("{0} is not a private RSA key" % tag)

        return private_key

    @staticmethod
    def __generate_nonce(nonce=None):
        return base64.b64encode(uuid.uuid4().bytes).decode('utf-8') if nonce is None else nonce

    def request_vouchers(self, vouchers: list, nonce: str = None, password: str = None) -> (str, str):
        """
        Obtains vouchers from WOM Registry through Registry remote API.
        It returns a list containing the OTC representing the vouchers and the associated password.

        :param vouchers: list: A list of Voucher items or a list of properly structure dictionaries
        :param nonce: str:  Communication nonce. If None, a proper nonce will be generated. (Default value = None)
        :param password: str:  Voucher OTC password. If None, a secure password will be generated by the Registry. (Default value = None)
        :returns: OTC, password): (str, str)
        :rtype: list(str, str)

        """

        # call to voucher/create API
        response_data = self.__voucher_create(vouchers, nonce, password)

        # call to voucher/verify API
        self.__voucher_verify(response_data['otc'])

        return response_data['otc'], response_data['password']

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

        payload = json.dumps({'sourceId': self.ID,
                              'nonce': effective_nonce,
                              'password': password,
                              'vouchers': vouchers}, cls=VoucherEncoder if isinstance(vouchers[0], Voucher) else None)

        self.__logger.debug(payload)

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

        encrypted_otc = Crypto.encrypt(json.dumps({'otc': otc}), public_key=self.__registry_proxy.PublicKey)
        self.__registry_proxy.voucher_verify(encrypted_otc.decode('utf-8'))
