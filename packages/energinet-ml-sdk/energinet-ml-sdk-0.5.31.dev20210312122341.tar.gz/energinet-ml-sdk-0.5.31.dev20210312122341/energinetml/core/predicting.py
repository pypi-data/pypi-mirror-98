"""
/predict request body JSON example:

    {
        "inputs": [
            {
                "identifier": "foo",
                "features": {
                    "age": 20,
                    "height": 180
                }
            },
            {
                "identifier": "bar",
                "features": {
                    "age": 30,
                    "height": 200
                }
            },
            {
                "identifier": "foo",
                "features": {
                    "age": 20,
                    "height": 180
                }
            }
        ]
    }

"""
import json
import logging
from enum import Enum
from typing import List, Any
from functools import cached_property
from pydantic import BaseModel, create_model
from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status


tracer = trace.get_tracer(__name__)


class PredictionInput(list):
    """
    TODO
    """
    def __init__(self, features, *args, **kwargs):
        super(PredictionInput, self).__init__(*args, **kwargs)
        self.features = features

    def as_dict_of_lists(self):
        """
        TODO
        """
        return {
            feature: [input[feature] for input in self]
            for feature in self.features
        }

    def as_pandas_dataframe(self):
        """
        :rtype: pandas.DataFrame
        """
        try:
            import pandas
        except ImportError:
            raise RuntimeError((
                'Failed to import pandas. Make sure to add '
                'pandas to your requirements.txt file'
            ))

        return pandas.DataFrame(self.as_dict_of_lists())


# -- Data models -------------------------------------------------------------


class PredictRequest(BaseModel):
    """
    TODO
    """
    inputs: List[Any]

    def group_input_by_identifier(self):
        inputs_per_identifier = {}

        for index, input in enumerate(self.inputs):
            if hasattr(input, 'identifier'):
                identifier = input.identifier.value
            else:
                identifier = None

            inputs_per_identifier \
                .setdefault(identifier, []) \
                .append((index, dict(input.features)))

        return inputs_per_identifier.items()


class PredictResponse(BaseModel):
    predictions: List[Any]


# -- Controller --------------------------------------------------------------


class PredictionController(object):
    """
    TODO
    """
    def __init__(self, model, trained_model, model_version):
        """
        :param energinetml.Model model:
        :param energinetml.TrainedModel trained_model:
        :param typing.Optional[str] model_version:
        """
        self.model = model
        self.trained_model = trained_model
        self.model_version = model_version

    @cached_property
    def logger(self):
        """
        :rtype: logging.Logger
        """
        logger = logging.getLogger(__name__)

        # Setup Azure App Insights backend (using OpenCensus) if necessary
        # if APP_INSIGHT_INSTRUMENTATION_KEY:
        #     conn = 'InstrumentationKey=%s' % APP_INSIGHT_INSTRUMENTATION_KEY
        #     handler = AzureLogHandler(connection_string=conn, export_interval=15)
        #     logger.setLevel(logging.INFO)
        #     logger.addHandler(handler)

        return logger

    @property
    def identifiers(self):
        """
        :rtype: List[str]
        """
        return self.trained_model.identifiers

    @property
    def features(self):
        """
        :rtype: List[str]
        """
        return self.trained_model.features

    @property
    def requires_identity(self):
        """
        :rtype: bool
        """
        return not self.trained_model.has_default_model()

    @cached_property
    def request_model(self):
        """
        TODO
        """
        PredictFeatures = create_model('PredictFeatures', **{
            feature: (Any, ...) for feature in self.features
        })

        predict_input_attributes = {'features': (PredictFeatures, ...)}

        if self.requires_identity:
            IdentifierEnum = Enum('IdentifierEnum', {
                i: i for i in self.identifiers
            })
            predict_input_attributes['identifier'] = (IdentifierEnum, ...)

        PredictInput = create_model(
            __model_name='PredictInput',
            **predict_input_attributes,
        )

        return create_model(
            __model_name='PredictRequest',
            __base__=PredictRequest,
            inputs=(List[PredictInput], ...),
        )

    @property
    def response_model(self):
        """
        TODO
        """
        return PredictResponse

    def predict(self, request):
        """
        :param PredictRequest request:
        :rtype: PredictResponse
        """
        start_span = tracer.start_span(
            name='prediction',
            kind=SpanKind.SERVER,
        )

        with start_span as span:
            identifiers, inputs, predictions = self.invoke_model(request)

            span.set_attribute('model_name', self.model.name)
            if self.model_version is not None:
                span.set_attribute('model_version', self.model_version)
            span.set_attribute('identifiers', json.dumps(identifiers))
            span.set_attribute('input_data', json.dumps(inputs))
            span.set_attribute('predictions', json.dumps(predictions))

        return self.response_model(predictions=predictions)

    def invoke_model(self, request):
        """
        :param PredictRequest request:
        :rtype: PredictResponse
        """
        groups = request.group_input_by_identifier()
        identifiers_ordered = [_[0] for _ in groups]
        inputs_ordered = [_[1] for _ in groups]
        predictions_ordered = [... for _ in range(len(request.inputs))]

        # Invoke predict() for each unique identifier
        for identifier, inputs in groups:
            indexes = [i[0] for i in inputs]
            feature_sets = [i[1] for i in inputs]
            input_data = PredictionInput(self.features, feature_sets)

            predict_result = self.model.predict(
                trained_model=self.trained_model,
                identifier=identifier,
                input_data=input_data,
            )

            # TODO Verify predict_result

            for index, prediction in zip(indexes, predict_result):
                predictions_ordered[index] = prediction

        if ... in predictions_ordered:
            # TODO Raise...
            raise RuntimeError()

        return (
            identifiers_ordered,
            inputs_ordered,
            predictions_ordered,
        )

    # def invoke_model(self, identifier, input_data):
    #     """
    #     :param energinetml.PredictionInput input_data:
    #     :param str identifier:
    #     :rtype: typing.List[typing.Any]
    #     """
    #     start_span = tracer.start_span(
    #         name='prediction',
    #         kind=SpanKind.SERVER,
    #     )
    #
    #     with start_span as span:
    #         if identifier is not None:
    #             span.set_attribute('identifier', identifier)
    #         span.set_attribute('input_data', json.dumps(input_data))
    #         span.set_attribute('model_name', self.model.name)
    #         if self.model_version is not None:
    #             span.set_attribute('model_version', self.model_version)
    #
    #         predict_result = self.model.predict(
    #             trained_model=self.trained_model,
    #             identifier=identifier,
    #             input_data=input_data,
    #         )
    #
    #         span.set_attribute('prediction', json.dumps(predict_result))
    #
    #     return predict_result

    def log_prediction(self, input, prediction):
        """
        Logs a single prediction specifically for Azure App Insight
        """
        i = input.dict()
        if 'identifier' in i and isinstance(i['identifier'], Enum):
            i['identifier'] = i['identifier'].value

        self.logger.info('Prediction', extra={
            'custom_dimensions': {
                'modelVersion': json.dumps(self.model_version),
                'input': json.dumps(i),
                'prediction': json.dumps(prediction),
            },
        })
