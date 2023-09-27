import uuid
import re

from flask import Flask, render_template, request, redirect, url_for, make_response

from data.Configuration import *
test = True

configuration_filename = ""
if test:
    configuration_filename = "tests/testConfiguration.yaml"
else:
    configuration_filename = "config/config.yaml"
config = ConfigFromYAML(filename=configuration_filename)
adminCookies = dict()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config)


@app.route("/lorem")
def loremPage():
    return render_template("lorem.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config)


@app.route(config["AdminURL"], methods=['POST', 'GET'])
def adminPage():
    cookie = getadmincookie()
    try:
        if adminCookies[cookie]:
            if request.method == 'POST':
                for key in request.form:
                    if re.match( "\d+",request.form[key]):
                        config[key] = int(request.form[key])
                    else:
                        config[key] = request.form[key]
                    ConfigToYAML(config, configuration_filename)
                return render_template("admin.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config)
            else:
                return render_template("admin.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config)
        else:
            return render_template("login.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config, message="Cookie expiré, veuillez vous reconnecter")
    except Exception as exception:
        print(exception)
        return render_template("login.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config, message="Merci de vous connecter pour continuer")


@app.route("/session/")
def handlePOSTSession():
    cookie = getadmincookie()
    try:
        if adminCookies[cookie]:
            if request.method == 'POST':
                for key in request.form:
                    if re.match("\d+", request.form[key]):
                        config[key] = int(request.form[key])
                    else:
                        config[key] = request.form[key]
                    ConfigToYAML(config, configuration_filename)
                return redirect(config["AdminURL"])
            else:
                return redirect(config["AdminURL"])
        else:
            return redirect(config["AdminURL"])
    except:
        return redirect(config["AdminURL"])


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
            return render_template("login.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config, message="Échec d'authentification")
    else:
        return render_template("login.html", theme=config["Theme"], themejs=config["ThemeJS"], config=config, message="Méthode HTTP non autorisée")


def getadmincookie():
   cookie = request.cookies.get('adminCookie')
   return cookie


def setadmincookie():
    cookie = uuid.uuid4().hex
    adminCookies[cookie] = True
    return cookie


if __name__ == '__main__':
    app.run()
