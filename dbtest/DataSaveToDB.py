#!/usr/bin/python
#-*-coding:utf-8-*-
import MySQLdb
from __builtin__ import list
import sys
reload(sys)
sys.setdefaultencoding('utf8')



class DataSave(object):
    def __init__(self):
#         self.initDB()
        pass
    #初始化数据库
    def initDB(self):
        self.conn= MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='111111',
        db ='oudb'
        )
        self.conn.set_character_set('utf8')
        self.conncur = self.conn.cursor()
        
    #向数据库插入数据,判断是字典还是元组的集合
    def insertData(self,data):
        print "开始插入数据库"
        #插入一条数据
        sqli="insert into oneapp_ask_db values(%s,%s,%s,%s)"
        if type(data)==dict:
            array2=(data["pageindex"],data["title"],data["ask_info"],data["content"])
            self.conncur.execute(sqli,array2)
        if type(data)==list:
            for k in data:
                array2=(k["pageindex"],k["title"],k["ask_info"],k["content"])
                self.conncur.execute(sqli,array2)
        print "数据插入完毕"
        
        
    #查看数据库所有数据
    def querryAllData(self):
        #获得表中有多少条数据
        aa=self.conncur.execute("select * from oneapp_ask_db")
        #打印表中的多少数据
        info = self.conncur.fetchmany(aa)
        for ii in info:
            print str(ii).decode('string_escape')#对输出函数decode，显示中文
            
    #数据库删除数据
    def deleteData(self):
        sql = "delete from oneapp_ask_db where 条件"
        self.conncur.execute(sql)

    #关闭数据库连接
    def closedDB(self):
        self.conncur.close()
        self.conn.commit()
        self.conn.close()  