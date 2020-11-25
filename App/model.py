from os import cpu_count
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.ADT import orderedmap as om
from math import cos, asin, sqrt, pi
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# =====================================================
#                       API
# =====================================================

# Funciones para agregar informacion al grafo

def newCitibike():

    citibike = {
               'stations': None,
               'connections': None,
               'idName_stations': None,
               'components': None,
               'coords': None#,
               #'triptime': None
               }
    
    citibike['stations'] = m.newMap(numelements=1000,
                                    maptype='PROBING',
                                    comparefunction=compareStations)
    
    citibike['name_IDstations'] = m.newMap(numelements=1000,
                                            comparefunction=compareStations)
    
    citibike['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=compareStations)

    citibike['coords'] = om.newMap(omaptype='BST',
                                    comparefunction=compareStations)
    
    return citibike

def addStationRoute(citibike, trip):
    start = trip['start station id']
    end = trip['end station id']
    duration = float(trip['tripduration'])

    addStation(citibike, start); addStation(citibike, end)
    addRoute(citibike, start, end, duration)

    #addTime(citibike, trip)

    #Req 3
    addStationName(citibike, trip)

    #Req 6
    #addStationCoords(citibike, trip)
    return citibike

# ==============================
# Funciones de Load
# ==============================

def addStation(citibike, station):

    if not gr.containsVertex(citibike['connections'], station):
        gr.insertVertex(citibike['connections'], station)

    return citibike

def addRoute(citibike, start, end, duration):

    edge = gr.getEdge(citibike['connections'], start, end)
    
    if edge is None:
        gr.addEdge(citibike['connections'], start, end, duration)

    else:
        gr.addEdgeCount(citibike['connections'], edge)
        #gr.promediateWeight(citibike['connections'], edge)

"""def addTime(citibike, trip):
    mapTrip = m.get(citibike['triptime'], trip['start station name'])
    if mapTrip is None:
        m.put(citibike['triptime'], trip['start station name'], trip['tripduration'])
    return citibike"""

def addStationName(citibike, station):
    """
    Para el req 3
    """
    entry = citibike['name_IDstations']
    stationStart = station['start station id']
    stationEnd = station['end station id']
    if not m.contains(entry, stationStart):
            m.put(citibike['name_IDstations'], stationStart, station['start station name'])
    else:
        m.put(citibike['name_IDstations'], stationEnd, station['end station name'])
        
    if not m.contains(entry, stationEnd):
            m.put(citibike['name_IDstations'], stationEnd, station['end station name'])
    else:
        m.put(citibike['name_IDstations'], stationStart, station['start station name'])
    
    return citibike

def addStationCoords(citibike, trip):
    """
    Para el req 6
    """
    entry = citibike['coordStation']
    stationStart = str((trip['start station latitude'], trip['start station longitude']))
    stationEnd = str((trip['end station latitude'], trip['end station longitude']))
    if not om.contains(entry, stationStart):
        om.put(entry, stationStart, trip['start station id'])

    if not om.contains(entry, stationEnd):
        om.put(entry, stationEnd, trip['end station id'])
    return citibike

def totalConnections(citibike):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(citibike['connections'])

def totalStations(citibike):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(citibike['connections'])

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(station, keyvaluestation):
    """
    Compara dos estaciones
    """
    stationid = keyvaluestation['key']
    if (station == stationid):
        return 0
    elif (station > stationid):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

# ==============================
# Funciones de Requerimientos
# ==============================

def criticStations(citibike):
    """
    Top 3 Llegada, Top 3 Salida y Top 3 menos usadas
    """
    #Listas respuesta
    topLlegada = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    topSalida = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    intopUsadas = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)

    #Listas temporales para obtener el top 3
    top3LS = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    inTop3 = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)

    tempLT = lt.newList(cmpfunction=compareroutes)
    ltKeys = gr.edges(citibike['connections'])
    for arc in range(1, lt.size(ltKeys)+1):
        lt.addLast(tempLT, lt.getElement(ltKeys, arc)['count'])

    ms.mergesort(tempLT, greatequal)

    for i in range(1,4):
        lt.addLast(top3LS, lt.getElement(tempLT, i))
    for i in range(3):
        lt.addLast(inTop3, lt.getElement(tempLT, lt.size(tempLT)-i))

    vxl = 1
    while vxl <= lt.size(tempLT) and lt.size(topLlegada) <= 3:
        if lt.isPresent(top3LS, lt.getElement(ltKeys, vxl)['count']):
            vxA = getStation(citibike, lt.getElement(ltKeys, vxl)['vertexA'])[1]
            lt.addLast(topLlegada, vxA)
        vxl +=1

    vxs = 1
    while vxs <= lt.size(tempLT) and lt.size(topSalida) <= 3:
        if lt.isPresent(top3LS, lt.getElement(ltKeys, vxs)['count']):
            vxB = getStation(citibike, lt.getElement(ltKeys, vxs)['vertexB'])[1]
            lt.addLast(topSalida, vxB)
        vxs +=1

    vxin = 1
    while vxin <= lt.size(tempLT) and lt.size(intopUsadas) <= 3:
        if lt.isPresent(inTop3, lt.getElement(ltKeys, vxin)['count']):
            vxA =  getStation(citibike, lt.getElement(ltKeys, vxin)['vertexA'])[1]
            if not lt.isPresent(intopUsadas, vxA):
                lt.addLast(intopUsadas, vxA)
        vxin +=1

    return topLlegada, topSalida, intopUsadas

