from adapter import DatadogAdapter, HoneycombAdapter, JaegerAdapter, PrometheusAdapter


class TracerFactory:
    def __init__(self, **kwargs):
        self.tracer = kwargs.get("tracer", None)
        self.kwargs = kwargs
        pass

    def create_tracer(self):
        if self.tracer == "Jaeger":
            return JaegerAdapter(**self.kwargs)
        elif self.tracer == "Prometheus":
            return PrometheusAdapter(**self.kwargs)
        elif self.tracer == "Honeycomb":
            return HoneycombAdapter(**self.kwargs)
        elif self.tracer == "Datadog":
            return DatadogAdapter(**self.kwargs)
        else:
            raise ValueError(f"Invalid tracer: {self.tracer}")
