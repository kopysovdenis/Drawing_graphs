import os
import re
import datetime
import londas as pd
import gzip

#----------------ПЕРЕМЕННЫЕ---------------------------------------------------------------------------------------------
from numpy import sort

FileRead = []
FileReadAll = []
FileReadAll1 = []
lable=[]
str = ''
pickle_sar = '//192.168.50.30/inotes/personal/s.danilov/pkl/{0}/sar/sar_{0}.pkl.zip'
pickle_saru = '//192.168.50.30/inotes/personal/s.danilov/pkl/{0}/sar/saru_{0}.pkl.zip'
#pickle_nmon_dbu = '//192.168.50.30/inotes/personal/s.danilov/pkl/{0}/nmon/nmon_dbu_{0}.pkl.zip'
#pickle_nmon_app = '//192.168.50.30/inotes/personal/s.danilov/pkl/{0}/nmon/nmon_app_{0}.pkl.zip'
#pickle_nmon_appu = '//192.168.50.30/inotes/personal/s.danilov/pkl/{0}/nmon/nmon_appu_{0}.pkl.zip'
#-----------------------------------------------------------------------------------------------------------------------
def to_groups(fileArr):
    servers = []
    for fn in fileArr:
        srv = re.split('(?<=app\d\d).', fn)[0]
        if srv not in servers:
            servers.append(srv)
    return [list(sort(filter(lambda x: x.startswith(srv), fileArr))) for srv in servers]

class GraphicUtilCPU():

    def to_timestamp(self, t, t_format='%Y-%m-%d %H:%M:%S', tzoffset=0):
        u"""Конвертирует
        t  в таймштамп"""
        return float(datetime.datetime.strptime(t, t_format).strftime('%s.%f')) - tzoffset * 3600

    def to_timestring(self, t, t_format='%Y-%m-%d %H:%M:%S', tzoffset=0):
        u"""Конвертирует строку из таймштампа"""
        return datetime.datetime.fromtimestamp(float(t) + tzoffset * 3600.0).strftime(t_format)

    def sarLog(self,LOGS_sar,test_date):

        def to_groups(fileArr):
            servers = []
            for fn in fileArr:
                srv = re.split('(?<=app\d\d).', fn)[0]
                if srv not in servers:
                    servers.append(srv)
            return [list(filter(lambda x: x.startswith(srv), fileArr)) for srv in servers]


        if not os.path.exists(LOGS_sar):
            os.makedirs(LOGS_sar)
        pickle_sar.format(test_date)
        pickle_saru.format(test_date)
#        pickle_nmon_dbu.format(test_date)
#        pickle_nmon_app.format(test_date)
#        pickle_nmon_appu.pkl.zip'.format(test_date)
#SAR--Формирование-путей------------------------------------------------------------------------------------------------
        sarFiles = os.listdir(LOGS_sar)

        sarFileApp = []
        sarFileAppu = []

        for names in sarFiles:
            if names.startswith('sar_k10-szp-app'):
                sarFileApp.append(names)
            elif names.startswith('sar_k10-usbsm-app'):
                sarFileAppu.append(names)
        sarFileAppu.sort()
        sarFileApp.sort()

        sarFileApp = to_groups(sarFileApp)
        sarFileAppu = to_groups(sarFileAppu)
