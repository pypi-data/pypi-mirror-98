# -*- coding: utf-8 -*-

"""
keras_resnet.blocks._time_distributed_2d
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements a number of popular time distributed two-dimensional residual blocks.
"""
import tensorflow as tf
from xtreme_vision.Detection.keras_resnet import layers

parameters = {
    "kernel_initializer": "he_normal"
}


def time_distributed_basic_2d(
    filters,
    stage=0,
    block=0,
    kernel_size=3,
    numerical_name=False,
    stride=None,
    freeze_bn=False
):
    """

    A time distributed two-dimensional basic block.

    :param filters: the output’s feature space

    :param stage: int representing the stage of this block (starting from 0)

    :param block: int representing this block (starting from 0)

    :param kernel_size: size of the kernel

    :param numerical_name: if true, uses numbers to represent blocks instead of chars (ResNet{101, 152, 200})

    :param stride: int representing the stride used in the shortcut and the first conv layer, default derives stride from block id

    :param freeze_bn: if true, freezes BatchNormalization layers (ie. no updates are done in these layers)

    Usage:

        >>> import keras_resnet.blocks

        >>> keras_resnet.blocks.time_distributed_basic_2d(64)

    """
    if stride is None:
        if block != 0 or stage == 0:
            stride = 1
        else:
            stride = 2

    if tf.keras.backend.image_data_format() == "channels_last":
        axis = 3
    else:
        axis = 1

    if block > 0 and numerical_name:
        block_char = "b{}".format(block)
    else:
        block_char = chr(ord('a') + block)

    stage_char = str(stage + 2)

    def f(x):
        y = tf.keras.layers.TimeDistributed(tf.keras.layers.ZeroPadding2D(padding=1), name="padding{}{}_branch2a".format(stage_char, block_char))(x)

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(filters, kernel_size, strides=stride, use_bias=False, **parameters), name="res{}{}_branch2a".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(layers.BatchNormalization(axis=axis, epsilon=1e-5, freeze=freeze_bn), name="bn{}{}_branch2a".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Activation("relu"), name="res{}{}_branch2a_relu".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.ZeroPadding2D(padding=1), name="padding{}{}_branch2b".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(filters, kernel_size, use_bias=False, **parameters), name="res{}{}_branch2b".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(layers.BatchNormalization(axis=axis, epsilon=1e-5, freeze=freeze_bn), name="bn{}{}_branch2b".format(stage_char, block_char))(y)

        if block == 0:
            shortcut = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(filters, (1, 1), strides=stride, use_bias=False, **parameters), name="res{}{}_branch1".format(stage_char, block_char))(x)

            shortcut = tf.keras.layers.TimeDistributed(layers.BatchNormalization(axis=axis, epsilon=1e-5, freeze=freeze_bn), name="bn{}{}_branch1".format(stage_char, block_char))(shortcut)
        else:
            shortcut = x

        y = tf.keras.layers.Add(name="res{}{}".format(stage_char, block_char))([y, shortcut])

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Activation("relu"), name="res{}{}_relu".format(stage_char, block_char))(y)

        return y

    return f


def time_distributed_bottleneck_2d(
    filters,
    stage=0,
    block=0,
    kernel_size=3,
    numerical_name=False,
    stride=None,
    freeze_bn=False
):
    """

    A time distributed two-dimensional bottleneck block.

    :param filters: the output’s feature space

    :param stage: int representing the stage of this block (starting from 0)

    :param block: int representing this block (starting from 0)

    :param kernel_size: size of the kernel

    :param numerical_name: if true, uses numbers to represent blocks instead of chars (ResNet{101, 152, 200})

    :param stride: int representing the stride used in the shortcut and the first conv layer, default derives stride from block id

    :param freeze_bn: if true, freezes BatchNormalization layers (ie. no updates are done in these layers)

    Usage:

        >>> import keras_resnet.blocks

        >>> keras_resnet.blocks.time_distributed_bottleneck_2d(64)

    """
    if stride is None:
        if block != 0 or stage == 0:
            stride = 1
        else:
            stride = 2

    if tf.keras.backend.image_data_format() == "channels_last":
        axis = 3
    else:
        axis = 1

    if block > 0 and numerical_name:
        block_char = "b{}".format(block)
    else:
        block_char = chr(ord('a') + block)

    stage_char = str(stage + 2)

    def f(x):
        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(filters, (1, 1), strides=stride, use_bias=False, **parameters), name="res{}{}_branch2a".format(stage_char, block_char))(x)

        y = tf.keras.layers.TimeDistributed(layers.BatchNormalization(axis=axis, epsilon=1e-5, freeze=freeze_bn), name="bn{}{}_branch2a".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Activation("relu"), name="res{}{}_branch2a_relu".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.ZeroPadding2D(padding=1), name="padding{}{}_branch2b".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(filters, kernel_size, use_bias=False, **parameters), name="res{}{}_branch2b".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(layers.BatchNormalization(axis=axis, epsilon=1e-5, freeze=freeze_bn), name="bn{}{}_branch2b".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Activation("relu"), name="res{}{}_branch2b_relu".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(filters * 4, (1, 1), use_bias=False, **parameters), name="res{}{}_branch2c".format(stage_char, block_char))(y)

        y = tf.keras.layers.TimeDistributed(layers.BatchNormalization(axis=axis, epsilon=1e-5, freeze=freeze_bn), name="bn{}{}_branch2c".format(stage_char, block_char))(y)

        if block == 0:
            shortcut = tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(filters * 4, (1, 1), strides=stride, use_bias=False, **parameters), name="res{}{}_branch1".format(stage_char, block_char))(x)

            shortcut = tf.keras.layers.TimeDistributed(tf.keras.layers.BatchNormalization(axis=axis, epsilon=1e-5, freeze=freeze_bn), name="bn{}{}_branch1".format(stage_char, block_char))(shortcut)
        else:
            shortcut = x

        y = tf.keras.layers.Add(name="res{}{}".format(stage_char, block_char))([y, shortcut])

        y = tf.keras.layers.TimeDistributed(tf.keras.layers.Activation("relu"), name="res{}{}_relu".format(stage_char, block_char))(y)

        return y

    return f
