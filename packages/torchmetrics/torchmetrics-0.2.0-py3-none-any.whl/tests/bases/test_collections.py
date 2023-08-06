# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pickle

import pytest
import torch

from tests.helpers.testers import DummyMetricDiff, DummyMetricSum
from torchmetrics.collections import MetricCollection

torch.manual_seed(42)


def test_metric_collection(tmpdir):
    m1 = DummyMetricSum()
    m2 = DummyMetricDiff()

    metric_collection = MetricCollection([m1, m2])

    # Test correct dict structure
    assert len(metric_collection) == 2
    assert metric_collection['DummyMetricSum'] == m1
    assert metric_collection['DummyMetricDiff'] == m2

    # Test correct initialization
    for name, metric in metric_collection.items():
        assert metric.x == 0, f'Metric {name} not initialized correctly'

    # Test every metric gets updated
    metric_collection.update(5)
    for name, metric in metric_collection.items():
        assert metric.x.abs() == 5, f'Metric {name} not updated correctly'

    # Test compute on each metric
    metric_collection.update(-5)
    metric_vals = metric_collection.compute()
    assert len(metric_vals) == 2
    for name, metric_val in metric_vals.items():
        assert metric_val == 0, f'Metric {name}.compute not called correctly'

    # Test that everything is reset
    for name, metric in metric_collection.items():
        assert metric.x == 0, f'Metric {name} not reset correctly'

    # Test pickable
    metric_pickled = pickle.dumps(metric_collection)
    metric_loaded = pickle.loads(metric_pickled)
    assert isinstance(metric_loaded, MetricCollection)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_device_and_dtype_transfer_metriccollection(tmpdir):
    m1 = DummyMetricSum()
    m2 = DummyMetricDiff()

    metric_collection = MetricCollection([m1, m2])
    for _, metric in metric_collection.items():
        assert metric.x.is_cuda is False
        assert metric.x.dtype == torch.float32

    metric_collection = metric_collection.to(device='cuda')
    for _, metric in metric_collection.items():
        assert metric.x.is_cuda

    metric_collection = metric_collection.double()
    for _, metric in metric_collection.items():
        assert metric.x.dtype == torch.float64

    metric_collection = metric_collection.half()
    for _, metric in metric_collection.items():
        assert metric.x.dtype == torch.float16


def test_metric_collection_wrong_input(tmpdir):
    """ Check that errors are raised on wrong input """
    m1 = DummyMetricSum()

    # Not all input are metrics (list)
    with pytest.raises(ValueError):
        _ = MetricCollection([m1, 5])

    # Not all input are metrics (dict)
    with pytest.raises(ValueError):
        _ = MetricCollection({'metric1': m1, 'metric2': 5})

    # Same metric passed in multiple times
    with pytest.raises(ValueError, match='Encountered two metrics both named *.'):
        _ = MetricCollection([m1, m1])

    # Not a list or dict passed in
    with pytest.raises(ValueError, match='Unknown input to MetricCollection.'):
        _ = MetricCollection(m1)


def test_metric_collection_args_kwargs(tmpdir):
    """ Check that args and kwargs gets passed correctly in metric collection,
        Checks both update and forward method
    """
    m1 = DummyMetricSum()
    m2 = DummyMetricDiff()

    metric_collection = MetricCollection([m1, m2])

    # args gets passed to all metrics
    metric_collection.update(5)
    assert metric_collection['DummyMetricSum'].x == 5
    assert metric_collection['DummyMetricDiff'].x == -5
    metric_collection.reset()
    _ = metric_collection(5)
    assert metric_collection['DummyMetricSum'].x == 5
    assert metric_collection['DummyMetricDiff'].x == -5
    metric_collection.reset()

    # kwargs gets only passed to metrics that it matches
    metric_collection.update(x=10, y=20)
    assert metric_collection['DummyMetricSum'].x == 10
    assert metric_collection['DummyMetricDiff'].x == -20
    metric_collection.reset()
    _ = metric_collection(x=10, y=20)
    assert metric_collection['DummyMetricSum'].x == 10
    assert metric_collection['DummyMetricDiff'].x == -20
