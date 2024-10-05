from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic.fields import Field
from datetime import datetime, timedelta
import random
import time
import httpx
import meteoKeys as keys
from cors import configure_cors

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

#Returns the weather data on a week for the given datetime, data type, latitude, longitude
@app.get("/weather/week/{datetime}/{latitude},{longitude}")
async def getWeatherWeek(datetime: str, latitude: float, longitude: float):
    #Recibo una fecha y pido los datos de la semana
    try:
        request = WeatherRequest(
            datetime=datetime,
            data_type="wind_speed_10m:kmh,wind_dir_10m:d,wind_gusts_10m_1h:kmh,precip_1h:mm,precip_24h:mm,t_2m:C",
            latitude=latitude,
            longitude=longitude,
            response_format="json"
        )

        # Crear la fecha equivalente a 7 días después del parámetro datetime
        fechaSemana = request.datetime + timedelta(days=7)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    #Construir la peticion para los datos de la semana
    url = f"{API_URL}/{request.datetime.isoformat()}--{fechaSemana.isoformat()}/{request.data_type}/{request.latitude},{request.longitude}/{request.response_format}"
    return await petitions(url, request)

# Función para simular los datos del sensor de humedad
def simulate_humidity():
    global previous_humidity
    
    if previous_humidity is None:
        # Inicializa con un valor aleatorio entre 70 y 75
        previous_humidity = round(random.uniform(70, 75), 2)
    
    # Ajusta el nuevo valor dentro de un rango pequeño, para mantener entre 70 y 75
    adjustment = random.uniform(-1, 1)  # Cambia en un rango de -1 a +1
    new_humidity = max(70, min(75, previous_humidity + adjustment))  # Mantener entre 70-75%
    
    previous_humidity = new_humidity  # Actualiza el valor anterior
    return round(new_humidity, 2)

# Ruta de la API que proporciona la humedad simulada
@app.get("/humidity", response_model=HumidityResponse)
async def get_humidity():
    simulated_humidity = simulate_humidity()
    return HumidityResponse(timestamp=time.time(), humidity=simulated_humidity)
