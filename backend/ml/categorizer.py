"""
Expense Categorization ML Module
Uses Naive Bayes classifier for automatic expense categorization
"""
import re
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

class ExpenseCategorizer:
    def __init__(self, model_path='ml/models/category_model.pkl'):
        """Initialize the categorizer"""
        self.model_path = model_path
        self.model = None
        self.load_or_train_model()
    
    def preprocess_text(self, text):
        """Preprocess transaction description"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        return text
    
    def load_or_train_model(self):
        """Load existing model or train a new one"""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                print("Loaded existing categorization model")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.train_model()
        else:
            self.train_model()
    
    def train_model(self):
        """Train the categorization model with sample data"""
        # Sample training data
        training_data = {
            'description': [
                # Food & Dining
                'starbucks coffee', 'mcdonalds meal', 'pizza hut', 'grocery store',
                'whole foods', 'restaurant dinner', 'subway sandwich', 'dominos pizza',
                'chipotle lunch', 'dunkin donuts', 'burger king', 'taco bell',
                
                # Transportation
                'uber ride', 'lyft trip', 'gas station', 'shell fuel',
                'car insurance', 'auto repair', 'parking fee', 'toll road',
                'subway metro', 'bus fare', 'car wash', 'oil change',
                
                # Shopping
                'amazon purchase', 'walmart', 'target store', 'best buy electronics',
                'clothing store', 'shoes purchase', 'home depot', 'ikea furniture',
                'online shopping', 'ebay item', 'clothing retailer', 'electronics',
                
                # Bills & Utilities
                'electric bill', 'water bill', 'internet service', 'phone bill',
                'rent payment', 'mortgage payment', 'gas utility', 'cable tv',
                'streaming service', 'insurance premium', 'credit card payment',
                
                # Healthcare
                'pharmacy', 'doctor visit', 'hospital', 'dental appointment',
                'vision care', 'health insurance', 'medical lab', 'prescription',
                'clinic visit', 'therapy session', 'gym membership',
                
                # Entertainment
                'movie theater', 'concert tickets', 'sports event', 'netflix',
                'spotify premium', 'game purchase', 'hobby supplies', 'books',
                'museum admission', 'theme park', 'streaming service',
                
                # Education
                'tuition payment', 'textbooks', 'online course', 'school supplies',
                'training program', 'seminar fee', 'certification exam',
                
                # Others
                'atm withdrawal', 'bank fee', 'miscellaneous', 'gift purchase',
                'donation', 'pet supplies', 'personal care'
            ],
            'category': [
                # Food & Dining (12)
                'Food & Dining', 'Food & Dining', 'Food & Dining', 'Food & Dining',
                'Food & Dining', 'Food & Dining', 'Food & Dining', 'Food & Dining',
                'Food & Dining', 'Food & Dining', 'Food & Dining', 'Food & Dining',
                
                # Transportation (12)
                'Transportation', 'Transportation', 'Transportation', 'Transportation',
                'Transportation', 'Transportation', 'Transportation', 'Transportation',
                'Transportation', 'Transportation', 'Transportation', 'Transportation',
                
                # Shopping (12)
                'Shopping', 'Shopping', 'Shopping', 'Shopping',
                'Shopping', 'Shopping', 'Shopping', 'Shopping',
                'Shopping', 'Shopping', 'Shopping', 'Shopping',
                
                # Bills & Utilities (11)
                'Bills & Utilities', 'Bills & Utilities', 'Bills & Utilities', 'Bills & Utilities',
                'Bills & Utilities', 'Bills & Utilities', 'Bills & Utilities', 'Bills & Utilities',
                'Bills & Utilities', 'Bills & Utilities', 'Bills & Utilities',
                
                # Healthcare (11)
                'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare',
                'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare',
                'Healthcare', 'Healthcare', 'Healthcare',
                
                # Entertainment (11)
                'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment',
                'Entertainment', 'Entertainment', 'Entertainment', 'Entertainment',
                'Entertainment', 'Entertainment', 'Entertainment',
                
                # Education (7)
                'Education', 'Education', 'Education', 'Education',
                'Education', 'Education', 'Education',
                
                # Others (7)
                'Others', 'Others', 'Others', 'Others',
                'Others', 'Others', 'Others'
            ]
        }
        
        df = pd.DataFrame(training_data)
        df['processed_text'] = df['description'].apply(self.preprocess_text)
        
        # Create pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=100, ngram_range=(1, 2))),
            ('clf', MultinomialNB())
        ])
        
        # Train model
        self.model.fit(df['processed_text'], df['category'])
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print("Trained and saved new categorization model")
    
    def categorize(self, description, merchant=None):
        """Categorize a transaction based on description and merchant"""
        if not self.model:
            return 'Others', 0.0
        
        # Combine description and merchant
        text = f"{description or ''} {merchant or ''}"
        processed = self.preprocess_text(text)
        
        if not processed:
            return 'Others', 0.0
        
        try:
            # Predict category
            category = self.model.predict([processed])[0]
            
            # Get probability
            proba = self.model.predict_proba([processed])
            confidence = float(np.max(proba))
            
            return category, confidence
        except Exception as e:
            print(f"Error categorizing: {e}")
            return 'Others', 0.0
    
    def batch_categorize(self, transactions):
        """Categorize multiple transactions"""
        results = []
        for trans in transactions:
            category, confidence = self.categorize(
                trans.get('description'),
                trans.get('merchant')
            )
            results.append({
                'category': category,
                'confidence': confidence
            })
        return results


# Global instance
categorizer = ExpenseCategorizer()
