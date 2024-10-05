from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time

app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para la respuesta de humedad
class HumidityResponse(BaseModel):
    timestamp: float
    humidity: float

# Variable para almacenar la humedad anterior
previous_humidity = None

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time

app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para la respuesta de humedad
class HumidityResponse(BaseModel):
    timestamp: float
    humidity: float

# Variable para almacenar la humedad anterior
previous_humidity = None

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
