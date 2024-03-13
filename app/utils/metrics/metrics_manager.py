from typing import Iterable, Union

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.metrics import (
    CallbackOptions,
    Observation,
    get_meter_provider,
    set_meter_provider,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from app.config.metrics_config import MetricsConfigData
from app.utils.str_to_bool import str_to_bool

from app.utils.check_otlp_credentials import CertificateCredentialStrategy, TokenCredentialStrategy, CredentialStrategy


class MetricsManager:
    def __init__(self):
        self.metrics_enabled = MetricsConfigData.METRICS_ENABLE()
        self.metrics_use_credentials = MetricsConfigData.METRICS_USE_CREDENTIALS()
        self.metrics_use_ssl_certificate = False
        self.metrics_ssl_certificate_path = None
        self.metrics_token = MetricsConfigData.METRICS_TOKEN()
        self.metrics_otlp_endpoint = MetricsConfigData.METRICS_OTLP_ENDPOINT()
        self.metrics_otlp_insecure = str_to_bool(MetricsConfigData.METRICS_OTLP_INSECURE())
        self.metrics_service_name = MetricsConfigData.METRICS_SERVICE_NAME()
        self.metrics_library_name = MetricsConfigData.METRICS_LIBRARY_NAME()
        self.metrics_library_version = MetricsConfigData.METRICS_LIBRARY_VERSION()
        self.environment = MetricsConfigData.ENVIRONMENT()

        if self.metrics_enabled is True:
            credentials = None

            if self.metrics_use_credentials is True:
                credential_strategy: CredentialStrategy

                if self.metrics_use_ssl_certificate is True:
                    credential_strategy = CertificateCredentialStrategy(self.metrics_ssl_certificate_path)
                else:
                    credential_strategy = TokenCredentialStrategy(self.metrics_token)

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
        self.meter = get_meter_provider().get_meter(name=self.metrics_library_name,
                                                    version=self.metrics_library_version)

    # UpDownCounter is a synchronous Instrument which supports increments and decrements.
    def updown_counter_add(self, name: str, value: Union[int, float], unit: str = "", description: str = ""):
        if self.metrics_enabled is True:
            self.meter.create_up_down_counter(name, unit, description).add(value)

    # Counter is a synchronous Instrument which supports non-negative increments.
    def counter_add(self, name: str, value: Union[int, float], unit: str = "", description: str = ""):
        if self.metrics_enabled is True:
            self.meter.create_counter(name, unit, description).add(value)

    # Histogram is a synchronous Instrument which can be used to report arbitrary values that are likely to be statistically meaningful.
    # It is intended for statistics such as histograms, summaries, and percentile.
    def histogram_record(self, name: str, value: Union[int, float], unit: str = "", description: str = ""):
        if self.metrics_enabled is True:
            self.meter.create_histogram(name, unit, description).record(value)

    # Gauge is a synchronous Instrument which can be used to record non-additive value(s) (e.g. the background noise level -
    # it makes no sense to record the background noise level value from multiple rooms and sum them up) when changes occur.
    # TODO: add gauge Observe() https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge
