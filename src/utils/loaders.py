import pandas as pd
import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    """
    Handles the loading of configuration files and raw data
    safely using pathlib for OS-agnostic paths.
    """
    
    @staticmethod
    def load_yaml(file_path: Path) -> Dict[str, Any]:
        """Loads a YAML configuration file."""
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at: {file_path}")
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML file: {exc}")

    @staticmethod
    def load_csv(file_path: Path) -> pd.DataFrame:
        """Loads a CSV dataset."""
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found at: {file_path}")
