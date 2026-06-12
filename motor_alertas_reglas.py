import pandas as pd
import numpy as np
import os

def ejecutar_motor_alertas_tradicional():
    print("--- Iniciando Capa 1: Motor de Alertas por Reglas Tradicionales (Simulación SICENA) ---")
    
    # 1. Cargamos las transacciones y los clientes
    ruta_tx = 'data_sintetica/fact_transacciones.csv'
    ruta_clientes = 'data_sintetica/dim_clientes.csv'
    
    if not os.path.exists(ruta_tx) or not os.path.exists(ruta_clientes):
        print("Error: Faltan archivos base. Asegúrate de haber ejecutado los scripts anteriores.")
        return
        
    df_tx = pd.read_csv(ruta_tx)
    df_clientes = pd.read_csv(ruta_clientes)
    
    # Convertimos la columna de fecha a un formato que Python entienda como tiempo real
    df_tx['fecha_hora'] = pd.to_datetime(df_tx['fecha_hora'])
    
    # -------------------------------------------------------------------------
    # REGLA TRADICIONAL A: Control de Umbral en Efectivo (> $15,000 MXN)
    # -------------------------------------------------------------------------
    print("Analizando Regla A: Depósitos individuales en efectivo superiores al límite...")
    
    filtro_regla_a = (df_tx['tipo_transaccion'] == 'DEPOSITO_EFECTIVO') & (df_tx['monto'] > 15000)
    alertas_regla_a = df_tx[filtro_regla_a].copy()
    alertas_regla_a['tipo_alerta'] = 'UMBRAL_EFECTIVO_EXCEDIDO'
    
    # -------------------------------------------------------------------------
    # REGLA TRADICIONAL B: Monitoreo de Estructuración Avanzada (Smurfing / Pitufeo)
    # -------------------------------------------------------------------------
    print("Analizando Regla B: Detección de estructuración por acumulación en menos de 24 horas...")
    
    # Filtramos solo los depósitos en efectivo para buscar patrones sospechosos
    df_depositos = df_tx[df_tx['tipo_transaccion'] == 'DEPOSITO_EFECTIVO'].copy()
    
    # Ordenamos por cliente y fecha para poder agruparlos en ventanas de tiempo
    df_depositos = df_depositos.sort_values(by=['id_cliente_destino', 'fecha_hora'])
    
    alertas_smurfing_ids = []
    
    # Agrupamos por cada cliente de destino y evaluamos sus movimientos usando ventanas móviles
    for cliente, grupo in df_depositos.groupby('id_cliente_destino'):
        if len(grupo) >= 3: # Si tiene al menos 3 depósitos en el mes, investigamos de cerca
            # Establecemos al cliente como índice temporal para usar funciones de ventana de Pandas
            grupo_temporal = grupo.set_index('fecha_hora')
            
            # El truco: agrupamos en ventanas móviles de 24 horas ('24h') por cada transacción
            # Contamos cuántas operaciones se hicieron y cuánto sumaron en esa ventana de un día
            conteo_24h = grupo_temporal['monto'].rolling('24h').count()
            suma_24h = grupo_temporal['monto'].rolling('24h').sum()
            
            # REGLA DE NEGOCIO: Si en 24 horas hay más de 3 depósitos y suman más de $50,000 MXN
            condicion_sospecha = (conteo_24h >= 3) & (suma_24h > 50000)
            
            if condicion_sospecha.any():
                alertas_smurfing_ids.append(cliente)
                
    # Extraemos todas las transacciones asociadas a los clientes que activaron la alarma de estructuración
    alertas_regla_b = df_tx[df_tx['id_cliente_destino'].isin(alertas_smurfing_ids) & (df_tx['tipo_transaccion'] == 'DEPOSITO_EFECTIVO')].copy()
    alertas_regla_b['tipo_alerta'] = 'ESTRUCTURACION_SMURFING_DETECTADA'
    
    # -------------------------------------------------------------------------
    # CONSOLIDACIÓN Y GUARDADO DE ALERTAS
    # -------------------------------------------------------------------------
    # Juntamos las alertas encontradas por ambas reglas en un único archivo
    df_alertas_totales = pd.concat([alertas_regla_a, alertas_regla_b]).drop_duplicates(subset=['id_transaccion'])
    
    # Cruzamos datos con la tabla de clientes para saber sus nombres y ocupaciones reales en el reporte
    df_reporte_alertas = df_alertas_totales.merge(
        df_clientes[['id_cliente', 'nombre_cliente', 'ocupacion', 'ingreso_mensual_declarado']], 
        left_on='id_cliente_destino', 
        right_on='id_cliente', 
        how='left'
    )
    
    # Guardamos nuestro primer reporte de auditoría institucional
    ruta_salida = 'data_sintetica/alertas_sistema_sicena.csv'
    df_reporte_alertas.to_csv(ruta_salida, index=False)
    
    print("\n--- RESUMEN DE COMPLIANCE / CAPA 1 ---")
    print(f"Total de alertas emitidas automáticamente por SICENA: {len(df_reporte_alertas)}")
    print(f"Alertas guardadas exitosamente en: {ruta_salida}")

if __name__ == "__main__":
    ejecutar_motor_alertas_tradicional()
    