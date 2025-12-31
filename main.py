import sys
from pathlib import Path
import pandas as pd

# Add src to python path
sys.path.append(str(Path(__file__).parent / "src"))

from utils.loaders import ConfigLoader
from utils.reporter import HTMLReporter
from utils.security import AuditLogger # <--- NEW MODULE
from validations.validator import DataQualityEngine

# Constants
CONTRACT_PATH = Path("config/contracts/credit_risk_v1.yaml")
RAW_DATA_PATH = Path("data/01_raw")
REPORT_OUTPUT_PATH = Path("outputs/reports")
LOG_OUTPUT_PATH = Path("outputs/logs")

def main():
    print("[INFO] STARTING FINANCIAL DATA GOVERNANCE FRAMEWORK V2.0 (STRICT MODE)")
    print("====================================================")
    
    # Ensure log directory exists
    LOG_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    # 1. Load Contract
    try:
        contract = ConfigLoader.load_yaml(CONTRACT_PATH)
        print(f"[INFO] Contract loaded: {contract['metadata']['domain']}")
    except Exception as e:
        print(f"[CRITICAL ERROR] Error loading contract: {e}")
        return

    # 2. Initialize Reporter
    reporter = HTMLReporter(REPORT_OUTPUT_PATH)

    # 3. Execution Loop
    pipeline_success = True
    
    for dataset_def in contract['datasets']:
        dataset_name = dataset_def['name']
        print(f"\n[GOVERNANCE] Auditing Dataset: {dataset_name.upper()}")
        
        # Load Data
        try:
            file_path = RAW_DATA_PATH / f"{dataset_name}.csv"
            df = ConfigLoader.load_csv(file_path)
        except FileNotFoundError:
            print(f"   [WARNING] Dataset skipped (Not Found).")
            continue

        # Run Engine (Now with Strict Logic)
        engine = DataQualityEngine(dataset_name, dataset_def['schema'])
        report = engine.run_checks(df)
        
        # Log to Audit Master File
        AuditLogger.log_event(LOG_OUTPUT_PATH, dataset_name, report['status'], report['overall_score'])

        # Add to HTML
        reporter.add_result(dataset_name, report)

        # Console Feedback
        print(f"   Quality Score: {report['overall_score']}/100")
        print(f"   Compliance Status: {report['status']}")
        
        if report['status'] == "REJECTED":
            print("   ⛔ BLOCKED: Critical Compliance Violation Detected.")
            pipeline_success = False
        elif report['status'] == "FAILED":
            print("   ⚠️  WARNING: Quality Threshold not met.")
            pipeline_success = False

    # 4. Finalize & Sign
    print("\n====================================================")
    try:
        report_path = reporter.generate()
        # Digital Signature of the Report
        report_hash = AuditLogger.generate_file_hash(report_path)
        
        print(f"[INFO] Report generated: {report_path.name}")
        print(f"[SECURITY] Digital Signature (SHA-256): {report_hash}")
        print(f"[SECURITY] This hash serves as cryptographic proof for auditors.")
        
    except Exception as e:
        print(f"[ERROR] Reporting failed: {e}")

    # Final Pipeline Decision
    if pipeline_success:
        print("[SUCCESS] PIPELINE CLEARED. Data is ready for consumption.")
        sys.exit(0)
    else:
        print("[FAILURE] PIPELINE HALTED. Data Governance constraints triggered.")
        sys.exit(1)

if __name__ == "__main__":
    main()
