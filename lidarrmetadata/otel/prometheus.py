from prometheus_client import Gauge, Counter, Histogram, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

# prometheus metrics
registry = CollectorRegistry()

metric_request_time_histogram = Histogram(
    "http_request_time_histogram_seconds",
    "Duration of HTTP requests",
    ["method", "fname", "endpoint", "status_code"], # Labels for method, endpoint, and status code
    registry=registry, # Use the custom registry
)

metric_request_time = Gauge(
    "http_request_time_seconds",
    "Duration of HTTP requests",
    ["method", "fname", "endpoint", "status_code"], # Labels for method, endpoint, and status code
    registry=registry, # Use the custom registry
)

metric_request_active_count = Gauge(
    "http_request_active_count",
    "number of active http requests",
    registry=registry, # Use the custom registry
)

metric_request_count = Gauge(
    "http_request_time_seconds_sum",
    "Count of HTTP requests",
    ["method", "fname", "endpoint", "status_code"], # Labels for method, endpoint, and status code
    registry=registry, # Use the custom registry
)


def render_prometheus_exporter_metrics():
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}
