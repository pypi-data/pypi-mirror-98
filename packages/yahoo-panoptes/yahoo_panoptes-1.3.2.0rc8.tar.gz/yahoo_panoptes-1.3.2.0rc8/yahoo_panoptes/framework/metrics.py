"""
Copyright 2018, Oath Inc.
Licensed under the terms of the Apache 2.0 license. See LICENSE file in project root for terms.

This module defines metrics and their related abstractions
"""
import json
import re
import threading
from time import time

from six import string_types

from yahoo_panoptes.framework.exceptions import PanoptesBaseException
from yahoo_panoptes.framework.resources import PanoptesResource
from yahoo_panoptes.framework.validators import PanoptesValidators

_VALID_KEY = re.compile(r"^[^\d\W]\w*\Z")


METRICS_TIMESTAMP_PRECISION = 3
METRICS_GROUP_SCHEMA_VERSION = u'0.2'


class PanoptesMetricsException(PanoptesBaseException):
    pass


class PanoptesMetricsNullException(PanoptesMetricsException):
    pass


class PanoptesMetricType(object):
    GAUGE, COUNTER = list(range(2))


METRIC_TYPE_NAMES = dict((getattr(PanoptesMetricType, n), n) for n in dir(PanoptesMetricType) if u'_' not in n)


class PanoptesMetricValidators(object):
    @classmethod
    def valid_panoptes_resource(cls, resource):
        return resource and isinstance(resource, PanoptesResource)

    @classmethod
    def valid_panoptes_metric_type(cls, metric_type):
        return metric_type is not None and metric_type in METRIC_TYPE_NAMES

    @classmethod
    def valid_panoptes_metric(cls, metric):
        return metric and isinstance(metric, PanoptesMetric)

    @classmethod
    def valid_panoptes_metric_dimension(cls, metric_dimension):
        return metric_dimension and isinstance(metric_dimension, PanoptesMetricDimension)

    @classmethod
    def valid_panoptes_metrics_group(cls, metrics_group):
        return metrics_group and isinstance(metrics_group, PanoptesMetricsGroup)


class PanoptesMetric(object):
    """
    Representation of a metric monitored by a plugin

    A metric has a name and a corresponding value. It may also have associated dimension names and values

    Args:
        metric_name(str): The name of the metric
        metric_value(float): The value of the metric
        metric_type(int): The type of the metric - valid values are attributes of the PanoptesMetricType class
    """

    def __init__(self, metric_name, metric_value, metric_type, metric_creation_timestamp=None):
        assert PanoptesValidators.valid_nonempty_string(metric_name), 'metric_name must be a non-empty str'
        assert PanoptesValidators.valid_number(metric_value), 'metric_value must be number'
        assert PanoptesMetricValidators.valid_panoptes_metric_type(
                metric_type), u'metric_type must be an attribute of PanoptesMetricType'
        assert (metric_creation_timestamp is None) or PanoptesValidators.valid_number(metric_creation_timestamp), \
            u'metric_creation_timestamp should be None or a number'

        if not _VALID_KEY.match(metric_name):
            raise ValueError(
                    u'metric name "%s" has to match pattern: (letter|"_") (letter | digit | "_")*' % metric_name)

        self.__data = dict()
        self.__data[u'metric_creation_timestamp'] = round(metric_creation_timestamp, METRICS_TIMESTAMP_PRECISION) if \
            metric_creation_timestamp is not None else round(time(), METRICS_TIMESTAMP_PRECISION)
        self.__data[u'metric_name'] = metric_name
        self.__data[u'metric_value'] = metric_value
        self.__metric_type_raw = metric_type
        self.__data[u'metric_type'] = METRIC_TYPE_NAMES[metric_type].lower()

    @property
    def metric_name(self):
        """
        The name of the metric

        Returns:
            str: The name of the metric
        """
        return self.__data[u'metric_name']

    @property
    def metric_value(self):
        """
        The value of the metric

        Returns:
            float: The value of the metric
        """
        return self.__data[u'metric_value']

    @property
    def metric_timestamp(self):
        """
        The creation timestamp of the metric

        Returns:
            float: The creation timestamp of the metric
        """
        return round(self.__data[u'metric_creation_timestamp'], METRICS_TIMESTAMP_PRECISION)

    @property
    def metric_type(self):
        return self.__metric_type_raw

    @property
    def json(self):
        """
        The JSON representation of the metric

        Returns:
            str: The JSON representation of the metric
        """
        return json.dumps(self.__data, sort_keys=True)

    def __repr__(self):
        return u'PanoptesMetric[' + str(self.metric_name) + u'|' + str(self.metric_value) + u'|' + \
               METRIC_TYPE_NAMES[self.metric_type] + u'|' + str(self.metric_timestamp) + u']'

    def __hash__(self):
        return hash(self.__data[u'metric_name'] + str(self.__data[u'metric_value']))

    def __str__(self):
        return str(self.metric_name) + u'|' + str(self.metric_value) + u'|' + str(self.metric_type)

    def __lt__(self, other):
        if not isinstance(other, PanoptesMetric):
            return False
        return self.metric_name < other.metric_name

    def __eq__(self, other):
        if not isinstance(other, PanoptesMetric):
            return False

        return self.metric_name == other.metric_name and \
            self.metric_value == other.metric_value and \
            self.metric_type == other.metric_type


