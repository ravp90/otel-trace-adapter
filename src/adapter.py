class Adapter:
    def __init__(self, tracer: str, **kwargs):
        self.tracer = tracer
        self.kwargs = kwargs
        pass


class JaegerAdapter(Adapter):
    def __init__(self, **kwargs):
        super().__init__("Jaeger", **kwargs)


class PrometheusAdapter(Adapter):
    def __init__(self, **kwargs):
        super().__init__("Prometheus", **kwargs)


class HoneycombAdapter(Adapter):
    def __init__(self, **kwargs):
        super().__init__("Honeycomb", **kwargs)


class DatadogAdapter(Adapter):
    def __init__(self, **kwargs):
        super().__init__("Datadog", **kwargs)
