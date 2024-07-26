from flask import Flask,request, make_response, render_template

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template('inicial.html')

@app.route('/login')
def Login():
    return render_template('login.html')