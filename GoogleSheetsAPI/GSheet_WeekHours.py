import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import os
import json

# ---------------------------------------------------
# FUNCTION 1
# Authentication + Fetch Data
# ---------------------------------------------------

def authenticate_and_fetch_sheet_data(credentials_path, sheet_id):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_file(
        credentials_path,
        scopes=scopes
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet("Weekly-Review")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# ---------------------------------------------------
# FUNCTION 2
# Clean Data
# ---------------------------------------------------

def clean_sheet_week_hours_data(df):
    df = df.copy()
    df["Month"] = df["Month"].replace("", pd.NA)
    df["Month"] = df["Month"].ffill()
    df = df[~df["Date-Range"].astype(str).str.contains("to", case=False, na=False)]
    df["Hr-Summery"] = pd.to_numeric(df["Hr-Summery"], errors="coerce")
    df["Min-Summery"] = pd.to_numeric(df["Min-Summery"], errors="coerce")
    return df

# ---------------------------------------------------
# FUNCTION 3
# Format JSON
# ---------------------------------------------------

def format_sheet_week_hours_to_json(df):
    records = []
    for _, row in df.iterrows():
        hours = "" if pd.isna(row["Hr-Summery"]) else row["Hr-Summery"]
        minutes = "" if pd.isna(row["Min-Summery"]) else row["Min-Summery"]
        record = {
            "month": row["Month"],
            "range": row["Date-Range"],
            "hours": hours,
            "minutes": minutes,
            "summary": row["Weekly-Summery"] if row["Weekly-Summery"] else ""
        }
        records.append(record)
    return records

def main():
    credentials_path = "config/Credentials.json"
    sheet_id = "1x0CJgCUpj-DDvGyClKXdc9OhBpOwNO9AUIdoZ1nnAvM"
    dataset = authenticate_and_fetch_sheet_data(credentials_path, sheet_id)
    dataset = clean_sheet_week_hours_data(dataset)
    structured_data = format_sheet_week_hours_to_json(dataset)
    with open("JsonRes/week_hours_structured.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=4)
    print("Weekly Hours structured JSON created successfully.")


if __name__ == "__main__":
    main()