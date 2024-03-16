import os
from abc import ABC, abstractmethod
from grpc import ssl_channel_credentials, access_token_call_credentials, composite_channel_credentials


class CredentialStrategy(ABC):
    @abstractmethod
    def get_credentials(self):
        pass


class CertificateCredentialStrategy(CredentialStrategy):
    def __init__(self, cert_path):
        self.cert_path = cert_path
        if not os.path.exists(self.cert_path):
            raise FileNotFoundError(f"Certificate file not found: {self.cert_path}")

    def get_credentials(self):
        with open(self.cert_path, 'rb') as cert_file:
            cert = cert_file.read()
        return ssl_channel_credentials(cert)


class TokenCredentialStrategy(CredentialStrategy):
    def __init__(self, token, cert_path=None):
        self.token = token
        self.cert_path = cert_path

    def get_credentials(self):
        token_credentials = access_token_call_credentials(self.token)
        if self.cert_path:
            with open(self.cert_path, 'rb') as cert_file:
                cert = cert_file.read()
            ssl_credentials = ssl_channel_credentials(cert)
            return composite_channel_credentials(ssl_credentials, token_credentials)
        else:
            return token_credentials

