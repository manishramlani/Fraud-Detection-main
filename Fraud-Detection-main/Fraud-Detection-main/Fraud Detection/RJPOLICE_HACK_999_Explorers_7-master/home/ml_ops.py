import joblib

def load_ml_model():
    # Load your ML model from the file
    model = joblib.load('home/models/model.pkl')
    return model

def make_prediction(model, input_data):
    # Use the loaded model to make predictions
    prediction = model.predict(input_data)
    return prediction