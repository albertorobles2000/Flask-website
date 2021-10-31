def corchetes(cadena):
    correcto = True
    stack = []
    for i in cadena:
        if(i=='['):
            stack.append(i)
        else:
            if(len(stack)>0):
                stack.pop()
            else:
                correcto=False
                break
    if(len(stack)>0):
        correcto = False

    return correcto

def primos(max):
    lista = []
    lista2 = []
    for i in range(2,max+1):
        lista.append(i)
        lista2.append(True)
    for i in range(0,len(lista)-1):
        if(lista2[i]==True):
            for j in range(i+1,len(lista)):
                if(lista2[j]==True and lista[j]%lista[i]==0):
                    lista2[j] = False
    l = []
    for i in range(len(lista)):
        if(lista2[i]==True):
            l.append(str(lista[i]))

def ordenaVector(vector):
    lista = vector.split(",")
    lista = [int(i) for i in lista]
    for i in range(len(lista)):
        for j in range((len(lista)-i)-1):
            if(lista[j]>lista[j+1]):
                lista[j], lista[j+1] = lista[j+1], lista[j]
    lista = [str(i) for i in lista]
    return lista

def expresionRegular(cadena):
    import re
    patron = "[A|a]pellido [A-Z][a-z]*"
    l1 = re.findall(patron, cadena)
    patron = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
    l2 = re.findall(patron, cadena)
    patron = "[0-9]{4}[-|\s][0-9]{4}[-|\s][0-9]{4}[-|\s][0-9]{4}"
    l3 = re.findall(patron, cadena)

    return (",".join(l1),",".join(l2),",".join(l3))