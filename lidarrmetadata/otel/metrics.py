import logging
import os
import socket
from pprint import pformat
import opentelemetry
import opentelemetry.sdk.metrics
import opentelemetry.sdk.metrics.export
import opentelemetry.sdk.resources
import opentelemetry.exporter.prometheus
import prometheus_client


logger = logging.getLogger(__name__)
meter = opentelemetry.metrics.get_meter(__name__)


otlp_instance_name = os.getenv('OTLP_INSTANCE_NAME', socket.gethostname())
otlp_service_name = os.getenv('OTLP_SERVICE_NAME', 'lidarr-metadata-api')
resource = opentelemetry.sdk.resources.Resource.create({
  "instance.name": otlp_instance_name,
  "service.name": otlp_service_name,
})

reader = opentelemetry.exporter.prometheus.PrometheusMetricReader()
meter_provider = opentelemetry.sdk.metrics.MeterProvider(metric_readers=[reader], resource=resource)
opentelemetry.metrics.set_meter_provider(meter_provider)


metric_request_counter = meter.create_counter(
        name="http_request_counter",
        description="Total number of requests"
)

metric_request_duration_gauge = meter.create_gauge(
        name="http_request_duration_gauge",
        description="duration of request"
)

metric_request_duration_histogram = meter.create_histogram(
        name="http_request_duration_histogram",
        description="duration of request"
)

def render_prometheus_exporter_metrics():
    return prometheus_client.generate_latest(), 200, {'Content-Type': prometheus_client.CONTENT_TYPE_LATEST}
