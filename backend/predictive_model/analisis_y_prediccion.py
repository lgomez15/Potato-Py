import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Cargar los datos desde la nueva ruta
data = pd.read_csv('SalamancaLST.csv')

# Convertir la columna de fecha a tipo datetime (corregido formato)
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

# Filtrar las filas con valores de -273.15 (indicando temperaturas inválidas)
data = data[data['LST_Day_Celsius'] > -273.15]

# Graficar las temperaturas a lo largo del tiempo
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['LST_Day_Celsius'], marker='o', linestyle='-', label='Temperatura (°C)')
plt.title('Temperaturas en Celsius a lo largo del tiempo')
plt.xlabel('Fecha')
plt.ylabel('Temperatura (°C)')
plt.grid()
plt.legend()

# Guardar la gráfica como imagen
plt.savefig('temperaturas_a_lo_largo_del_tiempo.png')
print("Gráfica guardada como imagen")

# Extraer características útiles (como el día del año)
data['DayOfYear'] = data['Date'].dt.dayofyear

# Definir las variables independientes (X) y dependientes (y)
X = data[['DayOfYear']]
y = data['LST_Day_Celsius']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Hacer predicciones
y_pred = model.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Crear fechas futuras (por ejemplo, 5 días después de la última fecha en el conjunto de datos)
future_dates = pd.date_range(start=data['Date'].max() + pd.Timedelta(days=1), periods=5)
future_day_of_year = future_dates.dayofyear

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
