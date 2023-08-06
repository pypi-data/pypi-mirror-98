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
from collections import OrderedDict
from distutils.version import LooseVersion

import cloudpickle
import numpy as np
import pytest
import torch
from torch import nn

from tests.helpers.testers import DummyListMetric, DummyMetric, DummyMetricSum

torch.manual_seed(42)


def test_inherit():
    DummyMetric()


def test_add_state():
    a = DummyMetric()

    a.add_state("a", torch.tensor(0), "sum")
    assert a._reductions["a"](torch.tensor([1, 1])) == 2

    a.add_state("b", torch.tensor(0), "mean")
    assert np.allclose(a._reductions["b"](torch.tensor([1.0, 2.0])).numpy(), 1.5)

    a.add_state("c", torch.tensor(0), "cat")
    assert a._reductions["c"]([torch.tensor([1]), torch.tensor([1])]).shape == (2, )

    with pytest.raises(ValueError):
        a.add_state("d1", torch.tensor(0), 'xyz')

    with pytest.raises(ValueError):
        a.add_state("d2", torch.tensor(0), 42)

    with pytest.raises(ValueError):
        a.add_state("d3", [torch.tensor(0)], 'sum')

    with pytest.raises(ValueError):
        a.add_state("d4", 42, 'sum')

    def custom_fx(x):
        return -1

    a.add_state("e", torch.tensor(0), custom_fx)
    assert a._reductions["e"](torch.tensor([1, 1])) == -1


def test_add_state_persistent():
    a = DummyMetric()

    a.add_state("a", torch.tensor(0), "sum", persistent=True)
    assert "a" in a.state_dict()

    a.add_state("b", torch.tensor(0), "sum", persistent=False)

    if LooseVersion(torch.__version__) >= LooseVersion("1.6.0"):
        assert "b" not in a.state_dict()


def test_reset():

    class A(DummyMetric):
        pass

    class B(DummyListMetric):
        pass

    a = A()
    assert a.x == 0
    a.x = torch.tensor(5)
    a.reset()
    assert a.x == 0

    b = B()
    assert isinstance(b.x, list) and len(b.x) == 0
    b.x = torch.tensor(5)
    b.reset()
    assert isinstance(b.x, list) and len(b.x) == 0


def test_update():

    class A(DummyMetric):

        def update(self, x):
            self.x += x

    a = A()
    assert a.x == 0
    assert a._computed is None
    a.update(1)
    assert a._computed is None
    assert a.x == 1
    a.update(2)
    assert a.x == 3
    assert a._computed is None


def test_compute():

    class A(DummyMetric):

        def update(self, x):
            self.x += x

        def compute(self):
            return self.x

    a = A()
    assert 0 == a.compute()
    assert 0 == a.x
    a.update(1)
    assert a._computed is None
    assert a.compute() == 1
    assert a._computed == 1
    a.update(2)
    assert a._computed is None
    assert a.compute() == 3
    assert a._computed == 3

    # called without update, should return cached value
    a._computed = 5
    assert a.compute() == 5


def test_hash():

    class A(DummyMetric):
        pass

    class B(DummyListMetric):
        pass

    a1 = A()
    a2 = A()
    assert hash(a1) != hash(a2)

    b1 = B()
    b2 = B()
    assert hash(b1) == hash(b2)
    assert isinstance(b1.x, list) and len(b1.x) == 0
    b1.x.append(torch.tensor(5))
    assert isinstance(hash(b1), int)  # <- check that nothing crashes
    assert isinstance(b1.x, list) and len(b1.x) == 1
    b2.x.append(torch.tensor(5))
    # Sanity:
    assert isinstance(b2.x, list) and len(b2.x) == 1
    # Now that they have tensor contents, they should have different hashes:
    assert hash(b1) != hash(b2)


def test_forward():

    class A(DummyMetric):

        def update(self, x):
            self.x += x

        def compute(self):
            return self.x

    a = A()
    assert a(5) == 5
    assert a._forward_cache == 5

    assert a(8) == 8
    assert a._forward_cache == 8

    assert a.compute() == 13


def test_pickle(tmpdir):
    # doesn't tests for DDP
    a = DummyMetricSum()
    a.update(1)

    metric_pickled = pickle.dumps(a)
    metric_loaded = pickle.loads(metric_pickled)

    assert metric_loaded.compute() == 1

    metric_loaded.update(5)
    assert metric_loaded.compute() == 6

    metric_pickled = cloudpickle.dumps(a)
    metric_loaded = cloudpickle.loads(metric_pickled)

    assert metric_loaded.compute() == 1


def test_state_dict(tmpdir):
    """ test that metric states can be removed and added to state dict """
    metric = DummyMetric()
    assert metric.state_dict() == OrderedDict()
    metric.persistent(True)
    assert metric.state_dict() == OrderedDict(x=0)
    metric.persistent(False)
    assert metric.state_dict() == OrderedDict()


def test_child_metric_state_dict():
    """ test that child metric states will be added to parent state dict """

    class TestModule(nn.Module):

        def __init__(self):
            super().__init__()
            self.metric = DummyMetric()
            self.metric.add_state('a', torch.tensor(0), persistent=True)
            self.metric.add_state('b', [], persistent=True)
            self.metric.register_buffer('c', torch.tensor(0))

    module = TestModule()
    expected_state_dict = {
        'metric.a': torch.tensor(0),
        'metric.b': [],
        'metric.c': torch.tensor(0),
    }
    assert module.state_dict() == expected_state_dict


@pytest.mark.skipif(not torch.cuda.is_available(), reason="Test requires GPU.")
def test_device_and_dtype_transfer(tmpdir):
    metric = DummyMetricSum()
    assert metric.x.is_cuda is False
    assert metric.x.dtype == torch.float32

    metric = metric.to(device='cuda')
    assert metric.x.is_cuda

    metric = metric.double()
    assert metric.x.dtype == torch.float64

    metric = metric.half()
    assert metric.x.dtype == torch.float16
