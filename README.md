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

**API / Postman testing**

This project includes a Flask app (`app.py`) that will load an exported model file (`logistic_model.pkl` or `rf_model.pkl`) if present and expose two endpoints useful for testing with Postman or curl:

- `GET /info` — returns whether a model is loaded and the model class name.
- `POST /predict` — accepts JSON with an `input` array and returns a predicted label.

Setup and run (recommended using a virtual environment):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# produce a trained model (creates logistic_model.pkl)
python3 sqlite_demo.py
# start the API
python3 app.py
```

Postman examples

- GET /info
	- Method: `GET`
	- URL: `http://localhost:5000/info`
	- Expected response (when model exists):
		```json
		{"loaded": true, "model_path": ".../logistic_model.pkl", "model_class": "LogisticRegression"}
		```

- POST /predict
	- Method: `POST`
	- URL: `http://localhost:5000/predict`
	- Body (JSON example — adjust length to match model's expected features):
		```json
		{"input": [30, 80000, 1]} 
		```
	- Expected response (on success):
		```json
		{"prediction": 1}
		```

Troubleshooting

- If the server fails to start with `ModuleNotFoundError: No module named 'sklearn'`, create and activate the virtual environment and install `scikit-learn` as shown above. The error occurs when unpickling a model that depends on scikit-learn.
- If you don't want the CSV overwritten, keep a copy of `Social_Network_Ads - Social_Network_Ads.csv` before running `sqlite_demo.py` (or I can add an automatic backup step).

If you want, I can also export a ready-made Postman collection (v2.1 JSON) with the two requests pre-configured — shall I add that to the repo?

**Contact**
If you want me to add the CLI flags or update `model_training.py` to persist its DataFrame into the SQLite DB, tell me which option you prefer.

