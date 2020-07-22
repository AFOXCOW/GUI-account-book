import sqlite3
import os 
import pandas as pd
import numpy as np 

class DataBase:
    def __init__(self,dbname):
        self.dbname = dbname
        self.__connect()
        self.__init_tablename()

    def __del__(self):
        print("Closing Database......")
        self.__close()
        print("Database Closed!")

    def __connect(self):
        if not os.path.exists(self.dbname):
            print("Database not exists, creating a new database now!")
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def __close(self):
        self.cur.close()
        self.conn.close()

    def create_table(self,tablename):
        sql = '''CREATE TABLE %s
               (BeiJing_Time DATE                 NOT NULL,
               COMMENT       TEXT                 NOT NULL,
               Money_float   REAL                 NOT NULL);''' % tablename
        self.cur.execute(sql)
        self.conn.commit()

    def execute_sql(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def search_by_time(self, time_string):
        time_string = self.Time_Format(time_string)
        error = True
        result = []
        if time_string!='error':
            sql = "select * from %s where BeiJing_Time = '%s'" % (self.tablename,time_string)
            result = self.execute_sql(sql)
            return result,not error
        else:
            return result,error

    def delete_by_time(self, time_string):
        time_string = self.Time_Format(time_string)
        if time_string!='error':
            sql = "delete from %s where BeiJing_Time='%s'"%(self.tablename,Time)
            self.execute_sql(sql)
            self.msg = "Delete Entry Accomplished"

    def export_table_to_excel(self,tablename=None):
        if tablename==None:
            tablename = self.tablename
        self.sql = "select * from %s" % tablename
        self.db_df = pd.read_sql_query(self.sql,self.conn)
        self.db_df.to_excel(str(self.dbname.split('.')[0])+'_'+str(tablename)+'.xlsx',index=False)

    def __init_tablename(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        tablenames = self.execute_sql(sql)
        self.tablename = tablenames[0]

    def set_default_table(self,tablename):
        self.tablename = tablename

    def insert(self,string,tablename=None):
        # string format:2020-06-06 some_comment 200
        if tablename==None:
            tablename = self.tablename
        BeiJing_Time = string.split(' ')[0]
        COMMENT = string.split(' ')[1]
        Money = string.split(' ')[2]
        if BeiJing_Time=='' or COMMENT=='' or Money=='':
            self.msg = "No enough insert data!"
        else:
            BeiJing_Time = self.Time_Format(BeiJing_Time)
            COMMENT = COMMENT.replace('_',' ')
            Money_float = float(Money)
            sql = "insert into %s values ('%s','%s',%f)" % (tablename,BeiJing_Time,COMMENT,Money_float)
            self.cur.execute(sql)
            self.conn.commit()
            self.msg = "Insert Entry Accomplished"

    def import_from_excel(self,excel_path):
        df = pd.read_excel(excel_path)
        nparr = df.values
        for row in nparr:
            time = str(row[0]).split(' ')[0] 
            time = time.replace(' ','_') #change space to _
            row[1] = row[1].replace(' ','_')
            string = time + ' ' + row[1] + ' ' + str(row[2])
            self.insert(string)
    def Time_Format(self, time_string):
        # time_string may be 2020-6-1 or 2020-06-01 or a combination of both.
        # this function convert different format to 2020-06-01 format
        year = int(time_string.split('-')[0])
        month = int(time_string.split('-')[1])
        day = int(time_string.split('-')[2])
        if month<1 or day<1 :
            self.msg = "Wrong date!"
            return 'error'
        elif year<1000:
            self.msg = "Year must greater than 1000!"
            return 'error'
        if month<10:
            str_month = '0'+str(month)
        else:
            str_month = str(month)
        if day<10:
            str_day = '0'+str(day)
        else:
            str_day = str(day)
        str_year = str(year)
        return str_year+'-'+str_month+'-'+str_day
