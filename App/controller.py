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

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    citibike = model.newCitibike()
    return citibike

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadFile(citibike, tripfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    laststation = None
    for station in input_file:
        if laststation is not None:
            samestation = laststation['start station id'] == station['start station id']
            samedirection = laststation['end station id'] == station['end station id']
            if samestation and samedirection:
                model.addStationConnection(citibike, laststation, station)
        laststation = station
    model.addRoutConnections(citibike)
    return citibike

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def totalStations(citibike):
    """
    Total de estaciones de bicicleta
    """
    return model.totalStations(citibike)

def totalConnections(citibike):
    """
    Total de enlaces entre las estaciones
    """
    return model.totalConnections(citibike)

def numSCC(citibike):
    """
    Numero de componentes fuertemente conectados
    """
    return model.numSCC(citibike)

def sameSCC(citibike, station1, station2):
    """
    Numero de componentes fuertemente conectados
    """
    return model.sameSCC(citibike, station1, station2)

# ___________________________________________________
#  Funciones para Reqs
# ___________________________________________________

def criticStations(citibike):
    """
    Top 3 Llegada, Top 3 Salida y Top 3 menos usadas\n
    Req 3
    """
    return model.criticStations(citibike)

def turistInteres(citibike, latitudActual, longitudActual, latitudDestino, longitudDestino):
    """
    Estacion mas cercana a la posicion actual, Estacion mas cercana al destino, (Menor) Tiempo estimado, Lista de estaciones para llegar al destino\n
    Req 6
    """
    return model.turistInteres(citibike, latitudActual, longitudActual, latitudDestino, longitudDestino)

def ageStations(citibike, team):
    """
    Lista de tuplas con las parejas Entrada, Salida y la cantidad de viajes\n
    Req 7
    """
    return model.ageStations(citibike, team)