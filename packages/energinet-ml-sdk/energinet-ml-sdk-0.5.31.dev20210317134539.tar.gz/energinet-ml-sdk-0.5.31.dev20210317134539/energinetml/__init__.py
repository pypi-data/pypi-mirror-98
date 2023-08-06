from opentelemetry.sdk.trace.sampling import ALWAYS_ON

from .settings import (
    PACKAGE_NAME,
    PACKAGE_VERSION,
    APP_INSIGHT_INSTRUMENTATION_KEY,
)


__name__ = PACKAGE_NAME
__version__ = PACKAGE_VERSION


# OpenTelemetry must be configured before importing any packages using it
if APP_INSIGHT_INSTRUMENTATION_KEY:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
    from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

    conn = f'InstrumentationKey={APP_INSIGHT_INSTRUMENTATION_KEY}'
    exporter = AzureMonitorTraceExporter(connection_string=conn)
    span_processor = BatchExportSpanProcessor(exporter)

    trace.set_tracer_provider(TracerProvider(sampler=ALWAYS_ON))
    provider = trace.get_tracer_provider()
    provider.add_span_processor(span_processor)


# Importing pandas must be done before importing modules using OpenTelemetry,
# otherwise an (apparent) bug in Pandas causes an exception in a second thread
import pandas

from .cli import main
from .core.project import Project
from .core.logger import MetricsLogger
from .core.model import Model, TrainedModel
from .core.predicting import PredictionInput
from .core.training import requires_parameter
from .core.insight import query_predictions, query_predictions_as_dataframe
