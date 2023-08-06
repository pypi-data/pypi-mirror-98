#   coding:utf-8
#   This file is part of Alkemiems.
#
#   Alkemiems is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = '2021/03/11 16:20:25'


def check_empty(config_dict):
    for k, v in config_dict.items():
        if not v:
            raise ValueError("Please set %s." % k)


def get_new_point_dict(config_dict: dict, needed_config: list):
    new_dict = dict()
    for i in needed_config:
        new_dict[i] = config_dict[i]
    
    return new_dict
