### opentelemetry instrumentation
import logging
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, BatchSpanProcessor
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# # instrumentation
logger = logging.getLogger(__name__)

from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from lidarrmetadata.otel.config import OTLP

def init_otel_app_tracing(app):
    if OTLP.RESOURCE is None:
        logger.info(f"OLTP_RESOURCE is None!")
        print(f"OLTP_RESOURCE is None!")
        # init_otel_config()
    provider = TracerProvider(resource=OTLP.RESOURCE)

    if bool(OTLP.CONFIG.REMOTE_EXPORTER_INSECURE) is True:
        remote_trace_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP.CONFIG.REMOTE_EXPORTER_EDNPOINT, insecure=OTLP.CONFIG.REMOTE_EXPORTER_INSECURE))
        provider.add_span_processor(remote_trace_processor)

    if bool(OTLP.CONFIG.CONSOLE_EXPORTER_ENABLED) is True:
        console_trace_processor = SimpleSpanProcessor(ConsoleSpanExporter()) # Or your preferred exporter (e.g., OTLPSpanExporter)
        provider.add_span_processor(console_trace_processor)

    trace.set_tracer_provider(provider)
    app.asgi_app = OpenTelemetryMiddleware(app.asgi_app)
    return app


def init_otel_instrumentation():
    logger.info(f'{__name__}: initializing otel instrumentation...')
    AioHttpClientInstrumentor().instrument()
    AsyncPGInstrumentor().instrument()
    RedisInstrumentor().instrument()
