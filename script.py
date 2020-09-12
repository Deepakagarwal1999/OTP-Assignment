from flask import Flask,render_template,request,session
import requests
import random
import math

app = Flask(__name__)
app.secret_key = 'otp'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/getotp',methods = ['POST'])
def getotp():
    number = request.form['number']
    val = getotpAPI(number)
    if val:
        return render_template('enterotp.html')
    
@app.route('/validateotp',methods = ['POST'])
def validateOTP():
    otp = request.form['otp']
    if 'response' in session:
        s = session['response']
        session.pop('response',None)
        if s == otp:
            return "Success"
        else:
            return "Failure"

def getotpAPI(number):
    otp = generateOTP()
    session['response'] = str(otp)
    url = "https://www.fast2sms.com/dev/bulk"
    querystring = {"authorization":"YIDm10BL2GgbhZUsz7cHwWnxX4eJViE6ROMvoA8Sp3fCNKqFdTMA4jJcCL0lrwSH9ukemRoIP3YTUD2a",
               "sender_id":"FSTSMS","message":str(otp),"language":"english",
               "route":"p","numbers":number}
    headers = {
            'cache-control': "no-cache"
            }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text
    
def generateOTP():
    data = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    leng = len(data)
    otp = ""
    for i in range(6):
        otp += data[math.floor((random.random() * leng))]
    return otp

if __name__== '__main__':
    app.run(debug = True)