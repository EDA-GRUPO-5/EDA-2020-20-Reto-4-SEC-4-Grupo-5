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
               }
    
    citibike['stations'] = m.newMap(numelements=1000,
                                    maptype='PROBING',
                                    comparefunction=compareStations)
    
    citibike['idName_stations'] = m.newMap(numelements=1000,
                                            comparefunction=compareStations)
    
    citibike['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=compareStations)
    return citibike


def addStationConnection(citibike, laststation, station):
    origin = formatVertex(laststation)
    destination = formatVertex(station)
    cleanServiceDuration(laststation, station)
    duration = float(station['tripduration']) - float(laststation['tripduration'])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
    addRouteStation(citibike, station)
    addRouteStation(citibike, laststation)

    addIdName(citibike, laststation)
    addIdName(citibike, station)

    return citibike


def addRouteStation(citibike, station):
    entry = m.get(citibike['stations'], station['end station id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, station['start station id'])
        m.put(citibike['stations'], station['end station id'], lstroutes)
    else:
        lstroutes = entry['value']
        info = station['start station id']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return citibike


def addRoutConnections(citibike):
    lststations = m.keySet(citibike['stations'])
    stationsiterator = it.newIterator(lststations)
    while it.hasNext(stationsiterator):
        key = it.next(stationsiterator)
        lstroutes = m.get(citibike['stations'], key)['value']
        prevrout = None
        routeiterator = it.newIterator(lstroutes)
        while it.hasNext(routeiterator):
            route = key + '-' + it.next(routeiterator)
            if prevrout is not None:
                addConnection(citibike, prevrout, route, 0)
                addConnection(citibike, route, prevrout, 0)
            prevrout = route


def addTrip(citibike, trip):

    origin = trip['start station id']
    destination =  trip['end station id']
    duration = int(trip['tripduration'])
    
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)

    return citibike


def addStation(citibike, stationid):
    
    if not gr.containsVertex(citibike['connections'], stationid):
            gr.insertVertex(citibike['connections'], stationid)
    return citibike

def addConnection(citibike, origin, destination, duration):

    edge = gr.getEdge(citibike['connections'], origin, destination)

    if edge is None:
        gr.addEdge(citibike['connections'], origin, destination, duration)
    
    return citibike

def addIdName(citibike, station):
    entry = citibike['idName_stations']
    stationStart = station['start station id']
    stationEnd = station['end station id']
    if not m.contains(entry, stationStart):
            m.put(citibike['idName_stations'], stationStart, station['start station name'])
    else:
        m.put(citibike['idName_stations'], stationEnd, station['end station name'])
        
    if not m.contains(entry, stationEnd):
            m.put(citibike['idName_stations'], stationEnd, station['end station name'])
    else:
        m.put(citibike['idName_stations'], stationStart, station['start station name'])
    
    return citibike

# ==============================
# Funciones de consulta
# ==============================

def totalStations(citibike):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(citibike['connections'])

def totalConnections(citibike):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(citibike['connections'])

def numSCC(citibike):

    citibike['components'] = scc.KosarajuSCC(citibike['connections'])
    return scc.connectedComponents(citibike['components'])

def sameSCC(citibike, station1, station2):
    return scc.stronglyConnected(citibike, station1, station2)

# ==============================
# Funciones Helper
# ==============================

def cleanServiceDuration(laststation, station):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if station['tripduration'] == '':
        station['tripduration'] = 0
    if laststation['tripduration'] == '':
        laststation['tripduration'] = 0

def formatVertex(station):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = station['end station id'] + '-'
    name = name + station['start station id']
    return name

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
    topLlegada = lt.newList(datastructure='ARRAY_LIST')
    topSalida = lt.newList(datastructure='ARRAY_LIST')
    intopUsadas = lt.newList(datastructure='ARRAY_LIST')

    #Listas temporales para obtener el top 3
    countLlegada = lt.newList(datastructure='ARRAY_LIST')
    countSalida = lt.newList(datastructure='ARRAY_LIST')
    incountUsadas = lt.newList(datastructure='ARRAY_LIST')

    ltKeys = gr.vertices(citibike['connections'])
    for st in range(1, lt.size(ltKeys)+1):
        stationVx = lt.getElement(ltKeys, st)
        inVx = gr.indegree(citibike['connections'], stationVx)
        outVx = gr.outdegree(citibike['connections'], stationVx)
        deVx = gr.degree(citibike['connections'], stationVx)

        lt.addLast(countLlegada, inVx)
        lt.addLast(countSalida, outVx)
        lt.addLast(incountUsadas, deVx)

    top3L = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    top3S = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    inTop3 = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)

    #Ordenar las 3 listas para despues obtener los 3 valores que esten en el top
    ms.mergesort(countLlegada, greatequal)
    ms.mergesort(countSalida, greatequal)
    ms.mergesort(incountUsadas, lessequal)

    for i in range(1,4):
        lt.addLast(top3L, lt.getElement(countLlegada, i))
        lt.addLast(top3S, lt.getElement(countSalida, i))
        lt.addLast(inTop3, lt.getElement(incountUsadas, i))


    Vxl = 1
    while lt.size(topLlegada) < 3 and Vxl <= lt.size(ltKeys):
        stationVxl = lt.getElement(ltKeys, Vxl)
        if lt.isPresent(top3L, gr.indegree(citibike['connections'], stationVxl)):
            stationNameL = getStation(citibike, stationVxl, 0)
            lt.addLast(topLlegada, stationNameL[1])
        Vxl += 1

    Vxs = 1
    while lt.size(topSalida) < 3 and Vxs <= lt.size(ltKeys):
        stationVxs = lt.getElement(ltKeys, Vxs)
        if lt.isPresent(top3S, gr.outdegree(citibike['connections'], stationVxs)):
            stationNameS = getStation(citibike, stationVxs, 1)
            lt.addLast(topSalida, stationNameS[1])
        Vxs += 1

    Vxi = 1
    while lt.size(intopUsadas) < 3 and Vxi <= lt.size(ltKeys):
        stationVxi = lt.getElement(ltKeys, Vxi)
        if lt.isPresent(inTop3, gr.degree(citibike['connections'], stationVxi)):
            stationNameI = getStation(citibike, stationVxi, 2)
            lt.addLast(intopUsadas, stationNameI[1])
        Vxi += 1

    return topLlegada, topSalida, intopUsadas



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