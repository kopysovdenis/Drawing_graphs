from flask import Flask, request, render_template
from numpy import sort
from SQLQuery import sqlQuery as sqlQuery
from GraphicsCreaterUtilCPU import GraphicUtilCPU
import os
import re
import datetime
import londas as pd

test_date = '171214'
directory = '//192.168.50.30/inotes/personal/s.danilov/data/171214/sar'
LOGS_sar = '//192.168.50.30/inotes/personal/s.danilov/data/{0}/sar/'.format(test_date)
LOGS_nmon = '//192.168.50.30/inotes/personal/s.danilov/data/{0}/nmon/'.format(test_date)

smit = sqlQuery()
graf = GraphicUtilCPU()
#-----------------------------------------------------------------------------------------------------------------------
#logread = graf.sarLog(LOGS_sar,LOGS_nmon,test_date)
lable = graf.getLegendaSar(test_date)
print(lable)
idle = graf.getQueryColumn(test_date,'%user')
print(idle)

#app = Flask(__name__)
#
#@app.route("/")
#def hello():
#   return render_template('index.html',values='', Errors = '')
#
#@app.route("/echo", methods=['POST'])
#def echo():
#    try:
#        if(request.form['text'] == ''):
#            return render_template('index.html', values = '')
#        exeptonsed = smit.functions(request.form['text'])
#        return render_template('index.html',values=exeptonsed)
#    except Exception as e:
#        return render_template('index.html', values = '', Errors = e)
#
#@app.route("/clearBD", methods=['GET'])
#def clearBDA():
#    statistic = smit.StatisticTable()
#    return render_template('clearBD.html',static = statistic, day = '', result = '')
#
#@app.route("/clearBD", methods=['POST'])
#def clearBDAs():
#    statistic = smit.StatisticTable()
#    if (request.form['day'] == ''):
#        return render_template('clearBD.html',static = statistic, day = '', result = '')
#    days = smit.ClearOrDB(request.form['day'])
#    return render_template('clearBD.html',static = statistic, result = days, day = request.form['day'])
#
#@app.route("/graphics", methods=['GET'])
#def graphic():
#    legend1 =  graf.getLegendaSar(test_date)
#    temperatures1 = graf.getIdleSar(test_date)
#    times1 = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
#             '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
#             '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']
#    return render_template('Graphics.html',values1=temperatures1, labels1=times1, legend1=legend1)
#
#@app.route("/graphics", methods=['POST'])
#def graphics():
#    return render_template('Graphics.html')
#
#if __name__ == '__main__':
#    app.run()
#----------------ПЕРЕМЕННЫЕ---------------------------------------------------------------------------------------------