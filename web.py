from flask import Flask, render_template, request, redirect, url_for, make_response
import RPi.GPIO as GPIO
import os
from time import sleep
from signal import pause
import string  
import random  


users = {"admin" : "admin"}

GPIO.setmode(GPIO.BCM)

SERVER_IP = "0.0.0.0"
PORT = 8080

GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

LED1 = GPIO.PWM(16, 100)
LED2 = GPIO.PWM(20, 100)
LED3 = GPIO.PWM(21, 100)


TEMPLATE_DIR = os.getcwd() + "/site"


def light(ledNo, level):

    if(ledNo == "1"):
        LED1.start(float(level))

    if(ledNo == "2"):
        LED2.start(float(level))

    if(ledNo == "3"):
        LED3.start(float(level))

def checkUser(cookie):
    try:
        cookies = open(TEMPLATE_DIR+"/cookies.txt", "r")
        if(cookies.readline() == cookie):
            cookies.close()
            return True
        else:
            cookies.close()
            return False
    except:
        return redirect("/login.html")
webServer = Flask(__name__, template_folder=TEMPLATE_DIR)

@webServer.route("/<path:path>", methods=["GET"])
def renderIndex(path):
    return render_template(path)

@webServer.route("/", methods=["GET"])
def yonlendir():
    return redirect("/ahmetbey.html")

@webServer.route("/login.html", methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        username =  request.form["username"]
        password =  request.form["password"]

        if(username in users):
            if(password == users[username]):
                result = ''.join((random.choice(string.ascii_lowercase) for x in range(15)))
                cookies = open(TEMPLATE_DIR+"/cookies.txt", "w")
                cookies.write(result)
                cookies.close()
                resp = make_response(redirect("/ahmetbey.html"))
                resp.set_cookie("userCookie", result)
                return resp
        return "kullanici adi veya sifreyi yanlis girdiniz"
    else:
        return render_template("/login.html")

@webServer.route("/ahmetbey.html", methods=["GET", "POST"])
def renderAhmet():
    if (request.method == "POST"):
        pass

    if (request.method == "GET"):
        userCookie = request.cookies.get('userCookie')

        if(checkUser(userCookie) == True):
            pass
        else:
            return redirect("/login.html")
 
        return render_template("/ahmetbey.html")
    

@webServer.route("/light", methods=["GET"])
def lightadj():
    userCookie = request.cookies.get('userCookie')

    if(checkUser(userCookie) == True):
        pass
    else:
        return redirect("/login.html")


    if (request.method == "GET"):
        secim = request.args.get("secim")
        level = request.args.get("level")
        light(secim, level)

        return redirect("/close.html")



#Run
if (__name__ == "__main__"):
    print("!!!" + TEMPLATE_DIR + "!!!")
    webServer.run(host=SERVER_IP, port=PORT, debug=True)

