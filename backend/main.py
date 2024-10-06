from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic.fields import Field
from datetime import datetime, timedelta
from typing import List
import joblib
import random, time
import numpy as np
import time
import httpx
import meteoKeys as keys
from cors import configure_cors

# Cargar el modelo previamente entrenado
modelo_cargado = joblib.load('modelo_xgboost_entrenado.pkl')

#Constantes
API_URL = "https://api.meteomatics.com"

app = FastAPI()

#Configurar CORS
configure_cors(app)

#Modelo para las peticiones
class WeatherRequest(BaseModel):
    datetime: datetime
    data_type: str
    latitude: float
    longitude: float
    response_format: str = Field(default="json", pattern=r"^(json|html|xml)$")

# Modelo de datos para la respuesta de humedad
class HumidityResponse(BaseModel):
    timestamp: float
    humidity: float
    
class Sensor(BaseModel):
    id: int
    name: str
    humedadDetectada: float

class PlantData(BaseModel):
    week_of_year: int
    row: int
    column: int
    plant_id: int
    stem_diameter: float
    highest_truss: float
    temp_mean: float
    temp_min: float
    temp_max: float
    humidity_mean: float
    humidity_min: float
    humidity_max: float

# Variable para almacenar la humedad anterior
previous_humidity = None

async def petitions(url, request):
    # Autenticación para la API
    auth = (keys.USERNAME, keys.PASSWORD)

    # Realizar la petición a la API de Meteomatics
    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=auth)

    # Manejar errores de la API
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener datos de Meteomatics")

    # Devolver la respuesta de la API de Meteomatics
    return response.json() if request.response_format == "json" else response.text


@app.get("/")
def read_root():
    return {"message": "Hello World"}

#Returns the weather data for the given datetime, data type, latitude, longitude, and response format
@app.get("/weather/{datetime}/{data_type}/{latitude},{longitude}/{response_format}")
async def getWeather(datetime: str, data_type: str, latitude: float, longitude: float, response_format: str):

    # Crear una instancia de WeatherRequest
    try:
        request = WeatherRequest(
            datetime=datetime,
            data_type=data_type,
            latitude=latitude,
            longitude=longitude,
            response_format=response_format
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Construir la URL para la API de Meteomatics
    url = f"{API_URL}/{request.datetime.isoformat()}/{request.data_type}/{request.latitude},{request.longitude}/{request.response_format}"

    # Autenticación para la API
    auth = (keys.USERNAME, keys.PASSWORD)

    # Realizar la petición a la API de Meteomatics
    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=auth)


    # Manejar errores de la API
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener datos de Meteomatics")

    # Devolver la respuesta de la API de Meteomatics
    return response.json() if request.response_format == "json" else response.text

