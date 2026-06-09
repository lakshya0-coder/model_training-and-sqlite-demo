import glob
import os
import numpy as np
import pandas as pd

# Try to find the Social_Network_Ads CSV even if the exact filename differs
candidates = glob.glob("Social_Network_Ads*.csv") + glob.glob("*Social_Network_Ads*.csv")
candidates = list(dict.fromkeys(candidates))
if not candidates:
	available = ", ".join(sorted(os.listdir('.')))
	raise FileNotFoundError(
		"Could not find 'Social_Network_Ads.csv' (or similar). "
		f"Files in working directory: {available}"
	)
csv_path = candidates[0]
print(f"Using CSV: {csv_path}")
df = pd.read_csv(csv_path)
print(df.head(2))


df = df.drop(columns = ['User ID', 'Gender'])

x = df.drop(columns = ['Purchased'])
y = df['Purchased']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(x_train, y_train)

import joblib


# save the model 
joblib.dump(rf, 'rf_model.pkl')
print("Model saved as 'rf_model.pkl'")
