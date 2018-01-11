from flask import Flask, request, render_template
from param_Stabs import param_stabs
from SQLQuery import sqlQuery as sqlQuery
from GraphicsCreaterUtilCPU import GraphicUtilCPU
#----------------ПЕРЕМЕННЫЕ---------------------------------------------------------------------------------------------
test_date = '171214'
directory = '//192.168.50.30/inotes/personal/s.danilov/data/171214/sar'
LOGS_sar = '//192.168.50.30/inotes/personal/s.danilov/data/{0}/sar/'.format(test_date)
LOGS_nmon = '//192.168.50.30/inotes/personal/s.danilov/data/{0}/nmon/'.format(test_date)
pickle_sar = '//192.168.50.30/inotes/personal/s.danilov/pkl/{0}/sar/sar_{0}.pkl.zip'
filess = 'C:/Users/d.kopysov/Desktop/logQuerty.csv'
fillessCard = 'C:/Users/d.kopysov/Desktop/time_cards.csv'
fillessCard1 = 'C:/Users/d.kopysov/Desktop/time_cards1.csv'
filessPerfomance = 'C:/Users/d.kopysov/Desktop/Perfomance.csv'
resu = []

percent = [8.2, 10.02, 81.78]  # Вводится 1 раз за 1 релиз
names = ['Загрузка единого реестра без акцепта, БКО',
         'Загрузка реестра зачислений с акцептом, БКО',
         'Загрузка реестра зачислений без акцепта, БКО'
         ]
namesFolders = ['BCO_UNION_NO_Accept',
                'BCO_Zachislenia_Accept',
                'BCO_Zachislenia_No_Accept'
                ]
filescount = [2.0, 1.0, 1.0]

sql_q = sqlQuery()
GUCPU = GraphicUtilCPU()
param_stab = param_stabs()




app = Flask(__name__)

@app.route("/")
def hello():
   return render_template('index.html',values='', Errors = '')

@app.route("/echo", methods=['POST'])
def echo():
   try:
       if(request.form['text'] == ''):
           return render_template('index.html', values = '')
       exeptonsed = sql_q.functions(request.form['text'])
       return render_template('index.html',values=exeptonsed)
   except Exception as e:
       return render_template('index.html', values = '', Errors = e)

@app.route("/clearBD", methods=['GET'])
def clearBDA():
   statistic = sql_q.StatisticTable()
   return render_template('clearBD.html',static = statistic, day = '', result = '')

@app.route("/clearBD", methods=['POST'])
def clearBDAs():
   statistic = sql_q.StatisticTable()
   if (request.form['day'] == ''):
       return render_template('clearBD.html',static = statistic, day = '', result = '')
   days = sql_q.ClearOrDB(request.form['day'])
   return render_template('clearBD.html',static = statistic, result = days, day = request.form['day'])

@app.route("/graphics", methods=['GET'])
def graphic():
   return render_template('Graphics.html')
@app.route("/graphics1", methods=['POST'])
def graphics():
#----------------------------------------------------------------------------------------------------------------------
   try:
       VarCh1 = sql_q.getUTL(filess)
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

# --1 График--Количество реестров в разных статусах в минуту------------------------------------------------------------
       legend1 = 'New'
       temperatures1 = VarCh1['New']
       legend2 = 'Check'
       temperatures2 = VarCh1['Check']
       legend3 = 'Enroll'
       temperatures3 = VarCh1['Enroll']
       legend4 = 'Enrolled'
       temperatures4 = VarCh1['Enrolled']
       legend51 = 'Enrolled(Усред.до 10 минут)'
       avg_sd1 = sql_q.getCard(fillessCard1)['AVG_SD']
       # Не хватает среднего времени обработки реестров

# --2 График--Производительность (накопленная)--------------------------------------------------------------------------
       legend5 = 'New'
       temperatures5 = Newall
       legend6 = 'Check'
       temperatures6 = Checkall
       legend7 = 'Enroll'
       temperatures7 = Enrollall
       legend8 = 'Enrolled'
       temperatures8 = Enrolledall
       times = VarCh1['Time']
