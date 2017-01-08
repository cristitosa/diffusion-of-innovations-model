#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 10:45:16 2016

@author: carlos
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_adopters(data, par_name, par_value, axis=None, cumulative=False,
                  fontsize=15):
    """
    data contains the output of compute_run
    """
    no_rx_data = [d['adopters'] for d in data['no_rx']]
    rx_data = [d['adopters'] for d in data['rx']]

    if cumulative:
        no_rx_data = map(np.cumsum, no_rx_data)
        rx_data = map(np.cumsum, rx_data)

    if axis:
        sns.tsplot(data=no_rx_data, condition='Without Reflexivity', ax=axis)
        sns.tsplot(data=rx_data, color='m', condition='With Reflexivity',
                   ax=axis)
        axis.set_xlabel(r'$%s = %s$' % (par_name, str(par_value)),
                        fontsize=fontsize)
        axis.legend(loc='best', fontsize=fontsize-2)
        axis.tick_params(axis='both', which='major', labelsize=fontsize-2)
    else:
        sns.tsplot(data=no_rx_data, condition='Without Reflexivity')
        sns.tsplot(data=rx_data, color='m', condition='With Reflexivity')
        plt.title(r'$%s = %s$' % (par_name, str(par_value)), fontsize=fontsize)
        plt.legend(loc='best', fontsize=fontsize-2)
        plt.tick_params(axis='both', which='major', labelsize=fontsize-2)


def plot_global_utility(data, axis, critical_mass, max_time):
    """
    Plot global utility against time.

    data: contains the output of compute_run.
    """
    rx_data = [d['global_utility'] for d in data['rx']]

    axis.yaxis.grid(False)
    plt.setp(axis.get_xticklabels(), visible=False)
    plt.setp(axis.get_yticklabels(), visible=False)
    plt.setp(axis.yaxis.get_majorticklines(), visible=False)
    plt.setp(axis.yaxis.get_minorticklines(), visible=False)

    sns.tsplot(data=rx_data, color='m', ax=axis)
    plt.plot([critical_mass] * max_time, '--', linewidth=1, color='0.5')
