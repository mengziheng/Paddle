#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
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

import unittest

import gradient_checker
import numpy as np
from decorator_helper import prog_scope
from eager_op_test import OpTest, convert_float_to_uint16

import paddle
from paddle import fluid
from paddle.fluid import Program, core, program_guard


# Situation 1: repeat_times is a list (without tensor)
class TestTileOpRank1(OpTest):
    def setUp(self):
        self.op_type = "tile"
        self.python_api = paddle.tile
        self.init_data()
        self.inputs = {'X': np.random.random(self.ori_shape).astype("float64")}
        self.attrs = {'repeat_times': self.repeat_times}
        output = np.tile(self.inputs['X'], self.repeat_times)
        self.outputs = {'Out': output}
        self.prim_op_type = "prim"
        self.enable_cinn = False
        self.public_python_api = paddle.tile

    def init_data(self):
        self.ori_shape = [100]
        self.repeat_times = [2]

    def test_check_output(self):
        self.check_output()

    def test_check_grad(self):
        self.check_grad(['X'], 'Out', check_prim=True)


class TestTileOpRank_ZeroDim1(TestTileOpRank1):
    def setUp(self):
        self.op_type = "tile"
        self.python_api = paddle.tile
        self.init_data()
        self.inputs = {'X': np.random.random(self.ori_shape).astype("float64")}
        self.attrs = {'repeat_times': self.repeat_times}
        output = np.tile(self.inputs['X'], self.repeat_times)
        self.outputs = {'Out': output}
        self.prim_op_type = "prim"
        self.enable_cinn = False
        self.public_python_api = paddle.tile

    def init_data(self):
        self.ori_shape = []
        self.repeat_times = []

    def test_check_output(self):
        self.check_output()

    def test_check_grad(self):
        self.check_grad(['X'], 'Out')


class TestTileOpRank_ZeroDim2(TestTileOpRank1):
    def setUp(self):
        self.op_type = "tile"
        self.python_api = paddle.tile
        self.init_data()
        self.inputs = {'X': np.random.random(self.ori_shape).astype("float64")}
        self.attrs = {'repeat_times': self.repeat_times}
        output = np.tile(self.inputs['X'], self.repeat_times)
        self.outputs = {'Out': output}
        self.prim_op_type = "prim"
        self.enable_cinn = False
        self.public_python_api = paddle.tile

    def init_data(self):
        self.ori_shape = []
        self.repeat_times = [2]

    def test_check_output(self):
        self.check_output()

    def test_check_grad(self):
        self.check_grad(['X'], 'Out')


class TestTileOpRank_ZeroDim3(TestTileOpRank1):
    def setUp(self):
        self.op_type = "tile"
        self.python_api = paddle.tile
        self.init_data()
        self.inputs = {'X': np.random.random(self.ori_shape).astype("float64")}
        self.attrs = {'repeat_times': self.repeat_times}
        output = np.tile(self.inputs['X'], self.repeat_times)
        self.outputs = {'Out': output}
        self.prim_op_type = "prim"
        self.enable_cinn = False
        self.public_python_api = paddle.tile

    def init_data(self):
        self.ori_shape = []
        self.repeat_times = [2, 3]

    def test_check_output(self):
        self.check_output()

    def test_check_grad(self):
        self.check_grad(['X'], 'Out')


# with dimension expanding
class TestTileOpRank2Expanding(TestTileOpRank1):
    def init_data(self):
        self.ori_shape = [120]
        self.repeat_times = [2, 2]


class TestTileOpRank2(TestTileOpRank1):
    def init_data(self):
        self.ori_shape = [12, 14]
        self.repeat_times = [2, 3]


class TestTileOpRank3_Corner(TestTileOpRank1):
    def init_data(self):
        self.ori_shape = (2, 10, 5)
        self.repeat_times = (1, 1, 1)


class TestTileOpRank3_Corner2(TestTileOpRank1):
    def init_data(self):
        self.ori_shape = (2, 10, 5)
        self.repeat_times = (2, 2)


class TestTileOpRank3(TestTileOpRank1):
    def init_data(self):
        self.ori_shape = (2, 4, 15)
        self.repeat_times = (2, 1, 4)


class TestTileOpRank4(TestTileOpRank1):
    def init_data(self):
        self.ori_shape = (2, 4, 5, 7)
        self.repeat_times = (3, 2, 1, 2)


