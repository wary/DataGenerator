#!/usr/bin/python
#!coding=utf-8

'''
Created on 2013-7-17

@author: lei
'''
import logging
import sys

FORMAT = '%(asctime)-15s-%(levelname)s-%(filename)s-%(message)s'
logging.basicConfig(format=FORMAT,stream=sys.stdout,level=logging.INFO)

def getLogger(name):
    return logging.getLogger(name)