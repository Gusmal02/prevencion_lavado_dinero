import argparse
import logging
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib

# Configuración de Logging para producción
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def validar_esquema(df: pd.DataFrame, columnas_esperadas: list, nombre_dataset: str):
    columnas_faltantes = [col for col in columnas_esperadas if col not in df.columns]
    if columnas_faltantes:
        logging.error(f"Error de esquema en {nombre_dataset}. Faltan columnas: {columnas_faltantes}")
        raise ValueError(f"Esquema inválido en {nombre_dataset}")
    logging.info(f"Validación de esquema exitosa para {nombre_dataset}.")

def procesar_pipeline(data_dir: str, output_dir: str, mode: str):
    try:
        base_path = Path(data_dir)
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        ruta_tx = base_path / 'fact_transacciones.csv'
        ruta_clientes = base_path / 'dim_clientes.csv'

        if not ruta_tx.exists() or not ruta_clientes.exists():
            raise FileNotFoundError("No se encontraron los archivos CSV dentro de la carpeta especificada.")

        logging.info("Iniciando ingesta de datos transaccionales y maestros...")
        df_tx = pd.read_csv(ruta_tx)
        df_clientes = pd.read_csv(ruta_clientes)

        columnas_tx = ['id_transaccion', 'id_cliente_origen', 'id_cliente_destino', 'monto', 'tipo_transaccion']
        columnas_cli = ['id_cliente', 'nombre_cliente', 'ingreso_mensual_declarado', 'ocupacion']
        
        validar_esquema(df_tx, columnas_tx, "Fact Transacciones")
        validar_esquema(df_clientes, columnas_cli, "Dim Clientes")

        df_tx = df_tx.drop_duplicates(subset=['id_transaccion'])

        logging.info("Ejecutando ingeniería de características...")
        if (df_clientes['ingreso_mensual_declarado'] < 0).any():
            df_clientes['ingreso_mensual_declarado'] = df_clientes['ingreso_mensual_declarado'].clip(lower=0)

        efectivo_recibido = df_tx[df_tx['tipo_transaccion'] == 'DEPOSITO_EFECTIVO'].groupby('id_cliente_origen')['monto'].sum()
        monto_enviado = df_tx.groupby('id_cliente_origen')['monto'].sum()

        df_features = df_clientes.copy()
        df_features['monto_efectivo_recibido'] = df_features['id_cliente'].map(efectivo_recibido).fillna(0)
        df_features['monto_enviado'] = df_features['id_cliente'].map(monto_enviado).fillna(0)

        df_features['inconsistencia_efectivo'] = np.where(
            df_features['ingreso_mensual_declarado'] == 0,
            df_features['monto_efectivo_recibido'],
            df_features['monto_efectivo_recibido'] / df_features['ingreso_mensual_declarado']
        )
        
        df_features['inconsistencia_salidas'] = np.where(
            df_features['monto_efectivo_recibido'] == 0,
            0,
            df_features['monto_enviado'] / df_features['monto_efectivo_recibido']
        )

        features_cols = ['ingreso_mensual_declarado', 'monto_efectivo_recibido', 'monto_enviado', 
                         'inconsistencia_efectivo', 'inconsistencia_salidas']

        scaler_file = out_path / 'scaler.pkl'
        model_file = out_path / 'kmeans_model.pkl'

        if mode == 'train':
            logging.info("Modo ENTRENAMIENTO: Calculando parámetros del modelo...")
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(df_features[features_cols])
            
            model = KMeans(n_clusters=5, init='k-means++', max_iter=300, random_state=42)
            model.fit(X_scaled)
            
            joblib.dump(scaler, scaler_file)
            joblib.dump(model, model_file)
            logging.info("Modelos entrenados y guardados con éxito.")
        else:
            logging.info("Modo INFERENCIA: Cargando artefactos desde disco...")
            if not scaler_file.exists() or not model_file.exists():
                raise FileNotFoundError("Modelos no encontrados. Ejecute el script primero con '--mode train'.")
            scaler = joblib.load(scaler_file)
            model = joblib.load(model_file)
            X_scaled = scaler.transform(df_features[features_cols])

        df_features['cluster_comportamiento'] = model.predict(X_scaled)
        df_features['sospechoso_ml'] = np.where(df_features['cluster_comportamiento'] == 4, 1, 0)

        df_alertas_raw = df_tx[df_tx['tipo_transaccion'] == 'DEPOSITO_EFECTIVO'].copy()
        df_alertas_finales = df_alertas_raw.merge(
            df_features[['id_cliente', 'nombre_cliente', 'ocupacion', 'cluster_comportamiento', 'sospechoso_ml']],
            left_on='id_cliente_origen',
            right_on='id_cliente',
            how='inner'
        )

        df_optimizadas = df_alertas_finales[df_alertas_finales['sospechoso_ml'] == 1].copy()
        df_optimizadas = df_optimizadas.drop(columns=['id_cliente'])

        # Guardamos los resultados directamente sobre tu estructura existente de data_sintetica
        df_features.to_csv(out_path / 'perfil_clientes_clusters.csv', index=False)
        df_optimizadas.to_csv(out_path / 'alertas_finales_optimizadas.csv', index=False)
        
        logging.info(f"Procesamiento concluido. Archivos generados en: {out_path}")
        logging.info(f"Casos críticos de alto riesgo detectados: {len(df_optimizadas)}")

    except Exception as e:
        logging.critical(f"Falla catastrófica: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pipeline PLD/FT")
    parser.add_argument('--data_dir', type=str, default='data_sintetica', help='Carpeta de entrada')
    parser.add_argument('--output_dir', type=str, default='data_sintetica', help='Carpeta de salida')
    parser.add_argument('--mode', type=str, choices=['train', 'predict'], default='predict')
    
    args = parser.parse_args()
    procesar_pipeline(args.data_dir, args.output_dir, args.mode)