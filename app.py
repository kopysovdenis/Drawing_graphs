from flask import Flask, request, render_template
from param_Stabs import param_stabs
from SQLQuery import sqlQuery as sqlQuery
from GraphicsCreaterUtilCPU import GraphicUtilCPU
#----------------ПЕРЕМЕННЫЕ---------------------------------------------------------------------------------------------
test_date = '171214'
directory = '//192.168.50.30/inotes/personal/s.danilov/data/171214/sar'
LOGS_sar = '//192.168.50.30/inotes/personal/s.danilov/data/{0}/sar/'.format(test_date)
LOGS_nmon = '//192.168.50.30/inotes/personal/s.danilov/data/{0}/nmon/'.format(test_date)
filess = 'C:/Users/d.kopysov/Desktop/logQuerty.csv'
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

start_intense = 1140 #реестров в час, стартовая интенсивность
final_intense = 1140 #реестров в час, финишная интенсивность
step_length = 600 #минут, длительность "полки"
interval = 5         #минут, частота отправки файлов
duration = 600       #минут, длительность теста
init_delay = 0
step_length1 = 5   #(interval = 5 :раз в 5 минут)
files_count = 2

smit = sqlQuery()
graf = GraphicUtilCPU()
param_stab = param_stabs()

if sum(percent) == 100:
    for n, nf, p, fc in zip(names, namesFolders, percent, filescount):
        out = param_stab.make_intervals(start_intense * p / 100, final_intense * p / 100, interval, duration,
                                        step_length, step_length1, files_count)
        out = [out[0]] + [[i[0], i[1] / fc] for i in out[1:]]
        resu.append(out)
    print(resu[0][1:])
    print(resu[1][1:])
    print(resu[2][1:])

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
#----------------------------------------------------------------------------------------------------------------------
   try:
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

# --1 График------------------------------------------------------------------------------------------------------------
       legend1 = 'New'
       temperatures1 = VarCh1['New']
       legend2 = 'Check'
       temperatures2 = VarCh1['Check']
       legend3 = 'Enroll'
       temperatures3 = VarCh1['Enroll']
       legend4 = 'Enrolled'
       temperatures4 = VarCh1['Enrolled']
# --2 График------------------------------------------------------------------------------------------------------------
       legend5 = 'New'
       temperatures5 = Newall
       legend6 = 'Check'
       temperatures6 = Checkall
       legend7 = 'Enroll'
       temperatures7 = Enrollall
       legend8 = 'Enrolled'
       temperatures8 = Enrolledall
       times = VarCh1['Time']
# --3 График---10 минут-------------------------------------------------------------------------------------------------


       LabelsEnrolled = 'Обработано, реестров зачисл. в час'
       Enrolled10 = smit.getEnrolled10(filess)
       LabelsWeb = 'Успешные web-операции'
       FainWebs = smit.dataProcessing(request.form['ValuesTest'])
       """start_intense = request.form['start_intense']
#final_intense = request.form['final_intense']
#interval = request.form['interval']
#duration = request.form['duration']
#step_length = request.form['step_length']
#step_length1 = request.form['step_length1']
#files_count = 2"""



       return render_template('TestGrapics.html', labels1=times,
                              NewLegend=legend1, NewValues=temperatures1,
                              CheckLegend=legend2, CheckValues=temperatures2,
                              EnrollLegend=legend3, EnrollValues=temperatures3,
                              EnrolledLegend=legend4, EnrolledValues=temperatures4,
                              Legend1=legend5, Values1=temperatures5,
                              Legend2=legend6, Values2=temperatures6,
                              Legend3=legend7, Values3=temperatures7,
                              Legend4=legend8, Values4=temperatures8,
                              LabelsEnrolled=LabelsEnrolled, Enrolled10=Enrolled10,
                              LabelsWeb=LabelsWeb, FainWebs=FainWebs)
   except Exception as e:
       return render_template('Graphics.html', Error = 'Попробуй еще РАЗ!'+'\n'+str(e))

if __name__ == '__main__':
   app.run(host='192.168.70.127')
