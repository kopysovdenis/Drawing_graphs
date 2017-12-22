import re

from flask import Flask, request, render_template
from numpy import sort
import os

from SQLQuery import sqlQuery as sqlQuery
from GraphicsCreaterUtilCPU import GraphicUtilCPU
import pandas as pd
#----------------ПЕРЕМЕННЫЕ---------------------------------------------------------------------------------------------
test_date = '171214'
directory = '//192.168.50.30/inotes/personal/s.danilov/data/171214/sar'
LOGS_sar = '//192.168.50.30/inotes/personal/s.danilov/data/{0}/sar/'.format(test_date)
LOGS_nmon = '//192.168.50.30/inotes/personal/s.danilov/data/{0}/nmon/'.format(test_date)
filess = 'C:/Users/d.kopysov/Desktop/logQuerty.csv'

smit = sqlQuery()
graf = GraphicUtilCPU()


app = Flask(__name__)

@app.route("/")
def hello():
   return render_template('index.html',values='', Errors = '')

@app.route("/echo", methods=['POST'])
def echo():
    try:
        if(request.form['text'] == ''):
            return render_template('index.html', values = '')
        exeptonsed = smit.functions(request.form['text'])
        return render_template('index.html',values=exeptonsed)
    except Exception as e:
        return render_template('index.html', values = '', Errors = e)

@app.route("/clearBD", methods=['GET'])
def clearBDA():
    statistic = smit.StatisticTable()
    return render_template('clearBD.html',static = statistic, day = '', result = '')

@app.route("/clearBD", methods=['POST'])
def clearBDAs():
    statistic = smit.StatisticTable()
    if (request.form['day'] == ''):
        return render_template('clearBD.html',static = statistic, day = '', result = '')
    days = smit.ClearOrDB(request.form['day'])
    return render_template('clearBD.html',static = statistic, result = days, day = request.form['day'])

@app.route("/graphics", methods=['GET'])
def graphic():
    return render_template('Graphics.html')
@app.route("/graphics1", methods=['POST'])
def graphics():
# ----------------------------------------------------------------------------------------------------------------------
    VarCh1 = smit.getUTL(filess)
    Newall = []
    Checkall = []
    Enrollall = []
    Enrolledall = []
    i = 0
    for row in VarCh1['New']:
        i = i + int(row)
        Newall.append(i)
    i = 0
    for row in VarCh1['Check']:
        i = i + int(row)
        Checkall.append(i)
    i = 0
    for row in VarCh1['Enroll']:
        i = i + int(row)
        Enrollall.append(i)
    i = 0
    for row in VarCh1['Enrolled']:
        i = i + int(row)
        Enrolledall.append(i)
# ----------------------------------------------------------------------------------------------------------------------
    legend1 = 'New'
    temperatures1 = VarCh1['New']
    legend2 = 'Check'
    temperatures2 = VarCh1['Check']
    legend3 = 'Enroll'
    temperatures3 = VarCh1['Enroll']
    legend4 = 'Enrolled'
    temperatures4 = VarCh1['Enrolled']
    legend5 = 'New'
    temperatures5 = Newall
    legend6 = 'Check'
    temperatures6 = Checkall
    legend7 = 'Enroll'
    temperatures7 = Enrollall
    legend8 = 'Enrolled'
    temperatures8 = Enrolledall
    times = VarCh1['Time']
    return render_template('TestGrapics.html', labels1=times,
                           NewLegend=legend1, NewValues=temperatures1,
                           CheckLegend=legend2, CheckValues=temperatures2,
                           EnrollLegend=legend3, EnrollValues=temperatures3,
                           EnrolledLegend=legend4, EnrolledValues=temperatures4,
                           Legend1=legend5, Values1=temperatures5,
                           Legend2=legend6, Values2=temperatures6,
                           Legend3=legend7, Values3=temperatures7,
                           Legend4=legend8, Values4=temperatures8, )

if __name__ == '__main__':
    app.run()
