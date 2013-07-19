DataGenerator
=============

DataGenerator

做前端开发时,用来伪造数据库数据的小工具

配置

BuyItem: 
  -
    - refer #从sql获取数据
    - name: productKey,platform,deviceForm,server,channel  #列名,号隔开
      sql: select a.productKey, a.platform, deviceForm, server, channel from SysAppInfo a 
        join SysAppServer b ON a.productKey = b.productKey and a.platform = b.platform
        join SysAppChannel c on a.productKey = c.productKey and a.platform = c.platform where a.productKey = '5a105e8b9d40e1329780d62ea2265d8a'
  -
    - range #范围数据
    - name: staType  #列名
      start: 1 #开始
      end: 3 #结束
  - 
    - date #日期范围
    - name: logDay #列名字
      start: !!str 2013-06-01 #开始日期
      end: !!str 2013-08-01 #结束日期
  - 
    - custom #自定义
    - name: buyAmount #列名
      expression: FLOOR(3000 + RAND() * 1000) #表达式
  - 
    - custom
    - name: buyGameMoney
      expression: FLOOR(3000 + RAND() * 1000)
  -
    - custom
    - name: useAmount
      expression: FLOOR(3000 + RAND() * 1000)
  - 
    - range
    - name: items
      start: 1
      end: 11
      prefix: item #前缀