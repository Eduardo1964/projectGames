from tools import load_csv, correct_data
from parameters import details

df = load_csv(details=details)
df = correct_data(df)
