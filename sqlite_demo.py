import sqlite3
from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from joblib import dump


def main():
    db_path = Path(__file__).with_name("example.db")

    # Load DataFrame from the Social_Network_Ads CSV file
    csv_path = Path(__file__).with_name("Social_Network_Ads - Social_Network_Ads.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    df = pd.read_csv(csv_path)
    print("Loaded CSV data from:", csv_path)
    # Connect to (or create) the SQLite database
    conn = sqlite3.connect(db_path)
    try:
        # Try to use pandas to_sql (works with sqlite3.Connection)
        df.to_sql("social_network_ads", conn, if_exists="replace", index=False)
    except Exception:
        # Fallback: create table dynamically and insert rows manually
        cur = conn.cursor()
        cols = list(df.columns)
        col_defs = ", ".join(f'"{c}" TEXT' for c in cols)
        cur.execute(f"CREATE TABLE IF NOT EXISTS social_network_ads ({col_defs})")
        placeholders = ", ".join("?" for _ in cols)
        col_names = ", ".join(f'"{c}"' for c in cols)
        cur.executemany(
            f"INSERT INTO social_network_ads ({col_names}) VALUES ({placeholders})",
            [tuple(x) for x in df.to_numpy()],
        )
        conn.commit()

    # Read the table back into a DataFrame
    df_read = pd.read_sql_query("SELECT * FROM social_network_ads", conn)
    print("Database file:", db_path)
    print(df_read)

    # --- Train Logistic Regression on the imported DataFrame ---
    def _find_target_column(df_: pd.DataFrame):
        # common target names
        for name in ("Purchased", "purchased", "Purchased?", "target", "label", "y"):
            if name in df_.columns:
                return name
        # prefer last column if binary
        last = df_.columns[-1]
        vals = df_[last].dropna().unique()
        if len(vals) == 2:
            return last
        # check for 0/1 numeric in any column
        for c in df_.columns:
            v = df_[c].dropna().unique()
            if set(np.unique(v)).issubset({0, 1}):
                return c
        return None

    target_col = _find_target_column(df_read)
    if target_col is None:
        print("No binary target column found — skipping training.")
    else:
        print(f"Using target column: {target_col}")
        # prepare features
        X = df_read.drop(columns=[target_col])
        y = df_read[target_col]
        # Simple preprocessing: select numeric features and one-hot encode non-numeric
        X_num = X.select_dtypes(include=[np.number])
        X_cat = X.select_dtypes(exclude=[np.number])
        if not X_num.shape[1] and X_cat.shape[1]:
            X_pre = pd.get_dummies(X_cat, drop_first=True)
        elif X_num.shape[1] and X_cat.shape[1]:
            X_pre = pd.concat([X_num, pd.get_dummies(X_cat, drop_first=True)], axis=1)
        else:
            X_pre = X_num

        # ensure no missing values
        X_pre = X_pre.fillna(0)

        # convert y to numeric if needed
        if y.dtype == object:
            y = pd.factorize(y)[0]

        X_train, X_test, y_train, y_test = train_test_split(
            X_pre, y, test_size=0.2, random_state=42, stratify=y if len(np.unique(y)) > 1 else None
        )

        model = LogisticRegression(solver="liblinear")
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test) if len(y_test) > 0 else model.score(X_train, y_train)
        model_path = Path(__file__).with_name("logistic_model.pkl")
        dump(model, model_path)
        print(f"Trained LogisticRegression saved to: {model_path} (test score: {score:.4f})")

    conn.close()


if __name__ == "__main__":
    main()