#Returns the weather data (speed, direction, gusts) for the given datetime, latitude, and longitude
@app.get("/weather/wind/{datetime}/{latitude},{longitude}")
async def getWindStats(datetime: str, latitude: float, longitude: float):
    #Creo una instancia de WeatherRequest
    try:
        request = WeatherRequest(
            datetime=datetime,
            data_type="wind_speed_10m:kmh,wind_dir_10m:d,wind_gusts_10m_1h:kmh",
            latitude=latitude,
            longitude=longitude,
            response_format="json"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    #Construir la peticion para los datos de hoy
    url = f"{API_URL}/{request.datetime.isoformat()}/{request.data_type}/{request.latitude},{request.longitude}/{request.response_format}"

    return await petitions(url, request)

#Returns the precipitation data (last hour and last 24 hours) for the given datetime, latitude, and longitude
@app.get("/weather/precipitation/{datetime}/{latitude},{longitude}")
async def getPrecipitationStats(datetime: str, latitude: float, longitude: float):
    #Creo una instancia de WeatherRequest
    try:
        request = WeatherRequest(
            datetime=datetime,
            data_type="precip_1h:mm,precip_24h:mm",
            latitude=latitude,
            longitude=longitude,
            response_format="json"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    #Construir la peticion para los datos de hoy
    url = f"{API_URL}/{request.datetime.isoformat()}/{request.data_type}/{request.latitude},{request.longitude}/{request.response_format}"

    return await petitions(url, request)

#Returns a JSON with wind(speed, direction, gusts), precipitation(last hour and last 24 hours), temperature (now, max, min), precipitation data for the given datetime, latitude, and longitude
@app.get("/weather/{datetime}/{latitude},{longitude}")
async def getWeatherStats(datetime: str, latitude: float, longitude: float):
    #Creo una instancia de WeatherRequest
    try:
        request = WeatherRequest(
            datetime=datetime,
            data_type="wind_speed_10m:kmh,wind_dir_10m:d,wind_gusts_10m_1h:kmh,precip_1h:mm,precip_24h:mm,t_2m:C",
            latitude=latitude,
            longitude=longitude,
            response_format="json"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    #Construir la peticion para los datos de hoy
    url = f"{API_URL}/{request.datetime.isoformat()}/{request.data_type}/{request.latitude},{request.longitude}/{request.response_format}"

    return await petitions(url, request)

#Returns the weather data for the given datetime, data type, latitude, longitude
@app.get("/weather/week/{datetime}/{latitude},{longitude}")
async def getTemperatureWeek(datetime: str, latitude: float, longitude: float):
    #Recibo una fecha y pido los datos de la semana
    try:
        request = WeatherRequest(
            datetime=datetime,
            data_type="t_2m:C,t_max_2m_24h:C,t_min_2m_24h:C,precip_24h:mm",
            latitude=latitude,
            longitude=longitude,
            response_format="json"
        )

        # Crear la fecha equivalente a 7 días después del parámetro datetime
        fechaSemana = request.datetime + timedelta(days=7)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    #Construir la peticion para los datos de la semana
    url = f"{API_URL}/{request.datetime.isoformat()}--{fechaSemana.isoformat()}:P1D/{request.data_type}/{request.latitude},{request.longitude}/{request.response_format}"
    return await petitions(url, request)


def createArraySensors(num_sensors: List[Sensor]):
    sensors = []
    num_baja_humedad = round(num_sensors * 0.1)
    num_media_humedad = round(num_sensors * 0.2)
    num_alta_humedad = num_sensors - num_baja_humedad - num_media_humedad

    # Crear sensores con baja humedad
    for i in range(num_baja_humedad):
        sensor = Sensor(
            id=i,
            humedadDetectada=round(float(random.uniform(0, 25)), 2),
            name=f"Sensor {i}"
        )
        sensors.append(sensor)

    # Crear sensores con media humedad
    for i in range(num_baja_humedad, num_baja_humedad + num_media_humedad):
        sensor = Sensor(
            id=i,
            humedadDetectada=round(float(random.uniform(25, 75)), 2),
            name=f"Sensor {i}"
        )
        sensors.append(sensor)

    # Crear sensores con alta humedad
    for i in range(num_baja_humedad + num_media_humedad, num_sensors):
        sensor = Sensor(
            id=i,
            humedadDetectada=round(float(random.uniform(75, 100)), 2),
            name=f"Sensor {i}"
        )
        sensors.append(sensor)

    # Barajar los sensores para distribuirlos aleatoriamente
    random.shuffle(sensors)

    # Actualizar los IDs después de barajar
    for idx, sensor in enumerate(sensors):
        sensor.id = idx
        sensor.name = f"Sensor {idx}"

    return sensors

def criticSensors(sensorsArray):
    criticSensors = []
    for sensor in sensorsArray:
        if sensor.humedadDetectada <= 25:
            criticSensors.append(sensor)
    return criticSensors

def getNeighbors(sensorID, grid_size=3):
    neighbors = []
    row, col = divmod(sensorID, grid_size)
    
    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if (0 <= r < grid_size) and (0 <= c < grid_size) and (r != row or c != col):
                neighbors.append(r * grid_size + c)
                
    return neighbors

@app.get("/sensorsB/{num_sensors}")
def sendBadSensors(num_sensors:int):
    # Crear los sensores
    sensors = createArraySensors(num_sensors)
    
    # Encontrar los sensores criticos (humedad <= 25)
    critic_sensors = criticSensors(sensors)
    
    #encuentra los vecinos de los sensores criticos
    for sensor in critic_sensors:
        neighbors = getNeighbors(sensor.id)
        
        for neighbor in neighbors:
            sensors[neighbor].humedadDetectada -= (sensors[neighbor].humedadDetectada * 0.3)
            
    return sensors

@app.get("/sensorsG/{num_sensors}")
def sendGoodSensors(num_sensors: int):
    # Crear los sensores
    sensors = createArraySensors(num_sensors)
    
    for sensor in sensors:
        sensor.humedadDetectada = round(float(random.uniform(75, 100)), 2)
    return sensors

# Función para clasificar el resultado
def clasificar_crecimiento(prediccion):
    if prediccion < 30:
        return "bajo"
    elif 30 <= prediccion <= 35:
        return "medio"
    else:
        return "alto"
    
@app.post("/predict/")
def predict_growth(data: PlantData):
    # Crear un array con los datos recibidos
    entrada = np.array([[data.week_of_year, data.row, data.column, data.plant_id, 
                        data.stem_diameter, data.highest_truss, data.temp_mean, 
                        data.temp_min, data.temp_max, data.humidity_mean, 
                        data.humidity_min, data.humidity_max]])
    
    # Realizar la predicción con el modelo cargado
    prediccion = modelo_cargado.predict(entrada)[0]  # Obtener la predicción como un número
    
    # Convertir el resultado a un tipo de datos nativo de Python (float)
    prediccion = float(prediccion)
    
    # Clasificar el crecimiento en "bajo", "medio" o "alto"
    categoria = clasificar_crecimiento(prediccion)
    
    # Devolver la predicción y la categoría como respuesta
    return {
        "predicted_stem_growth": prediccion,
        "categoria": categoria
    }
    
