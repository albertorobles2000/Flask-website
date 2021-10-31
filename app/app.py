#./app/app.py
from flask import (Flask, render_template, session, request, session, redirect, url_for, flash)
from flask import make_response
import model
import ejercicios


app = Flask(__name__)
app.secret_key = "123456789"   

@app.route('/')
def Home():
  parameters = {}
  #Guardamos un parametro con la pagina en la que estamos
  parameters["page"] = "home"
  #Guardamos el usuario, si no hay uno logueado se devuelve None
  parameters["user"] = userLoged()
  lastPages = updateLastPagesSeen('Home')
  parameters = lastPagesSeenToParameters(lastPages,parameters)
  response = make_response(render_template('main.html',**parameters))
  response = setCookiesWithLastPages(response, lastPages)
  return response
  

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
        flash('Correo electronico o contraseña incorrectos')
        return redirect(url_for('login'))
    else:
      #Actualizamos las ultimas paginas visitadas
      lastPages = updateLastPagesSeen('Login')
      parameters = lastPagesSeenToParameters(lastPages,parameters)
      response = make_response(render_template('login.html',**parameters))
      #Actualizamos las cookies con las ultimas paginas visitadas
      response = setCookiesWithLastPages(response, lastPages)
      return response

@app.route('/signin',methods=['POST','GET'])
def signin():
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
      flash('El correo electronico introducido ya tiene una cuenta asociada')
      return redirect(url_for('signin'))
  else:
    lastPages = updateLastPagesSeen('Sign In')
    parameters = lastPagesSeenToParameters(lastPages,parameters)
    response = make_response(render_template('signin.html',**parameters))
    response = setCookiesWithLastPages(response, lastPages)
    return response

@app.route('/logout',methods=['GET'])
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

      lastPages = updateLastPagesSeen('User Page')
      parameters = lastPagesSeenToParameters(lastPages,parameters)
      response = make_response(render_template('user.html',**parameters))
      response = setCookiesWithLastPages(response, lastPages)
      return response
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
          password = request.form["password"]
          cookiesCorreo = request.cookies.get('user',None)
          correcto = model.usuarioCorrecto(cookiesCorreo,password)
          if(correcto):
            model.eliminaUsuario(cookiesCorreo)
            model.registrarNuevoUsuario(name,userMail,password,password,phone,direcction)
            response = make_response(redirect(url_for('user')))
            response.set_cookie('user',userMail)
            return response
          else:
            return redirect(url_for('datachange'))
        else:
          return redirect(url_for('user'))  
      else:
        mail = request.cookies.get('user',None)
        info = model.getAllData(mail)
        parameters["mail"] = mail
        parameters["phone"] = info[1]
        parameters["direction"] = info[2]

        lastPages = updateLastPagesSeen('Modificación de datos')
        parameters = lastPagesSeenToParameters(lastPages,parameters)
        response = make_response(render_template('datachange.html',**parameters))
        response = setCookiesWithLastPages(response, lastPages)


        return render_template('datachange.html', **parameters)
    else:
      return redirect(url_for('login'))

@app.route('/ordenavector',methods=['POST','GET'])
def ordenavector():
    usuario = userLoged()
    parameters = {}
    parameters["page"] = "ejercicios"
    parameters["user"] = usuario
    if(request.method == 'POST'):
        parameters["vectorOrdenado"] = ejercicios.ordenaVector(request.form["vector"])
        lastPages = getPagesSeen()
        parameters = lastPagesSeenToParameters(lastPages,parameters)
        return render_template('ordenavector.html', **parameters)
    else:
        #Actualizamos las ultimas paginas visitadas
        lastPages = updateLastPagesSeen('Ordena Vector')
        parameters = lastPagesSeenToParameters(lastPages,parameters)
        response = make_response(render_template('ordenavector.html',**parameters))
        #Actualizamos las cookies con las ultimas paginas visitadas
        response = setCookiesWithLastPages(response, lastPages)
        return response
        
@app.route('/numerosprimos',methods=['POST','GET'])
def numerosprimos():
    usuario = userLoged()
    parameters = {}
    parameters["page"] = "ejercicios"
    parameters["user"] = usuario
    if(request.method == 'POST'):
        parameters["vectorPrimos"] = ejercicios.primos(int(request.form["numero"]))
        lastPages = getPagesSeen()
        parameters = lastPagesSeenToParameters(lastPages,parameters)
        return render_template('numerosprimos.html', **parameters)
    else:
        lastPages = updateLastPagesSeen('Numeros primos')
        parameters = lastPagesSeenToParameters(lastPages,parameters)
        response = make_response(render_template('numerosprimos.html',**parameters))
        #Actualizamos las cookies con las ultimas paginas visitadas
        response = setCookiesWithLastPages(response, lastPages)
        return response


