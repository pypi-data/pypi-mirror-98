# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
数据类定义

Authors: fubo
Date: 2019/11/28 00:00:00
"""
from pydantic import BaseModel
from typing import List


class Tokens(BaseModel):
    """ token序列数据 """
    # 原始query
    query: str

    # 分词token的id序列
    tokens: List[int]

    # 分词token的id序列，padding到最大长度
    padding_tokens: List[int]


class TokenLabel(BaseModel):
    """ 实体标签 """
    # 实体名
    label: str

    # 起始点
    pos: int

    # 长度
    length: int

    # 实体内容
    text: str = ""


class SentTokenSample(BaseModel):
    """ intent slot数据 """
    # query
    query: str

    # 意图label
    sent_label: str

    # 实体label
    token_labels: List[TokenLabel] = []


class SentClassifySample(BaseModel):
    """ 文本分类问题数据 """
    # query
    queries: List[str]

    # label
    labels: List[str]


class TokenClassifySample(BaseModel):
    # query
    query: str

    # 实体label
    token_labels: List[TokenLabel] = []
