import sqlite3
from pathlib import Path

import pandas as pd


def main():
    db_path = Path(__file__).with_name("example.db")

    # Example DataFrame
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Carol"],
            "age": [25, 30, 27],
        }
    )

    # Connect to (or create) the SQLite database
    conn = sqlite3.connect(db_path)
    try:
        # Try to use pandas to_sql (works with sqlite3.Connection)
        df.to_sql("users", conn, if_exists="replace", index=False)
    except Exception:
        # Fallback: create table and insert rows manually
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, age INTEGER)"
        )
        cur.executemany(
            "INSERT INTO users (id, name, age) VALUES (?, ?, ?)",
            [tuple(x) for x in df.to_numpy()],
        )
        conn.commit()

    # Read the table back into a DataFrame
    df_read = pd.read_sql_query("SELECT * FROM users", conn)
    print("Database file:", db_path)
    print(df_read)

    conn.close()


if __name__ == "__main__":
    main()
