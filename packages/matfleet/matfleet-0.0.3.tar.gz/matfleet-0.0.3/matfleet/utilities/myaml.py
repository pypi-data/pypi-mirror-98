#   coding:utf-8
#   This file is part of Alkemiems.
#
#   Alkemiems is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = '2021/01/14 17:46:39'

import yaml


def read_yaml_from_fn(ffn):
    with open(ffn, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f.read())


