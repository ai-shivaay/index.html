import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

MODEL_DIR = 'models'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Career mapping
CAREER_MAPPING = {
    0: 'ML Engineer',
    1: 'Data Scientist',
    2: 'AI Researcher',
    3: 'NLP Specialist',
    4: 'AI Architect',
    5: 'Data Engineer',
    6: 'AI Ethics Officer',
    7: 'Product Manager'
}

REVERSE_CAREER_MAPPING = {v: k for k, v in CAREER_MAPPING.items()}

class CareerPredictionModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = ['technical_score', 'behavioral_score', 'ml_score', 'hr_score']
        
    def generate_training_data(self, n_samples=500):
        """Generate synthetic training data for demonstration"""
        np.random.seed(42)
        X_data = np.random.rand(n_samples, 4) * 100  # 4 interview scores (0-100)
        
        # Create labels based on score patterns
        y_data = []
        for scores in X_data:
            technical, behavioral, ml, hr = scores
            
            if ml > 75 and technical > 70:
                y_data.append(REVERSE_CAREER_MAPPING['ML Engineer'])
            elif technical > 80 and behavioral > 60:
                y_data.append(REVERSE_CAREER_MAPPING['Data Scientist'])
            elif ml > 80 and technical > 75:
                y_data.append(REVERSE_CAREER_MAPPING['AI Researcher'])
            elif technical > 70 and ml > 70:
                y_data.append(REVERSE_CAREER_MAPPING['NLP Specialist'])
            elif technical > 80 and behavioral > 75:
                y_data.append(REVERSE_CAREER_MAPPING['AI Architect'])
            elif technical > 70 and hr > 65:
                y_data.append(REVERSE_CAREER_MAPPING['Data Engineer'])
            elif behavioral > 75:
                y_data.append(REVERSE_CAREER_MAPPING['AI Ethics Officer'])
            else:
                y_data.append(REVERSE_CAREER_MAPPING['Product Manager'])
        
        return X_data, np.array(y_data)
    
    def train(self):
        """Train the decision tree and random forest models"""
        X_train, y_train = self.generate_training_data(500)
        
        # Normalize features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train Decision Tree
        self.model = DecisionTreeClassifier(
            max_depth=8,
            min_samples_split=5,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Train Random Forest for ensemble predictions
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.rf_model.fit(X_train_scaled, y_train)
        
        # Save models
        joblib.dump(self.model, f'{MODEL_DIR}/career_dt_model.pkl')
        joblib.dump(self.rf_model, f'{MODEL_DIR}/career_rf_model.pkl')
        joblib.dump(self.scaler, f'{MODEL_DIR}/scaler.pkl')
        
        print("✅ Models trained and saved successfully!")
    
    def load(self):
        """Load pre-trained models"""
        model_paths = [
            f'{MODEL_DIR}/career_dt_model.pkl',
            f'{MODEL_DIR}/career_rf_model.pkl',
            f'{MODEL_DIR}/scaler.pkl'
        ]

        try:
            self.model = joblib.load(model_paths[0])
            self.rf_model = joblib.load(model_paths[1])
            self.scaler = joblib.load(model_paths[2])

            if self.model is None or self.rf_model is None or self.scaler is None:
                raise ValueError("Missing model state")

            print("✅ Models loaded successfully!")
        except (FileNotFoundError, ValueError, EOFError, AttributeError, ImportError, TypeError):
            for path in model_paths:
                if os.path.exists(path):
                    os.remove(path)
            print("⚠️ Previous models were missing or incompatible. Training new models...")
            self.train()
    
    def predict(self, scores):
        """
        Predict career paths based on interview scores
        scores: dict with keys: technical_score, behavioral_score, ml_score, hr_score
        """
        feature_vector = np.array([[
            scores.get('technical_score', 50),
            scores.get('behavioral_score', 50),
            scores.get('ml_score', 50),
            scores.get('hr_score', 50)
        ]])
        
        # Normalize
        feature_scaled = self.scaler.transform(feature_vector)
        
        # Predict with both models
        dt_pred = self.model.predict(feature_scaled)[0]
        rf_pred = self.rf_model.predict(feature_scaled)[0]
        
        # Get probabilities
        dt_proba = self.model.predict_proba(feature_scaled)[0]
        rf_proba = self.rf_model.predict_proba(feature_scaled)[0]
        
        # Ensemble predictions (average probabilities)
        ensemble_proba = (dt_proba + rf_proba) / 2
        top_3_indices = np.argsort(ensemble_proba)[-3:][::-1]
        
        predictions = [
            (CAREER_MAPPING[idx], float(ensemble_proba[idx]))
            for idx in top_3_indices
        ]
        
        return predictions
    
    def analyze_strengths(self, scores):
        """Analyze which areas are strengths"""
        technical = scores.get('technical_score', 0)
        behavioral = scores.get('behavioral_score', 0)
        ml = scores.get('ml_score', 0)
        hr = scores.get('hr_score', 0)
        
        strengths = []
        if technical > 75:
            strengths.append('Strong Technical Foundation')
        if behavioral > 75:
            strengths.append('Excellent Communication Skills')
        if ml > 75:
            strengths.append('Advanced ML Knowledge')
        if hr > 75:
            strengths.append('Leadership Potential')
        
        return strengths if strengths else ['Growing Technical Skills']
    
    def suggest_learning_path(self, predicted_career):
        """Suggest learning path for predicted career"""
        learning_paths = {
            'ML Engineer': [
                'Advanced Python Programming',
                'TensorFlow & Keras',
                'Deep Learning Specialization',
                'MLOps & Deployment',
                'System Design for ML'
            ],
            'Data Scientist': [
                'Advanced Statistics',
                'SQL & Data Manipulation',
                'Python Data Science Stack',
                'Machine Learning Algorithms',
                'Data Visualization & Communication'
            ],
            'AI Researcher': [
                'Research Methodology',
                'Advanced Mathematics',
                'State-of-the-Art Models',
                'Paper Writing & Publishing',
                'Specialized AI Domains'
            ],
            'NLP Specialist': [
                'Natural Language Processing',
                'Transformer Models',
                'LLM Fine-tuning',
                'Text Generation',
                'Speech Processing'
            ],
            'AI Architect': [
                'System Design',
                'Cloud Architecture',
                'Scalable ML Systems',
                'Leadership & Management',
                'Enterprise ML Solutions'
            ],
            'Data Engineer': [
                'Big Data Technologies',
                'Apache Spark & Hadoop',
                'Cloud Databases',
                'ETL Pipeline Design',
                'Data Infrastructure'
            ],
            'AI Ethics Officer': [
                'AI Ethics Principles',
                'Bias & Fairness',
                'Regulatory Compliance',
                'Stakeholder Management',
                'Policy Development'
            ],
            'Product Manager': [
                'Product Management Fundamentals',
                'AI/ML for Non-technical',
                'User Research',
                'Roadmap Planning',
                'Cross-functional Leadership'
            ]
        }
        
        return learning_paths.get(predicted_career, [
            'Fundamental ML Concepts',
            'Programming Skills',
            'Problem Solving',
            'Communication',
            'Continuous Learning'
        ])

# Initialize global model
model = CareerPredictionModel()

def init_model():
    """Initialize the career prediction model"""
    global model
    model.load()

def predict_career(scores):
    """Wrapper function to predict career"""
    return model.predict(scores)

def get_learning_recommendations(career):
    """Get learning recommendations for a career"""
    return model.suggest_learning_path(career)

def analyze_profile(scores):
    """Analyze user profile"""
    strengths = model.analyze_strengths(scores)
    predictions = model.predict(scores)
    learning_path = model.suggest_learning_path(predictions[0][0])
    
    return {
        'strengths': strengths,
        'predictions': predictions,
        'learning_path': learning_path
    }
