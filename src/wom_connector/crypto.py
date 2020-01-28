import base64

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric import padding


class Crypto(object):

    @classmethod
    def Encrypt(cls, payload, receiver_public_key):
        payload_bytes = payload.encode()

        encrypted_payload_bytes = cls.__encrypt(payload_bytes, receiver_public_key)

        return base64.b64encode(encrypted_payload_bytes) # TODO: check

    @classmethod
    def __encrypt(cls, payload_bytes, receiver_public_key : RSAPublicKey):
        return receiver_public_key.encrypt(payload_bytes, padding.PKCS1v15())


'''
public string Encrypt<T>(T payload, AsymmetricKeyParameter receiverPublicKey) {
            if (receiverPublicKey.IsPrivate) {
                throw new ArgumentException("Public key of receiver required for encryption", nameof(receiverPublicKey));
            }

            var payloadBytes = JsonConvert.SerializeObject(payload, JsonSettings).ToBytes();
            var signedBytes = Encrypt(payloadBytes, receiverPublicKey);

            Logger.LogTrace(LoggingEvents.Cryptography,
                "Encrypt object (bytes {0} => {1})",
                payloadBytes.Length, signedBytes.Length);

            return signedBytes.ToBase64();
        }
'''