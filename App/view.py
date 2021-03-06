import sys
import config
from App import controller
from DISClib.ADT import stack as st
from DISClib.ADT import list as lt
import timeit
assert config

# ___________________________________________________
#  Variables
# ___________________________________________________

file1 = '201801-1-citibike-tripdata.csv'
file2 = '201801-2-citibike-tripdata.csv'
file3 = '201801-3-citibike-tripdata.csv'
file4 = '201801-4-citibike-tripdata.csv'
file5 = '201801-1-citibike-tripdata-small.csv'
filename = file1
recursionLimit = 8000

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
    print("5- Ruta turistica de menor tiempo / Estaciones criticas (REQ 3)")
    print("6- Ruta turistica por resistencia (REQ 4)")
    print("7- Recomendador de rutas (REQ 5)")
    print("8- Ruta de interes turistico (REQ 6)")
    print("9- Identificación de Estaciones para Publicidad (REQ 7) - Bono")
    print("10- Identificación de Bicicletas para Mantenimiento (REQ 8) - Bono")
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
    station1 = input("\nIngrese ID de la estación 1: ") 
    station2 = input("\nIngrese ID de la estación 2: ")
    print('\nEl número de componentes conectados es: ' +
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
    initialStation = input("\nIngrese el ID de la estación inicial: ")
    print("\nAhora ingrese su tiempo disponible en minutos: ")
    availableTime1 = int(input("\nEntre: "))
    availableTime2 = int(input("\nHasta: "))
    controller.circularRoutes(citibike, availableTime1, availableTime2, initialStation)

def optionFive():
    """
    Req 3
    """
    llegada, salida, menosUsadas = controller.criticStations(citibike)

    print(f'Las 3 estaciones en el TOP de llegada: <{lt.getElement(llegada,1)}>, <{lt.getElement(llegada,2)}>, <{lt.getElement(llegada,3)}>')
    print(f'Las 3 estaciones en el TOP de salida: <{lt.getElement(salida,1)}>, <{lt.getElement(salida,2)}>, <{lt.getElement(salida,3)}>')
    print(f'Las 3 estaciones en el TOP de menos usadas: <{lt.getElement(menosUsadas,1)}>, <{lt.getElement(menosUsadas,2)}>, <{lt.getElement(menosUsadas,3)}>')
    
def optionSix():
    """
    Req 4
    """  
    var = True
    while var:
        tiempoMax = input("\nTiempo máximo de resistencia (Minutos): ")
        idEstacionInicial = input("ID estación inicial: ")
        try:
            tiempoMax, idEstacionInicial = int(tiempoMax), int(idEstacionInicial)
        except ValueError:
            print('Ingrese valores validos')
        else:
            var = False
    listaRutas = controller.rutaPorResistencia(citibike, tiempoMax, idEstacionInicial)
    if listaRutas == []:
        print('\nNO HAY RUTAS CON UN TIEMPO MENOR O IGUAL A', tiempoMax,'\n')
    else:
        print('\nRUTAS TURISTICAS DESDE LA ESTACION', idEstacionInicial, 'CON', tiempoMax, 'MINUTOS\n',listaRutas,'\n')

def optionSeven():
    """
    Req 5
    """    
    print('\nRANGOS DE EDAD\n', '<0-10> , <11-20> , <21-30> , <31-40> , <41-50> , <51-60> , <60+>\n')
    var = True
    while var:
        edad1 = input('\nIngrese el PRIMER numero del rango de edad del turista:')
        edad2 = input('Ingrese el SEGUNDO numero del rango de edad del turista:')
        try:
            edad1, edad2 = int(edad1), int(edad2)
        except ValueError:
            print('\nIngrese valores validos')
        else:
            var = False
    recomendadorRutas = controller.recomendadorPorAños(citibike, edad1, edad2)
    if recomendadorRutas == []:
        print('\nNo hay rutas en este rango de edad.\n')
    else:
        print('\nEstacion Inicial - Año \n', recomendadorRutas)

def optionEight():
    """
    Req 6
    """
    centi = True
    while centi:
        latAct = input('Latitud Actual\n')
        lonAct = input('Longitud Actual\n')
        latDes = input('Latitud Destino\n')
        lonDes = input('Longitud Destino\n')
        try:
            latAct, lonAct, latDes, lonDes = float(latAct),float(lonAct),float(latDes),float(lonDes)
        except ValueError:
            print('Ingrese coordenadas validas')
        else:
            centi = False

    nearStationActual, nearStationDestiny, tripTime, stationList = controller.turistInteres(citibike, latAct, lonAct, latDes, lonDes)

    print(f'La estacion mas cercana a su ubicacion actual es: <{nearStationActual[1]}>')
    print(f'La estacion mas cercana a su ubicacion destino es: <{nearStationDestiny[1]}>')
    print(f'El tiempo estimado de viaje es: <{tripTime}>')
    print('La lista de estaciones en la ruta es:\n<')
    if stationList is not None:
        for item in range(lt.size(stationList)):
            station = lt.getElement(stationList, item)
            print(f'\t{item+1}) De {station[0]} a {station[1]}')
    else: print('\tNo hay estaciones de por medio')
    print('>')

def optionNine():
    """
    Req 7
    """
    edad = int(input('Ingrese su edad\n'))
    temp = (edad-1)//10 if edad > 0 else 0
    temp = temp if edad < 61 else 6
    if temp < 6:
        sup = (temp+1)*10
        inf = (temp*10)+1 if temp > 0 else 0
    team = f'{inf}-{sup}' if temp < 6 else f'{61}+'
    
    stationsStartStopTrips = controller.ageStations(citibike, temp)

    print(f'En el rango de edad <{team}>:')
    for i in range(lt.size(stationsStartStopTrips)):
        info = lt.getElement(stationsStartStopTrips, i)
        print(f'{i+1}-> Entrada <{info[0]}>, Salida <{info[1]}>, Con {info[2]} viajes registrados')

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
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(optionEight, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 9:
        executiontime = timeit.timeit(optionNine, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))

    elif int(inputs) == 10:
        executiontime = timeit.timeit(optionTen, number=1)
        print("\nTiempo de ejecución: " + str(executiontime))
    
    else:
        sys.exit(0)

sys.exit(0)
