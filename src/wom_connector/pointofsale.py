import uuid
import json

from .filter import Filter, FilterEncoder
from .registry_proxy import RegistryProxy
from .crypto import Crypto
from .wom_logger import WOMLogger
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class POS:
    """
        Create an instance of a WOM PointOfSale able to generate payment instance.

        Keys should be loaded using:
            privk = open("keys/pos1.pem", "rb")
        and provided as:
            privk.read()

        :rtype: POS
        :param domain: str: Domain of the Registry (e.g., wom.social).
        :param pos_id: str: Unique instrument ID, assigned by the WOM platform.
        :param pos_privk: bytes: POS private key in bytes format.
        :param pos_privk_password: bytes: Optional password for POS private key (Default value = None)

    """

    def __init__(self, domain: str, pos_id: str, pos_privk: bytes, pos_privk_password: str=None):
        self.__registry_proxy = RegistryProxy(domain)
        self.ID = pos_id
        self.__pos_privk = self.__load_private_key(pos_privk, pos_privk_password,
                                                   "POS Private Key")
        self.__logger = WOMLogger("POS")

    @classmethod
    def __load_private_key(cls, private_key_str, password, tag):
        private_key = load_pem_private_key(private_key_str, password, default_backend())
        if not isinstance(private_key, RSAPrivateKey):
            raise TypeError("{0} is not a private RSA key" % tag)

        return private_key

    @staticmethod
    def __generate_nonce(nonce=None):
        return base64.b64encode(uuid.uuid4().bytes).decode('utf-8') if nonce is None else nonce

    def request_payment(self, amount: int,
                        pocket_ack_url: str,
                        filter: Filter = None,
                        pos_ack_url: str = None,
                        persistent: bool = False,
                        nonce=None,
                        password=None) -> (str, str):
        """
        Obtains payment requests from WOM Registry through Registry remote API.
        It returns a list containing the OTC representing the payment request and the associated password.

        :param amount: int: the number of voucher needed as a payment
        :param pocket_ack_url: str: the URL to be called for voucher spending notification, on pocket side
        :param filter: Filter:  filter to be applied on vouchers to be valid for the payment (Default value = None)
        :param pos_ack_url: str:  the URL to be called for voucher spending notification, on pos side (Default value = None)
        :param persistent: bool:  is this payment persistent? (Default value = False)
        :param nonce: str:  Communication nonce. If None, a proper nonce will be generated. (Default value = None)
        :param password: str:  Payment OTC password. If None, a secure password will be generated by the Registry. (Default value = None)
        :returns: OTC, password): (str, str)
        :rtype: list(str, str)

        """

        # call to payment/register API
        response_data = self.__payment_register(amount, pocket_ack_url, filter, pos_ack_url, persistent, nonce, password)

        # call to payment/verify API
        self.__payment_verify(response_data['otc'])

        return response_data['otc'], response_data['password']

    def __payment_register(self, amount,
                           pocket_ack_url: str,
                           filter: Filter = None,
                           pos_ack_url: str = None,
                           persistent: bool = False,
                           nonce=None,
                           password=None):

        # check arguments
        if amount < 1:
            raise ValueError("Amount has to be a positive, non-zero, integer")

        if len(pocket_ack_url) < 5:
            raise ValueError("PocketAckUrl has to be a valid URL")

        if pos_ack_url is not None and len(pos_ack_url) < 5:
            raise ValueError("PosAckUrl has to be a valid URL or None")

        # generate a valid nonce if there is no one
        effective_nonce = self.__generate_nonce(nonce)

        payload = json.dumps({'posId': self.ID,
                              'nonce': effective_nonce,
                              'password': password,
                              'amount': amount,
                              'simpleFilter': filter,
                              'pocketAckUrl': pocket_ack_url,
                              'posAckUrl': pos_ack_url,
                              'persistent': persistent
                              }, cls=FilterEncoder if filter is not None else None)
        self.__logger.debug(payload)

        # encrypt inner payload
        payment_register_payload = Crypto.encrypt(payload,
                                                  public_key=self.__registry_proxy.PublicKey)

        # make registry request
        json_response = self.__registry_proxy.payment_register(source_id=self.ID,
                                                               nonce=effective_nonce,
                                                               payload=payment_register_payload.decode('utf-8'))

        # decode registry response
        response = Crypto.decrypt(json_response['payload'], private_key=self.__pos_privk)

        return json.loads(response.decode('utf-8'))

    def __payment_verify(self, otc):
        encrypted_otc = Crypto.encrypt(json.dumps({'otc': otc}), public_key=self.__registry_proxy.PublicKey)
        self.__registry_proxy.payment_verify(encrypted_otc.decode('utf-8'))