@app.route('/corchetesbalanceados',methods=['POST','GET'])
def corchetesBalanceados():
    usuario = userLoged()
    parameters = {}
    parameters["page"] = "ejercicios"
    parameters["user"] = usuario
    if(request.method == 'POST'):
        correcto = ejercicios.corchetes(request.form["secuenciaCorchetes"])

        if(correcto):
            parameters["secuenciaCorrecta"] = "True"
        else:
            parameters["secuenciaCorrecta"] = "False"
          
        lastPages = getPagesSeen()
        parameters = lastPagesSeenToParameters(lastPages,parameters)

        return render_template('corchetesbalanceados.html', **parameters)
    else:
        lastPages = updateLastPagesSeen('Corchetes balanceados')
        parameters = lastPagesSeenToParameters(lastPages,parameters)
        response = make_response(render_template('corchetesbalanceados.html',**parameters))
        #Actualizamos las cookies con las ultimas paginas visitadas
        response = setCookiesWithLastPages(response, lastPages)

        return response

@app.route('/expresionregular',methods=['POST','GET'])
def expresionregular():
    usuario = userLoged()
    parameters = {}
    parameters["page"] = "ejercicios"
    parameters["user"] = usuario
    if(request.method == 'POST'):
        apellidos,correos,tarjetas = ejercicios.expresionRegular(request.form["texto"])
        parameters["apellidos"] = apellidos
        parameters["correos"] = correos
        parameters["tarjetas"] = tarjetas
        
        lastPages = getPagesSeen()
        parameters = lastPagesSeenToParameters(lastPages,parameters)

        return render_template('expresionesregulares.html', **parameters)
    else:

        lastPages = updateLastPagesSeen('Expresión regular')
        parameters = lastPagesSeenToParameters(lastPages,parameters)
        response = make_response(render_template('expresionesregulares.html',**parameters))
        #Actualizamos las cookies con las ultimas paginas visitadas
        response = setCookiesWithLastPages(response, lastPages)

        return response

@app.errorhandler(404)
def page_not_found(error):
    return "<h1>Vaya!! Parece que esta ruta no existe</h1>"



def userLoged():
	userLogin = "None"
	cookies = request.cookies.get('user',None)
	if cookies is not None:
		userLogin = model.getNameUser(cookies)
	return userLogin


def getPagesSeen():
  paginaAnterior0 = request.cookies.get('lastPage0',None)
  if paginaAnterior0 is None:
    paginaAnterior0 = ""
  paginaAnterior1 = request.cookies.get('lastPage1',None)
  if paginaAnterior1 is None:
    paginaAnterior1 = ""
  paginaAnterior2 = request.cookies.get('lastPage2',None)
  if paginaAnterior2 is None:
    paginaAnterior2 = ""
  paginaAnterior3 = request.cookies.get('lastPage3',None)
  if paginaAnterior3 is None:
    paginaAnterior3 = ""
  
  lista = []
  lista.append(paginaAnterior0)
  lista.append(paginaAnterior1)
  lista.append(paginaAnterior2)
  lista.append(paginaAnterior3)

  return lista


def updateLastPagesSeen(thisPage):
  lista = getPagesSeen()
  lista.pop(-1)
  lista.insert(0,thisPage)
  
  return lista

def lastPagesSeenToParameters(lastSeen,parameters):
  parameters["lastPage1"] = lastSeen[1]
  parameters["lastPage2"] = lastSeen[2]
  parameters["lastPage3"] = lastSeen[3]
  return parameters

def setCookiesWithLastPages(response, lastPages):
  #for i in range(len(lastPages)):
    #response.set_cookie('lastPage'+str(i),lastPages[i])
  response.set_cookie('lastPage0',lastPages[0])
  response.set_cookie('lastPage1',lastPages[1])
  response.set_cookie('lastPage2',lastPages[2])
  response.set_cookie('lastPage3',lastPages[3])

  return response



########
#Añadir contraseña en el cambio de datos
#Poder seleccionar elementos de la barra lateral