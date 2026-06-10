from flask import Flask, request, jsonify
import joblib
import numpy as np
from pathlib import Path

import traceback

app = Flask(__name__)

# Try to load exported model(s)
MODEL_PATHS = [Path(__file__).with_name("logistic_model.pkl"), Path(__file__).with_name("rf_model.pkl")]
model = None
model_path = None
for p in MODEL_PATHS:
    if p.exists():
        try:
            model = joblib.load(p)
            model_path = p
            break
        except Exception:
            # continue to next
            traceback.print_exc()


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = np.array(data['input']).reshape(1, -1)
        if model is None:
            return jsonify({'error': 'No model loaded'}), 500
        prediction = model.predict(input_data)
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
        
if __name__ == '__main__':
    if model is None:
        print("Warning: no model found at", [str(p) for p in MODEL_PATHS])
    else:
        print(f"Loaded model from: {model_path}")
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/info', methods=['GET'])
def info():
    if model is None:
        return jsonify({'loaded': False, 'model_path': None})
    return jsonify({'loaded': True, 'model_path': str(model_path), 'model_class': type(model).__name__})