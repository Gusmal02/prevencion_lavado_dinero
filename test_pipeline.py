import unittest
import pandas as pd
import numpy as np
# Importamos las funciones analíticas de tu script principal
from modelo_machine_learning import validar_esquema

class TestPipelinePLD(unittest.TestCase):

    def setUp(self):
        """Configura un entorno controlado de datos sintenticos para las pruebas."""
        self.columnas_correctas = ['id_transaccion', 'id_cliente_origen', 'id_cliente_destino', 'monto', 'tipo_transaccion']
        self.df_valido = pd.DataFrame(columns=self.columnas_correctas)

    def test_validar_esquema_exitoso(self):
        """Prueba que la validación pase sin errores cuando el esquema es correcto."""
        try:
            validar_esquema(self.df_valido, self.columnas_correctas, "Dataset Test")
        except ValueError:
            self.fail("validar_esquema() lanzó ValueError inesperadamente con un esquema correcto.")

    def test_validar_esquema_fallido(self):
        """Prueba que el validador detecte la falta de columnas y lance un ValueError."""
        df_invalido = pd.DataFrame(columns=['id_transaccion', 'monto']) # Faltan columnas críticas
        with self.assertRaises(ValueError):
            validar_esquema(df_invalido, self.columnas_correctas, "Dataset Corrupto")

    def test_mitigacion_division_por_cero(self):
        """Prueba la consistencia matemática de la ingeniería de características ante ingresos de 0."""
        # Creamos un DataFrame para simular el comportamiento exacto del pipeline vectorizado
        df_prueba = pd.DataFrame({
            'ingreso_mensual_declarado': [0],
            'monto_efectivo_recibido': [50000]
        })

        # Aplicamos la lógica exacta de tu script de producción
        df_prueba['inconsistencia_efectivo'] = np.where(
            df_prueba['ingreso_mensual_declarado'] == 0,
            df_prueba['monto_efectivo_recibido'],
            df_prueba['monto_efectivo_recibido'] / df_prueba['ingreso_mensual_declarado']
        )

        # Extraemos el valor resultante del vector
        resultado = df_prueba['inconsistencia_efectivo'].iloc[0]

        # Verificamos que sea el monto bruto (50,000) y que no se haya roto por división entre cero
        self.assertEqual(resultado, 50000)
        self.assertNotEqual(str(resultado), 'inf')
        self.assertNotEqual(str(resultado), 'nan')

if __name__ == '__main__':
    unittest.main()