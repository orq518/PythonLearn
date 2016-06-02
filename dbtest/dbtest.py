#!/usr/bin/python
#-*-coding:utf-8-*-
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')


conn= MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='111111',
        db ='oudb',
        )
cur = conn.cursor()
#  
# #获得表中有多少条数据
# aa=cur.execute("select * from student")
# print aa
#  
# #打印表中的多少数据
# info = cur.fetchmany(aa)
# for ii in info:
#     print "表格数据",ii
    
    
    
#创建数据表    
#cur.execute("create table oneapp_ask_db(pageindex varchar(10) ,title varchar(100),question varchar(1000),answer varchar(10000))")
#删除数据表    
# cur.execute("DROP TABLE IF EXISTS `oneapp_ask_db`")
    
#插入一条数据
# sqli="insert into oneapp_ask_db values(%s,%s,%s,%s)"
# cur.execute(sqli,('4','外国人','摄影师盲问','我深信全世界人民的情感都是一样浓烈炽热的'))
# sqli="insert into oneapp_ask_db values(%s,%s,%s)"
# cur.execute(sqli,("insert into student values('外国人','摄影师盲问','我深信全世界人民的情感都是一样浓烈炽热的 ')"))    
# 
#获得表中有多少条数据
aa=cur.execute("select * from oneapp_ask_db")
#打印表中的多少数据
info = cur.fetchmany(aa)
for ii in info:
    print str(ii).decode('string_escape')#对输出函数decode，显示中文
cur.close()
conn.commit()
conn.close()


