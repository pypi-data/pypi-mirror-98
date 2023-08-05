#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : image2vec
# @Time         : 2020/12/30 2:47 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://github.com/milvus-io/bootcamp/blob/db5dfd63dc052ca15bdf28e7c6b7a8d510dd15f6/solutions/pic_search/webserver/src/preprocessor/vggnet.py#L19


class Image2vec(object):
    pass



import numpy as np
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg
from keras.preprocessing import image
from numpy import linalg as LA
# from common.const import input_shape

class VGGNet:
    def __init__(self):
        self.input_shape = (224, 224, 3)
        self.weight = 'imagenet'
        self.pooling = 'max'
        self.model_vgg = VGG16(weights=self.weight,
                               input_shape=(self.input_shape[0], self.input_shape[1], self.input_shape[2]),
                               pooling=self.pooling,
                               include_top=False)
        self.model_vgg.predict(np.zeros((1, 224, 224, 3)))

    def vgg_extract_feat(self, img_path):
        img = image.load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input_vgg(img)
        feat = self.model_vgg.predict(img)
        norm_feat = feat[0] / LA.norm(feat[0])
        norm_feat = [i.item() for i in norm_feat]
        return norm_feat
