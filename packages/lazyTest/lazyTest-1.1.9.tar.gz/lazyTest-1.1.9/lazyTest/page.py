# -*- coding = UTF-8 -*-
# Author   :buxiubuzhi
# File     : page.py
# project  : McenterSystem
# time     : 2020/12/3 11:56
# Describe :
# ---------------------------------------

import logging
from lazyTest import *


class Page(object):
    filePath = r"/resources/element/"

    suffix = ".yaml"

    def __init__(self, base_driver: browser_Config) -> None:
        self.base_driver = base_driver
        self.log = logging.getLogger(self.getClassName())
        self.log.info("元素文件: -> %s" % (self.getProjectPath() + self.filePath + self.getClassName() + self.suffix))
        self.selector = readElementSource(
            self.getProjectPath() + self.filePath + self.getClassName() + self.suffix).readFileToDict()

    def getProjectPath(self) -> str: ...

    @classmethod
    def getClassName(cls):
        return cls.__name__

    @classmethod
    def writeKey(cls):
        """
        自动创建yaml资源文件
        :return:
        """
        key = {}
        methods = list(
            filter(lambda m: not m.startswith("__") and not m.endswith("__") and callable(getattr(cls, m)), dir(cls)))
        methods.pop(methods.index("writeKey"))
        methods.pop(methods.index("getProjectPath"))
        methods.pop(methods.index("getClassName"))
        for i in methods:
            func = getattr(cls, i)
            doc = func.__doc__
            key[i] = doc
        writeElementKey(cls.getProjectPath(cls) + cls.filePath, cls.getClassName(), cls.suffix, key)
