#!/usr/bin/python
#!coding=utf-8

from datetime import datetime, timedelta
import db_util as db
import log_conf
import common_util as util
import re

__logger = log_conf.getLogger("data_util")
__holder = re.compile(r'(,?%s\s*)+')

@db.execute_from_cp
def generate_data_with_refer(conn,name,sql) :
	cursor = conn.cursor()
	values_keys = name.strip().split(',')
	result_keys = []
	values = []
	for item in  db.query_with_columns(cursor, sql) :
		row = []
		for k,v in item.items() :
			if k in values_keys :
				if k not in result_keys :
					result_keys.append(k)
				row.append(v)
		if len(result_keys) != len(values_keys) :
			raise Exception, "can't find value for keys : %s " % str([ key for key in values_keys if key not in  result_keys ])
		values.append(",".join(row))
	return ",".join(result_keys), values

def generate_data_with_range(name, end, start = 0, prefix = '') :
	values = []
	for value in range(start, end + 1) :
		values.append(prefix and prefix+str(value) or value)
	return name, values

def generate_data_with_items (name, items) :
	return name, items

def generate_data_with_date_range(name, start, end) :
	items = []
	start_time = datetime.strptime(start, "%Y-%m-%d")
	end_time = datetime.strptime(end, "%Y-%m-%d")
	interval = timedelta(1)
	while start_time <= end_time :
		items.append(start_time.strftime("%Y-%m-%d"))
		start_time += interval
	return name, items

def generate_data_with_custom(name, expression) :
	return name, expression

__type_map = {
	'refer'  : generate_data_with_refer,
	'range'  : generate_data_with_range,
	'items'   : generate_data_with_items,
	'date'   : generate_data_with_date_range,
	'custom' : generate_data_with_custom
}

def parse_meta(meta) :
	items_names = []
	items_holders = []
	value_items = []
	custom_names = []
	custom_hloders = []
	for k, v in meta :
		if k in __type_map :
			name, values = __type_map[k](**v)
			if not values :
				raise Exception, "empty value please check the conf of column: %s" % name
			name_seq = name.split(',')
			if type(values) is list :
				items_names.append(name)
				items_holders.extend(['%s'] * len(name_seq))
				value_items.append(values)
			else :
				custom_names.append(name)
				custom_hloders.append(values)
	items_names.extend(custom_names)
	items_holders.extend(custom_hloders)
	return items_names, items_holders, value_items
	
def generate_exexute_sql(table, meta) :
	sql_template = """insert into %s (%s) values """
	items_names, items_holders, value_items = parse_meta(meta)
	sql = sql_template % (table, ",".join(items_names)) + "".join(("(",",".join(items_holders),")"))
	
	def fill_values(row_values = "", index = 0) :
		if index < len(value_items) :
			for value_item in value_items[index] :
				result = row_values + str(value_item) + ","
				if index == (len(value_items) - 1) :
					yield result
				else :
					for result_item in fill_values(result, index + 1) :
						yield result_item
						
	result_set = []
	for result in fill_values() :
		result_set.append([param for param in result.split(',') if param])
		if len(result_set) == 1000 :
			yield sql, result_set
			result_set = []
	yield sql, result_set
	
@db.execute_from_cp
@db.transaction
@util.record_time
def generate_data(table, meta, conn = None) :
	cursor = conn.cursor()
	count_sum = 0
	for sql, value_brunch in generate_exexute_sql('BuyItem',meta) :
		execute_sql_many(cursor, sql, value_brunch)
		count = len(value_brunch)
		count_sum += count
		__logger.info("insert %d records with sql: %s " % (count, sql))
	__logger.info("generate data completed for table %s with %d records" % (table, count_sum))

def execute_sql_one(cursor, sql, value_brunch) :
	for item in value_brunch :
			cursor.execute(sql,item)

def execute_sql_many(cursor, sql, value_brunch) :
	sql_parts = sql.split('values')
	value_list =[__holder.sub(row,sql_parts[1]) for row in [str(row_list).strip(('[]'))for row_list in value_brunch]]
	sql = "%s values %s" % (sql_parts[0],",".join(value_list))
	__logger.debug("execute sql : %s " % sql)
	cursor.execute(sql)
		
	

if __name__ == '__main__' :
	meta = [
		('refer',{
			'name':'productKey,platform,deviceForm,server,channel',
			'sql':'''
			select a.productKey, a.platform, deviceForm, server, channel from SysAppInfo a 
			join SysAppServer b ON a.productKey = b.productKey and a.platform = b.platform
			join SysAppChannel c on a.productKey = c.productKey and a.platform = c.platform where a.productKey = '5a105e8b9d40e1329780d62ea2265d8a'
			'''
		}),
		('range', {
			'name':'staType',
			'start':1,
			'end':3
		}),
		('range', {
			'name':'level',
			'start':1,
			'end':11
		}),
		('items',{
			'name':'items',
			'items':['item %d' % item for item in range(10)]
		}),
		('date',{
			'name':'logDay',
			'start':'2013-06-01',
			'end':'2013-08-01'
		}),
		('custom',{
			'name':'buyAmount',
			'expression' : 'FLOOR(3000 + RAND() * 1000)'
		}),
		('custom',{
			'name':'buyGameMoney',
			'expression' : 'FLOOR(3000 + RAND() * 1000)'
		}),
		('custom',{
			'name':'useAmount',
			'expression' : 'FLOOR(3000 + RAND() * 1000)'
		})
	]
	
	generate_data("BuyItem", meta)


	
