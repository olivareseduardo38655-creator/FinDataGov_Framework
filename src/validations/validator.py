import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime

class DataQualityEngine:
    """
    Core engine that validates a dataset against its YAML definition.
    Implements 'Strict Governance': Any CRITICAL issue fails the entire dataset.
    """

    def __init__(self, dataset_name: str, schema_config: List[Dict]):
        self.dataset_name = dataset_name
        self.schema = schema_config
        self.validation_log = []
        self.quality_score = 100.0
        self.has_critical_violation = False  # New Governance Flag

    def _log_issue(self, column: str, rule: str, failed_count: int, severity: str):
        """Internal method to register a quality issue and apply penalties."""
        self.validation_log.append({
            "timestamp": datetime.now().isoformat(),
            "dataset": self.dataset_name,
            "column": column,
            "rule": rule,
            "failed_rows": failed_count,
            "severity": severity
        })
        
        # Governance Logic: Critical issues trigger the kill switch
        if severity == "CRITICAL" and failed_count > 0:
            self.has_critical_violation = True
            
        # Penalty Scoring Logic
        weights = {"CRITICAL": 20.0, "HIGH": 5.0, "MEDIUM": 2.0}
        penalty = weights.get(severity, 1.0)
        
        # Deduction based on existence of error, not just volume (Binary penalty)
        if failed_count > 0:
            self.quality_score = max(0.0, self.quality_score - penalty)

    def run_checks(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Main execution method. Runs all defined checks sequentially.
        """
        # 1. Structural Check: Do all columns exist?
        expected_cols = [col['column'] for col in self.schema]
        missing_cols = set(expected_cols) - set(df.columns)
        
        if missing_cols:
            self._log_issue("SCHEMA", "Missing Columns", len(missing_cols), "CRITICAL")
            return self._generate_report() # Stop immediately

        # 2. Iterative Check per Column defined in Contract
        for col_config in self.schema:
            col_name = col_config['column']
            is_nullable = col_config.get('nullable', True)
            
            # A. Completeness Check (Nulls)
            if not is_nullable:
                null_count = df[col_name].isnull().sum()
                if null_count > 0:
                    self._log_issue(col_name, "Non-Null Constraint", int(null_count), "HIGH")

            # B. Domain Specific Checks (Simulated)
            if col_name == 'email':
                # Simplified check for demonstration
                invalid_emails = df[col_name].apply(lambda x: 0 if isinstance(x, str) and '@' in x else 1).sum()
                if invalid_emails > 0:
                     self._log_issue(col_name, "Email Format", int(invalid_emails), "MEDIUM")

            if col_name == 'age':
                invalid_ages = df[((df[col_name] < 18) | (df[col_name] > 100)) & (df[col_name].notnull())].shape[0]
                if invalid_ages > 0:
                    self._log_issue(col_name, "Age Validity (18-100)", int(invalid_ages), "HIGH")

            if col_name == 'requested_amount':
                # CRITICAL BUSINESS RULE: No negative money
                invalid_amounts = df[df[col_name] <= 0].shape[0]
                if invalid_amounts > 0:
                    self._log_issue(col_name, "Positive Amount", int(invalid_amounts), "CRITICAL")

        return self._generate_report()

    def _generate_report(self) -> Dict[str, Any]:
        """Compiles the final report object with strict governance logic."""
        
        # Governance Decision: 
        # Even if Score is 90, if a CRITICAL rule broke, status is REJECTED.
        if self.has_critical_violation:
            final_status = "REJECTED"
        elif self.quality_score < 80:
            final_status = "FAILED"
        else:
            final_status = "PASSED"

        return {
            "dataset": self.dataset_name,
            "overall_score": round(self.quality_score, 2),
            "status": final_status,
            "issues_found": len(self.validation_log),
            "details": self.validation_log
        }
