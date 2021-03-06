#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctypes import cdll, c_char, c_char_p, cast, POINTER
import os.path
import platform

# path = os.path.dirname(os.path.realpath(__file__)) #设置so文件的位置
class SoExtention:
    def __init__(self, model_path, user_dict_path, t2s, just_seg):
        root = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) #设置so文件的位置
        # if(platform.system() == "Darwin"):
        #     self._lib = cdll.LoadLibrary(root+'/macos_lib.so') #读取so文件
        # elif(platform.system() == "Linux"):
        #     self._lib = cdll.LoadLibrary(root+'/linux_lib.so') #读取so文件
        # else:
        #     print("没有合适当前系统的.so文件，请使用普通分词方法")
        self._lib = cdll.LoadLibrary(root+'/libthulac.so') #读取so文件
        self._lib.init(c_char_p(model_path), c_char_p(user_dict_path), int(t2s), int(just_seg)) #调用接口进行初始化

    def clear(self):
        if self._lib != None: self._lib.deinit()

    def seg(self, data):
        r = self._lib.seg(c_char_p(data))
        assert r > 0
        self._lib.getResult.restype = POINTER(c_char)
        p = self._lib.getResult()
        s = cast(p,c_char_p)
        d = '%s'%s.value
        self._lib.freeResult();
        return d