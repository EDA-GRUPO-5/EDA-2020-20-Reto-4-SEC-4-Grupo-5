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
from DISClib.ADT import stack as st
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
               'coords': None
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

    citibike['coords'] = m.newMap(numelements=1000,
                                comparefunction=compareStations)
    
    citibike['components'] = om.newMap(omaptype='BST',
                                    comparefunction=compareroutes)
 
    return citibike

def addStationRoute(citibike, trip):
    start = trip['start station id']
    end = trip['end station id']
    duration = float(trip['tripduration'])

    addStationToGraph(citibike, start)
    addStationToGraph(citibike, end)
    addRoute(citibike, start, end, duration)

    addStationToMap(citibike, trip)

    #Req 3
    addStationName(citibike, trip)

    #Req 6
    addStationCoords(citibike, trip)
    
    #Birth Year
    addBirthYear(citibike, trip)
    
    return citibike

# ==============================
# Funciones de Load
# ==============================

def addStationToGraph(citibike, station):

    if not gr.containsVertex(citibike['connections'], station):
        gr.insertVertex(citibike['connections'], station)

    return citibike

def addStationToMap(citibike, trip):
    entry = m.get(citibike['stations'], trip['end station id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, trip['start station id'])
        m.put(citibike['stations'], trip['end station id'], lstroutes)
    else:
        lstroutes = entry['value']
        info = trip['start station id']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return citibike

def addRoute(citibike, start, end, duration):

    edge = gr.getEdge(citibike['connections'], start, end)
    
    if edge is None:
        gr.addEdge(citibike['connections'], start, end, duration)

    else:
        gr.addEdgeCount(citibike['connections'], edge)
        #gr.promediateWeight(citibike['connections'], edge)

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
    entry = citibike['coords']
    stationStart = (trip['start station latitude'], trip['start station longitude'], 0)
    stationEnd = (trip['end station latitude'], trip['end station longitude'], 1)

    e1 = m.get(entry, trip['start station id'])
    if e1 is None:
        m.put(entry, trip['start station id'], stationStart)

    e2 = m.get(entry, trip['end station id'])
    if e2 is None:
        m.put(entry, trip['end station id'], stationEnd)

    return citibike

def addBirthYear(citibike, trip):
    """
    Para los REQs {}
    """
    entry = citibike['components']
    year = trip['birth year']

    if not om.contains(entry, int(trip['start station id'])):
        om.put(entry, int(trip['start station id']), year)

    if not om.contains(entry, int(trip['end station id'])):
        om.put(entry, int(trip['end station id']), year)

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

def numSCC(citibike):

    citibike['components'] = scc.KosarajuSCC(citibike['connections'])
    return scc.connectedComponents(citibike['components'])


def sameSCC(citibike, satation1, station2):
    return scc.stronglyConnected(citibike, satation1, station2)


def circularRoutes(citibike, availableTime1, availableTime2, initialStation):
    """
    Rutas circulares
    Req 2
    """
    ltEdges = gr.edges(citibike['connections'])
    numRutas = 0
    ltCircularRoutes = lt.newList(datastructure='ARRAY_LIST')
    
    for i in range(1, lt.size(ltEdges)+1): 
        station = lt.getElement(ltEdges, i)
        if str(initialStation) == station['vertexA']:
            finalStation = station['vertexB']
            try:
                arcoExiste = gr.getEdge(citibike['connections'], finalStation, initialStation)
                weightFinalStation = arcoExiste['weight']
                duration = station['weight'] + weightFinalStation
                if duration+20 >= availableTime1 and duration+20 <= availableTime2:
                    numRutas += 1
                    nameStartStation = getStation(citibike, initialStation)[1]
                    nameEndStation = getStation(citibike, finalStation)[1]
                    lt.addLast(ltCircularRoutes, (nameStartStation, nameEndStation, duration))
            except:
                pass   
    
    print("\nEl número de rutas circulares es " + str(numRutas) + " y estos son los datos: ")

    for i in range(1, lt.size(ltCircularRoutes)+1):
        print("\nNombre de estación inicial: " + str(lt.getElement(ltCircularRoutes, i)[0]))
        print("\nNombre de estación final: " + str(lt.getElement(ltCircularRoutes, i)[1]))
        print("\nDuración estimada: " + str(lt.getElement(ltCircularRoutes, i)[2]) + " minutos")


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

    for i in range(1,10):
        lt.addLast(top3LS, lt.getElement(tempLT, i))
    for i in range(3):
        lt.addLast(inTop3, lt.getElement(tempLT, lt.size(tempLT)-i))

    vxl = 1
    while vxl <= lt.size(tempLT) and lt.size(topLlegada) <= 3:
        if lt.isPresent(top3LS, lt.getElement(ltKeys, vxl)['count']):
            vxA = getStation(citibike, lt.getElement(ltKeys, vxl)['vertexA'])[1]
            if not lt.isPresent(topLlegada, vxA):
                lt.addLast(topLlegada, vxA)
        vxl +=1

    vxs = 1
    while vxs <= lt.size(tempLT) and lt.size(topSalida) <= 3:
        if lt.isPresent(top3LS, lt.getElement(ltKeys, vxs)['count']):
            vxB = getStation(citibike, lt.getElement(ltKeys, vxs)['vertexB'])[1]
            if not lt.isPresent(topLlegada, vxB):
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
    ltEdges = gr.edges(citibike['connections']) #Retornar lista con todos los arcos del arco (Vertices - Peso Arco)
    rutas = lt.newList(datastructure='ARRAY_LIST') #Lista vacia para agregar las rutas -> return 
    for i in range(1, lt.size(ltEdges)+1): 
        station = lt.getElement(ltEdges, i) #Estacion final - Estacion inicial (id) -> str
        if str(idEstacionInicial) == station['vertexA']: #Identificar los que tienen el mismo idEstacionInicial
            duration = station['weight']/60 #Duracion (tripduration) en minutos
            duration = round(duration, 2)
            if duration <= tiempoMax:
                lt.addLast(rutas, (station['vertexA'], station['vertexB'], duration))
    return rutas['elements']


def turistInteres(citibike, latitudActual, longitudActual, latitudDestino, longitudDestino):
    """
    Estacion mas cercana a la posicion actual, Estacion mas cercana al destino, (Menor) Tiempo estimado, Lista de estaciones para llegar al destino
    """
    actualNearStationID = destinyNearStationID = None

    coords = citibike['coords']
    actualNear = destinyNear = float('INF')
    keyList = m.keySet(coords)

    #Conseguir las estaciones mas cercanas al destino
    for i in range(m.size(coords)):
        key = lt.getElement(keyList, i)
        lat, lon, s_e = m.get(coords, key)['value']
        lat = float(lat); lon = float(lon)

        distanceToActual = distance(lat, lon, latitudActual, longitudActual)
        distanceToDestiny = distance(lat, lon, latitudDestino, longitudDestino)

        #s_e esta para verificar que sea entrada o salida
        if distanceToActual < actualNear and s_e == 0:
            actualNear = distanceToActual
            actualNearStationID = key
            
        if distanceToDestiny < destinyNear and s_e == 1:
            destinyNear = distanceToDestiny
            destinyNearStationID = key

    #Obtener el nombre
    actualNearStation = getStation(citibike, actualNearStationID)
    destinyNearStation = getStation(citibike, destinyNearStationID)

    #Usar Dijsktra para conseguir el resto de info
    structureActual = djk.Dijkstra(citibike['connections'], actualNearStationID)
    if djk.hasPathTo(structureActual, destinyNearStationID):
        tripTime = djk.distTo(structureActual, destinyNearStationID)
        stationStack = djk.pathTo(structureActual, destinyNearStationID)
    else:
        return (actualNearStation, destinyNearStation,float('INF'), None)

    #De stack a lista con la informacion pulida
    stationList = lt.newList(datastructure='ARRAY_LIST')
    for i in range(st.size(stationStack)):
        stationD = st.pop(stationStack)
        vA = getStation(citibike, stationD["vertexA"])[1]; vB = getStation(citibike, stationD["vertexB"])[1]
        lt.addLast(stationList, (vA, vB))

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

def getStation(citibike, idStation):
    """
    Args:\n
    citibike: El archivo en total; idStation el vertice <end station id>-<start station id>
    """
    if m.contains(citibike['name_IDstations'], idStation):
        keyValue = m.get(citibike['name_IDstations'], idStation)
        return (keyValue['key'], keyValue['value'])
    return None, None

#Harvesine Formula
#Nota: tarda menos que importar harvesine (por 0.02 s)
def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a)) #2*radio*asin(...)
