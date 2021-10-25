#./app/app.py
from flask import (Flask, render_template, session, request, session, redirect, url_for)
from flask import make_response
import model


app = Flask(__name__)
app.secret_key = "123456789"   

@app.route('/')
def hello_world():
  parameters = {}
  parameters["page"] = "home"
  parameters["user"] = userLoged()


  return render_template('main.html',**parameters)
  

@app.route('/login',methods=['POST','GET'])
def login():
  parameters = {}
  parameters["page"] = "login"
  parameters["user"] = userLoged()
  #Si el usuario ya tiene una sesion iniciada lo redirigimos a la
  #pagina de bienvenida
  cookies = request.cookies.get('user',None)
  if cookies is not None:
    return redirect(url_for('user'))
  else:
    #Si el usuario solicita iniciar sesion
    if(request.method == 'POST'):
      userMail = request.form["email"]
      #Si los datos son correctos lo redirigimos a usuario
      if(model.usuarioCorrecto(userMail,request.form["password"])):
        response = make_response(redirect(url_for('user')))
        response.set_cookie('user',userMail)
        return response
      #Si no son correctos lo mandamos a loguearse
      else:
        return render_template('login.html',**parameters)
    else:
      return render_template('login.html',**parameters)

@app.route('/signin',methods=['POST','GET'])
def singin():
  parameters = {}
  parameters["page"] = "signin"
  parameters["user"] = userLoged()
  if(request.method == 'POST'):
    userName = request.form["name"]
    userMail = request.form["email"]
    passwd = request.form["password"]
    userRePasswd = request.form["repassword"]
    phone = request.form["phone"]
    direccion = request.form["localitation"]
    insercion = model.registrarNuevoUsuario(userName,userMail,passwd,userRePasswd,phone,direccion)
    if(insercion):
      response = make_response(redirect(url_for('user')))
      response.set_cookie('user',userMail)
      return response
    else:
      render_template('signin.html',**parameters)
  else:
    return render_template('signin.html',**parameters)

@app.route('/logout',methods=['POST','GET'])
def logout():
    usuario = userLoged()
    if usuario != "None":
      #El usuario a pulsado log out
      response = make_response(redirect(url_for('login')))
      response.set_cookie('user', '', expires=0)
      return response
    else:
      return redirect(url_for('login'))

@app.route('/user',methods=['POST','GET'])
def user():
    usuario = userLoged()
    parameters = {}
    parameters["page"] = "user"
    parameters["user"] = usuario
    if usuario != "None":
      mail = request.cookies.get('user',None)
      info = model.getAllData(mail)
      parameters["mail"] = mail
      parameters["phone"] = info[1]
      parameters["direction"] = info[2]

      return render_template('user.html', **parameters)
    else:
      return redirect(url_for('login'))

@app.route('/datachange',methods=['POST','GET'])
def datachange():
    usuario = userLoged()
    parameters = {}
    parameters["page"] = "user"
    parameters["user"] = usuario
    if usuario != "None":
      if(request.method == 'POST'):
        if request.form.get("modifica"):
          name = request.form["name"]
          userMail = request.form["email"]
          phone = request.form["phone"]
          direcction = request.form["direction"]
          model.eliminaUsuario(userMail)
          model.registrarNuevoUsuario(name,userMail,123456,123456,phone,direcction)
          redirect(url_for('user'))
        else:
          redirect(url_for('user'))  
      else:
        mail = request.cookies.get('user',None)
        info = model.getAllData(mail)
        parameters["mail"] = mail
        parameters["phone"] = info[1]
        parameters["direction"] = info[2]
        return render_template('datachange.html', **parameters)
    else:
      return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return "<h1>Vaya!! Parece que esta ruta no existe</h1>"



def userLoged():
	userLogin = "None"
	cookies = request.cookies.get('user',None)
	if cookies is not None:
		userLogin = model.getNameUser(cookies)
	return userLogin
