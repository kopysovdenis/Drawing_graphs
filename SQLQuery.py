import cx_Oracle
import pandas as pd

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

    def getQuerySql_count(self):
        try:
            tns = cx_Oracle.makedsn(host, port, SID)
            connect = cx_Oracle.connect(UserName, pswd, tns)
            cur = connect.cursor()
            cur.execute("""
            WITH dt
                 AS (SELECT to_char(beg_date + NUMTODSINTERVAL (LEVEL, 'minute'), 'DD-MM-YYYY HH24:mi') tme
                           FROM (SELECT TO_DATE ('26-06-2017 16:10', 'dd.mm.yyyy HH24:mi') beg_date,
                                        TO_DATE ('26-06-2017 22:10', 'dd.mm.yyyy HH24:mi') end_date
                                   FROM DUAL)
                     CONNECT BY LEVEL <= (end_date - beg_date) * 24 * 60),
                 n
                 AS (  SELECT TO_CHAR (h.statedate, 'DD-MM-YYYY HH24:mi') tme,
                              COUNT (*) cnt,
                              h.statuscode
                         FROM salaryreestrenrol e, salaryreestrenrolstatehistory h
                        WHERE     e.createdate >= TO_DATE ('26.06.2017', 'dd.mm.yyyy')
                              --AND e.delivchannelcode = 'BCO'
                              AND e.reestrid = h.reestrid
                              AND h.statuscode = 'NEW'
                     GROUP BY TO_CHAR (h.statedate, 'DD-MM-YYYY HH24:mi'), h.statuscode
                     ORDER BY 1),
                 ch
                 AS (  SELECT TO_CHAR (h.statedate, 'DD-MM-YYYY HH24:mi') tme,
                              COUNT (*) cnt,
                              h.statuscode
                         FROM salaryreestrenrol e, salaryreestrenrolstatehistory h
                        WHERE     e.createdate >= TO_DATE ('26.06.2017', 'dd.mm.yyyy')
                              --AND e.delivchannelcode = 'BCO'
                              AND e.reestrid = h.reestrid
                              AND h.statuscode = 'CHECK'
                     GROUP BY TO_CHAR (h.statedate, 'DD-MM-YYYY HH24:mi'), h.statuscode
                     ORDER BY 1),
                 enr
                 AS (  SELECT TO_CHAR (h.statedate, 'DD-MM-YYYY HH24:mi') tme,
                              COUNT (*) cnt,
                              h.statuscode
                         FROM salaryreestrenrol e, salaryreestrenrolstatehistory h
                        WHERE     e.createdate >= TO_DATE ('26.06.2017', 'dd.mm.yyyy')
                              --AND e.delivchannelcode = 'BCO'
                              AND e.reestrid = h.reestrid
                              AND h.statuscode = 'ENROLLMENT'
                     GROUP BY TO_CHAR (h.statedate, 'DD-MM-YYYY HH24:mi'), h.statuscode
                     ORDER BY 1),
                 enrd
                 AS (  SELECT TO_CHAR (h.statedate, 'DD-MM-YYYY HH24:mi') tme,
                              COUNT (*) cnt,
                              h.statuscode
                         FROM salaryreestrenrol e, salaryreestrenrolstatehistory h
                        WHERE     e.createdate >= TO_DATE ('26.06.2017', 'dd.mm.yyyy')
                              --AND e.delivchannelcode = 'BCO'
                              AND e.reestrid = h.reestrid
                              AND h.statuscode = 'ENROLLED'
                     GROUP BY TO_CHAR (h.statedate, 'DD-MM-YYYY HH24:mi'), h.statuscode
                     ORDER BY 1)
            SELECT dt.tme,
                   NVL(n.cnt, 0) n,
                   NVL(ch.cnt, 0) ch,
                   NVL(enr.cnt, 0) enr,
                   NVL(enrd.cnt,0) enrd
              FROM dt
                   LEFT JOIN n ON dt.tme = n.tme
                   LEFT JOIN ch ON dt.tme = ch.tme
                   LEFT JOIN enr ON dt.tme = enr.tme
                   LEFT JOIN enrd ON dt.tme = enrd.tme
            order by 1
            """)
            mast = list(cur)
            print(mast)
            cur.close()
            connect.close()
            return mast
        except Exception as e:
            return e
    def getQuerySql_time(self):
        try:
            tns = cx_Oracle.makedsn(host, port, SID)
            connect = cx_Oracle.connect(UserName, pswd, tns)
            cur = connect.cursor()
            cur.execute("""
                WITH dt
                     AS (    SELECT TO_CHAR (beg_date + NUMTODSINTERVAL (LEVEL, 'minute'),
                                             'DD-MM-YYYY HH24:mi')
                                       tme
                               FROM (SELECT TO_DATE ('04-09-2017 11:30', 'dd.mm.yyyy HH24:mi')
                                               beg_date,
                                            TO_DATE ('04-09-2017 17:30', 'dd.mm.yyyy HH24:mi')
                                               end_date
                                       FROM DUAL)
                         CONNECT BY LEVEL <= (end_date - beg_date) * 24 * 60),
                     rst
                     AS (SELECT h1.statedate AS ReestrTime,
                                (    EXTRACT (
                                        DAY FROM (  h2.statedate
                                                  - CAST (h1.statedate AS TIMESTAMP)))
                                   * 24
                                   * 60
                                   * 60
                                 +   EXTRACT (
                                        HOUR FROM (  h2.statedate
                                                   - CAST (h1.statedate AS TIMESTAMP)))
                                   * 60
                                   * 60
                                 +   EXTRACT (
                                        MINUTE FROM (  h2.statedate
                                                     - CAST (h1.statedate AS TIMESTAMP)))
                                   * 60
                                 + EXTRACT (
                                      SECOND FROM (  h2.statedate
                                                   - CAST (h1.statedate AS TIMESTAMP))))
                                   AS sd
                           FROM salaryreestrenrolstatehistory h1,
                                salaryreestrenrolstatehistory h2
                          WHERE     h1.reestrid = h2.reestrid
                                AND LOWER (h1.statuscode) = 'new'
                                AND LOWER (h2.statuscode) = 'enrolled'
                                --AND h.statuscode = 'ENROLLEDPARTIALLY'
                                AND h1.statedate BETWEEN TO_DATE ('04-09-2017 11:30',
                                                                  'dd.mm.yyyy HH24:mi')
                                                     AND TO_DATE ('04-09-2017 17:30',
                                                                  'dd.mm.yyyy HH24:mi')),
                     grp
                     AS (  SELECT TO_CHAR (ReestrTime, 'DD-MM-YYYY HH24:mi') AS tme,
                                  ROUND (AVG (sd), 0) AS AVG_SD,
                                  ROUND (MAX (sd), 0) AS MAX_SD,
                                  ROUND (MIN (sd), 0) AS MIN_SD,
                                  ROUND (MEDIAN (sd), 0) AS MEDIAN_SD,
                                  ROUND (PERCENTILE_CONT (0.9) WITHIN GROUP (ORDER BY sd ASC),
                                         0)
                                     AS PERCENTILE_SD
                             FROM rst
                         GROUP BY TO_CHAR (ReestrTime, 'DD-MM-YYYY HH24:mi'))
                  SELECT dt.tme,
                         grp.AVG_SD AVG_SD,
                         grp.MAX_SD MAX_SD,
                         grp.MIN_SD MIN_SD,
                         grp.MEDIAN_SD MEDIAN_SD,
                         grp.PERCENTILE_SD PERCENTILE_SD
                    FROM dt LEFT JOIN grp ON dt.tme = grp.tme
                ORDER BY 1
                """)
            mast = list(cur)
            print(mast)
            cur.close()
            connect.close()
            return mast
        except Exception as e:
            return e

    def getUTL(self,filess):
        VarCh1 = pd.read_csv(filess, sep=';', header=None,
                             names=['Time', 'New', 'Check', 'Enroll', 'Enrolled', 'NewALL', 'CheckALL', 'EnrollALL',
                                    'wqrw'])
        return VarCh1