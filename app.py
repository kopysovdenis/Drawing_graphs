from flask import Flask, request, render_template
from SQLQuery import sqlQuery as sqlQuery

smit = sqlQuery()

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
    legend1 = 'Temperatures'
    temperatures1 = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times1 = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
             '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
             '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']
    return render_template('Graphics.html',values1=temperatures1, labels1=times1, legend1=legend1)

@app.route("/graphics", methods=['POST'])
def graphics():
    return render_template('Graphics.html')

if __name__ == '__main__':
    app.run()

