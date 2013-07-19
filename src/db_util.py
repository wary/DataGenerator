#!/usr/bin/python

import MySQLdb
import logging

dev = {'host':'lei.local','db':'gameanalytics','user':'root','passwd':'root','port':3306}

def get_conn(conf=dev) :
    conn = MySQLdb.connect(**conf)
    return conn

def transaction(func) :
    def warp_func(*args, **kargs) :
        conn = kargs['conn']
        conn.begin()
        try :
            result = func(*args, **kargs)
            conn.commit()
            return result
        except Exception, e :
            logging.exception(e)
            conn.rollback()
    return warp_func

def execute_from_cp (func) :
    def warp_func(*args, **kargs) :
        conn = get_conn()
        try :
            return func(conn = conn, *args, **kargs)
        finally :
            conn.close()
    return warp_func

def query_with_columns (cursor, sql):
    cursor.execute(sql)
    columns = cursor.description
    for value in cursor.fetchall() :
        value_map = {}
        for index, item in enumerate(value) :
            value_map[columns[index][0]] = item
        yield value_map
        
    

if __name__ == '__main__' :
    conn = get_conn()
    cursor = conn.cursor()
    sql = '''
        select a.productKey, a.platform, deviceForm, server, channel from SysAppInfo a 
        join SysAppServer b ON a.productKey = b.productKey and a.platform = b.platform
        join SysAppChannel c on a.productKey = c.productKey and a.platform = c.platform
    '''
    for item in query_with_columns(cursor, sql) :
        print item