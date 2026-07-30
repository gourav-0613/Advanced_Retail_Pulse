import os
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
# pyrefly: ignore [missing-import]
import joblib


def main():
    # Detect dataset path
    data_path = "data/train.csv" if os.path.exists("data/train.csv") else "train.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset file not found at {data_path}")

    # Load and clean dataset
    df_raw = pd.read_csv(data_path)
    df_raw["Order Date"] = pd.to_datetime(df_raw["Order Date"], dayfirst=True, errors="coerce")

    # Aggregate monthly sales
    monthly = (
        df_raw.groupby(df_raw["Order Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )
    monthly["Order Date"] = monthly["Order Date"].dt.to_timestamp()
    monthly = monthly.sort_values("Order Date").reset_index(drop=True)
    monthly.rename(columns={"Order Date": "Date"}, inplace=True)

    # Feature Engineering (8 features)
    df = monthly.copy()
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Quarter"] = df["Date"].dt.quarter
    df["Lag1"] = df["Sales"].shift(1)
    df["Lag2"] = df["Sales"].shift(2)
    df["Lag3"] = df["Sales"].shift(3)
    df["Rolling3"] = df["Sales"].rolling(3).mean()
    df["Rolling6"] = df["Sales"].rolling(6).mean()
    df = df.dropna().reset_index(drop=True)

    feature_cols = [
        "Year",
        "Month",
        "Quarter",
        "Lag1",
        "Lag2",
        "Lag3",
        "Rolling3",
        "Rolling6",
    ]
    X = df[feature_cols]
    y = df["Sales"]

    # Train Gradient Boosting Regressor
    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        random_state=42,
    )
    model.fit(X, y)

    # Overwrite model.pkl
    joblib.dump(model, "model.pkl")
    print("Model successfully trained with 8 features and saved to model.pkl.")


if __name__ == "__main__":
    main()
