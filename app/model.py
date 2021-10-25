from pickleshare import *

db = PickleShareDB('./data')


def usuarioCorrecto(userMail,userPasswd):
    correcto = False
    #Nos traemos los datos del usuario de la BD
    data = db.get(userMail)
    if(data is not None and data[1]==userPasswd):
        correcto = True
    return correcto

def eliminaUsuario(userMail):
    db.clear()



def registrarNuevoUsuario(userName,userMail,userPasswd,rePasswd,phone,direccion):
    insercion = False
    data = db.get(userMail)
    if(data is None and userPasswd==rePasswd):
        insercion = True
        db[userMail] = [userName,userPasswd,phone,direccion]
    return insercion

def getNameUser(userMail):
    data = db.get(userMail)
    if(data is not None):
        return data[0]
    else:
        return None

def getAllData(userMail):
    data = db.get(userMail)
    if(data is not None):
        return [data[index] for index in [0,2,3]]
    else:
        return None