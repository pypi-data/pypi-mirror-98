#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : tf_io
# @Time         : 2021/2/26 4:19 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://www.jianshu.com/p/c2fabc8a6dad
"""
tf 不支持Path
Path('hdfs://')会丢失一个/
"""

import tensorflow as tf
from meutils.pipe import *
from meutils.path_utils import get_module_path

HDFS = 'hdfs://zjyprc-hadoop'
DATA = get_module_path("../data", __file__)
_SUCCESS = f"{DATA}/_SUCCESS"


def _process_success(output_dir):
    if output_dir.startswith('hdfs:') and tf.io.gfile.isdir(output_dir):
        tf.io.gfile.copy(_SUCCESS, output_dir, True)


def _process_hdfs_path(p):
    if p.startswith('/user/'):
        p = HDFS + p
    return p


def _process_pattern(pattern):
    pattern = _process_hdfs_path(pattern)

    if tf.io.gfile.isdir(pattern):  # 如果是个文件夹，默认匹配所有文件
        pattern += '/*'
    return pattern


def if_not_exist_makdir(path):
    if not tf.io.gfile.exists(path):
        logger.warning(f"{path} does not exist")
        tf.io.gfile.makedirs(path)


def rm(path):
    path = _process_hdfs_path(path)

    if tf.io.gfile.isdir(path):
        tf.io.gfile.rmtree(path)
    elif tf.io.gfile.exists(path):  # 文件夹也返回 True
        tf.io.gfile.remove(path)


def cp(pattern, output_dir=DATA):
    """复制文件夹下的文件到新文件夹"""
    pattern = _process_pattern(pattern)
    output_dir = _process_hdfs_path(output_dir)

    if_not_exist_makdir(output_dir)

    files = tf.io.gfile.glob(pattern)

    logger.info("FILES:\n {}".format('\t' + '\n\t'.join(files)))

    new_files = []
    for file in files:
        new_file = f"{output_dir}/{Path(file).name}"
        tf.io.gfile.copy(file, new_file, True)

        new_files.append(new_file)

    return new_files


def df2write(df, file, num_partitions=1, sep='\t', index=False, header=False, **kwargs):
    """仅支持单文件，支持多线程写入
    写的时候不支持多个字符分割："delimiter" must be a 1-character string: 非逗号分割的提前合并
    """
    file = _process_hdfs_path(file)
    name = Path(file).name  # dir = file[::-1].split('/', 1)[1][::-1]
    dir = Path(file).parent.__str__().replace('hdfs:/', 'hdfs://')

    if_not_exist_makdir(str(dir))

    if num_partitions == 1:
        with tf.io.gfile.GFile(file, 'w') as f:
            df.to_csv(f, index=index, header=header, sep=sep, **kwargs)
    else:

        logger.info(f"MutiThreadWriter: part__*__{name}")

        def writer(args):
            idx, df = args
            file = f"{dir}/part__{idx}__{name}"

            with tf.io.gfile.GFile(file, 'w') as f:
                df.to_csv(f, index=index, header=header, sep=sep, **kwargs)

        enumerate(np.array_split(df, num_partitions)) | xThreadPoolExecutor(writer, num_partitions)


def read2df(file, **kwargs):
    """仅支持单文件
    sep: 本地文件支持多字符作为分隔符，HDFS文件好像不支持
    pd.read_csv(p, iterator=True, chunksize=10000)
    """
    file = _process_hdfs_path(file)

    with tf.io.gfile.GFile(file, 'r') as f:  # todo: 中文异常
        return pd.read_csv(f, **kwargs)


def read2dataset(pattern, fmt='TextLineDataset'):
    """支持多文件大数据

    :param pattern:
    :param format: 'TextLineDataset', 'TFRecordDataset'
    :return:
        df = pd.DataFrame(map(bytes.decode, ds.as_numpy_iterator()))
        df = pd.DataFrame(map(lambda r: r.decode().split('____'), ds.as_numpy_iterator()), columns=['itemid', 'title'])
        for i in ds:
            i.numpy().decode().split('\t')

        ds = tf_io.read2dataset('title.csv')
        num_part = 3
        batch_size = 4
        for n in range(num_part):
            print(n)
            for i in itertools.islice(ds, batch_size*n, batch_size*(n+1)):
                i.numpy().decode().split('____')
    """
    pattern = _process_pattern(pattern)

    try:
        fs = tf.io.gfile.glob(pattern)
    except Exception as e:
        logger.error(e)
        fs = tf.data.Dataset.list_files(file_pattern=pattern)
        fs = [f.decode() for f in fs.as_numpy_iterator()]

    logger.info("FILES: " + '\t' + '\n\t'.join(fs))

    ds = tf.data.__getattribute__(fmt)(fs)
    return ds
