"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack as st
from DISClib.ADT import list as lt
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

file1 = '201801-1-citibike-tripdata.csv'
file2 = '201801-2-citibike-tripdata.csv'
file3 = '201801-3-citibike-tripdata.csv'
file4 = '201801-4-citibike-tripdata.csv'
file5 = '201801-1-citibike-tripdata-small.csv'
filename = file5
recursionLimit = 80000

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar CitiBike")
    print("2- Cargar información de bicicletas de Nueva York")
    print("3- Cantidad de clusters de viajes (REQ 1)")
    print("4- Ruta turistica circular (REQ 2)")
    print("5- Ruta turistica de menor tiempo/<Estaciones criticas> (REQ 3)")
    print("6- Ruta turistica por resistencia (REQ 4)")
    print("7- Ruta mas corta entre estaciones (REQ 5)")
    print("8- Ruta de interes turistico (REQ 6)")
    print("9- Cantidad de clusters de viajes (REQ 7)")
    print("10- Cantidad de clusters de viajes (REQ 8)")

    print("0- Salir")
    print("*******************************************")

def optionTwo():
    print("\nCargando información de bicicletas de Nueva York ....")
    controller.loadFile(citibike, filename)
    numedges = controller.totalConnections(citibike)
    numvertex = controller.totalStations(citibike)
    print('Numero de vértices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


def optionThree():
    """
    Req 1
    """
    station1 = input("Ingrese la estación 1: ") 
    station2 = input("Ingrese la estación 2: ")
    print('El número de componentes conectados es: ' +
          str(controller.numSCC(citibike)))
    sameSCC = controller.sameSCC(citibike, station1, station2)
    if sameSCC == True:
        print("La estación " + station1 + " y la estación " + station2 + 
                " SÍ pertenecen al mismo cluster.")
    else:
        print("La estación " + station1 + " y la estación " + station2 + 
            " NO pertenecen al mismo cluster.")
    

def optionFour():
    """
    Req 2
    """    
    pass


def optionFive():
    """
    Req 3P
    """
    llegada, salida, menosUsadas = controller.criticStations(citibike)

    print(f'Las 3 estaciones en el TOP de llegada:<{lt.getElement(llegada,1)}>, <{lt.getElement(llegada,2)}>, <{lt.getElement(llegada,3)}>')
    print(f'Las 3 estaciones en el TOP de salida:<{lt.getElement(salida,1)}>, <{lt.getElement(salida,2)}>, <{lt.getElement(salida,3)}>')
    print(f'Las 3 estaciones en el TOP de menos usadas:<{lt.getElement(menosUsadas,1)}>, <{lt.getElement(menosUsadas,2)}>, <{lt.getElement(menosUsadas,3)}>')


def optionSix():
    """
    Req 4
    """    
    pass


def optionSeven():
    """
    Req 5
    """    
    pass


def optionEight():
    """
    Req 6P
    """    
    latAct = input('Latitud Actual\n')
    lonAct = input('Longitud Actual\n')
    latDes = input('Latitud Destino\n')
    lonDes = input('Longitud Destino\n')

    nearStationActual, nearStationDestiny, tripTime, stationList = controller.turistInteres(citibike, latAct, lonAct, latDes, lonDes)

    print(f'La estacion mas cercana a su ubicacion actual es <{nearStationActual}>')
    print(f'La estacion mas cercana a su ubicacion destino es <{nearStationDestiny}>')
    print(f'El tiempo estimado de viaje es <{tripTime}>')
    print(f'La lista de estaciones en la ruta es <{stationList}>')


def optionNine():
    """
    Req 7P
    """
    edad = int(input('Ingrese su edad\n'))
    temp = (edad-1)//10 if edad > 0 else 0
    temp = temp if edad < 61 else 6
    if temp < 6:
        sup = (temp+1)*10
        inf = (temp*10)+1 if temp > 0 else 0
    team = f'{inf}-{sup}' if temp < 6 else f'{61}+'
    
    stationsStartStopTrips = controller.ageStations(citibike, team)

    print(f'En el rango de edad <{team}>:')
    for i in range(lt.size(stationsStartStopTrips)):
        info = lt.getElement(stationsStartStopTrips, i)
        print(f'Entrada {info[0]}, Salida {info[1]}, Con {info[3]} viajes registrados')



def optionTen():
    """
    Req 8
    """    
    pass

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        citibike = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(optionEight, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 9:
        executiontime = timeit.timeit(optionNine, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs) == 10:
        executiontime = timeit.timeit(optionTen, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    else:
        sys.exit(0)

sys.exit(0)