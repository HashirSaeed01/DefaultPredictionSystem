import pandas as pd
import numpy as np
import joblib
from io import StringIO
from sklearn.ensemble import RandomForestClassifier
import os

class ModelService:
    def __init__(self, model_path="apps/datahandling/model.pkl"):
        # Check if model exists, if not create a basic one
        if not os.path.exists(model_path):
            print("Creating new model...")
            self.model = RandomForestClassifier()
            # Create a basic model with dummy data
            X = np.random.rand(100, 22)  # 22 features from your CSV
            y = np.random.randint(0, 2, 100)  # Binary classification
            self.model.fit(X, y)
            # Save the model
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            joblib.dump(self.model, model_path)
        else:
            self.model = joblib.load(model_path)
        
    def preprocess(self, csv_data):
        """Convert CSV string into a DataFrame and prepare for prediction."""
        df = pd.read_csv(StringIO(csv_data))
        
        # Standardize column names
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        
        # Select and order features needed for prediction
        feature_columns = [
            'quantity', 'musharaka', 'profit_rate', 'kibor_rate', 
            'financing_amount', 'tenure', 'actual_tenure', 'cos_qty',
            'remaining_principal_amount', 'charity_amount', 'business_years',
            'collection_period_days', 'repayment_days', 'repayment_days_ratio',
            'assisted_tv', 'previous_transactions', 'previous_data', 'ethic',
            'temperature', 'gdp', 'kse100_index', 'exchange_rate'
        ]
        
        # Ensure all columns exist and are numeric
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        return df[feature_columns]

    def predict(self, csv_data):
        """Make predictions on CSV data."""
        df = self.preprocess(csv_data)
        predictions = self.model.predict_proba(df)[:, 1]  # Get probability of positive class
        predictions = np.clip(predictions * 100, 0, 100)  # Scale to 0-100
        return predictions.tolist()
