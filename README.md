graph LR
    subgraph DataSources ["Fuentes de Datos"]
        RAW[("Datos Crudos (CSV)")]
    end

    subgraph GovernanceCore ["Núcleo de Gobernanza"]
        CONFIG["Contratos de Datos (YAML)"]
        ENGINE[("Motor de Validación")]
        SEC["Módulo de Auditoría (SHA-256)"]
    end

    subgraph OutputLayers ["Capas de Salida"]
        REPORT[("Informe HTML")]
        LOG[("Registro de Auditoría")]
        DECISION{{"Pasar / Bloquear"}}
    end

    RAW --> ENGINE
    CONFIG --> ENGINE
    ENGINE --> DECISION
    DECISION -->|Cumple| REPORT
    DECISION -->|Violación Crítica| LOG
    ENGINE -.-> SEC
    SEC -.-> LOG
