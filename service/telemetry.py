from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.pika import PikaInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

import os
from dotenv import load_dotenv

load_dotenv()


def retrys():
    OTP = os.getenv("OTP")
    if not OTP:
        raise ValueError("OTP is missing or empty")
    return OTP


OTP = retrys()

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

tracer_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=OTP, insecure=True))
)


def stopopentelemetry(app):
    print("Shutdown OpenTelemetry...")
    flush_ok = tracer_provider.force_flush(timeout_millis=10000)
    if flush_ok:
        print("Flush OpenTelemetry ...")
    else:
        print("No Flush OpenTelemetry ...")
    PikaInstrumentor().uninstrument()
    FastAPIInstrumentor.uninstrument_app(app)
    tracer_provider.shutdown()
    print("OpenTelemetry arrêté")


def init_opentelemetry(app):
    print("Init OpenTelemetry...")
    PikaInstrumentor().instrument()
    FastAPIInstrumentor.instrument_app(app)
    Instrumentator().instrument(app).expose(app)