class PanoptesMetricDimension(object):
    def __init__(self, name, value):
        assert name and isinstance(name, string_types), (
            u'dimension name must be non-empty str or unicode, is type %s' % type(name))
        assert value and isinstance(value, string_types), (
            u'dimension value for dimension "%s" must be non-empty str or unicode, is type %s' % (name, type(value)))

        if not _VALID_KEY.match(name):
            raise ValueError(
                    u'dimension name "%s" has to match pattern: (letter|"_") (letter | digit | "_")*' % name)

        if u'|' in value:
            raise ValueError(u'dimension value "%s" cannot contain |' % value)

        self.__data = dict()

        self.__data[u'dimension_name'] = name
        self.__data[u'dimension_value'] = value

    @property
    def name(self):
        return self.__data[u'dimension_name']

    @property
    def value(self):
        return self.__data[u'dimension_value']

    @property
    def json(self):
        return json.dumps(self.__data)

    def __repr__(self):
        return u'PanoptesMetricDimension[{}|{}]'.format(self.name, str(self.value))

    def __hash__(self):
        return hash(self.name + self.value)

    def __str__(self):
        return str(self.name) + u'|' + str(self.value)

    def __lt__(self, other):
        if not isinstance(other, PanoptesMetricDimension):
            return False
        return self.name < other.name

    def __eq__(self, other):
        if not isinstance(other, PanoptesMetricDimension):
            return False
        return self.name == other.name and self.value == other.value


class PanoptesMetricsGroupEncoder(json.JSONEncoder):
    # https://github.com/PyCQA/pylint/issues/414
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, set):
            return list(o)
        if isinstance(o, PanoptesResource):
            return o.__dict__[u'_PanoptesResource__data']
        if isinstance(o, PanoptesMetric):
            return o.__dict__[u'_PanoptesMetric__data']
        if isinstance(o, PanoptesMetricDimension):
            return o.__dict__[u'_PanoptesMetricDimension__data']
        return json.JSONEncoder.default(self, o)