# NMON-------------------------------------------------------------------------------------------------------------------
#        nmonFiles = os.listdir(LOGS_nmon)
#
#        nmonFileDBu = []
#        nmonFileAppu = []
#        nmonFileApp = []
#
#        for names in nmonFiles:
#            if names.startswith('k10-usbsm-db'):
#                nmonFileDBu.append(names)
#            elif names.startswith('k10-usbsm-app'):
#                nmonFileAppu.append(names)
#            elif names.startswith('k10-szp-app'):
#                nmonFileApp.append(names)
#        nmonFileDBu.sort()
#        nmonFileAppu = to_groups(nmonFileAppu)
#        nmonFileApp = to_groups(nmonFileApp)
#
#        nmon_dbu = pd.read_nmon(LOGS_nmon + nmonFileDBu[0], compression='gzip')
#        s_name = nmon_dbu.info.server_name
#        for other in nmonFileDBu[1:]:
#            nmon_dbu = nmon_dbu.append(pd.read_nmon(LOGS_nmon + other, compression='gzip'))
#        nmon_dbu.info.server_name = s_name
#        nmon_dbu.to_comp_pickle(pickle_nmon_dbu, member=nmon_dbu.info.server_name + ".nmon.pkl")
# ----------------------------------------------------------------------------------------------------------------------
#        # nmon_db = pd.read_nmon(LOGS_nmon + nmonFileDB[0], compression='gzip')
#        # nmon_db.to_comp_pickle(pickle_nmon_db, member=nmon_db.info.server_name + ".nmon.pkl")
# ----------------------------------------------------------------------------------------------------------------------
#        for srv_nmon in nmonFileApp:
#            curNmon = pd.read_nmon(LOGS_nmon + srv_nmon[0], compression='gzip')
#            s_name = curNmon.info.server_name
#            for other in srv_nmon[1:]:
#                curNmon = curNmon.append(pd.read_nmon(LOGS_nmon + other, compression='gzip'))
#            curNmon.info.server_name = s_name
#            curNmon.to_comp_pickle(pickle_nmon_app, member=curNmon.info.server_name + ".nmon.pkl")
# ----------------------------------------------------------------------------------------------------------------------
#        for srv_nmon in nmonFileAppu:
#            curNmon = pd.read_nmon(LOGS_nmon + srv_nmon[0], compression='gzip')
#            s_name = curNmon.info.server_name
#            for other in srv_nmon[1:]:
#                curNmon = curNmon.append(pd.read_nmon(LOGS_nmon + other, compression='gzip'))
#            curNmon.info.server_name = s_name
#            curNmon.to_comp_pickle(pickle_nmon_appu, member=curNmon.info.server_name + ".nmon.pkl")
# ----------------------------------------------------------------------------------------------------------------------
# -----------sarFileApp-------------------------------------------------------------------------------------------------
        for srv_sar in sarFileApp:
            fSar = pd.read_sar(LOGS_sar + srv_sar[0], date_pattern='%d.%m.%Y', time_pattern='%H:%M:%S',
                               compression='gzip')
            for other in srv_sar[1:]:
                fSar = fSar.append(
                    pd.read_sar(LOGS_sar + other, date_pattern='%d.%m.%Y', time_pattern='%H:%M:%S', compression='gzip'))


#
#            # fSar.sort_index(axis=0, ascending=True, inplace=True)
#            fSar.info.server_name = s_name
#            fSar.to_comp_pickle(pickle_sar, member=fSar.info.server_name + ".sar.pkl")
#
#        for valFil in sarFileApp:
#            data = pd.read_sar(LOGS_sar + valFil, date_pattern='%d.%m.%Y', time_pattern='%H:%M:%S',
#                               compression='gzip')
#            FileRead.append(data)
        return
#----------sarFileAppu--------------------------------------------------------------------------------------------------
#        for srv_sar in sarFileAppu:
#            fSar = pd.read_sar(LOGS_sar + srv_sar[0], date_pattern='%d.%m.%Y', time_pattern='%H:%M:%S',
#                               compression='gzip')
#            s_name = fSar.info.server_name
#            for other in srv_sar[1:]:
#                fSar = fSar.append(
#                    pd.read_sar(LOGS_sar + other, date_pattern='%d.%m.%Y', time_pattern='%H:%M:%S', compression='gzip'))
#
#            # fSar.sort_index(axis=0, ascending=True, inplace=True)
#            fSar.info.server_name = s_name
#            fSar.to_comp_pickle(pickle_saru, member=fSar.info.server_name + ".sar.pkl")

#-----------------------------------------------------------------------------------------------------------------------
    def getLegendaSar(self, test_date, pickle_sar):
        for n, sar in enumerate(pd.read_comp_pickle(pickle_sar.format(test_date))):
            serv_name = sar.info.server_name.split('.passport.local')[0]
            lable.append(serv_name)
        return  lable

    def getQueryColumn(self, test_date,nameColumn):
        sarIdle = []
        for n, sar in pd.read_comp_pickle(pickle_sar.format(test_date)):
            sarIdle.append(sar[nameColumn])
        FileRead = list(sarIdle)
        return  FileRead


