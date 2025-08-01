import pandas as pd
import json
import kagglehub
import os

dataset_path = kagglehub.dataset_download("computingvictor/transactions-fraud-datasets")

def get_file_path(filename):
    return os.path.join(dataset_path, filename)

def get_local_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# --- TRANSACTIONS ---
def load_transactions():
    df = pd.read_csv(get_file_path("transactions_data.csv"))
    df["id"] = df["id"].astype(str)
    df["client_id"] = df["client_id"].astype(str)
    df["card_id"] = df["card_id"].astype(str)
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
    df["amount"] = (
        df["amount"]
        .replace(r"[$,]", "", regex=True)
        .astype(float)
    )

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["id", "amount"], inplace=True)

    return df

# --- USERS ---
def load_users():
    df = pd.read_csv(get_file_path("users_data.csv"))
    df["id"] = df["id"].astype(str)
    money_cols = ["per_capita_income", "yearly_income", "total_debt"]
    for col in money_cols:
        if col in df.columns:
            df[col] = df[col].replace(r"[$,]", "", regex=True).astype(float)
    df.dropna(subset=["id", "yearly_income"], inplace=True)
    return df

# --- CARDS ---
def load_cards():
    df = pd.read_csv(get_file_path("cards_data.csv"))
    df["id"] = df["id"].astype(str)
    if "card_on_dark_web" in df.columns:
        df["is_compromised"] = df["card_on_dark_web"].str.strip().str.lower() == "yes"
    else:
        df["is_compromised"] = False
    return df

# --- MCC Codes ---
def load_mcc_codes():
    with open(get_file_path("mcc_codes.json"), "r") as f:
        return json.load(f)

# --- FRAUD LABELS ---
def load_fraud_labels():
    with open(get_file_path("train_fraud_labels.json"), "r") as f:
        raw = json.load(f)["target"]
        return {str(k).strip(): v.strip().lower() for k, v in raw.items()}

def load_zip_coordinates():
    df = pd.read_csv(get_local_file_path("zip_lat_long.csv"))
    df["zip"] = df["zip"].astype(str).str.zfill(5)  # Ensure 5-digit zip
    return df.set_index("zip")[["latitude", "longitude"]].to_dict("index")