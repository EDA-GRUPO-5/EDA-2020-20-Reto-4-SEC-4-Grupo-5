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
from datetime import date 

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
               'coords': None,
               'in_out': None
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

    citibike['in_out'] = m.newMap(numelements=1000,
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
    addInOutStation(citibike, trip)

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

def addInOutStation(citibike, trip):

    entryI = m.get(citibike['in_out'], trip['start station id'])

    if entryI is None:
        m.put(citibike['in_out'], trip['start station id'], (0,0))
        entryI = m.get(citibike['in_out'], trip['start station id'])
    
    inNumberI = entryI['value'][0]
    outNumberI = entryI['value'][1]

    m.put(citibike['in_out'], trip['start station id'],(inNumberI,outNumberI+1))

    entryO = m.get(citibike['in_out'], trip['end station id'])

    if entryO is None:
        m.put(citibike['in_out'], trip['end station id'], (0,0))
        entryO = m.get(citibike['in_out'], trip['end station id'])
    

    inNumberO = entryO['value'][0]
    outNumberO = entryO['value'][1]

    m.put(citibike['in_out'], trip['end station id'],(inNumberO+1,outNumberO))
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
    elif (route2 is None) or (route1 > route2):
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
    Req 3
    """
    #Listas respuesta
    topLlegada = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    lt.addLast(topLlegada, None); lt.addLast(topLlegada, None); lt.addLast(topLlegada, None)

    topSalida = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    lt.addLast(topSalida, None); lt.addLast(topSalida, None); lt.addLast(topSalida, None)

    intopUsadas = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    lt.addLast(intopUsadas, None); lt.addLast(intopUsadas, None); lt.addLast(intopUsadas, None)

    #Listas para obtener el top 3
    top3Ltemp = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    top3Stemp = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)
    inTop3temp = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareroutes)

    inVertexOut = m.valueSet(citibike['in_out'])
    
    for inout in range(lt.size(inVertexOut)):
        value = lt.getElement(inVertexOut, inout)

        lt.addLast(top3Ltemp, value[0])
        lt.addLast(top3Stemp, value[1])
        lt.addLast(inTop3temp, value[0]+value[1])
        
    #Para obtener el top
    ms.mergesort(top3Ltemp, greatequal)
    ms.mergesort(top3Stemp, greatequal)
    ms.mergesort(inTop3temp, lessequal)
    
    #Para obtener IDS
    top3Ltemp = lt.subList(top3Ltemp, 1, 3)
    top3Stemp = lt.subList(top3Stemp, 1, 3)
    inTop3temp = lt.subList(inTop3temp, 1, 3)


    vxl = 1
    vertIn = m.keySet(citibike['in_out'])

    while vxl <= lt.size(vertIn) and lt.size(topLlegada) <= 3:
        key = lt.getElement(vertIn, vxl)
        d = m.get(citibike['in_out'], key)
        pos = lt.isPresent(top3Ltemp, d['value'][0])

        if pos != 0: #Si el elemento esta en la lista
            stat = getStation(citibike, d['key'])[1] #Se obtiene el nombre
            lt.changeInfo(topLlegada, pos, stat)#Se ubica en la lista de respuesta
            lt.changeInfo(top3Ltemp, pos, None)#Se "elimina" de la lista temp para evitar puestos repetidos
        vxl +=1


    vxs = 1
    vertOut = m.keySet(citibike['in_out'])
    
    while vxs <= lt.size(vertOut) and lt.size(topSalida) <= 3:
        key = lt.getElement(vertOut, vxs)
        d = m.get(citibike['in_out'], key)
        pos = lt.isPresent(top3Stemp, d['value'][1])

        if pos != 0:
            stat = getStation(citibike, d['key'])[1]
            lt.changeInfo(topSalida, pos, stat)
            lt.changeInfo(top3Stemp, pos, None)
        vxs +=1


    vxNot = 1
    vertNot = m.keySet(citibike['in_out'])
    
    while vxNot <= lt.size(vertNot) and lt.size(intopUsadas) <= 3:
        key = lt.getElement(vertNot, vxNot)
        d = m.get(citibike['in_out'], key)
        x = d['value'][0]+d['value'][1]
        pos = lt.isPresent(inTop3temp, x)
        
        if pos != 0:
            stat = getStation(citibike, d['key'])[1]
            lt.changeInfo(intopUsadas, pos, stat)
            lt.changeInfo(inTop3temp, pos, None)
        vxNot +=1

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

def recomendadorPorAños(citibike, edad1, edad2):
    """
    Recomendador de rutas por rango de edad
    req 5
    """
    year = citibike['components']
    valueList = om.valueSet(year)
    keyList = om.keySet(year)
    lista = lt.newList(datastructure='ARRAY_LIST')
    resultado = lt.newList(datastructure='ARRAY_LIST')
    for i in range(om.size(year)):
        value = lt.getElement(valueList, i) #Value -> Año
        key = lt.getElement(keyList, i)
        lt.addLast(lista, (key, value))
    for i in lista['elements']:
        valores = int(i[1])
        today = date.today() #Fecha Actual
        anioActual = today.year #Año Actual
        anio = anioActual - valores #Diferencia de años -> años
        if anio in range(edad1, edad2 + 1):
            lt.addLast(resultado, i)
    return resultado['elements']

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
    Args:
    citibike: El archivo en total; idStation el id de la estacion a buscar.
    Returns: Id y Nombre de la estacion
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
