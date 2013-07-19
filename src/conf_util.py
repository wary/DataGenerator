#!/usr/bin/python
#!coding=utf-8

'''
Created on 2013-7-18

@author: lei
'''
import yaml

def read_conf(conf) :
    f = open(conf)
    x = yaml.load(f)
    return x

if __name__ == '__main__' :
    read_conf('../conf/BuyItem.yaml')
    