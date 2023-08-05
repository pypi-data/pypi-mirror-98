#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : 内存管理
# @Time         : 2021/3/10 6:11 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from memory_profiler import profile


@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

from meutils.pipe import *



@profile
def df_func():
    df = pd.DataFrame(np.random.random((10000, 10000)))

    dfs = np.array_split(df, 20).__iter__()

    # for df in dfs.__iter__():
    for df_ in dfs:
        vecs = [[12345] * 768] * len(df_)

        df_['vector'] = vecs



#
# Line #    Mem usage    Increment  Occurences   Line Contents
# ============================================================
# 25    104.9 MiB    104.9 MiB           1   @profile
# 26                                         def df_func():
# 27    868.1 MiB    763.1 MiB           1       df = pd.DataFrame(np.random.random((10000, 10000)))
# 28
# 29   1634.6 MiB    766.5 MiB           1       dfs = np.array_split(df, 20)
# 30
# 31                                             # for df in dfs.__iter__():
# 32    877.8 MiB   -764.5 MiB          21       for df in dfs:
# 33    877.4 MiB      0.0 MiB          20           vecs = [[12345] * 768] * len(df)
# 34
# 35    877.8 MiB      7.7 MiB          20           df['vector'] = vecs

if __name__ == '__main__':

    df_func()
