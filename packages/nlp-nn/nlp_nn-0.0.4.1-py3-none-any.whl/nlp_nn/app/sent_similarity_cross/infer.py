# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本相关性模型预测

Authors: fubo
Date: 2019/11/28 00:00:00
"""
import torch
from typing import List
from ...base.common import DeviceSettings
from ...model.sent_similarity_cross import SentSimilarity as SentSimilarity_


class SentSimilarity(object):
    def __init__(self, model_path: str):
        self.__similarity = SentSimilarity_(device_settings=DeviceSettings(gpu_idx=-1))
        if self.__similarity.load_released_model(model_path_script=model_path) is False:
            raise ValueError

    def inference(self, query1: str, query2: str) -> float:
        """
        短文本分类
        :param pivot_query: pivot_query
        :param pos_query: pos_query
        :param neg_query: neg_query
        :return:
        是否pos query和pivot query的相关性大于 neg query和pivot query的相关性
        pos query和pivot query的相关性
        neg query和pivot query的相关性
        """
        return self.__similarity.inference(query1=query1, query2=query2)

    def sent_encode_batch(self, queries: List[str]) -> torch.FloatTensor:
        """
        短文本转向量(批量)
        :param queries:
        :return:
        """
        return self.__similarity.base_encode(queries=queries)

    def sent_encode_similarity(self, tokens1: torch.FloatTensor, tokens2: torch.FloatTensor) -> float:
        """
        短文本向量相关性
        :param tokens1:
        :param tokens2:
        :return:
        """
        return self.__similarity.base_encode_similarity(tokens1=tokens1, tokens2=tokens2)

