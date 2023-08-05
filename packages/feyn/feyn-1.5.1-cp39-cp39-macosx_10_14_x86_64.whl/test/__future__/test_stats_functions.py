import unittest
from unittest.case import TestCase
import pytest

import numpy as np

from feyn.__future__.contrib.stats._stats_functions import _residual_square_sum, _f_statistic, _t_statistic, _log_likelihood, _g_statistic, _log_likelihood_null_hypothesis

class Test_stats_funct(unittest.TestCase):

    def test_RSS(self):
        actuals = np.array([1,0.5,6])
        expected = 1
        sum = (0.5)**2 + 5**2
        assert(_residual_square_sum(actuals, expected) == sum)

    def test_f_statistic(self):
        rss_restricted = 25
        rss_mini = 10
        no_samples = 10
        no_parameters = 4
        no_hypoth_para = 1
        act = (15 * (10 - 4)) / 10
        F, _ = _f_statistic(rss_restricted, rss_mini, no_samples, no_parameters, no_hypoth_para)
        assert(F == act)

    def test_t_statistic(self):
        optimized_para = 1.5
        sample_var = 3
        deriv_inv = np.random.uniform(size = (3,3))
        idx_para = 1
        a = np.array([[0],[1],[0]])
        matrix_entr = np.matmul(np.matmul(a.T, deriv_inv), a)

        denom = sample_var * np.sqrt(matrix_entr)
        act = optimized_para / denom

        T, _ = _t_statistic(optimized_para, idx_para, sample_var, 50, 2, deriv_inv)

        assert(T == act)

    def test_log_like(self):

        loss = 5
        no_samples = 10
        actual_log_like = -1.5342640972002735
        assert(actual_log_like == _log_likelihood(loss, no_samples, errors = 'normal'))
        assert(-5 ==_log_likelihood(loss))

    def test_G_statistic(self):

        log_like_act = -5
        log_like_est = -3
        G_act = 4
        G, _ = _g_statistic(log_like_act, log_like_est, 1)
        assert(G_act == G)

    def test_log_like_null(self):

        actuals = np.array([0,1,0,0])
        act_log_like = 3 * np.log(3) + 1 * np.log(1) - (4 * np.log(4))
        assert(act_log_like == _log_likelihood_null_hypothesis(actuals))