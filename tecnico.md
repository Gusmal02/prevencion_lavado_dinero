# Technical Documentation: Machine Learning and Data Modeling Specification

## English Version

### Data Engineering and Feature Selection
The analytical core of the pipeline utilizes Know Your Customer (KYC) metrics combined with transactional behavioral data. To ensure accurate segmentation, the following features were engineered and selected:
* `ingreso_mensual_declarado`: Baseline continuous variable representing the client's self-reported monthly income.
* `monto_efectivo_recibido`: Cumulative continuous variable tracking total physical cash inflows during the monitored period.
* `monto_enviado`: Cumulative continuous variable tracking total monetary outflows.
* `inconsistencia_efectivo`: Calculated feature defining the absolute divergence between physical cash transactions and declared baseline income.
* `inconsistencia_salidas`: Calculated feature defining the structural ratio of money leaving the account versus total inflows.

### Data Preprocessing
To eliminate scale bias in distance-based calculations, continuous variables were processed using the standard standardization method (Z-score scaling):
$$z = \frac{x - \mu}{\sigma}$$
This process guarantees that high-magnitude attributes (e.g., total transactional volume) do not artificially dominate attributes with smaller ranges (e.g., risk ratios).

### Unsupervised Machine Learning Model
The segmentation layer uses the K-Means Clustering algorithm. Hyperparameter optimization was achieved using the Elbow Method and Silhouette Analysis.
* **Algorithm:** K-Means
* **Optimal Clusters (K):** 5
* **Initialization:** k-means++ (to prevent suboptimal local convergence)
* **Maximum Iterations:** 300
* **Random State:** 42 (for complete pipeline reproducibility)

#### Cluster Descriptions and Risk Topologies:
* **Cluster 0:** Standard low-risk retail clients. High correlation between declared income and transactional volumes.
* **Cluster 1:** High-net-worth individuals. Elevated transactional velocity but consistent with high historical income thresholds.
* **Cluster 2:** Dormant accounts or low-activity profiles.
* **Cluster 3:** High-velocity outflow profiles. Immediate dissipation of funds post-ingestion.
* **Cluster 4:** Critical high-risk profile (Structuring / Smurfing). Characterized by continuous cash deposits executed just below the legal reporting thresholds by individuals with low declared incomes (e.g., students, unemployed).

### Power BI Data Modeling and Relational Architecture
The business intelligence layer converts flat data assets into an optimized star schema variant. 

#### Relational Schemas:
* **Dimension Table:** `perfil_clientes_clusters` (Primary Key: `id_cliente`)
* **Fact Table:** `alertas_finales_optimizadas` (Foreign Key: `id_cliente`)

#### Relationship Properties:
* **Cardinality:** One-to-Many (1:*) from `perfil_clientes_clusters` to `alertas_finales_optimizadas`.
* **Cross-Filter Direction:** Single. This ensures strict unidirectional propagation of data constraints from the machine learning profiles down to individual transactional alerts.
* **Character Encoding:** UTF-8 to preserve localized alphanumeric formatting.

---

## Versión en Español

### Ingeniería de Características y Selección de Variables
El núcleo analítico del pipeline utiliza métricas de Know Your Customer (KYC) combinadas con datos de comportamiento transaccional. Para garantizar una segmentación precisa, se desarrollaron y seleccionaron las siguientes variables:
* `ingreso_mensual_declarado`: Variable continua base que representa los ingresos mensuales autodeclarados por el cliente.
* `monto_efectivo_recibido`: Variable continua acumulativa que registra las entradas totales de efectivo físico durante el período monitoreado.
* `monto_enviado`: Variable continua acumulativa que registra las salidas monetarias totales.
* `inconsistencia_efectivo`: Característica calculada que define la divergencia absoluta entre las transacciones en efectivo físico y los ingresos base declarados.
* `inconsistencia_salidas`: Característica calculada que define la relación estructural del dinero que sale de la cuenta frente a las entradas totales.

### Preprocesamiento de Datos
Para eliminar el sesgo de escala en los cálculos basados en distancias, las variables continuas se procesaron utilizando el método de estandarización estándar (Z-score):
$$z = \frac{x - \mu}{\sigma}$$
Este proceso garantiza que los atributos de gran magnitud (por ejemplo, el volumen transaccional total) no dominen artificialmente a los atributos con rangos más pequeños (por ejemplo, los coeficientes de riesgo).

### Modelo de Aprendizaje Automático No Supervisado
La capa de segmentación utiliza el algoritmo de clusterización K-Means. La optimización de hiperparámetros se logró mediante el Método del Codo y el Análisis de Silueta.
* **Algoritmo:** K-Means
* **Clústeres Óptimos (K):** 5
* **Inicialización:** k-means++ (para evitar una convergencia local subóptima)
* **Iteraciones Máximas:** 300
* **Random State:** 42 (para una reproducibilidad completa del pipeline)

#### Descripción de Clústeres y Topologías de Riesgo:
* **Clúster 0:** Clientes minoristas estándar de bajo riesgo. Alta correlación entre ingresos declarados y volúmenes transaccionales.
* **Clúster 1:** Personas de alto patrimonio neto. Elevada velocidad transaccional pero consistente con altos umbrales de ingresos históricos.
* **Clúster 2:** Cuentas inactivas o perfiles de baja actividad.
* **Clúster 3:** Perfiles de salida de alta velocidad. Disipación inmediata de fondos tras la recepción de los mismos.
* **Clúster 4:** Perfil crítico de alto riesgo (Estructuración / Smurfing). Caracterizado por depósitos continuos en efectivo ejecutados justo por debajo de los umbrales legales de reporte por personas con bajos ingresos declarados (por ejemplo, estudiantes o desempleados).

### Modelado de Datos de Power BI y Arquitectura Relacional
La capa de inteligencia de negocio convierte los activos de datos planos en una variante de esquema en estrella optimizada.

#### Esquemas Relacionales:
* **Tabla de Dimensión:** `perfil_clientes_clusters` (Clave Primaria: `id_cliente`)
* **Tabla de Hechos:** `alertas_finales_optimizadas` (Clave Foránea: `id_cliente`)

#### Propiedades de la Relación:
* **Cardinalidad:** Uno a varios (1:*) desde `perfil_clientes_clusters` hacia `alertas_finales_optimizadas`.
* **Dirección de Filtro Cruzado:** Único. Esto garantiza una propagación unidireccional estricta de las restricciones de datos desde los perfiles de aprendizaje automático hacia las alertas transaccionales individuales.
* **Codificación de Caracteres:** UTF-8 para preservar el formato alfanumérico localizado.S