import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Configuration Constants
NUM_CLIENTS = 1000
NUM_CREDITS = 1500
SEED_VALUE = 42

def get_raw_data_path() -> Path:
    """
    Resolves the absolute path to the data/01_raw directory
    based on the script location.
    """
    # Resolves to: ProjectRoot/data/01_raw
    base_dir = Path(__file__).resolve().parent.parent.parent
    data_path = base_dir / "data" / "01_raw"
    
    # Ensure directory exists
    data_path.mkdir(parents=True, exist_ok=True)
    return data_path

def generate_client_data() -> pd.DataFrame:
    """
    Generates a synthetic dataset for clients with intentional quality issues
    for testing data governance frameworks.
    """
    np.random.seed(SEED_VALUE)
    
    # Base data generation
    client_ids = np.arange(1000, 1000 + NUM_CLIENTS)
    names = [f"Client_{i}" for i in range(NUM_CLIENTS)]
    emails = [f"user_{i}@bankdomain.com" for i in range(NUM_CLIENTS)]
    ages = np.random.randint(18, 90, size=NUM_CLIENTS)
    income = np.random.normal(25000, 10000, NUM_CLIENTS).round(2)
    credit_scores = np.random.randint(300, 850, NUM_CLIENTS)
    registration_dates = pd.date_range(start='2020-01-01', periods=NUM_CLIENTS)

    df_clients = pd.DataFrame({
        'client_id': client_ids,
        'full_name': names,
        'email': emails,
        'age': ages,
        'monthly_income': income,
        'credit_score': credit_scores,
        'registration_date': registration_dates
    })

    # Intentional Data Quality Injection
    
    # Issue 1: Completeness (Null emails)
    df_clients.loc[0:49, 'email'] = np.nan 

    # Issue 2: Consistency (Invalid ages)
    df_clients.loc[50:55, 'age'] = -5 
    df_clients.loc[56:60, 'age'] = 150

    # Issue 3: Validity (Credit score out of bounds)
    df_clients.loc[100:110, 'credit_score'] = 900 
    df_clients.loc[111:115, 'credit_score'] = 0

    # Issue 4: Uniqueness (Duplicate records)
    duplicates = df_clients.iloc[200:220].copy()
    df_clients = pd.concat([df_clients, duplicates], ignore_index=True)

    return df_clients

def generate_credit_data(client_ids_pool: np.ndarray) -> pd.DataFrame:
    """
    Generates a synthetic dataset for credit applications.
    """
    np.random.seed(SEED_VALUE)
    
    credit_ids = [f"CR-{10000+i}" for i in range(NUM_CREDITS)]
    
    # Random assignment of credits to existing clients
    assigned_clients = np.random.choice(client_ids_pool, NUM_CREDITS)
    
    amounts = np.random.exponential(50000, NUM_CREDITS).round(2)
    interest_rates = np.random.uniform(5.0, 25.0, NUM_CREDITS).round(2)
    statuses = np.random.choice(['APPROVED', 'REJECTED', 'PENDING', 'PAID'], NUM_CREDITS)
    request_dates = pd.date_range(start='2021-01-01', periods=NUM_CREDITS)

    df_credits = pd.DataFrame({
        'credit_id': credit_ids,
        'client_id': assigned_clients,
        'requested_amount': amounts,
        'interest_rate': interest_rates,
        'status': statuses,
        'request_date': request_dates
    })

    # Intentional Data Quality Injection

    # Issue 1: Integrity (Orphan records - credits for non-existent clients)
    non_existent_ids = [99999, 88888, 77777]
    df_credits.loc[0:20, 'client_id'] = np.random.choice(non_existent_ids, 21)

    # Issue 2: Business Logic (Negative amounts)
    df_credits.loc[50:60, 'requested_amount'] = -1000.00

    # Issue 3: Business Logic (Interest rate outliers)
    df_credits.loc[100:105, 'interest_rate'] = 500.00

    return df_credits

def main():
    try:
        output_path = get_raw_data_path()
        print(f"Starting data generation process. Target directory: {output_path}")

        # 1. Generate Clients
        df_clients = generate_client_data()
        client_file = output_path / "clients.csv"
        df_clients.to_csv(client_file, index=False)
        print(f"[SUCCESS] Client data generated: {len(df_clients)} records at {client_file}")

        # 2. Generate Credits
        # We need the valid client IDs to maintain some consistency before breaking it
        unique_client_ids = df_clients['client_id'].unique()
        df_credits = generate_credit_data(unique_client_ids)
        credit_file = output_path / "credits.csv"
        df_credits.to_csv(credit_file, index=False)
        print(f"[SUCCESS] Credit data generated: {len(df_credits)} records at {credit_file}")

    except Exception as e:
        print(f"[ERROR] Data generation failed: {e}")

if __name__ == "__main__":
    main()