class PanoptesMetricsGroup(object):
    def __init__(self, resource, group_type, interval, creation_timestamp=None):
        assert PanoptesMetricValidators.valid_panoptes_resource(
                resource), u'resource must be an instance of PanoptesResource'
        assert PanoptesValidators.valid_nonempty_string(
                group_type), u'group_type must be a non-empty string'
        assert PanoptesValidators.valid_nonzero_integer(
                interval), u'interval must a integer greater than zero'

        self.__data = dict()
        self.__metrics_index = {metric_type: list() for metric_type in METRIC_TYPE_NAMES}
        self.__data[u'metrics_group_type'] = group_type
        self.__data[u'metrics_group_interval'] = interval
        self.__data[u'metrics_group_creation_timestamp'] = round(time(), METRICS_TIMESTAMP_PRECISION) \
            if creation_timestamp is None else creation_timestamp
        self.__data[u'metrics_group_schema_version'] = METRICS_GROUP_SCHEMA_VERSION
        self.__data[u'resource'] = resource
        self.__data[u'metrics'] = set()
        self.__data[u'dimensions'] = set()
        self._data_lock = threading.Lock()

    def copy(self, retain_timestamp=True):
        """
        Copy will retain the timestamp by default unless specified otherwise.
        The timestamp belongs to the timeseries, not the container.
        """
        timestamp = self.__data[u'metrics_group_creation_timestamp'] if retain_timestamp \
            else None

        copied_metrics_group = PanoptesMetricsGroup(self.resource, self.group_type,
                                                    self.interval, timestamp)
        for metric in self.metrics:
            copied_metrics_group.add_metric(metric)
        for dimension in self.dimensions:
            copied_metrics_group.add_dimension(dimension)

        return copied_metrics_group

    def add_metric(self, metric):
        assert PanoptesMetricValidators.valid_panoptes_metric(metric), u'metric must be an instance of PanoptesMetric'

        if metric.metric_name in self.__metrics_index[metric.metric_type]:
            raise KeyError(u'Metric name "%s" (type "%s") for metrics group type "%s" already populated' %
                           (metric.metric_name, METRIC_TYPE_NAMES[metric.metric_type], self.group_type))
        self.__data[u'metrics'].add(metric)
        self.__metrics_index[metric.metric_type].append(metric.metric_name)

    def add_dimension(self, dimension):
        assert PanoptesMetricValidators.valid_panoptes_metric_dimension(dimension), u'dimension must be instance ' \
                                                                                    u'of PanoptesMetricDimension'
        with self._data_lock:
            if self.contains_dimension_by_name(dimension.name):
                raise KeyError(u'Dimension name %s already populated. '
                               u'Please use upsert_dimension if you need to update dimensions' % dimension.name)
            else:
                self.__data[u'dimensions'].add(dimension)

    def get_dimension_by_name(self, dimension_name):
        assert dimension_name and isinstance(dimension_name, string_types), (
            u'dimension name must be non-empty str or unicode, is type %s' % type(dimension_name))
        dimension = [x for x in self.__data[u'dimensions'] if x.name == dimension_name]
        if not dimension:
            return None
        else:
            return dimension[0]

    def contains_dimension_by_name(self, dimension_name):
        assert dimension_name and isinstance(dimension_name, string_types), (
            u'dimension name must be non-empty str or unicode, is type %s' % type(dimension_name))
        return dimension_name in [x.name for x in self.__data[u'dimensions']]

    def delete_dimension_by_name(self, dimension_name):
        assert dimension_name and isinstance(dimension_name, string_types), (
            u'dimension name must be non-empty str or unicode, is type %s' % type(dimension_name))
        with self._data_lock:
            if self.contains_dimension_by_name(dimension_name):
                dimension = self.get_dimension_by_name(dimension_name)
                self.__data[u'dimensions'].remove(dimension)

    def upsert_dimension(self, dimension):
        assert PanoptesMetricValidators.valid_panoptes_metric_dimension(
                dimension), u'dimension must be instance of PanoptesMetricDimension'

        if self.contains_dimension_by_name(dimension.name):
            self.delete_dimension_by_name(dimension.name)
        self.__data[u'dimensions'].add(dimension)

    @staticmethod
    def flatten_dimensions(dimensions):
        """Changes list of dimensions to dict

        Args:
            dimensions(list): List of dictionaries containing name and value for each dimension

        Returns:
            dict: Key is dimension_name, Value is dimension_value
        """
        return {dimension[u'dimension_name']: dimension[u'dimension_value'] for dimension in dimensions}

    @staticmethod
    def flatten_metrics(metrics):
        """Changes list of metrics to nested dict

        Args:
            metrics(list): List of dictionaries containing name, value, type

        Returns:
            dict: Keys are counter, gauge, which then contain a dictionary of the metrics name paired with
            values and timestamps for each name.
        """
        metrics_dict = {u'counter': {}, u'gauge': {}}

        for metric in metrics:
            metrics_dict[metric[u'metric_type']][metric[u'metric_name']] = \
                {u'value': metric[u'metric_value'], u'timestamp': metric[u'metric_creation_timestamp']}

        return metrics_dict

    @property
    def resource(self):
        return self.__data[u'resource']

    @property
    def metrics(self):
        return sorted(self.__data[u'metrics'])

    @property
    def dimensions(self):
        return sorted(self.__data[u'dimensions'])

    @property
    def group_type(self):
        return self.__data[u'metrics_group_type']

    @property
    def interval(self):
        return self.__data[u'metrics_group_interval']

    @property
    def schema_version(self):
        return self.__data[u'metrics_group_schema_version']

    @property
    def creation_timestamp(self):
        return self.__data[u'metrics_group_creation_timestamp']

    @property
    def json(self):
        return json.dumps(self.__data, cls=PanoptesMetricsGroupEncoder)

    def __repr__(self):
        return u'PanoptesMetricsGroup[' \
            u'resource:' + repr(self.resource) + u',' \
            u'interval:' + str(self.interval) + u',' \
            u'schema_version:' + self.schema_version + u',' \
            u'group_type:' + self.group_type + u',' \
            u'creation_timestamp:' + str(self.creation_timestamp) + u',' \
            u'dimensions:[' + u','.join([repr(dimension) for dimension in sorted(self.dimensions)]) + u'],' \
            u'metrics:[' + u','.join([repr(metric) for metric in sorted(self.metrics)]) + u']]'

    def __hash__(self):
        metrics_string = str()
        dimensions_string = str()

        for metric in frozenset(self.metrics):
            metrics_string += str(metric)

        for dimension in frozenset(self.dimensions):
            dimensions_string += str(dimension)

        return hash(str(self.resource) + metrics_string + dimensions_string)

    def __lt__(self, other):
        if not isinstance(other, PanoptesMetricsGroup):
            return False
        return self.group_type < other.group_type

    def __eq__(self, other):
        if not isinstance(other, PanoptesMetricsGroup):
            return False
        return self.resource == other.resource and self.metrics == other.metrics and self.dimensions == other.dimensions


