# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
评估指标

Authors: fubo
Date: 2019/11/28 00:00:00
"""

from typing import List, Tuple
import torch
from .utils import Utils


class Metric(object):
    @staticmethod
    def positional_weighted_rpf(
            ground_truth: torch.LongTensor,
            scores: torch.FloatTensor,
            point_count: int = 10
    ) -> torch.FloatTensor:
        """
        基于位置权重的RPF
        ground_truth: 标注结果 batch * instance_count
        scores: 预测分数 batch * instance_count
        point_count: 阈值数量
        return point_count * batch * 4(point, recall, precision, f-score)
        """
        # ground_truth = torch.LongTensor([[1, 0, 1, 0]])
        # scores = torch.FloatTensor([[0.55, 0.13, 0.63, 0.99]])
        if point_count < 1:
            raise ValueError
        if point_count == 1:
            thresholds = [0.5]
        else:
            thresholds = [(i * 1.0) / point_count for i in range(point_count)]

        results = torch.zeros(point_count, ground_truth.shape[0], 4)
        ground_truth_count = ground_truth.sum(dim=1)

        for index, threshold in enumerate(thresholds):
            # 阈值
            threshold_m = threshold * torch.ones(ground_truth.shape[0], 1)

            # 阈值过滤
            predict_score = scores * (scores >= threshold)
            predict_count = (predict_score > 0).sum(dim=1)

            # 排序预测结果
            predict_score_values, predict_score_index = torch.sort(predict_score, descending=True)

            # 标注确认正确的数据
            confirm_label = ground_truth * predict_score
            confirm_count = (confirm_label > 0).sum(dim=1)

            # 召回
            recall = torch.unsqueeze(confirm_count.float() / ground_truth_count.float(), 1)

            # 精确率
            precision = torch.zeros(ground_truth.shape[0], 1)
            for i in range(confirm_label.shape[0]):
                predict_full = torch.ones(int(predict_count[i]))
                predict_select = (
                        (confirm_label[i, :].index_select(0, predict_score_index[i, :int(predict_count[i])])) > 0
                ).long()
                denominator = Utils.reciprocal_log_nature_sum(int(predict_count[i]), predict_full)
                numerator = Utils.reciprocal_log_nature_sum(int(predict_count[i]), predict_select)
                precision[i, 0] = numerator / (denominator + 0.0000000001)

            # F-Score
            f_score = (2 * recall * precision) / (recall + precision + 0.0000000001)

            results[index, :, :] = torch.cat((threshold_m, recall, precision, f_score), dim=1)

        return results

    @staticmethod
    def ranking_mean_average_precision(relevant_counts: List[int], correct_index: List[List[int]]) -> Tuple:
        """
        排序的NDCG指标
        :param relevant_counts: 相关文档数量列表
        :param correct_index: 正确文档列表位置（从1开始）
        """
        if (len(relevant_counts) <= 0) or (len(relevant_counts) != len(correct_index)):
            # 计算的检索数量不一致
            return -1.0, []

        sum_ap = 0.0
        aps = []
        for i, count in enumerate(relevant_counts):
            index = correct_index[i]
            if min(index) < 1:
                # 正确文档的位置不在正确的范围
                return -1.0, []
            scores = [(j + 1) / index[j] if j < len(index) else 0.0 for j in range(count)]
            aps.append(1.0 * sum(scores) / len(scores))
            sum_ap = sum_ap + aps[-1]

        return 1.0 * sum_ap / len(relevant_counts), aps
