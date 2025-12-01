import numpy as np
import pandas as pd
import random

def apply_generic_chaos(df):
    # Always work on a copy to avoid "SettingWithCopy" warnings
    df = df.copy()
    current_rows = len(df)
    
    # 1. Incompleteness: Random Nulls (10%)
    for col in df.columns:
        # Create a boolean mask where True = "make this value NaN"
        mask_indices = np.random.rand(current_rows) < 0.1
        
        # FIX: Use .mask() instead of .loc[]
        # .mask() automatically promotes types (Bool -> Object) to handle NaNs safely
        df[col] = df[col].mask(mask_indices, np.nan)

    # 2. Redundancy: Duplicates (5%)
    dupes = df.sample(frac=0.05)
    df = pd.concat([df, dupes], ignore_index=True)
    
    # Recalculate length after duplicates
    current_rows = len(df)

    # 3. Inaccuracy: Typos (Text columns only)
    str_cols = df.select_dtypes(include='object').columns
    if len(str_cols) > 0:
        col = random.choice(str_cols)
        # We use pd.notnull(x) so we don't accidentally turn the NaNs we just made into strings like "nan"
        df[col] = df[col].apply(lambda x: str(x).replace('a', 'aa') if pd.notnull(x) and random.random() < 0.05 else x)

    # 4. Inaccuracy: Encoding Errors (Text columns only)
    if len(str_cols) > 0:
        col = random.choice(str_cols)
        df[col] = df[col].apply(lambda x: str(x).replace('e', 'Ã©') if pd.notnull(x) and random.random() < 0.05 else x)

    # 5. Hidden Artifacts: Trailing Whitespace
    if len(str_cols) > 0:
        col = random.choice(str_cols)
        df[col] = df[col].apply(lambda x: f"{x} " if pd.notnull(x) and random.random() < 0.1 else x)

    # 6. Noise: Placeholders (-1) in Numeric Columns
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) > 0:
        col = random.choice(num_cols)
        mask_indices = np.random.rand(current_rows) < 0.02
        # .mask() is safer here too, though .loc usually handles numbers fine
        df[col] = df[col].mask(mask_indices, -1)

    return df.sample(frac=1).reset_index(drop=True)