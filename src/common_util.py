#!/usr/bin/python
#!coding=utf-8

'''
Created on 2013-7-17

@author: lei
'''
import time

def record_time(func) :
    import log_conf
    log = log_conf.getLogger("time_record")
    def warp_func(*args,**kargs) :
        start_time = time.time()
        func(*args, **kargs)
        cost_time  = time.time() - start_time
        log.info("%s spend time : %d (s)" % (func.__name__, cost_time))
                 
    return warp_func
        