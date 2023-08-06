# Copyright 2020 Huy Le Nguyen (@usimarit)
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

import re
import os
import sys
import math
from typing import Union, List

import numpy as np
import tensorflow as tf


def float_feature(list_of_floats):
    return tf.train.Feature(float_list=tf.train.FloatList(value=list_of_floats))


def int64_feature(list_of_ints):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=list_of_ints))


def bytestring_feature(list_of_bytestrings):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=list_of_bytestrings))


def append_default_keys_dict(default_dict, dest_dict):
    if not dest_dict:
        return default_dict
    for key in default_dict.keys():
        if key not in dest_dict.keys():
            dest_dict[key] = default_dict[key]
    return dest_dict


def check_key_in_dict(dictionary, keys):
    for key in keys:
        if key not in dictionary.keys():
            raise ValueError("{} must be defined".format(key))


def is_hdf5_filepath(filepath):
    return (filepath.endswith('.h5') or filepath.endswith('.keras') or filepath.endswith('.hdf5'))


def is_cloud_path(path):
    """ Check if the path is on cloud (which requires tf.io.gfile)

    Args:
        path (str): Path to directory or file

    Returns:
        bool: True if path is on cloud, False otherwise
    """
    return bool(re.match(r"^[a-z]+://", path))


def preprocess_paths(paths: Union[List, str]):
    """Expand the path to the root "/"

    Args:
        paths (Union[List, str]): A path or list of paths

    Returns:
        Union[List, str]: A processed path or list of paths, return None if it's not path
    """
    if isinstance(paths, list):
        return [path if is_cloud_path(path) else os.path.abspath(os.path.expanduser(path)) for path in paths]
    elif isinstance(paths, str):
        return paths if is_cloud_path(paths) else os.path.abspath(os.path.expanduser(paths))
    else:
        return None


def nan_to_zero(input_tensor):
    return tf.where(tf.math.is_nan(input_tensor), tf.zeros_like(input_tensor), input_tensor)


def bytes_to_string(array: np.ndarray, encoding: str = "utf-8"):
    if array is None: return None
    return [transcript.decode(encoding) for transcript in array]


def get_num_batches(samples, batch_size, drop_remainders=True):
    if samples is None or batch_size is None: return None
    if drop_remainders: return math.floor(float(samples) / float(batch_size))
    return math.ceil(float(samples) / float(batch_size))


def merge_two_last_dims(x):
    b, _, f, c = shape_list(x)
    return tf.reshape(x, shape=[b, -1, f * c])


def get_rnn(rnn_type: str):
    assert rnn_type in ["lstm", "gru", "rnn"]
    if rnn_type.lower() == "lstm": return tf.keras.layers.LSTM
    if rnn_type.lower() == "gru": return tf.keras.layers.GRU
    return tf.keras.layers.SimpleRNN


def get_conv(conv_type):
    assert conv_type in ["conv1d", "conv2d"]

    if conv_type == "conv1d":
        return tf.keras.layers.Conv1D

    return tf.keras.layers.Conv2D


def print_one_line(*args):
    tf.print("\033[K", end="")
    tf.print("\r", *args, sep="", end=" ", output_stream=sys.stdout)


def read_bytes(path: str) -> tf.Tensor:
    with tf.io.gfile.GFile(path, "rb") as f:
        content = f.read()
    return tf.convert_to_tensor(content, dtype=tf.string)


def shape_list(x, out_type=tf.int32):
    """Deal with dynamic shape in tensorflow cleanly."""
    static = x.shape.as_list()
    dynamic = tf.shape(x, out_type=out_type)
    return [dynamic[i] if s is None else s for i, s in enumerate(static)]


def get_shape_invariants(tensor):
    shapes = shape_list(tensor)
    return tf.TensorShape([i if isinstance(i, int) else None for i in shapes])


def get_float_spec(tensor):
    shape = get_shape_invariants(tensor)
    return tf.TensorSpec(shape, dtype=tf.float32)


def merge_repeated(yseqs, blank=0):
    result = tf.reshape(yseqs[0], [1])

    U = shape_list(yseqs)[0]
    i = tf.constant(1, dtype=tf.int32)

    def _cond(i, result, yseqs, U): return tf.less(i, U)

    def _body(i, result, yseqs, U):
        if yseqs[i] != result[-1]:
            result = tf.concat([result, [yseqs[i]]], axis=-1)
        return i + 1, result, yseqs, U

    _, result, _, _ = tf.while_loop(
        _cond,
        _body,
        loop_vars=[i, result, yseqs, U],
        shape_invariants=(
            tf.TensorShape([]),
            tf.TensorShape([None]),
            tf.TensorShape([None]),
            tf.TensorShape([])
        )
    )

    return tf.pad(result, [[U - shape_list(result)[0], 0]], constant_values=blank)


def log10(x):
    numerator = tf.math.log(x)
    denominator = tf.math.log(tf.constant(10, dtype=numerator.dtype))
    return numerator / denominator


def get_reduced_length(length, reduction_factor):
    return tf.cast(tf.math.ceil(tf.divide(length, tf.cast(reduction_factor, dtype=length.dtype))), dtype=tf.int32)


def count_non_blank(tensor: tf.Tensor, blank: int or tf.Tensor = 0, axis=None):
    return tf.reduce_sum(tf.where(tf.not_equal(tensor, blank), x=tf.ones_like(tensor), y=tf.zeros_like(tensor)), axis=axis)


def has_gpu_or_tpu():
    gpus = tf.config.list_logical_devices("GPU")
    tpus = tf.config.list_logical_devices("TPU")
    if len(gpus) == 0 and len(tpus) == 0: return False
    return True


def has_tpu():
    tpus = tf.config.list_logical_devices("TPU")
    if len(tpus) == 0: return False
    return True


def find_max_length_prediction_tfarray(tfarray: tf.TensorArray) -> tf.Tensor:
    with tf.name_scope("find_max_length_prediction_tfarray"):
        index = tf.constant(0, dtype=tf.int32)
        total = tfarray.size()
        max_length = tf.constant(0, dtype=tf.int32)

        def condition(index, _): return tf.less(index, total)

        def body(index, max_length):
            prediction = tfarray.read(index)
            length = tf.shape(prediction)[0]
            max_length = tf.where(tf.greater(length, max_length), length, max_length)
            return index + 1, max_length

        index, max_length = tf.while_loop(condition, body, loop_vars=[index, max_length], swap_memory=False)
        return max_length


def pad_prediction_tfarray(tfarray: tf.TensorArray, blank: int or tf.Tensor) -> tf.TensorArray:
    with tf.name_scope("pad_prediction_tfarray"):
        index = tf.constant(0, dtype=tf.int32)
        total = tfarray.size()
        max_length = find_max_length_prediction_tfarray(tfarray)

        def condition(index, _): return tf.less(index, total)

        def body(index, tfarray):
            prediction = tfarray.read(index)
            prediction = tf.pad(
                prediction, paddings=[[0, max_length - tf.shape(prediction)[0]]],
                mode="CONSTANT", constant_values=blank
            )
            tfarray = tfarray.write(index, prediction)
            return index + 1, tfarray

        index, tfarray = tf.while_loop(condition, body, loop_vars=[index, tfarray], swap_memory=False)
        return tfarray
