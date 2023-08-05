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
from meutils.pd_utils import df_split



@profile
def df_func():
    df = pd.DataFrame(np.random.random((10000, 10000)))

    for df_ in df_split(df, 20):
        vecs = [[12345] * 100] * len(df_)

        df_['vector'] = vecs

    del df
    # return


"""
del 有用
函数结尾相当于操作gc.collect()
"""
if __name__ == '__main__':
    df_func()
