from typing import Union
from pydantic import ValidationError
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

from app.schemas.metrics_manager import MetricsConfigData
from app.utils.str_to_bool import str_to_bool
from app.utils.check_otlp_credentials import (
    CertificateCredentialStrategy,
    TokenCredentialStrategy,
    CredentialStrategy
)


class MetricsManager:
    def __init__(self):
        try:
            config = MetricsConfigData()
        except ValidationError as e:
            raise SystemExit(e)

        self.metrics_enabled = str_to_bool(config.METRICS_ENABLE)

        if self.metrics_enabled:
            self.metrics_use_credentials = str_to_bool(config.METRICS_USE_CREDENTIALS)
            self.metrics_otlp_endpoint = config.METRICS_OTLP_ENDPOINT
            self.metrics_otlp_insecure = str_to_bool(config.METRICS_OTLP_INSECURE)
            self.metrics_service_name = config.METRICS_SERVICE_NAME
            self.metrics_library_name = config.METRICS_LIBRARY_NAME
            self.metrics_library_version = config.METRICS_LIBRARY_VERSION
            self.environment = config.ENVIRONMENT

            credentials = None
            if self.metrics_use_credentials:
                credential_strategy: CredentialStrategy

                if str_to_bool(config.METRICS_OTLP_USE_SSL_CERTIFICATE):
                    credential_strategy = CertificateCredentialStrategy(config.METRICS_SSL_CERTIFICATE_PATH)
                else:
                    credential_strategy = TokenCredentialStrategy(config.METRICS_TOKEN)

                credentials = credential_strategy.get_credentials()

            self.exporter = OTLPMetricExporter(
                endpoint=self.metrics_otlp_endpoint,
                insecure=self.metrics_otlp_insecure,
                credentials=credentials
            )

            self.reader = PeriodicExportingMetricReader(self.exporter)

            self.provider = MeterProvider(
                metric_readers=[self.reader],
                resource=Resource.create({SERVICE_NAME: self.metrics_service_name,
                                          "deployment.environment": self.environment})
            )

            set_meter_provider(self.provider)

            self.meter = get_meter_provider().get_meter(
                self.metrics_library_name,
                version=self.metrics_library_version
            )

            self.up_down_counter = self.meter.create_up_down_counter(
                "UpDownCounter",
                "",
                ""
            )
            self.counter = self.meter.create_counter(
                "Counter",
                "",
                ""
            )
            self.histogram = self.meter.create_histogram(
                "HistogramRecord",
                "ms",
                "HistogramRecord finished time in milliseconds"
            )

    def updown_counter_add(self, value: Union[int, float]):
        if self.metrics_enabled:
            self.up_down_counter.add(value)

    def counter_add(self, value: Union[int, float]):
        if self.metrics_enabled:
            self.counter.add(value)

    def histogram_record(self, value: Union[int, float]):
        if self.metrics_enabled:
            self.histogram.record(value)
