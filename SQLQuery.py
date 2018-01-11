import cx_Oracle
import pandas as pd
import numpy as np
import re
import Config

host = '192.168.50.24'
port = 1521
SID = 'bs'
UserName = 'pflb'
pswd = '123321'

class sqlQuery():
    def __init__(self):
        pass

    def functions(self, inquery):
        try:
            tns = cx_Oracle.makedsn(host, port, SID)
            connect = cx_Oracle.connect(UserName, pswd, tns)
            cur = connect.cursor()
            cur.execute(inquery)
            outExt = list(cur)
            print(outExt)
            cur.close()
            connect.close()
            return outExt
        except Exception as e:
            return e

    def ClearOrDB(self, days):
        try:
            if int(days) > 0:
                try:
                    tns = cx_Oracle.makedsn(host, port, SID)
                    connect = cx_Oracle.connect(UserName, pswd, tns)
                    cur = connect.cursor()
                    cur.execute(Config.sql.format(days= days))
                    outText = list(cur)
                    cur.close()
                    connect.close()
                    return outText
                except Exception as e:
                    return e
            else:
                return 'Вы ввели не коррктное число'
        except Exception as e:
            return e

    def StatisticTable(self):
        try:
            tns = cx_Oracle.makedsn(host, port, SID)
            connect = cx_Oracle.connect(UserName, pswd, tns)
            cur = connect.cursor()
            cur.execute(Config.StatisticTable)
            mast = list(cur)
            print(mast)
            cur.close()
            connect.close()
            return mast
        except Exception as e:
            return e

#    def SqlAlchimQuery(self):
#        valuse = []
#        engine = create_engine('oracle://'+UserName+':'+pswd+'@'+host+':'+str(port)+'/'+SID)
#        sql = text('select * from zagruzka')
#       result = engine.engine.execute(sql)
#        for row in result:
#            valuse.append(row)
#        return valuse

    def getQuerySql_count(self):
        try:
            """
            Переменные для SQL запроса
            """
            start = '26-06-2017 16:10'
            stop = '26-06-2017 22:10'
            data = '26.06.2017'
            tns = cx_Oracle.makedsn(host, port, SID)
            connect = cx_Oracle.connect(UserName, pswd, tns)
            cur = connect.cursor()
            cur.execute(Config.getQuerySql_count.format(start = start, stop = stop, data = data))
            mast = list(cur)
            print(mast)
            cur.close()
            connect.close()
            return mast
        except Exception as e:
            return e

    def get_Count_Reestrs_Cards(self):
        try:
            """
            Переменные для SQL запроса
            """
            beg_date = '03-10-2017 13:20'
            end_date = '03-10-2017 19:20'
            data = '03.10.2017'
            tns = cx_Oracle.makedsn(host, port, SID)
            connect = cx_Oracle.connect(UserName, pswd, tns)
            cur = connect.cursor()
            cur.execute(Config.Count_Reestrs_Cards.format(beg_date = beg_date, end_date = end_date, data = data))
            mast = list(cur)
            print(mast)
            cur.close()
            connect.close()
            return mast
        except Exception as e:
            return e

    def get_Time_Reestrs_Cards(self):
        try:
            """
            Переменные для SQL запроса
            """
            beg_date = '03-10-2017 13:20'
            end_date = '03-10-2017 19:20'
            tns = cx_Oracle.makedsn(host, port, SID)
            connect = cx_Oracle.connect(UserName, pswd, tns)
            cur = connect.cursor()
            cur.execute(Config.Time_Reestrs_Cards.format(beg_date = beg_date, end_date = end_date))
            mast = list(cur)
            print(mast)
            cur.close()
            connect.close()
            return mast
        except Exception as e:
            return e


    def getQuerySql_time(self):
        try:
            """
            Переменные для SQL запроса
            """
            beg_date = '04-09-2017 11:30'
            end_date = '04-09-2017 17:30'
            tns = cx_Oracle.makedsn(host, port, SID)
            connect = cx_Oracle.connect(UserName, pswd, tns)
            cur = connect.cursor()
            cur.execute(Config.getQuerySql_time.format(beg_date = beg_date, end_date = end_date))
            mast = list(cur)
            print(mast)
            cur.close()
            connect.close()
            return mast
        except Exception as e:
            return e

    def getUTL(self,filess):
        VarCh1 = pd.read_csv(filess, sep=';', header=None,
                             names=['Time', 'New', 'Check', 'Enroll', 'Enrolled'])
        return VarCh1

    def getEnrolled10(self,filess):
        VarCh1 = pd.read_csv(filess, sep=';', header=None,
                             names=['Time', 'New', 'Check', 'Enroll', 'Enrolled'])
        count = 0
        envereds10 = []
        envereds11 = []
        VarCh2 = np.array(VarCh1['Enrolled'])


        for x in VarCh2:
            envereds10.append(VarCh2[count:count + 10].sum())
            count += 1

        for x in envereds10:
            envereds11.append(int(x)*6)
        return envereds11

    def get_delivered_load_per_10minute(self,delivered_load_per_minute):
        count = 0
        envereds10 = []
        delse = []
        VarCh2 = np.array(delivered_load_per_minute)

        for x in VarCh2:
            envereds10.append(VarCh2[count:count + 10].sum())
            count += 1

        for x in envereds10:
            delse.append(int(x) * 6)
        return delse

    def getSummAllElements(self, liseted):
        listy = []
        listy1 = []
        c = 0.0
        for m in liseted:
            m = str(m).replace(',', '.')
            listy1.append(m)
        for x in listy1:
            c = c + float(x)
            listy.append(c)
        return listy

    def dataProcessing(self, DataValues):
        try:
            b = re.compile(r"[0-9]+:[0-9]+\s.*?\s(.*?)\s")
            Passe = re.findall(b, DataValues)
            far = np.array(Passe)
            fat = []
            fat1 = []
            for x in far:
                if len(x) <= 1:
                    x = x+'.0'
                    fat.append(x)
                x = str(x).replace(',','.')
                fat.append(x)
            fats = np.array(fat, dtype=float)
            for x in fats:
                fat1.append(x*3600)
            return fat1
        except Exception as e:
            return  e


    def getCard(self, filles):
        Val1 = pd.read_csv(filles, sep=';', header=None,
                           names=['AVG_SD', 'MAX_SD', 'MIN_SD', 'MEDIAN_SD', 'PERCENTILE_SD'], index_col=0, na_filter = False)
        return Val1

    def getPerformance(self, filles):
        Val1 = pd.read_csv(filles, sep=';', header=None,
                           names=['DATAOK','Processed'], index_col=0, na_filter = False)
        return Val1
