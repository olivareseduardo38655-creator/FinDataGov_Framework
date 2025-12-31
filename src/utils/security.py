import hashlib
from pathlib import Path
from datetime import datetime

class AuditLogger:
    """
    Handles cryptographic signing of reports and audit logs.
    This simulates a 'Digital Notary' for compliance.
    """
    
    @staticmethod
    def generate_file_hash(file_path: Path) -> str:
        """Calculates SHA-256 hash of a file to ensure immutability."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # Read file in chunks to handle large files efficiently
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return "ERROR_FILE_NOT_FOUND"

    @staticmethod
    def log_event(output_dir: Path, dataset: str, status: str, score: float):
        """Appends execution result to an immutable audit log (CSV)."""
        log_file = output_dir / "audit_master_log.csv"
        timestamp = datetime.now().isoformat()
        
        # Create header if new file
        if not log_file.exists():
            with open(log_file, "w") as f:
                f.write("timestamp,dataset,status,score,hash_signature\n")
        
        # Create a simple signature of this event
        event_signature = hashlib.sha256(f"{timestamp}{dataset}{status}".encode()).hexdigest()[:16]
        
        with open(log_file, "a") as f:
            f.write(f"{timestamp},{dataset},{status},{score},{event_signature}\n")