def rutaPorResistencia(citibike, tiempoMax, idEstacionInicial):
    """
    Rutas turisticas por resistencia
    Req 4
    """
    ltEdges = gr.edges(citibike['connections']) #Vertices - Peso arcos
    for i in range(1, lt.size(ltEdges)+1): 
        station = lt.getElement(ltEdges, i) #Estacion final - Estacion inicial (id) -> str
        if str(idEstacionInicial) == station['vertexA']: #Identificar los que tienen el mismo idEstacionInicial
            duration = station['weight']/60 #Duracion (tripduration) en minutos
            duration = round(duration,2)
            if duration <= tiempoMax:
                rutasLista = lt.newList(datastructure='ARRAY_LIST')
                lt.addFirst(rutasLista, station['vertexA'])
                lt.addLast(rutasLista, station['vertexB'])
                lt.addLast(rutasLista, duration)
                print (rutasLista['elements'])

def turistInteres(citibike, latitudActual, longitudActual, latitudDestino, longitudDestino):
    """
    Estacion mas cercana a la posicion actual, Estacion mas cercana al destino, (Menor) Tiempo estimado, Lista de estaciones para llegar al destino
    """
    #Primero encontrar las dos estaciones mas cercanas a las dos posiciones, despues usando el grafo para calcular el tiempo
    # Se usa el grafo o se usa otra estructura de datos?
    #Arbol (maybe)
    actualNearStation, destinyNearStation = None, None
    tripTime = 0
    stationList = lt.newList()
    lt.addFirst(stationList, 'Ninguno')

    return actualNearStation, destinyNearStation, tripTime, stationList

def ageStations(citibike, team):
    """
    Lista de tuplas con las parejas Entrada, Salida y la cantidad de viajes
    """
    rta = lt.newList()
    lt.addFirst(rta, (None, None, 0))

    return rta

#=-=-=-=-=-=-=-=-=-=-=-=
#Funciones usadas
#=-=-=-=-=-=-=-=-=-=-=-=

def lessequal(k1,k2=None):
    if k2 == None:
        return True
    return k1 <= k2

def greatequal(k1,k2=None):
    return not(lessequal(k1,k2))

def getStation(citibike, idStation, e_s_a=0):
    """
    Args:\n
    citibike: El archivo en total; idStation el vertice <end station id>-<start station id>; e_s_a: end = 0, start = 1, any = 2 o mas para obtener el vertice buscado
    """
    idStation = idStation.split('-')
    e_s_a = e_s_a if e_s_a < 2 else 0
    if m.contains(citibike['idName_stations'], idStation[e_s_a]):
        keyValue = m.get(citibike['idName_stations'], idStation[e_s_a])
        return (keyValue['key'], keyValue['value'])
    return None, None

#Harvesine Formula
#Nota: Tarda menos que importar harvesine (por 0.02 ms)
def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a)) #2*radio*asin(...)
