"""
Module 1: RandomForest Model for Stress Level Prediction
Predicts stress level based on employee metrics
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os


class StressLevelPredictor:
    def __init__(self, model_path='models/stress_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.label_encoder = LabelEncoder()
        
    def generate_training_data(self, n_samples=1000):
        """Generate synthetic training data for stress level prediction"""
        np.random.seed(42)
        
        # Generate features
        data = {
            'work_hours_per_week': np.random.normal(45, 10, n_samples),
            'sleep_hours_per_day': np.random.normal(7, 1.5, n_samples),
            'meetings_per_week': np.random.randint(5, 30, n_samples),
            'emails_per_day': np.random.randint(20, 150, n_samples),
            'deadline_pressure': np.random.randint(1, 11, n_samples),  # 1-10 scale
            'task_complexity': np.random.randint(1, 11, n_samples),  # 1-10 scale
            'team_support': np.random.randint(1, 11, n_samples),  # 1-10 scale
            'work_life_balance': np.random.randint(1, 11, n_samples),  # 1-10 scale
        }
        
        df = pd.DataFrame(data)
        
        # Calculate stress level based on features
        stress_score = (
            (df['work_hours_per_week'] - 40) * 0.5 +
            (8 - df['sleep_hours_per_day']) * 5 +
            df['meetings_per_week'] * 0.3 +
            df['emails_per_day'] * 0.05 +
            df['deadline_pressure'] * 3 +
            df['task_complexity'] * 2 -
            df['team_support'] * 2 -
            df['work_life_balance'] * 2
        )
        
        # Categorize into stress levels
        df['stress_level'] = pd.cut(
            stress_score, 
            bins=[-np.inf, 20, 40, 60, np.inf],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
        
        return df
    
    def train(self, df=None):
        """Train the RandomForest model"""
        if df is None:
            df = self.generate_training_data()
        
        # Prepare features and target
        X = df.drop('stress_level', axis=1)
        y = self.label_encoder.fit_transform(df['stress_level'])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        # Calculate accuracy
        accuracy = self.model.score(X_test, y_test)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'label_encoder': self.label_encoder,
            'feature_names': X.columns.tolist()
        }, self.model_path)
        
        return accuracy
    
    def load_model(self):
        """Load the trained model"""
        if os.path.exists(self.model_path):
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.label_encoder = model_data['label_encoder']
            return True
        return False
    
    def predict(self, features):
        """
        Predict stress level for given features
        
        Args:
            features: dict with keys matching training features
        
        Returns:
            dict with prediction and probability
        """
        if self.model is None:
            if not self.load_model():
                raise ValueError("Model not trained or loaded")
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # Predict
        prediction_encoded = self.model.predict(df)[0]
        probabilities = self.model.predict_proba(df)[0]
        
        # Decode prediction
        prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Get feature importance
        feature_importance = dict(zip(
            df.columns,
            self.model.feature_importances_
        ))
        
        return {
            'stress_level': prediction,
            'confidence': float(max(probabilities)),
            'probabilities': {
                level: float(prob) 
                for level, prob in zip(self.label_encoder.classes_, probabilities)
            },
            'feature_importance': feature_importance
        }


if __name__ == '__main__':
    # Train model
    predictor = StressLevelPredictor()
    accuracy = predictor.train()
    print(f"Model trained with accuracy: {accuracy:.2%}")
    
    # Test prediction
    test_features = {
        'work_hours_per_week': 50,
        'sleep_hours_per_day': 6,
        'meetings_per_week': 20,
        'emails_per_day': 100,
        'deadline_pressure': 8,
        'task_complexity': 7,
        'team_support': 5,
        'work_life_balance': 4
    }
    
    result = predictor.predict(test_features)
    print(f"\nTest Prediction:")
    print(f"Stress Level: {result['stress_level']}")
    print(f"Confidence: {result['confidence']:.2%}")
