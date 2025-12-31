# Financial Data Governance Framework

![Python](https://img.shields.io/badge/Python-3.9-00568f?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat-square)
![Architecture](https://img.shields.io/badge/Architecture-Metadata_Driven-orange?style=flat-square)
![Security](https://img.shields.io/badge/Security-SHA256_Audit-red?style=flat-square)
![Status](https://img.shields.io/badge/Build-Passing-success?style=flat-square)

## Descripción Ejecutiva

Este proyecto establece un marco de trabajo de ingeniería de datos diseñado para mitigar riesgos operativos en instituciones financieras. El sistema actúa como una barrera de control automatizada entre la ingesta de datos crudos (Raw Data) y los modelos de riesgo crediticio.

A diferencia de validaciones tradicionales embebidas en código, esta solución implementa una arquitectura dirigida por metadatos (Metadata-Driven). El motor asegura que ningún registro financiero violente las reglas de negocio críticas definidas en los "Contratos de Datos", garantizando la integridad para reportes regulatorios (CNBV/Basel III) y protegiendo el cálculo de reservas de capital ante inyecciones de datos corruptos.

## Objetivos Técnicos

1.  **Arquitectura Desacoplada:** Separación total entre la lógica de validación (Python) y las reglas de negocio (YAML), permitiendo actualizaciones de reglas sin despliegues de código (CI/CD).
2.  **Gobernanza Estricta (Strict Governance):** Implementación de mecanismos de bloqueo automático ("Kill Switch") ante violaciones de reglas críticas, priorizando la seguridad sobre la disponibilidad.
3.  **Trazabilidad Inmutable:** Generación de bitácoras de auditoría firmadas criptográficamente (SHA-256) para asegurar la no repudia y la integridad histórica de las ejecuciones.
4.  **Clean Code & SOLID:** Código estructurado modularmente, tipado estático y semántica profesional para facilitar la mantenibilidad empresarial.
5.  **Reporte Ejecutivo Automatizado:** Renderizado de informes HTML autónomos para la toma de decisiones por parte de los Data Stewards.

## Arquitectura del Sistema

El siguiente diagrama ilustra el flujo de datos unidireccional y los puntos de decisión lógica dentro del pipeline de gobierno.

```mermaid
graph LR
    subgraph Data Sources
        RAW[("Raw Data (CSV)")]
    end

    subgraph Governance Core
        CONFIG["Data Contracts (YAML)"]
        ENGINE[("Validation Engine")]
        SEC["Audit Module (SHA-256)"]
    end

    subgraph Output Layers
        REPORT[("HTML Report")]
        LOG[("Immutable Audit Log")]
        DECISION{{"Pass / Block"}}
    end

    RAW --> ENGINE
    CONFIG --> ENGINE
    ENGINE --> DECISION
    DECISION -->|Compliance OK| REPORT
    DECISION -->|Critical Violation| LOG
    ENGINE -.-> SEC
    SEC -.-> LOG
