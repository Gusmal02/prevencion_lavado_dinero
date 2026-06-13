# Technical Documentation: Machine Learning and Data Modeling Specification

## English Version

### Data Engineering and Feature Selection
The analytical core of the pipeline utilizes Know Your Customer (KYC) metrics combined with transactional behavioral data. To ensure accurate segmentation, the following features were engineered and selected:
* `ingreso_mensual_declarado`: Baseline continuous variable representing the client's self-reported monthly income.
* `monto_efectivo_recibido`: Cumulative continuous variable tracking total physical cash inflows (`DEPOSITO_EFECTIVO`) during the monitored period.
* `monto_enviado`: Cumulative continuous variable tracking total monetary outflows.
* `inconsistencia_efectivo`: Calculated feature defining the absolute divergence between physical cash transactions and declared baseline income. To prevent mathematical failure, if the declared income is 0, the absolute cash amount is mapped directly instead of raising an undefined ratio.
* `inconsistencia_salidas`: Calculated feature defining the structural ratio of money leaving the account versus total inflows.

### Data Preprocessing & Mathematical Hardening
To eliminate scale bias in distance-based calculations, continuous variables are processed using standard standardization (Z-score scaling):
$$z = \frac{x - \mu}{\sigma}$$

#### Vectorized Exception Handling (Zero-Division Mitigation)
In financial data modeling, clients with an income profile of 0 cause execution crashes when evaluating risk ratios. The pipeline implements a vectorized conditioning block using `numpy.where`:
$$\text{inconsistencia\_efectivo} = \begin{cases} \text{monto\_efectivo\_recibido}, & \text{if } \text{ingreso\_mensual\_declarado} = 0 \\ \frac{\text{monto\_efectivo\_recibido}}{\text{ingreso\_mensual\_declarado}}, & \text{otherwise} \end{cases}$$
This architecture guarantees that the script executes natively without generating infinite (`inf`) or undefined (`nan`) values, ensuring full operational reproducibility under automated testing.

### Unsupervised Machine Learning Model
The segmentation layer uses the K-Means Clustering algorithm. Hyperparameter optimization was achieved using the Elbow Method and Silhouette Analysis.
* **Algorithm:** K-Means (Scikit-Learn)
* **Optimal Clusters (K):** 5
* **Initialization:** k-means++ (to prevent suboptimal local convergence)
* **Maximum Iterations:** 300
* **Random State:** 42 (for complete pipeline reproducibility)

#### Model Persistence (Serialization)
The pipeline isolates and saves model parameters in binary format using `joblib`. This decouples the training execution phase from the execution phase of new inferences:
* `scaler.pkl`: Serialized `StandardScaler` state.
* `kmeans_model.pkl`: Trained state of the cluster definitions.

#### Cluster Descriptions and Risk Topologies:
* **Cluster 0:** Standard low-risk retail clients. High correlation between declared income and transactional volumes.
* **Cluster 1:** High-net-worth individuals. Elevated transactional velocity but consistent with high historical income thresholds.
* **Cluster 2:** Dormant accounts or low-activity profiles.
* **Cluster 3:** High-velocity outflow profiles. Immediate dissipation of funds post-ingestion.
* **Cluster 4:** Critical high-risk profile (Structuring / Smurfing). Characterized by continuous cash deposits executed just below the legal reporting thresholds by individuals with low declared incomes. The pipeline isolated exactly **577 high-risk anomalies** belonging to this segment.

### Power BI Data Modeling and Relational Architecture
The business intelligence layer converts flat data assets into an optimized star schema variant. 

#### Relational Schemas:
* **Dimension Table:** `perfil_clientes_clusters` (Primary Key: `id_cliente`)
* **Fact Table:** `alertas_finales_optimizadas` (Foreign Key: `id_cliente_origen`)

#### Relationship Properties:
* **Cardinality:** One-to-Many (1:*) from `perfil_clientes_clusters` to `alertas_finales_optimizadas`.
* **Cross-Filter Direction:** Single. This ensures strict unidirectional propagation of data constraints from the machine learning profiles down to individual transactional alerts.
* **Character Encoding:** UTF-8 to preserve localized alphanumeric formatting.

---

## Versión en Español

