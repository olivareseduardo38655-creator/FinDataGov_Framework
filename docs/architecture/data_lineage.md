# Data Lineage: Credit Risk Flow

Este diagrama representa el flujo de vida del dato para el cálculo de reservas.

```mermaid
graph TD
    %% Nodos del Linaje
    CoreBanking[("🏦 Core Banking System<br>(Source)")] 
    RawZone[("📂 Data Lake: RAW<br>(S3/Local)")]
    QualityEngine[("⚙️ Data Quality Engine<br>(Python + Great Expectations)")]
    
    %% Salidas del Motor
    CleanZone[("✅ Trusted Data Zone<br>(Parquet)")]
    Quarantine[("☣️ Quarantine Zone<br>(Bad Data)")]
    
    %% Consumidores
    RiskModel[("📈 Risk Models<br>(Scoring)")]
    RegReport[("🏛️ Regulatory Report<br>(CNBV/IFRS9)")]
    
    %% Flujo
    CoreBanking -->|Daily Batch| RawZone
    RawZone -->|Ingestion| QualityEngine
    QualityEngine -->|Passes Contract| CleanZone
    QualityEngine -->|Breaks Contract| Quarantine
    
    CleanZone --> RiskModel
    CleanZone --> RegReport
    
    %% Estilos
    style QualityEngine fill:#f9f,stroke:#333,stroke-width:2px
    style Quarantine fill:#ffaaaa,stroke:#333
    style RegReport fill:#lightblue,stroke:#333
