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
from DISClib.ADT import stack
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
filename = file1
recursionLimit = 20000

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
    
    

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        citibike = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)

sys.exit(0)