# Situation 3: repeat_times is a tensor
class TestTileOpRank1_tensor(OpTest):
    def setUp(self):
        self.op_type = "tile"
        self.python_api = paddle.tile
        self.init_data()

        self.inputs = {
            'X': np.random.random(self.ori_shape).astype("float64"),
            'RepeatTimes': np.array(self.repeat_times).astype("int32"),
        }
        self.attrs = {}
        output = np.tile(self.inputs['X'], self.repeat_times)
        self.outputs = {'Out': output}

    def init_data(self):
        self.ori_shape = [100]
        self.repeat_times = [2]

    def test_check_output(self):
        self.check_output()

    def test_check_grad(self):
        self.check_grad(['X'], 'Out')


class TestTileOpRank2_tensor(TestTileOpRank1_tensor):
    def init_data(self):
        self.ori_shape = [12, 14]
        self.repeat_times = [2, 3]


# Situation 4: input x is Integer
class TestTileOpInteger(OpTest):
    def setUp(self):
        self.op_type = "tile"
        self.python_api = paddle.tile
        self.inputs = {
            'X': np.random.randint(10, size=(4, 4, 5)).astype("int32")
        }
        self.attrs = {'repeat_times': [2, 1, 4]}
        output = np.tile(self.inputs['X'], (2, 1, 4))
        self.outputs = {'Out': output}

    def test_check_output(self):
        self.check_output()


class TestTileFP16OP(OpTest):
    def setUp(self):
        self.op_type = "tile"
        self.dtype = np.float16
        self.python_api = paddle.tile
        self.init_data()
        x = np.random.uniform(10, size=self.ori_shape).astype(self.dtype)
        output = np.tile(x, self.repeat_times)
        self.inputs = {'X': x}
        self.attrs = {'repeat_times': self.repeat_times}
        self.outputs = {'Out': output}

    def init_data(self):
        self.dtype = np.float16
        self.ori_shape = [100, 4, 5]
        self.repeat_times = [2, 1, 4]

    def test_check_output(self):
        self.check_output()

    def test_check_grad(self):
        self.check_grad(['X'], 'Out')


@unittest.skipIf(
    not core.is_compiled_with_cuda()
    or not core.is_bfloat16_supported(core.CUDAPlace(0)),
    "core is not complied with CUDA and not support the bfloat16",
)
class TestTileBF16OP(OpTest):
    def setUp(self):
        self.op_type = 'tile'
        self.__class__.op_type = self.op_type
        self.python_api = paddle.tile
        self.init_data()
        x = np.random.uniform(10, size=self.ori_shape).astype(np.float32)
        output = np.tile(x, self.repeat_times)
        self.inputs = {'X': convert_float_to_uint16(x)}
        self.attrs = {'repeat_times': self.repeat_times}
        self.outputs = {'Out': convert_float_to_uint16(output)}
        self.enable_cinn = False

    def test_check_output(self):
        place = core.CUDAPlace(0)
        self.check_output_with_place(place)

    def init_data(self):
        self.dtype = np.uint16
        self.ori_shape = [100, 4, 5]
        self.repeat_times = [2, 1, 4]

    def test_check_grad(self):
        place = core.CUDAPlace(0)
        self.check_grad_with_place(place, ['X'], 'Out')


# Situation 5: input x is Bool
class TestTileOpBoolean(OpTest):
    def setUp(self):
        self.op_type = "tile"
        self.python_api = paddle.tile
        self.inputs = {'X': np.random.randint(2, size=(2, 4, 5)).astype("bool")}
        self.attrs = {'repeat_times': [2, 1, 4]}
        output = np.tile(self.inputs['X'], (2, 1, 4))
        self.outputs = {'Out': output}

    def test_check_output(self):
        self.check_output()


# Situation 56: input x is Integer
class TestTileOpInt64_t(OpTest):
    def setUp(self):
        self.op_type = "tile"
        self.python_api = paddle.tile
        self.inputs = {
            'X': np.random.randint(10, size=(2, 4, 5)).astype("int64")
        }
        self.attrs = {'repeat_times': [2, 1, 4]}
        output = np.tile(self.inputs['X'], (2, 1, 4))
        self.outputs = {'Out': output}

    def test_check_output(self):
        self.check_output()