class PanoptesMetricsGroupSet(object):
    def __init__(self):
        self._metrics_groups = set()

    def add(self, metrics_group):
        assert PanoptesMetricValidators.valid_panoptes_metrics_group(
                metrics_group), u'metrics_group must be an instance of PanoptesMetricsGroup'
        self._metrics_groups.add(metrics_group)

    def remove(self, metrics_group):
        assert PanoptesMetricValidators.valid_panoptes_metrics_group(
                metrics_group), u'metrics_group must be an instance of PanoptesMetricsGroup'
        self._metrics_groups.remove(metrics_group)

    @property
    def metrics_groups(self):
        return self._metrics_groups

    def __add__(self, other):
        if not other or not isinstance(other, PanoptesMetricsGroupSet):
            raise TypeError(u'Unsupported type for addition: {}'.format(type(other)))

        new_metrics_group_set = PanoptesMetricsGroupSet()
        list(map(new_metrics_group_set.add, self.metrics_groups))
        list(map(new_metrics_group_set.add, other.metrics_groups))

        return new_metrics_group_set

    def __iter__(self):
        return iter(self._metrics_groups)

    def __next__(self):
        return next(iter(self._metrics_groups))

    def __len__(self):
        return len(self._metrics_groups)

    def __repr__(self):
        return u'PanoptesMetricsGroupSet[' + \
            u','.join([repr(metric_group) for metric_group in sorted(self._metrics_groups)]) + \
            u']'


class PanoptesMetricSet(object):
    """
    An (un-ordered) set of PanoptesMetrics
    """

    def __init__(self):
        self.__metrics = set()

    def add(self, metric):
        """
        Add a metric to the set

        Args:
            metric (PanoptesMetric): The metric to add

        Returns:
            None

        """
        assert isinstance(metric, PanoptesMetric), 'metric must be an instance of PanoptesMetric'
        self.__metrics.add(metric)

    def remove(self, metric):
        """
        Remove a metric from the set

        Args:
            metric (PanoptesMetric): The metric to remove

        Returns:
            None

        """
        assert isinstance(metric, PanoptesMetric), 'metric must be an instance of PanoptesMetric'
        self.__metrics.remove(metric)

    @property
    def metrics(self):
        """
        Return the list of metrics in this set

        Returns:
            list: The set of metrics

        """
        return self.__metrics

    def __iter__(self):
        return iter(self.__metrics)

    def __next__(self):
        """
        Returns the next metric in the set

        Returns:
            PanoptesMetric: The next metric in the set
        """
        return next(iter(self.__metrics))

    def __repr__(self):
        return u'PanoptesMetricSet[' + \
               u','.join([repr(metric) for metric in self.__metrics]) + \
               u']'

    def __len__(self):
        return len(self.__metrics)
