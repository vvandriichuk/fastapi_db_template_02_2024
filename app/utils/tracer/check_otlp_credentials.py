import os
from abc import ABC, abstractmethod
from grpc import ssl_channel_credentials, access_token_call_credentials


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
    def __init__(self, token):
        self.token = token

    def get_credentials(self):
        return access_token_call_credentials(self.token)
