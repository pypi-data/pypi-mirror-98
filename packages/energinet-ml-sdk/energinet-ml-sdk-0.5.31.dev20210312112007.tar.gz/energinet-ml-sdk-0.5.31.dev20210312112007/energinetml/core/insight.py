import json
import subprocess
from datetime import datetime, date


QUERY = (
    'traces | order by timestamp | project timestamp, '
    'input = customDimensions["input"], '
    'prediction = customDimensions["prediction"], '
    'modelVersion = customDimensions["modelVersion"]'
)


def query(app, resource_group, subscription, start_date, end_date):
    """
    TODO

    :param str app: Azure Application Insight app name
    :param str resource_group: Azure Resource group
    :param str subscription: Azure Subscription
    :param date start_date: Start date (included)
    :param date end_date: End date (included)
    :rtype: typing.Dict[str, typing.Any]
    """
    command = ['az', 'monitor', 'app-insights', 'query']
    command.extend(('--apps', app))
    command.extend(('--resource-group', resource_group))
    command.extend(('--subscription', subscription))
    command.extend(('--start-time', start_date.isoformat()))
    command.extend(('--end-time', end_date.isoformat()))
    command.extend(('--analytics-query', QUERY))

    output_bytes = subprocess.check_output(command)
    output_string = output_bytes.decode("utf-8")
    # String may contain trailing characters, not part of the JSON document
    output_string = output_string[:output_string.rfind('}')+1]

    return json.loads(output_string)


def parse_return_json(return_json):
    """
    :param typing.Dict[str, typing.Any] return_json:
    :rtype: typing.Iterable[typing.Dict[str, typing.Any]]
    """
    columns = [c['name'] for c in return_json['tables'][0]['columns']]

    for row in return_json['tables'][0]['rows']:
        result = dict(zip(columns, row))
        result['input'] = json.loads(result['input'])
        result['prediction'] = json.loads(result['prediction'])
        result['modelVersion'] = json.loads(result['modelVersion'])
        result['timestamp'] = datetime \
            .strptime(result['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ') \
            .replace(microsecond=0)
        yield result


def query_predictions(expand=True, keep_keys=False, **kwargs):
    """
    Perform an Application Insight query to get inputs with their respective
    predictions from a deployed model. These are the entries logged by models
    when deployed in Azure using the SDK.

    Example usage:

        from datetime import date
        from energinetml import query_predictions

        entries = query_predictions(
            app='MyApplicationInsightAppName',
            resource_group='MyAzureResourceGroup',
            subscription='MyAzureSubscription',
            start_date=date(2021, 1, 1),
            end_date=date(2021, 12, 31),
        )

    :param bool expand: Whether or not to expand input features from raw
        JSON into columns in the DataFrame
    :param bool keep_keys: Whether or not to keep origin keys/values
        after expanding dictionaries.
    :param typing.Any kwargs: Keyword args for query() method
    :rtype: typing.Iterable[typing.Dict[str, typing.Any]]
    """
    def __expand_dict(d):
        for k, v in [(k, v) for k, v in d.items() if isinstance(v, dict)]:
            if keep_keys:
                d.update(__expand_dict(v))
            else:
                d.update(__expand_dict(d.pop(k)))
        return d

    return_json = query(**kwargs)
    parsed_json = parse_return_json(return_json)

    if expand:
        return (__expand_dict(e) for e in parsed_json)
    else:
        return parsed_json


def query_predictions_as_dataframe(**kwargs):
    """
    Shortcut for query_predictions() but returns a Pandas DataFrame
    instead of a list of dicts.

    :param typing.Any kwargs: Keyword args for query_predictions() method
    :rtype: pd.DataFrame
    """
    try:
        import pandas as pd
    except ImportError:
        raise RuntimeError((
            'Failed to import pandas. Make sure to add '
            'pandas to your requirements.txt file'
        ))

    return pd.DataFrame(query_predictions(**kwargs))
