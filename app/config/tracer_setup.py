import os

from app.utils.tracer.tracer_manager import TraceManager


def setup_tracing():
    trace_manager = TraceManager(
        service_name="vandr-fastapi-db-sqs-template",
        trace_enabled=os.environ.get('TRACE_ENABLED', 'False'),
        endpoint=os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://otel-collector:4317'),
        insecure=True,
        use_credentials=False,
        use_ssl_certificate=False,
        ssl_certificate_path=None,
        token=""
    )

    return trace_manager