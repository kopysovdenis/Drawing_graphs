import cx_Oracle

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
            if days > 0:
                try:
                    tns = cx_Oracle.makedsn(host, port, SID)
                    connect = cx_Oracle.connect(UserName, pswd, tns)
                    cur = connect.cursor()
                    cur.execute("""
                    DECLARE
                    dt DATE;
                    BEGIN
                    FOR x IN
                    (SELECT table_name,
                        partition_name,
                        high_value
                    FROM user_tab_partitions
                        WHERE partition_name != 'FIRST_PARTITION'
                        )
                        LOOP
                            EXECUTE immediate 'select '||x.high_value||' from dual' INTO dt;
                            dbms_output.put_line(dt);
                                IF dt < sysdate - """ + days + """ THEN
                                    dbms_output.put_line('Droping partition '||x.partition_name||' of table '||x.table_name||' with high_value '||x.high_value);
                                    EXECUTE IMMEDIATE 'ALTER TABLE '|| x.table_name ||' DROP PARTITION ' || x.partition_name;
                                END IF;
                        END LOOP;
                    END;""")
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
            cur.execute("""select ts.name TNAME ,round(sum(allocated_space)/sum(file_maxsize)*100) PERCENT_USED
                                            from v$filespace_usage fu
                                                JOIN v$tablespace ts ON (fu.tablespace_id = ts.ts#)
                                                    GROUP BY ts.name""")
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
