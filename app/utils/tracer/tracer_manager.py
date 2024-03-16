import os

from pydantic import ValidationError

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

from app.schemas.tracer_manager import TraceConfigData
from app.utils.custom_exceptions import ConfigValidationError
from app.utils.check_otlp_credentials import CertificateCredentialStrategy, TokenCredentialStrategy, CredentialStrategy
from app.utils.str_to_bool import str_to_bool


class TraceManager:
    def __init__(self):
        self.trace_enabled = str_to_bool(os.getenv("TRACE_ENABLED", "False"))

        if self.trace_enabled:
            try:
                config = TraceConfigData()
            except ValidationError as e:
                raise ConfigValidationError(f"Configuration validation failed: {e}")

            trace_use_credentials = config.TRACE_USE_CREDENTIALS
            self.use_ssl_certificate = config.USE_SSL_CERTIFICATE
            self.ssl_certificate_path = config.SSL_CERTIFICATE_PATH
            self.trace_service_name = config.TRACE_SERVICE_NAME
            self.token = config.TRACE_TOKEN
            self.endpoint = config.OTEL_EXPORTER_OTLP_ENDPOINT
            self.insecure = config.TRACE_INSECURE
            self.environment = config.ENVIRONMENT
            self.trace_sample_rate = config.TRACE_SAMPLE_RATE

            self.tracer_provider = TracerProvider(
                resource=Resource.create({SERVICE_NAME: self.trace_service_name,
                                          "deployment.environment": self.environment}),
                sampler=self._initialize_sampler(self.trace_enabled, self.trace_sample_rate)
            )

            credentials = None

            if trace_use_credentials:
                credential_strategy: CredentialStrategy

                if self.use_ssl_certificate:
                    credential_strategy = CertificateCredentialStrategy(self.ssl_certificate_path)
                else:
                    credential_strategy = TokenCredentialStrategy(self.token)

                credentials = credential_strategy.get_credentials()

            otlp_exporter = OTLPSpanExporter(
                endpoint=self.endpoint,
                insecure=self.insecure,
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
