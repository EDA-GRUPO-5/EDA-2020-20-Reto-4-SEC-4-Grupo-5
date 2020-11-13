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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo


def newCitibike():

    citibike = {
               'stations': None,
               'connections': None,
               'components': None,
               }
    
    citibike['stations'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStations)
    
    citibike['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=compareStations)


def addSationConnection(citibike, laststation, station):
    origin = formatVertex(laststation)
    destination = formatVertex(station)
    cleanServiceDuration(laststation, station)
    duration = float(station['tripduration']) - float(laststation['tripduration'])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
    addRouteStation(citibike, station)
    addRouteStation(citibike, laststation)
    return citibike


def addRouteStation(citibike, station):
    entry = m.get(citibike['stations'], station['end station id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, station['start station id'])
        m.put(citibike['stations'], citibike['end station id'], lstroutes)
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

def sameCC(citibike, satation1, station2):
    return scc.stronglyConnected(ciitbike, satation1, station2)

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