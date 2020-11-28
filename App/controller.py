import config as cf
from App import model
import csv

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
    for station in input_file:
        model.addStationRoute(citibike, station)
    
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

def circularRoutes(citibike, availableTime1, availableTime2, initialStation):
    """
    Rutas circulares
    Req 2
    """
    model.circularRoutes(citibike, availableTime1, availableTime2, initialStation)

def criticStations(citibike):
    """
    Top 3 Llegada, Top 3 Salida y Top 3 menos usadas\n
    Req 3
    """
    return model.criticStations(citibike)

def rutaPorResistencia(citibike, tiempoMax, idEstacionInicial):
    """
    Rutas turisticas por resistencia
    Req 4
    """
    return model.rutaPorResistencia(citibike, tiempoMax, idEstacionInicial)

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
