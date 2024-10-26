import json
import pandas as pd

from utils import folder_to_dataframes


passwords = json.loads(open("passwords.txt").read())
dataframes = folder_to_dataframes(
    "data", password_map=passwords, rename_func=lambda x: str(x.iloc[0]["Student ID"])
)
all_cols = []

renames = {
    "test date": "Test Date",
    "test name": "Test Name",
    "standardised score": "Standardised Score",
    "version": "Version",
    "level": "Level",
    "gender": "Gender",
}

combined_df = pd.DataFrame()
for df in dataframes:
    df = df.rename(columns=renames)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

combined_df.to_csv("combined.csv")
