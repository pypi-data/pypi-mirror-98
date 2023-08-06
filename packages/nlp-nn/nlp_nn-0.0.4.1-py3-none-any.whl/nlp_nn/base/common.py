# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
通用数据定义

Authors: fubo
Date: 2019/11/28 00:00:00
"""
from pydantic import BaseModel
from enum import Enum


class ModelState(Enum):
    """ 模型状态 """
    # 预测状态
    INFERENCE = 0
    TRAIN = 1


class BerType(Enum):
    """ bert类型 """
    # Base Bert
    BASE_BERT = 0

    # Lite Bert tiny
    LITE_BERT_TINY = 1

    # Lite Bert small
    LITE_BERT_SMALL = 2

    # Lite Bert large
    LITE_BERT_LARGE = 3

    # Lite Bert xlarge
    LITE_BERT_XLARGE = 4

    # Lite Bert xxlarge
    LITE_BERT_XXLARGE = 5


class ModelDataType(Enum):
    """ 模型数据类型 """
    # 训练数据
    TRAIN = 0

    # 验证数据
    VALID = 1


class DeviceSettings(BaseModel):
    """ 模型使用的设备信息（GPU） """
    # gpu的device序号(-1表示使用CPU)
    gpu_idx: int = -1


class ExportModelSettings(BaseModel):
    """ 导出模型文件配置 """

    # 导出模型文件配置文件
    model_config_file: str = "config.json"

    # 主模型文件
    model_file: str = "model.pt"

    # 第三方词典文件
    third_dict_dir: str = "dict"


class CoachSettings(BaseModel):
    """ 训练配置 """
    # tf board 日志存放路径
    tf_log_dir: str = "log"

    # 模型训练环境临时模型存储路径
    train_models_dir: str = "train_dir"

    # 第三方资源路径
    dict_dir: str = "dict"

    # 数据集路径
    data_dir: str = "data"

    # 模型文件名
    model_file: str = "model.pkl"

    # 模型配置文件名
    model_conf_file: str = "config.json"

    # 训练集文件名
    train_data_set_file: str = ""

    # 验证集文件名
    valid_data_set_file: str = ""

    # valid模型的频次per epoch
    valid_interval: int = 1

    # 模型训练最大epoch数量
    max_epoch_times: int = 100

    # 训练集的batch size
    train_batch_size: int = 10

    # 验证集的batch size
    valid_batch_size: int = 0

    # 学习率
    lr: float = 0.000001

    # 学习率的衰减率
    lr_weight_decay: float = 0.0000005


class ModelSettings(BaseModel):
    """ 模型配置 """

    # 模型名称
    model_name: str = ""

    # 模型描述
    model_describe: str = ""


class Const(object):
    """ 通用的常量 """

    # 最小正数
    MIN_POSITIVE_NUMBER = 0.0000000001
