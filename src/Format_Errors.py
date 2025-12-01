import pandas as pd
import random

def chaotic_date(d):
    if pd.isnull(d): return None
    r = random.random()
    if r < 0.2: return d.strftime("%m/%d/%Y")
    if r < 0.4: return d.strftime("%d-%m-%Y")
    if r < 0.6: return d.strftime("%Y.%m.%d")
    if r < 0.8: return d.strftime("%d %b %Y")
    return d

def chaotic_case(s):
    if pd.isnull(s): return s
    r = random.random()
    if r < 0.3: return s.upper()
    if r < 0.6: return s.lower()
    return s.title()