### Ingeniería de Características y Selección de Variables
El núcleo analítico del pipeline utiliza métricas de Know Your Customer (KYC) combinadas con datos de comportamiento transaccional. Para garantizar una segmentación precisa, se desarrollaron y seleccionaron las siguientes variables:
* `ingreso_mensual_declarado`: Variable continua base que representa los ingresos mensuales autodeclarados por el cliente.
* `monto_efectivo_recibido`: Variable continua acumulativa que registra las entradas totales de efectivo físico (`DEPOSITO_EFECTIVO`) durante el período monitoreado.
* `monto_enviado`: Variable continua acumulativa que registra las salidas monetarias totales.
* `inconsistencia_efectivo`: Característica calculada que define la divergencia absoluta entre las transacciones en efectivo físico y los ingresos base declarados. Si el ingreso es 0, se asigna el monto bruto en efectivo para evitar indeterminaciones.
* `inconsistencia_salidas`: Característica calculada que define la relación estructural del dinero que sale de la cuenta frente a las entradas totales.

### Preprocesamiento de Datos y Blindaje Matemático
Para eliminar el sesgo de escala en los cálculos basados en distancias, las variables continuas se procesaron utilizando el método de estandarización estándar (Z-score):
$$z = \frac{x - \mu}{\sigma}$$

#### Manejo de Excepciones Vectorizadas (Mitigación de División por Cero)
En el modelado de datos financieros, los clientes con perfiles de ingresos en 0 provocan caídas de ejecución al evaluar coeficientes de riesgo. El pipeline implementa un bloque de condicionamiento vectorizado mediante `numpy.where`:
$$\text{inconsistencia\_efectivo} = \begin{cases} \text{monto\_efectivo\_recibido}, & \text{si } \text{ingreso\_mensual\_declarado} = 0 \\ \frac{\text{monto\_efectivo\_recibido}}{\text{ingreso\_mensual\_declarado}}, & \text{en otro caso} \end{cases}$$
Esta arquitectura garantiza que el script se ejecute de forma nativa sin generar valores infinitos (`inf`) o no definidos (`nan`), asegurando la reproducibilidad operativa bajo pruebas automatizadas.

### Modelo de Aprendizaje Automático No Supervisado
La capa de segmentación utiliza el algoritmo de clusterización K-Means. La optimización de hiperparámetros se logró mediante el Método del Codo y el Análisis de Silueta.
* **Algoritmo:** K-Means (Scikit-Learn)
* **Clústeres Óptimos (K):** 5
* **Inicialización:** k-means++ (para evitar una convergencia local subóptima)
* **Iteraciones Máximas:** 300
* **Random State:** 42 (para una reproducibilidad completa del pipeline)

#### Persistencia del Modelo (Serialización)
El pipeline aísla y guarda los parámetros del modelo en formato binario utilizando `joblib`. Esto desacopla la fase de entrenamiento de la fase de ejecución de nuevas inferencias:
* `scaler.pkl`: Estado serializado del `StandardScaler`.
* `kmeans_model.pkl`: Estado entrenado de las definiciones de los clústeres.

#### Descripción de Clústeres y Topologías de Riesgo:
* **Clúster 0:** Clientes minoristas estándar de bajo riesgo. Alta correlación entre ingresos declarados y volúmenes transaccionales.
* **Clúster 1:** Personas de alto patrimonio neto. Elevada velocidad transaccional pero consistente con altos umbrales de ingresos históricos.
* **Clúster 2:** Cuentas inactivas o perfiles de baja actividad.
* **Clúster 3:** Perfiles de salida de alta velocidad. Disipación inmediata de fondos tras la recepción de los mismos.
* **Clúster 4:** Perfil crítico de alto riesgo (Estructuración / Smurfing). Caracterizado por depósitos continuos en efectivo ejecutados justo por debajo de los umbrales legales de reporte por personas con bajos ingresos declarados. El pipeline aisló exactamente **577 anomalías críticas** pertenecientes a este segmento.

### Modelado de Datos de Power BI y Arquitectura Relacional
La capa de inteligencia de negocio convierte los activos de datos planos en una variante de esquema en estrella optimizada.

#### Esquemas Relacionales:
* **Tabla de Dimensión:** `perfil_clientes_clusters` (Clave Primaria: `id_cliente`)
* **Tabla de Hechos:** `alertas_finales_optimizadas` (Clave Foránea: `id_cliente_origen`)

#### Propiedades de la Relación:
* **Cardinalidad:** Uno a varios (1:*) desde `perfil_clientes_clusters` hacia `alertas_finales_optimizadas`.
* **Dirección de Filtro Cruzado:** Único. Esto garantiza una propagación unidireccional estricta de las restricciones de datos desde los perfiles de aprendizaje automático hacia las alertas transaccionales individuales.
* **Codificación de Caracteres:** UTF-8 para preservar el formato alfanumérico localizado.