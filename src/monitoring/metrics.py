"""Prometheus metrics configuration."""
from prometheus_client import Counter, Histogram, start_http_server
from functools import wraps
import time

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

INGESTION_RECORDS = Counter(
    'ingestion_records_total',
    'Total records processed during ingestion',
    ['status']
)

def track_request_metrics():
    """Decorator to track request metrics."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            method = kwargs.get('request').method
            endpoint = kwargs.get('request').url.path
            
            start_time = time.time()
            try:
                response = await func(*args, **kwargs)
                REQUEST_COUNT.labels(
                    method=method,
                    endpoint=endpoint,
                    status=response.status_code
                ).inc()
                return response
            finally:
                REQUEST_LATENCY.labels(
                    method=method,
                    endpoint=endpoint
                ).observe(time.time() - start_time)
        return wrapper
    return decorator