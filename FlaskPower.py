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
    return render_template('Graphics.html')

@app.route("/graphics", methods=['POST'])
def graphics():
    return render_template('Graphics.html')

if __name__ == '__main__':
    app.run()

