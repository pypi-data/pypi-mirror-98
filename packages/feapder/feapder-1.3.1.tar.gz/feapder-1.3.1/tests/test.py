# -*- coding: utf-8 -*-
"""
Created on 2021/3/18 12:05 上午
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""


import importlib

model, class_name = "feapder.pipelines.mysql_pipeline", "MysqlPipeline"
a = importlib.import_module(model)
pipeline = a.__getattribute__(class_name)
print(pipeline)
print(pipeline().save_data())