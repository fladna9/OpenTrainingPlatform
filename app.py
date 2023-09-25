import uuid
from flask import Flask, render_template, request, redirect, url_for, make_response

from data.Configuration import *
test = True


if test:
    config = ConfigFromYAML(filename="tests/testConfiguration.yaml")
    ConfigToYAML(config, filename="tests/ConfigToYAML.yaml")
    config["TestMode"] = True
else:
    config = ConfigFromYAML(filename="config/config.yaml")
    config["TestMode"] = False

adminCookies = dict()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config)


@app.route("/lorem")
def loremPage():
    return render_template("lorem.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config)


@app.route(config["AdminURL"])
def adminPage():
    cookie = getadmincookie()
    try:
        if adminCookies[cookie]:
            return render_template("admin.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config)
        else:
            return render_template("login.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config, message="Cookie expired, please reconnect")
    except:
        return render_template("login.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config, message="Please login to continue")


@app.route("/login", methods=['POST'])
def handlePOSTLogin():
    if request.method == 'POST':
        typedpass = request.form["adminPassword"]
        if typedpass == config["AdminPassword"]:
            cookie = setadmincookie()
            resp = redirect(config["AdminURL"], code=302)
            resp.set_cookie('adminCookie', cookie)
            return resp
        else:
            return render_template("login.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config, message="Bad username or password")
    else:
        return render_template("login.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config, message="Use POST method please.")


def getadmincookie():
   cookie = request.cookies.get('adminCookie')
   return cookie


def setadmincookie():
    cookie = uuid.uuid4().hex
    adminCookies[cookie] = True
    return cookie


if __name__ == '__main__':
    app.run()