# --3 График---10 минут--Производительность и подаваемая нагрузка-------------------------------------------------------


       LabelsEnrolled = 'Обработано, реестров зачисл. в час'
       Enrolled10 = sql_q.getEnrolled10(filess)
       LabelsWeb = 'Успешные web-операции'
       FainWebs = sql_q.dataProcessing(request.form['ValuesTest'])
       start_intense = float(request.form['start_intense'])
       final_intense = float(request.form['final_intense'])
       interval = float(request.form['interval'])
       duration = float(request.form['duration'])
       step_length = float(request.form['step_length'])
       step_length1 = float(request.form['step_length1'])
       files_count = 2
# ----------------------------------------------------------------------------------------------------------------------
       if sum(percent) == 100 and start_intense >= 0 and final_intense >= 0 and interval >= 0 and duration >= 0 and step_length >= 0:
           for n, nf, p, fc in zip(names, namesFolders, percent, filescount):
               out = param_stab.make_intervals(start_intense * p / 100, final_intense * p / 100, interval, duration,
                                               step_length, step_length1, files_count)
               out = [out[0]] + [[i[0], i[1] / fc] for i in out[1:]]
               resu.append(out)
       union = [a[1] for a in resu[0][1:]]        # union
       accept = [a[1]/2 for a in resu[1][1:]]     # accept
       no_accept = [a[1]/2 for a in resu[2][1:]]  # no_accept

       delivered_load_per_minute = [sum(am) for am in zip(union,accept,no_accept)]
       count = 4
       final_delivered_load = []
       for x in delivered_load_per_minute:
           final_delivered_load.append(x)
           final_delivered_load.extend([0.0]*count)

# ----------------------------------------------------------------------------------------------------------------------
       delivered_load_per_10minute = sql_q.get_delivered_load_per_10minute(final_delivered_load)
       label_delivered_10minuts = 'Подача нагрузки реестров зачисления в час'
# --График 4--Производительность----------------------------------------------------------------------------------------
       DATAOK = sql_q.getSummAllElements(sql_q.getPerformance(filessPerfomance)['DATAOK'])
       LabelsDATAOK = 'DATAOK'
       Processed = sql_q.getSummAllElements(sql_q.getPerformance(filessPerfomance)['Processed'])
       LabelsProcessed ='Processed'
# --График 6--Время обработки реестров----------------------------------------------------------------------------------
       avg_sd = sql_q.getCard(fillessCard)['AVG_SD']
       print(avg_sd)
       legendAVG_SD = 'Среднее время обработки реестров'



       sumDelivered = sql_q.getSummAllElements(final_delivered_load)
       legendSumDelivered = 'Подача нагрузки с накоплением'
       return render_template('TestGrapics.html', labels1=times,
                              NewLegend=legend1, NewValues=temperatures1,
                              CheckLegend=legend2, CheckValues=temperatures2,
                              EnrollLegend=legend3, EnrollValues=temperatures3,
                              EnrolledLegend=legend4, EnrolledValues=temperatures4,avg_sd1 = avg_sd1,
                              legend51 = legend51,
                              Legend1=legend5, Values1=temperatures5,
                              Legend2=legend6, Values2=temperatures6,
                              Legend3=legend7, Values3=temperatures7,
                              Legend4=legend8, Values4=temperatures8,
                              LabelsEnrolled=LabelsEnrolled, Enrolled10=Enrolled10,
                              LabelsWeb=LabelsWeb, FainWebs=FainWebs,
                              label_delivered_10minuts = label_delivered_10minuts,delivered_load_per_10minute = delivered_load_per_10minute,
                              legendSumDelivered = legendSumDelivered, sumDelivered = sumDelivered,
                              legendAVG_SD = legendAVG_SD, avg_sd = avg_sd,
                              LabelsDATAOK = LabelsDATAOK, DATAOK = DATAOK,
                              LabelsProcessed = LabelsProcessed, Processed = Processed
                              )
   except Exception as e:
       print(request.form['startTest0'])
       return render_template('Graphics.html', Error = 'Попробуй еще РАЗ!'+'\n'+str(e))

if __name__ == '__main__':
   app.run(host='192.168.70.127')