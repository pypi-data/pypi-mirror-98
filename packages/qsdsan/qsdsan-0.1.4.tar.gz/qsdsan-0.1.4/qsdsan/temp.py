#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 19:13:17 2021

@author: Yalin Li
"""


# %%

from qsdsan import stats as s
from qsdsan.systems import bwaise as bw

m = bw.models
modelA = m.modelA

a = bw.analyses
key_metrics = a.key_metrics

spearman_rho, fig, ax, all_params = a.run_plot_spearman(modelA, N=100)


key_paramsA = modelA.get_parameters()


# %%

morris_dct, fig, ax = a.run_plot_morris(modelA, 10, test_convergence=False)

morris_dct_conv, fig, ax = a.run_plot_morris(modelA, 100, test_convergence=True)


fast_dct, fig, ax = a.run_plot_fast(modelA, 'FAST', 100, M=4)

rbd_dct, fig, ax = a.run_plot_fast(modelA, 'RBD', 100, M=10)


sobol_dct, fig, ax = a.run_plot_sobol(modelA, 10, file_prefix='')


# %%

fig, ax = s.plot_uncertainties(modelA, x_axis=key_metrics, kind='box')

fig, ax = s.plot_uncertainties(modelA, y_axis=key_metrics, kind='hist',
                                center_kws={'kde':True, 'log_scale': 10})

fig, ax = s.plot_uncertainties(modelA, x_axis=key_metrics, kind='kde',
                                center_kws={'fill': True, 'log_scale': 2})

fig, axes = s.plot_uncertainties(modelA, x_axis=key_metrics[0],
                                  y_axis=key_metrics[1], kind='hist-box')


fig, axes = s.plot_uncertainties(modelA, x_axis=key_metrics[0],
                                  y_axis=key_metrics[1], kind='kde-kde',
                                  margin_kws={'fill': True})

fig, axes = s.plot_uncertainties(modelA, x_axis=key_metrics[0],
                                  y_axis=key_metrics[1], kind='kde-hist',
                                  center_kws={'fill': True},
                                  margin_kws={'kde': True, 'fill': False})


fig, ax = s.plot_correlations(spearman_rho, parameters=modelA.get_parameters(),
                              metrics=key_metrics[0])

fig, ax = s.plot_correlations(spearman_rho, parameters=modelA.get_parameters(),
                              metrics=key_metrics)


fig, ax = s.plot_morris_results(morris_dct, key_metrics[0], label_kind='name')

fig, ax = s.plot_morris_convergence(morris_dct_conv,
                                    parameters=modelA.get_parameters(),
                                    metric=key_metrics[0], plot_rank=True)

fig, ax = s.plot_fast_results(fast_dct, key_metrics[0])

fig, ax = s.plot_fast_results(rbd_dct, key_metrics[0])


fig, ax = s.plot_sobol_results(sobol_dct, metric=key_metrics[0], kind='STS2',
                                plot_in_diagonal='ST')





