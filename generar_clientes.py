import pandas as pd
import numpy as np
from faker import Faker
import random
import os

# Inicializamos 'Faker' con la configuración de México ('es_MX')
# Esto nos dará nombres y estructuras lógicas de nuestro entorno local.
fake = Faker('es_MX')

# Fijamos una 'semilla' (seed) para que los datos aleatorios sean siempre los mismos.
# Esto asegura que si corres el script hoy o mañana, generes los mismos clientes exactos.
random.seed(42)
np.random.seed(42)

def crear_dimension_clientes(num_clientes=5000):
    print(f"--- Iniciando la generación de {num_clientes} perfiles de clientes (KYC) ---")
    
    # REGLA DE NEGOCIO INSTITUCIONAL: En un banco, cada ocupación tiene un perfil de riesgo
    # y un rango de ingresos mensuales estimado.
    # Formato: (Ingreso Mínimo, Ingreso Máximo, Riesgo Inicial asignado por Ley)
    perfiles_ingresos = {
        'Estudiante': (2000, 8000, 'Bajo'),
        'Empleado Sector Privado': (12000, 45000, 'Medio'),
        'Profesionista Independiente': (15000, 60000, 'Medio'),
        'Empresario / Comerciante': (50000, 250000, 'Alto'),
        'Jubilado': (5000, 18000, 'Bajo'),
        'Desempleado': (0, 4000, 'Alto')  # Riesgo Alto: Si no hay origen claro de ingresos, se vigila más.
    }
    
    lista_ocupaciones = list(perfiles_ingresos.keys())
    lista_clientes = []
    
    for i in range(1, num_clientes + 1):
        # Generamos un ID institucional único para el cliente (Ej: CLI-00001)
        id_cliente = f"CLI-{i:05d}"
        
        # Faker se encarga de inventar un nombre completo realista
        nombre = fake.name()
        
        # Seleccionamos una ocupación al azar
        ocupacion = random.choice(lista_ocupaciones)
        
        # Extraemos los límites y el riesgo configurados en nuestra regla de negocio superior
        min_ingreso, max_ingreso, riesgo_kyc = perfiles_ingresos[ocupacion]
        
        # Generamos un ingreso mensual simulado dentro de su rango correspondiente
        ingreso_declarado = round(random.uniform(min_ingreso, max_ingreso), 2)
        
        # Simulamos la fecha en la que el cliente abrió su cuenta (en los últimos 3 años)
        fecha_alta = fake.date_between(start_date='-3y', end_date='today')
        
        # Guardamos los datos ordenados en un diccionario para este cliente
        lista_clientes.append({
            'id_cliente': id_cliente,
            'nombre_cliente': nombre,
            'ocupacion': ocupacion,
            'ingreso_mensual_declarado': ingreso_declarado,
            'nivel_riesgo_kyc': riesgo_kyc,
            'fecha_alta_sistema': fecha_alta
        })
        
    # Convertimos nuestra lista de diccionarios en un DataFrame de Pandas (una tabla formal)
    df_clientes = pd.DataFrame(lista_clientes)
    
    # Definimos dónde guardaremos el archivo resultante
    ruta_salida = 'data_sintetica/dim_clientes.csv'
    df_clientes.to_csv(ruta_salida, index=False)
    
    print(f"¡Éxito! Archivo de Dimensión de Clientes guardado en: {ruta_salida}")
    return df_clientes

# Bloque de seguridad para ejecutar el código desde la terminal
if __name__ == "__main__":
    # Nos aseguramos de que la carpeta de destino exista
    os.makedirs('data_sintetica', exist_ok=True)
    crear_dimension_clientes(num_clientes=5000)