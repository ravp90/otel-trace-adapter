from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Start Prometheus HTTP server on port 8000
    start_http_server(port=8000)
    logger.info("Prometheus metrics server started on port 8000")

    # Create a shared resource for both traces and metrics
    resource = Resource.create({ResourceAttributes.SERVICE_NAME: "my-service"})

    # === TRACES SETUP ===
    # Configure the Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )

    # Create a tracer provider with the resource
    tracer_provider = TracerProvider(resource=resource)
    span_processor = BatchSpanProcessor(jaeger_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Set the tracer provider
    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer("my-service-tracer")

    # === METRICS SETUP ===
    # Create a Prometheus metrics reader
    prometheus_reader = PrometheusMetricReader()

    # Create a meter provider with Prometheus reader
    meter_provider = MeterProvider(
        resource=resource, metric_readers=[prometheus_reader]
    )
    metrics.set_meter_provider(meter_provider)
    meter = metrics.get_meter("my-service-meter")

    # Create metric instruments
    request_counter = meter.create_counter(
        name="hello_requests_total",
        description="Total number of hello requests",
        unit="1",
    )

    request_duration = meter.create_histogram(
        name="hello_duration_milliseconds",
        description="Duration of hello requests in milliseconds",
        unit="ms",
    )

    logger.info("OpenTelemetry setup complete")

    def say_hello(name):
        # Start timing
        start_time = time.time()

        # Increment the counter with attributes
        request_counter.add(1, {"name": name})
        logger.info(f"Incremented request counter for {name}")

        with tracer.start_as_current_span("say_hello") as span:
            # Add attributes to the span
            span.set_attribute("name", name)
            print(f"Hello, {name}!")

            with tracer.start_as_current_span("say_hello_to_someone"):
                print(f"Hello, {name}!")

        # Record the duration
        duration_ms = (time.time() - start_time) * 1000
        request_duration.record(duration_ms, {"name": name})
        logger.info(f"Recorded duration {duration_ms}ms for {name}")

    # Generate one request immediately to register metrics
    say_hello("OpenTelemetry-init")
    logger.info("Initial request generated to register metrics")

    # Function to continuously generate traffic
    count = 0
    logger.info("Starting continuous traffic generation...")
    while True:
        count += 1
        say_hello(f"OpenTelemetry-{count}")
        logger.info(f"Generated request #{count}")
        time.sleep(1)  # Generate a request every second

except KeyboardInterrupt:
    logger.info("Application stopped by user")
except Exception as e:
    logger.error(f"Error in application: {e}", exc_info=True)
