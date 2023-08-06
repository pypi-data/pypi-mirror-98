import time

from prometheus_client import CollectorRegistry, Histogram, push_to_gateway
from prometheus_client.utils import INF

from . import Middleware
from ..app import get_app


DEFAULT_BUCKETS = (
    0.001,
    0.005,
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    10.0,
    INF,
)


class ListenMonitoringMiddleware(Middleware):
    def __init__(
        self,
        pushgateway_url: str = "localhost:9091",
        app=None,
        frequency: float = 10.0,
        metric_key_suffix: str = "listen_latency",
        job: str = "microservices_activity",
        buckets=DEFAULT_BUCKETS,
    ):
        if app is None:
            app = get_app()
        assert app is not None
        self.pushgateway_url = pushgateway_url
        self.registry = CollectorRegistry()
        self.metric_key_suffix = metric_key_suffix
        self.app_name = app.service_name
        self.metric_key_suffix = metric_key_suffix
        self.histograms = {}
        self.buckets = buckets

        @app.timer_task(frequency)
        async def push_to_prometheus():
            push_to_gateway(pushgateway_url, job=job, registry=self.registry)

    def create_histogram(self, subject: str):

        return Histogram(
            f"{self.app_name}__{subject.replace('.', '_').replace('/', '').replace('*', 'ANY').replace('>', 'ANY_LINE_CONTINUATION')}__{self.metric_key_suffix}",
            "Listen latency in seconds",  # description
            registry=self.registry,
            buckets=self.buckets,
        )

    async def listen_any(self, msg, callback):
        start_time = time.time()
        response = await callback(msg)
        duration = time.time() - start_time
        if msg.subject not in self.histograms:
            self.histograms[msg.subject] = self.create_histogram(msg.subject)

        self.histograms[msg.subject].observe(duration)

        return response
