import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
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
    worksheet = spreadsheet.worksheet("Day-Hours-Review")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# ---------------------------------------------------
# FUNCTION 2
# Clean Data
# ---------------------------------------------------

def clean_sheet_day_hours_data(df):
    df = df.copy()

    # Drop rows where Date is empty
    df = df[df["Date"] != ""]

    # Remove month summary rows like "October"
    df = df[df["Date"].astype(str).str.contains("/")]

    # Convert numeric columns
    df["Min-Summery"] = pd.to_numeric(df["Min-Summery"], errors="coerce")
    df["Hr-Summery"] = pd.to_numeric(df["Hr-Summery"], errors="coerce")

    return df


# ---------------------------------------------------
# FUNCTION 3
# Format to JSON
# ---------------------------------------------------

def format_sheet_day_hours_to_json(df):
    records = []
    for _, row in df.iterrows():
        try:
            date_obj = datetime.strptime(row["Date"], "%m/%d/%Y")
            date_iso = date_obj.strftime("%Y-%m-%d")
        except:
            continue

        minutes = "" if pd.isna(row["Min-Summery"]) else row["Min-Summery"]
        hours = "" if pd.isna(row["Hr-Summery"]) else row["Hr-Summery"]
        record = {
            "date": date_iso,
            "day": row["Day"],
            "minutes": minutes,
            "hours": hours,
            "summary": row["Overall-Summery"] if row["Overall-Summery"] else ""
        }
        records.append(record)
    return records

def main():
    credentials_path = "config/Credentials.json"
    sheet_id = "1x0CJgCUpj-DDvGyClKXdc9OhBpOwNO9AUIdoZ1nnAvM"
    dataset = authenticate_and_fetch_sheet_data(credentials_path, sheet_id)
    dataset = clean_sheet_day_hours_data(dataset)
    structured_data = format_sheet_day_hours_to_json(dataset)
    with open("JsonRes/day_hours_structured.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=4)
    print("Day Hours structured JSON created successfully.")

if __name__ == "__main__":
    main()