import pandas as pd
import random

def load_sample(csv_path: str, sample_size: int = 1000):
    df = pd.read_csv(csv_path)
    return df.sample(n=sample_size, random_state=42).reset_index(drop=True)
