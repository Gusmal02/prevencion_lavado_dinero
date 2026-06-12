# Financial Intelligence Pipeline: ML-Driven AML/CFT Transaction Monitoring

## English Version

### Project Overview
This project implements an advanced Anti-Money Laundering (AML) and Counter-Financing of Terrorism (CFT) transaction monitoring pipeline. By combining traditional rule-based compliance systems with unsupervised machine learning (K-Means Clustering), this solution optimizes financial auditing workflows. It significantly reduces false positives, isolates anomalous behavioral profiles, and provides an interactive executive dashboard for operational decision-making.

### Problem Statement
Traditional transaction monitoring systems (such as the legacy SICENA framework) generate high volumes of alerts based on rigid, static thresholds. This approach results in an overwhelming number of false positives, causing operational fatigue for compliance analysts and delaying the identification of complex financial crimes such as structuring (smurfing).

### Solution Architecture
The pipeline is structured into three continuous layers:
1. **Rule-Based Ingestion:** Simulates transaction ingestion and triggers preliminary alerts based on regulatory thresholds.
2. **Analytical Optimization (Machine Learning):** Applies an unsupervised K-Means algorithm in Python to analyze behavioral inconsistencies (cash discrepancies, transactional velocity, and declared monthly income), segmenting users into specialized risk profiles.
3. **Executive Visualization & Audit Ledger:** An interactive Power BI dashboard connected directly to the pipeline's output, allowing the Compliance Officer to filter data dynamically by cluster and audit specific client profiles.

### Key Metrics and Business Impact
* **False Positive Reduction:** Operational alerts requiring urgent manual review were reduced from the initial batch down to 492 prioritized cases, optimizing analyst efficiency.
* **Capital Under Investigation:** Successfully isolated and tracked 188 million MXN across anomalous clusters.
* **Risk Concentration:** Identified high-risk clusters (such as Cluster 4), exposing specific profiles (e.g., students or unemployed individuals) executing structural cash deposits near regulatory limits, totaling over 41 million MXN.

### Repository Structure
* `data/`: Contains synthetic transactional datasets and Know Your Customer (KYC) records.
* `notebooks/`: Jupyter Notebook containing the Exploratory Data Analysis (EDA) and K-Means model training.
* `src/`: Modular Python scripts for data cleaning, engineering, and cluster assignment.
* `dashboard/`: Power BI Desktop file (.pbix) containing the interactive auditing dashboard.

---

## Versión en Español

### Descripción del Proyecto
Este proyecto implementa un pipeline avanzado de monitoreo de transacciones para la Prevención de Lavado de Dinero y Financiamiento al Terrorismo (PLD/FT). Al combinar los sistemas tradicionales basados en reglas con aprendizaje automático no supervisado (Clusterización K-Means), esta solución optimiza los flujos de auditoría financiera, reduce significativamente los falsos positivos, aísla perfiles conductuales anómalos y proporciona un tablero ejecutivo interactivo para la toma de decisiones operativas.

### Problema Operativo
Los sistemas tradicionales de monitoreo transaccional (como el marco heredado SICENA) generan altos volúmenes de alertas basados en umbrales rígidos y estáticos. Este enfoque produce una cantidad abrumadora de falsos positivos, lo que genera fatiga operativa en los analistas de cumplimiento y retrasa la identificación de delitos financieros complejos como la estructuración (smurfing).

### Arquitectura de la Solución
El pipeline se compone de tres capas continuas:
1. **Ingesta Basada en Reglas:** Simula la recepción de transacciones y dispara alertas preliminares basadas en umbrales regulatorios.
2. **Optimización Analítica (Machine Learning):** Aplica un algoritmo no supervisado K-Means en Python para evaluar inconsistencias conductuales (discrepancias en efectivo, velocidad transaccional e ingresos mensuales declarados), segmentando a los usuarios en perfiles de riesgo especializados.
3. **Visualización Ejecutiva y Mesa de Control:** Un tablero interactivo en Power BI conectado directamente a la salida del pipeline, permitiendo al Oficial de Cumplimiento filtrar datos dinámicamente por clúster y auditar perfiles específicos de clientes.

### Métricas Clave e Impacto de Negocio
* **Reducción de Falsos Positivos:** Las alertas operativas que requerían revisión manual urgente se optimizaron a un lote priorizado de 492 casos, incrementando la eficiencia del equipo de análisis.
* **Capital Bajo Investigación:** Aislamiento y seguimiento preciso de 188 millones de pesos mexicanos distribuidos en clústeres anómalos.
* **Concentración de Riesgo:** Identificación del Clúster 4 como grupo de alto riesgo, exponiendo perfiles inconsistentes (ej. estudiantes o desempleados) realizando depósitos estructurados en efectivo cercanos al límite regulatorio por montos superiores a los 41 millones de pesos.

### Estructura del Repositorio
* `data/`: Contiene los conjuntos de datos sintéticos transaccionales y registros KYC (Know Your Customer).
* `notebooks/`: Jupyter Notebook con el Análisis Exploratorio de Datos (EDA) y el entrenamiento del modelo K-Means.
* `src/`: Scripts modulares de Python para la limpieza, ingeniería de variables y asignación de clústeres.
* `dashboard/`: Archivo de Power BI Desktop (.pbix) que contiene la mesa de control interactiva de auditoría.