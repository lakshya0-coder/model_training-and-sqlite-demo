# Deltro — ML model & SQLite demo

This repository contains a small ML-data experiment and an SQLite demo used for testing and teaching how to persist pandas DataFrames.

**Summary**
- **Project:** simple ML model data preparation and SQLite DataFrame roundtrip.
- **Languages:** Python 3.10+ (tested on 3.14 in this environment).

**Files**
- `model_training.py`: loads the Social Network Ads CSV (auto-finds filenames like `Social_Network_Ads*.csv`) and prints the first rows.
- `sqlite_demo.py`: creates an example DataFrame, writes it to `example.db` (table `users`), then reads it back into a pandas DataFrame and prints it.
- `example.db`: SQLite database created by `sqlite_demo.py` (generated at runtime).
- `Social_Network_Ads - Social_Network_Ads.csv`: example dataset (if present in the repo root).
- `main.py`, `pyproject.toml`, `requirements.txt`: supporting project files.

**Quickstart**

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the model training script (it will auto-locate the CSV):

```bash
python model_training.py
```

4. Run the SQLite demo (creates `example.db` and prints the table):

```bash
python sqlite_demo.py
```

**Notes**
- `model_training.py` was updated to search for files matching `Social_Network_Ads*.csv` and will raise a clear error listing files in the working directory if no candidate is found.
- `sqlite_demo.py` demonstrates using `pandas.DataFrame.to_sql()` to persist a DataFrame to SQLite and reading it back with `pd.read_sql_query()`.

**Git / Upload to GitHub**

Recommended minimal commands to push this repo to GitHub:

```bash
git init
git add .
git commit -m "Initial import: model_training and sqlite demo"
git branch -M main
git remote add origin <YOUR_GIT_URL>
git push -u origin main
```

Replace `<YOUR_GIT_URL>` with your repository URL.

**Next steps (suggested)**
- Add a CLI to `sqlite_demo.py`/`model_training.py` supporting `--db`, `--table`, and `--csv` flags.
- Add tests and a short example notebook showing results.

**Contact**
If you want me to add the CLI flags or update `model_training.py` to persist its DataFrame into the SQLite DB, tell me which option you prefer.

