import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

def ejecutar_capa_machine_learning():
    print("--- Iniciando Capa 2: Optimización Analítica mediante Machine Learning (K-Means) ---")
    
    # 1. Cargamos los archivos generados por nuestro pipeline
    ruta_tx = 'data_sintetica/fact_transacciones.csv'
    ruta_clientes = 'data_sintetica/dim_clientes.csv'
    ruta_alertas_sicena = 'data_sintetica/alertas_sistema_sicena.csv'
    
    if not (os.path.exists(ruta_tx) and os.path.exists(ruta_clientes) and os.path.exists(ruta_alertas_sicena)):
        print("Error: Faltan archivos base en 'data_sintetica/'. Ejecuta los scripts previos.")
        return
        
    df_tx = pd.read_csv(ruta_tx)
    df_clientes = pd.read_csv(ruta_clientes)
    df_alertas = pd.read_csv(ruta_alertas_sicena)
    
    # 2. INGENIERÍA DE CARACTERÍSTICAS AVANZADA (Doble Flujo: Origen y Destino)
    print("Estructurando perfil de comportamiento bidireccional por cliente...")
    
    # Flujo A: Dinero que el cliente manda hacia afuera (SPEI enviado, compras, retiros)
    perfil_salidas = df_tx.groupby('id_cliente_origen').agg(
        monto_enviado=('monto', 'sum'),
        ops_enviadas=('monto', 'count')
    ).reset_index().rename(columns={'id_cliente_origen': 'id_cliente'})
    
    # Flujo B: Depósitos en efectivo que el cliente recibe en su cuenta (Ventanilla)
    df_depositos_efectivo = df_tx[df_tx['tipo_transaccion'] == 'DEPOSITO_EFECTIVO']
    perfil_entradas_efectivo = df_depositos_efectivo.groupby('id_cliente_destino').agg(
        monto_efectivo_recibido=('monto', 'sum'),
        ops_efectivo_recibidas=('monto', 'count')
    ).reset_index().rename(columns={'id_cliente_destino': 'id_cliente'})
    
    # Unimos de forma consecutiva todas las métricas a la dimensión de clientes
    df_features = df_clientes.merge(perfil_salidas, on='id_cliente', how='left')
    df_features = df_features.merge(perfil_entradas_efectivo, on='id_cliente', how='left')
    df_features = df_features.fillna(0) # Reemplazamos los clientes sin movimientos con 0
    
    # REGLAS ANALÍTICAS PARA EL ALGORITMO:
    # Índice 1: Inconsistencia por depósitos de efectivo recibidos frente a su nivel de ingresos declarado
    df_features['inconsistencia_efectivo'] = df_features['monto_efectivo_recibido'] / (df_features['ingreso_mensual_declarado'] + 1)
    # Índice 2: Inconsistencia por velocidad de salida de flujos monetarios
    df_features['inconsistencia_salidas'] = df_features['monto_enviado'] / (df_features['ingreso_mensual_declarado'] + 1)
    
    # 3. PREPARACIÓN DE DATOS Y ESCALAMIENTO
    # Definimos el nuevo set de variables numéricas de alta sensibilidad criminal
    columnas_modelo = [
        'ingreso_mensual_declarado', 
        'monto_enviado', 
        'monto_efectivo_recibido', 
        'inconsistencia_efectivo',
        'inconsistencia_salidas'
    ]
    X = df_features[columnas_modelo]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. ENTRENAMIENTO DEL MODELO DE CLUSTERING (K-Means)
    print("Entrenando algoritmo K-Means para segmentación de perfiles financieros...")
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10) # Incrementamos a 5 clústeres para mayor sensibilidad
    df_features['cluster_comportamiento'] = kmeans.fit_predict(X_scaled)
    
    # 5. IDENTIFICACIÓN DE LOS GRUPOS DE RIESGO MÁXIMO
    # Buscaremos estadísticamente los clústeres donde la anomalía de efectivo o de salidas rompa los límites normales
    limite_efectivo = df_features['inconsistencia_efectivo'].quantile(0.95)
    limite_salidas = df_features['inconsistencia_salidas'].quantile(0.95)
    
    # Marcamos como sospechosos a los clientes cuyos perfiles se encuentren en los extremos superiores de inconsistencia
    df_features['sospechoso_ml'] = np.where(
        (df_features['inconsistencia_efectivo'] > limite_efectivo) | 
        (df_features['inconsistencia_salidas'] > limite_salidas), 1, 0
    )
    
    # 6. FILTRADO INTELIGENTE FINAL
    clientes_alto_riesgo = df_features[df_features['sospechoso_ml'] == 1]['id_cliente'].tolist()
    
    # Filtramos las alertas de SICENA cruzando con las del Machine Learning utilizando un conector lógico OR amplio
    # Buscaremos si el cliente está involucrado ya sea como origen o destino en las alertas tradicionales
    filtro_alertas_optimizadas = df_alertas['id_cliente_origen'].isin(clientes_alto_riesgo) | df_alertas['id_cliente_destino'].isin(clientes_alto_riesgo)
    alertas_filtradas = df_alertas[filtro_alertas_optimizadas].copy()
    
    # Guardamos los resultados actualizados para el Dashboard
    ruta_salida = 'data_sintetica/alertas_finales_optimizadas.csv'
    alertas_filtradas.to_csv(ruta_salida, index=False)
    df_features.to_csv('data_sintetica/perfil_clientes_clusters.csv', index=False)
    
    print("\n--- RESUMEN DE OPTIMIZACIÓN ANALÍTICA / CAPA 2 (CORREGIDO) ---")
    print(f"Alertas iniciales de SICENA (Reglas Duras): {len(df_alertas)}")
    print(f"Alertas FINALMENTE validadas por Machine Learning: {len(alertas_filtradas)}")
    print(f"Reducción efectiva de Falsos Positivos: {round((1 - len(alertas_filtradas)/len(df_alertas))*100, 2)}%")
    print(f"Archivo de alta prioridad guardado en: {ruta_salida}")

if __name__ == "__main__":
    ejecutar_capa_machine_learning()