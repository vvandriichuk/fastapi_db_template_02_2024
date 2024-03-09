from typing import Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

from app.utils.check_otlp_credentials import CertificateCredentialStrategy, TokenCredentialStrategy, CredentialStrategy


class TraceManager:
    def __init__(self, service_name: str = '',
                 trace_enabled: bool = False,
                 endpoint: str = '',
                 insecure: bool = True,
                 use_credentials: bool = False,
                 use_ssl_certificate: bool = False,
                 ssl_certificate_path: Optional[str] = None,
                 token: str = '',
                 rate: float = 1/100) -> None:
        self.tracer_provider = TracerProvider(
            resource=Resource.create({SERVICE_NAME: service_name}),
            sampler=self._initialize_sampler(trace_enabled, rate)
        )

        if trace_enabled:
            credentials = None

            if use_credentials:
                credential_strategy: CredentialStrategy

                if use_ssl_certificate:
                    credential_strategy = CertificateCredentialStrategy(ssl_certificate_path)
                else:
                    credential_strategy = TokenCredentialStrategy(token)

                credentials = credential_strategy.get_credentials()

            sampler = TraceIdRatioBased(rate)

            otlp_exporter = OTLPSpanExporter(
                endpoint=endpoint,
                insecure=insecure,
                credentials=credentials
            )
            span_processor = BatchSpanProcessor(otlp_exporter)
            self.tracer_provider.add_span_processor(span_processor)

        trace.set_tracer_provider(self.tracer_provider)

    def get_tracer(self, name):
        return trace.get_tracer(name)

    def _initialize_sampler(self, trace_enabled: bool, rate: float):
        if trace_enabled:
            return TraceIdRatioBased(rate)
        else:
            return None
