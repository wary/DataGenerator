#!/usr/bin/python
#!coding=utf-8

import data_util
import conf_util

'''
Created on 2013-7-18

@author: lei
'''

if __name__ == '__main__':
    conf = conf_util.read_conf("../conf/BuyItem.yaml")
    for k, v in conf.items() :
        data_util.generate_data(k, v)