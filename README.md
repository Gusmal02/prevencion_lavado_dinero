# Financial Intelligence Pipeline: ML-Driven AML/CFT Transaction Monitoring

## English Version

### Project Overview
This project implements a production-ready Anti-Money Laundering (AML) and Counter-Financing of Terrorism (CFT) transaction monitoring pipeline. By combining traditional rule-based compliance elements with unsupervised machine learning (K-Means Clustering), this solution optimizes financial auditing workflows, reduces false positives, isolates anomalous behavioral profiles, and provides automated testing and infrastructure deployment under a DevSecOps approach.

### Problem Statement
Traditional transaction monitoring systems generate high volumes of alerts based on rigid, static thresholds. This approach results in an overwhelming number of false positives, causing operational fatigue for compliance analysts and delaying the identification of complex financial crimes such as structuring (smurfing).

### Solution Architecture
The pipeline is structured into four continuous layers:
1. **Rule-Based Ingestion:** Validates schema integrity and processes transaccional inputs.
2. **Analytical Optimization (Machine Learning):** Applies an unsupervised K-Means algorithm via Scikit-Learn to evaluate behavioral inconsistencies (cash discrepancies, transactional velocity, and declared monthly income), segmenting users into specialized risk profiles.
3. **Automated Hardening & DevSecOps:** Integrated automated testing with Python's `unittest` framework to guarantee mathematical consistency (mitigating zero-division errors) and continuous validation via GitHub Actions.
4. **Infrastructure as Code (IaC):** Declarative configuration using Terraform to provision secure, encrypted cloud storage (AWS S3) for data lake architecture.

### Key Metrics and Business Impact
* **False Positive Optimization:** Operational alerts requiring urgent manual review were reduced and isolated down to **577 prioritized cases** (Cluster 4), maximizing analyst efficiency.
* **Robust Behavioral Segmentation:** Successfully mapped structural cash deposits executing transactions near regulatory limits, protecting operational integrity.

### Repository Structure
* `.github/workflows/`: Contains `devsecops_pipeline.yml` for automated CI/CD testing and security scanning (Bandit).
* `data_sintetica/`: Contains synthetic transactional datasets, KYC records, and exported analytical results (`.csv`) along with serialized model artifacts (`scaler.pkl`, `kmeans_model.pkl`).
* `graficas/`: Contains visualization deliverables and control desk resources (`Mesa_Control_PLD.pbix`).
* `terraform/`: Configuration files (`main.tf`) representing cloud infrastructure foundations.
* `modelo_machine_learning.py`: Core production pipeline with integrated schema validation, logging, and dual execution modes (`--mode train` / `--mode predict`).
* `test_pipeline.py`: Automated unit tests for data schema enforcement and mathematical exception handling.
* `requirements.txt`: Pinpointed python dependencies for clean environment environment replication.

---

## Versión en Español

### Descripción del Proyecto
Este proyecto implementa un pipeline de producción avanzado para el monitoreo de transacciones en la Prevención de Lavado de Dinero y Financiamiento al Terrorismo (PLD/FT). Al combinar los sistemas tradicionales con aprendizaje automático no supervisado (Clusterización K-Means), esta solución optimiza los flujos de auditoría financiera, reduce los falsos positivos, aísla perfiles conductuales anómalos y proporciona un despliegue e infraestructura automatizados bajo un enfoque DevSecOps.

### Problema Operativo
Los sistemas tradicionales de monitoreo transaccional generan altos volúmenes de alertas basados en umbrales rígidos y estáticos. Este enfoque produce una cantidad abrumadora de falsos positivos, lo que genera fatiga operativa en los analistas de cumplimiento y retrasa la identificación de delitos financieros complejos como la estructuración (smurfing).

### Arquitectura de la Solución
El pipeline se compone de cuatro capas continuas:
1. **Ingesta e Integridad:** Validación rigurosa de esquemas estructurales y procesamiento de datos transaccionales en memoria.
2. **Optimización Analítica (Machine Learning):** Aplica un algoritmo no supervisado K-Means mediante Scikit-Learn para evaluar de manera vectorizada inconsistencias conductuales (discrepancias en efectivo, velocidad transaccional e ingresos mensuales declarados), aislando los perfiles en clústeres de riesgo específicos.
3. **Robustez y DevSecOps (CI/CD):** Pruebas unitarias automatizadas con el framework `unittest` de Python para mitigar excepciones matemáticas críticas (como divisiones por cero en ingresos nulos) ejecutadas automáticamente en cada integración a través de GitHub Actions.
4. **Infraestructura como Código (IaC):** Modelado declarativo de infraestructura en la nube (AWS S3) utilizando Terraform para garantizar el almacenamiento seguro y cifrado del Lago de Datos.

### Métricas Clave e Impacto de Negocio
* **Optimización de Falsos Positivos:** Las alertas operativas de alto riesgo que requieren revisión manual urgente se redujeron y aislaron con precisión a un lote priorizado de **577 casos críticos** (Clúster 4).
* **Mitigación de Riesgo de Estructuración:** Identificación precisa de usuarios con un comportamiento de depósitos fraccionados en efectivo cercanos a los límites de reporte regulatorio.

### Estructura del Repositorio
* `.github/workflows/`: Contiene `devsecops_pipeline.yml` para la ejecución automática de pruebas y escaneo estático de seguridad de código (Bandit).
* `data_sintetica/`: Almacena los datasets de entrada, las salidas analíticas optimizadas y los archivos binarios del modelo persistido (`scaler.pkl`, `kmeans_model.pkl`).
* `graficas/`: Contiene recursos visuales y el archivo de mesa de control interactiva (`Mesa_Control_PLD.pbix`).
* `terraform/`: Archivos de configuración (`main.tf`) para la provisión de la infraestructura en AWS.
* `modelo_machine_learning.py`: Script principal de producción con logging profesional, validación de esquemas y modos de ejecución (`--mode train` / `--mode predict`).
* `test_pipeline.py`: Suite de pruebas unitarias automatizadas para la verificación matemática y de esquema.
* `requirements.txt`: Lista explícita de dependencias de Python para asegurar la replicabilidad del entorno virtual.