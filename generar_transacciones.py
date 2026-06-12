import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Fijamos las semillas para asegurar que los datos transaccionales coincidan siempre
random.seed(42)
np.random.seed(42)

def generar_historial_transacciones():
    print("--- Iniciando la generación de transacciones financieras masivas ---")
    
    # 1. Cargamos nuestra base de clientes existente
    ruta_clientes = 'data_sintetica/dim_clientes.csv'
    if not os.path.exists(ruta_clientes):
        print("Error: No se encontró dim_clientes.csv. Ejecuta primero generar_clientes.py")
        return
        
    df_clientes = pd.read_csv(ruta_clientes)
    lista_clientes = df_clientes['id_cliente'].tolist()
    
    # Creamos un diccionario rápido para cruzar el ingreso declarado de cada cliente
    ingresos_dict = dict(zip(df_clientes['id_cliente'], df_clientes['ingreso_mensual_declarado']))
    
    transacciones = []
    id_transaccion_actual = 1
    
    # Configuración de fechas (simularemos los últimos 30 días de operaciones)
    fecha_inicio = datetime.now() - timedelta(days=30)
    
    print("Generando comportamiento transaccional legítimo cotidiano...")
    # Generamos operaciones normales para todos los clientes
    for cliente in lista_clientes:
        ingreso = ingresos_dict[cliente]
        # Un cliente promedio hace entre 3 y 10 operaciones al mes
        num_ops = random.randint(3, 10)
        
        for _ in range(num_ops):
            # El monto promedio suele ser una fracción de sus ingresos declarados
            monto = round(random.uniform(100, ingreso * 0.3), 2)
            # Evitamos montos en 0
            if monto <= 0: monto = 50.0
                
            tipo_op = random.choice(['SPEI_RECIBIDO', 'SPEI_ENVIADO', 'COMPRA_TARJETA', 'RETIRO_CAJERO', 'DEPOSITO_EFECTIVO'])
            dias_extra = random.randint(0, 30)
            horas_extra = random.randint(0, 23)
            minutos_extra = random.randint(0, 59)
            fecha_op = fecha_inicio + timedelta(days=dias_extra, hours=horas_extra, minutes=minutos_extra)
            
            transacciones.append({
                'id_transaccion': f"TX-{id_transaccion_actual:07d}",
                'id_cliente_origen': cliente,
                'id_cliente_destino': random.choice(lista_clientes) if 'ENVIADO' in tipo_op else 'SISTEMA',
                'tipo_transaccion': tipo_op,
                'monto': monto,
                'fecha_hora': fecha_op.strftime('%Y-%m-%d %H:%M:%S'),
                'etiqueta_lavado': 0  # 0 significa operación legítima normal
            })
            id_transaccion_actual += 1

    print("Inyectando tipología criminal 1: 'Smurfing' (Pitufeo)...")
    # Elegiremos 5 clientes específicos de perfil 'Estudiante' o 'Desempleado' para corromper su historial
    clientes_sospechosos_smurfing = df_clientes[df_clientes['ocupacion'].isin(['Estudiante', 'Desempleado'])]['id_cliente'].head(5).tolist()
    
    for cliente_blanco in clientes_sospechosos_smurfing:
        fecha_ataque = fecha_inicio + timedelta(days=15) # Ocurre a mitad de mes
        
        # El pitufeo consiste en muchos depósitos chicos repetitivos para no encender alarmas de $15,000
        for i in range(8): 
            # Modificamos sutilmente los minutos para que ocurran casi al mismo tiempo (mismo día)
            fecha_op = fecha_attack = fecha_ataque + timedelta(minutes=i * 20)
            monto_pitufeo = round(random.uniform(14200, 14900), 2) # Justo abajo del límite regulatorio de control
            
            transacciones.append({
                'id_transaccion': f"TX-{id_transaccion_actual:07d}",
                'id_cliente_origen': 'VENTANILLA_EFECTIVO',
                'id_cliente_destino': cliente_blanco,
                'tipo_transaccion': 'DEPOSITO_EFECTIVO',
                'monto': monto_pitufeo,
                'fecha_hora': fecha_op.strftime('%Y-%m-%d %H:%M:%S'),
                'etiqueta_lavado': 1  # 1 mapea que este registro es lavado por Smurfing
            })
            id_transaccion_actual += 1

    print("Inyectando tipología criminal 2: 'Cuentas Puente' (Dispersión Inmediata)...")
    # Elegiremos 3 clientes comerciantes/empresarios para simular la recepción y vaciado de capital ilícito
    clientes_puente = df_clientes[df_clientes['ocupacion'] == 'Empresario / Comerciante']['id_cliente'].tail(3).tolist()
    
    for cp in tuple(clientes_puente):
        fecha_puente = fecha_inicio + timedelta(days=20)
        
        # Paso A: Recibe un golpe de dinero masivo (Inusual para cualquier cuenta)
        monto_enorme = 850000.00
        transacciones.append({
            'id_transaccion': f"TX-{id_transaccion_actual:07d}",
            'id_cliente_origen': 'CUENTA_DESCONOCIDA_EXTRANJERO',
            'id_cliente_destino': cp,
            'tipo_transaccion': 'SPEI_RECIBIDO',
            'monto': monto_enorme,
            'fecha_hora': fecha_puente.strftime('%Y-%m-%d %H:%M:%S'),
            'etiqueta_lavado': 1
        })
        id_transaccion_actual += 1
        
        # Paso B: Minutos después distribuye todo el dinero a 5 cuentas diferentes para pulverizar el rastro
        for j in range(5):
            fecha_dispersion = fecha_puente + timedelta(minutes=15 + (j * 2)) # Ocurre de inmediato
            monto_fraccion = round(monto_enorme / 5, 2)
            
            transacciones.append({
                'id_transaccion': f"TX-{id_transaccion_actual:07d}",
                'id_cliente_origen': cp,
                'id_cliente_destino': random.choice(lista_clientes),
                'tipo_transaccion': 'SPEI_ENVIADO',
                'monto': monto_fraccion,
                'fecha_hora': fecha_dispersion.strftime('%Y-%m-%d %H:%M:%S'),
                'etiqueta_lavado': 1
            })
            id_transaccion_actual += 1

    # Construimos el DataFrame global consolidado
    df_tx = pd.DataFrame(transacciones)
    
    # Ordenamos de forma cronológica real todas las operaciones para simular el paso del tiempo en el banco
    df_tx = df_tx.sort_values(by='fecha_hora').reset_index(drop=True)
    
    # Guardamos en la carpeta dedicada
    ruta_salida = 'data_sintetica/fact_transacciones.csv'
    df_tx.to_csv(ruta_salida, index=False)
    
    print(f"¡Éxito! Registros transaccionales masivos consolidados en: {ruta_salida}")
    print(f"Total de operaciones registradas en el libro diario: {len(df_tx)}")

if __name__ == "__main__":
    generar_historial_transacciones()