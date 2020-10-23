from itertools import combinations
from sys import argv

#Retorna la nueva cantidad de variables y un arreglo con las variables nuevas (positivas y negativas):
def crearVariables(cantidadVariables, cantidadVariablesNuevas, arreglo):
  for i in range(cantidadVariablesNuevas):
    cantidadVariables += 1
    arreglo.append(cantidadVariables)
    arreglo.append(-cantidadVariables)
  return cantidadVariables, arreglo

#Valida si una cláusula contiene variables repetidas (usando valor absoluto):
def repetida(combinacion):
  combinacion = list(map(abs,combinacion))
  combinacionFiltrada = []
  for i in combinacion:
    if (i not in combinacionFiltrada):
      combinacionFiltrada.append(i)
  if (len(combinacion) > len(combinacionFiltrada)):
    return True
  else:
    return False

#Retorna un arreglo con todas las combinaciones posibles de un arreglo de variables (positivas y negativas):
def combinar(variables, cantidad):
  combinacionesRepetidas = combinations(variables, cantidad)
  combinaciones = []
  for i in combinacionesRepetidas:
    if (not repetida(list(i))):
      combinaciones.append(list(i))
  return combinaciones

#Reduce una cláusula para K < X:
def menor(clausula, cantidadVariables, k, x):
  cantidadVariablesNuevas = x - k
  cantidadVariables, variablesNuevas = crearVariables(cantidadVariables, cantidadVariablesNuevas, [])
  combinaciones = combinar(variablesNuevas, cantidadVariablesNuevas)
  conversion = []
  for i in combinaciones:
    nuevaClausula = clausula[:]
    nuevaClausula += i
    conversion.append(nuevaClausula)
  return cantidadVariables, conversion

#Reduce una cláusula para K > X usando la convención de abajo:
#(Z1,Z2,Z3,...,Zx-1,V1)(-V1,Z(x-3),...,Z(x-1),Zp,V2)(-Vk-x,Zp-(x-3),...,Zp,Zk)
def mayor(clausula,cantidadVariables,k,x):
  contador = 0
  cantidadClausulasNuevas = k-x+1
  cantidadRepetidas = x-3
  clausulaReducida = []
  for i in range(cantidadClausulasNuevas):
   clausulaAuxiliar = []
   if((k-x) == 0):
     clausulaAuxiliar = clausula
   else:  
    if(i == 0):
      #(Z1,Z2,Z3,...,Zx-1,V1)
      clausulaAuxiliar = clausula[contador:x-1]
      contador += x-1
      cantidadVariables += 1
      clausulaAuxiliar += [cantidadVariables]
    elif((i+1) == cantidadClausulasNuevas):
      #(-V1,Z(x-3),...,Z(x-1),Zp,V2)
      clausulaAuxiliar = clausula[contador-(cantidadRepetidas):]
      clausulaAuxiliar += [-1*cantidadVariables]
    else:
     #(-V1,Zp-(x-3),...,Zp,V2)
     clausulaAuxiliar = clausula[contador-(cantidadRepetidas):contador+1]
     contador += 1
     clausulaAuxiliar += [-1*cantidadVariables]
     cantidadVariables += 1
     clausulaAuxiliar += [cantidadVariables]
   clausulaReducida.append(clausulaAuxiliar)
  return cantidadVariables, clausulaReducida

#Reduce una instancia SAT a X-SAT:
def balanceador(sat,cantidadVariables,x):
  xSat = []
  for clausula in sat:
    k = len(clausula)
    if(k <= x):
     cantidadVariables, clausulaReducida = menor(clausula, cantidadVariables, k, x)
    else:
     cantidadVariables, clausulaReducida = mayor(clausula, cantidadVariables, k, x)
    xSat += clausulaReducida
  return cantidadVariables, xSat

#Método principal (lectura del archivo e impresión del resultado):
def main():
  cantidadVariables = 0
  sat = []
  xSat = []
  archivoSat = open(str(argv[1]), "r")
  archivoSatR = archivoSat.readlines()
  x = int(argv[2])
  for linea in archivoSatR:
    if(linea[0:5] == 'p cnf'):
      primeraLinea = linea.split()
      cantidadVariables = int(primeraLinea[2])
    elif(linea[0] != "c"):
      clausula = linea.split()
      clausula = clausula[:len(clausula)-1]
      clausula = list(map(int,clausula))
      sat.append(clausula)
  archivoSat.close()
  cantidadVariables, xSat = balanceador(sat, cantidadVariables, x)	
  print("p cnf",cantidadVariables,len(xSat))
  for clausula in xSat:
    linea = ""
    for i in clausula:
      linea += str(i) + " "
    linea += "0"
    print(linea)
    
main()
