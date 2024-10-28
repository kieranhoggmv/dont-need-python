import json
import pandas as pd
from utils import folder_to_dataframes

"""
################################
### Open files in our folder ###
################################
"""
passwords = json.loads(open("data/passwords.txt").read())
rename = (
    lambda df: f"{pd.to_datetime(df.iloc[0]["test date"], format="mixed").year} {df.iloc[0]["test name"]}.xlsx"
)
dataframes = folder_to_dataframes("data", password_map=passwords, rename_func=rename)

"""
#######################################
### Combine our separate dataframes ###
#######################################
"""
combined_df = pd.DataFrame()
for df in dataframes:
    combined_df = pd.concat([combined_df, df], ignore_index=True)


"""
###############################
### Standardise our columns ###
###############################
"""
renames = {
    "test date": "Test Date",
    "test name": "Test Name",
    "standardised score": "Standardised Score",
    "version": "Version",
    "level": "Level",
    "gender": "Gender",
    "dob": "DOB",
    "student id": "Student ID",
    "email": "Email",
    "nationality": "Nationality",
    "name": "Name",
}
combined_df = combined_df.rename(columns=renames)
combined_df.to_csv("combined.csv")