class TestTileError(unittest.TestCase):
    def test_errors(self):
        with program_guard(Program(), Program()):
            x1 = fluid.create_lod_tensor(
                np.array([[-1]]), [[1]], fluid.CPUPlace()
            )
            repeat_times = [2, 2]
            self.assertRaises(TypeError, paddle.tile, x1, repeat_times)
            x2 = paddle.static.data(name='x2', shape=[-1, 4], dtype="uint8")
            self.assertRaises(TypeError, paddle.tile, x2, repeat_times)
            x3 = paddle.static.data(name='x3', shape=[-1, 4], dtype="bool")
            x3.stop_gradient = False
            self.assertRaises(ValueError, paddle.tile, x3, repeat_times)


class TestTileAPIStatic(unittest.TestCase):
    def test_api(self):
        with program_guard(Program(), Program()):
            repeat_times = [2, 2]
            x1 = paddle.static.data(name='x1', shape=[-1, 4], dtype="int32")
            out = paddle.tile(x1, repeat_times)
            positive_2 = paddle.tensor.fill_constant(
                [1], dtype="int32", value=2
            )
            out2 = paddle.tile(x1, repeat_times=[positive_2, 2])


# Test python API
class TestTileAPI(unittest.TestCase):
    def test_api(self):
        with fluid.dygraph.guard():
            np_x = np.random.random([12, 14]).astype("float32")
            x = paddle.to_tensor(np_x)

            positive_2 = np.array([2]).astype("int32")
            positive_2 = paddle.to_tensor(positive_2)

            repeat_times = np.array([2, 3]).astype("int32")
            repeat_times = paddle.to_tensor(repeat_times)

            out_1 = paddle.tile(x, repeat_times=[2, 3])
            out_2 = paddle.tile(x, repeat_times=[positive_2, 3])
            out_3 = paddle.tile(x, repeat_times=repeat_times)

            assert np.array_equal(out_1.numpy(), np.tile(np_x, (2, 3)))
            assert np.array_equal(out_2.numpy(), np.tile(np_x, (2, 3)))
            assert np.array_equal(out_3.numpy(), np.tile(np_x, (2, 3)))


class TestTileDoubleGradCheck(unittest.TestCase):
    def tile_wrapper(self, x):
        return paddle.tile(x[0], [2, 1])

    @prog_scope()
    def func(self, place):
        # the shape of input variable should be clearly specified, not inlcude -1.
        eps = 0.005
        dtype = np.float32

        data = paddle.static.data('data', [1, 2], dtype)
        data.persistable = True
        out = paddle.tile(data, [2, 1])
        data_arr = np.random.uniform(-1, 1, data.shape).astype(dtype)

        gradient_checker.double_grad_check(
            [data], out, x_init=[data_arr], place=place, eps=eps
        )
        gradient_checker.double_grad_check_for_dygraph(
            self.tile_wrapper, [data], out, x_init=[data_arr], place=place
        )

    def test_grad(self):
        paddle.enable_static()
        places = [fluid.CPUPlace()]
        if core.is_compiled_with_cuda():
            places.append(fluid.CUDAPlace(0))
        for p in places:
            self.func(p)


class TestTileTripleGradCheck(unittest.TestCase):
    def tile_wrapper(self, x):
        return paddle.tile(x[0], [2, 1])

    @prog_scope()
    def func(self, place):
        # the shape of input variable should be clearly specified, not inlcude -1.
        eps = 0.005
        dtype = np.float32

        data = paddle.static.data('data', [1, 2], dtype)
        data.persistable = True
        out = paddle.tile(data, [2, 1])
        data_arr = np.random.uniform(-1, 1, data.shape).astype(dtype)

        gradient_checker.triple_grad_check(
            [data], out, x_init=[data_arr], place=place, eps=eps
        )
        gradient_checker.triple_grad_check_for_dygraph(
            self.tile_wrapper, [data], out, x_init=[data_arr], place=place
        )

    def test_grad(self):
        paddle.enable_static()
        places = [fluid.CPUPlace()]
        if core.is_compiled_with_cuda():
            places.append(fluid.CUDAPlace(0))
        for p in places:
            self.func(p)


if __name__ == "__main__":
    paddle.enable_static()
    unittest.main()
