import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Cargar los datos
data = pd.read_csv('Salamanca-MOD11A1-061-results.csv')
print("Datos cargados")

# Mostrar las primeras filas del DataFrame
print(data.head())

# Convertir la columna de fecha a tipo datetime especificando el formato
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%y')
print("Fechas convertidas")

# Convertir temperaturas de Kelvin a Celsius
data['Temperature_C'] = data['MOD11A1_061_LST_Day_1km'] - 273.15
print("Temperaturas convertidas a Celsius")

# Verificar valores después de la conversión
print("Valores de temperatura (C) después de la conversión:")
print(data['Temperature_C'].describe())

# Filtrar datos donde la temperatura es válida (mayor que 0)
data = data[data['Temperature_C'] > -273.15]  # Temperatura mínima en Celsius
print("Datos filtrados para temperaturas válidas")

# Graficar las temperaturas a lo largo del tiempo usando la columna en Celsius
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Temperature_C'], marker='o', linestyle='-', label='Temperatura (°C)')
plt.title('Temperaturas en Celsius a lo largo del tiempo')
plt.xlabel('Fecha')
plt.ylabel('Temperatura (°C)')
plt.grid()
plt.legend()

# Guardar la gráfica como imagen
plt.savefig('temperaturas_a_lo_largo_del_tiempo.png')  # Guardar la imagen en formato PNG
print("Gráfica guardada como imagen")

# Extraer características útiles (como el día del año)
data['DayOfYear'] = data['Date'].dt.dayofyear
print("Día del año extraído")

# Definir las variables independientes (X) y dependientes (y)
X = data[['DayOfYear']]
y = data['Temperature_C']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Datos divididos en entrenamiento y prueba")

# Crear y entrenar el modelo
model = LinearRegression()
model.fit(X_train, y_train)
print("Modelo entrenado")

# Hacer predicciones
y_pred = model.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Crear fechas futuras (por ejemplo, 5 días después de la última fecha en el conjunto de datos)
future_dates = pd.date_range(start=data['Date'].max() + pd.Timedelta(days=1), periods=5)
future_day_of_year = future_dates.dayofyear
print("Fechas futuras creadas")

# Crear un DataFrame para las fechas futuras
future_X = pd.DataFrame({'DayOfYear': future_day_of_year})

# Hacer predicciones
future_predictions = model.predict(future_X)

# Crear un DataFrame para las predicciones futuras
predictions_df = pd.DataFrame({'Date': future_dates, 'Predicted_Temperature_C': future_predictions})

# Exportar las predicciones a un archivo JSON
predictions_df.to_json('predicciones_temperaturas.json', orient='records', date_format='iso')
print("Predicciones exportadas a JSON")

# Mostrar las predicciones
print(predictions_df)
