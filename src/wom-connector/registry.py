from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key

class Registry:

    def __init__(self, publicKey):
        """Initialize a Registry instance.

        Arguments:
        publicKey -- Registry's public RSA key (bytes)
        """
        self.__publicKey = load_pem_public_key(publicKey, default_backend())
        if !isinstance(self.__publicKey, rsa.RSAPublicKey):
            raise Exception("Key is not a public RSA key")
