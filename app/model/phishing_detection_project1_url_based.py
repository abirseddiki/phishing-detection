import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle
import re
import datetime

class PhishingDetection:
    def __init__(self):
        self.models = {
            "Logistic Regression": LogisticRegression(),
            "K-Nearest Neighbors": KNeighborsClassifier(),
            "Naive Bayes": GaussianNB(),
            "Decision Tree": DecisionTreeClassifier(max_depth=30),
            "Random Forest": RandomForestClassifier(n_estimators=10),
            "Gradient Boosting": GradientBoostingClassifier(max_depth=4, learning_rate=0.7),
            "Multi-Layer Perceptron": MLPClassifier(),
            "Support Vector": SVC()
        }
        self.best_model = None
        self.feature_names = ['UsingIP', 'PrefixSuffix-', 'SubDomains', 'HTTPS', 'NonStdPort', 'HTTPSDomainURL', 
                              'RequestURL', 'AnchorURL', 'LinksInScriptTags', 'ServerFormHandler', 'AbnormalURL',
                              'WebsiteForwarding', 'StatusBarCust', 'DisableRightClick', 'AgeofDomain', 
                              'DNSRecording', 'WebsiteTraffic', 'PageRank', 'GoogleIndex', 'StatsReport', 'InfoEmail']

    def load_data(self, csv_file):
        df = pd.read_csv(csv_file)
        df = df.drop(['Index'], axis=1)
        df.drop_duplicates(inplace=True)
        df.drop(columns=['LongURL','Symbol@','ShortURL','Redirecting//','DomainRegLen', 'Favicon', 'UsingPopupWindow', 'IframeRedirection', 'LinksPointingToPage'], inplace=True)
        return df

    def preprocess_data(self, df):
        X = df.drop(["class"], axis=1)
        y = df["class"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train_model(self, X_train, y_train):
        best_accuracy = 0
        for model_name, model in self.models.items():
            model.fit(X_train, y_train)
            accuracy = np.mean(cross_val_score(model, X_train, y_train, cv=11))
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                self.best_model = model
        return self.best_model

    def evaluate_model(self, model, X_test, y_test):
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        confusion = confusion_matrix(y_test, y_pred)
        classification = classification_report(y_test, y_pred)
        return accuracy, confusion, classification

    def save_model(self, model, model_filename='Phishing_model.pkl'):
        with open(model_filename, 'wb') as model_file:
            pickle.dump(model, model_file)

    def load_model(self, model_filename='Phishing_model.pkl'):
        with open(model_filename, 'rb') as model_file:
            self.best_model = pickle.load(model_file)

    def extract_features(self, url):
        features = {}
        try:
            features['UsingIP'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
            features['PrefixSuffix-'] = 1 if '-' in url.split('//')[1] else 0
            features['SubDomains'] = len(url.split('.')) - 2
            features['HTTPS'] = 1 if url.startswith('https') else 0
            features['NonStdPort'] = 1 if re.search(r':\d+', url) else 0
            features['HTTPSDomainURL'] = 1 if 'https://' in url else 0
            features['RequestURL'] = 1 if len(url.split('/')) > 3 else 0
            features['AnchorURL'] = 1 if re.search(r'#[^#]+', url) else 0
            features['LinksInScriptTags'] = 1 if re.search(r'<script', url, re.IGNORECASE) else 0
            features['ServerFormHandler'] = 1 if re.search(r'/cgi-bin/', url, re.IGNORECASE) else 0
            features['AbnormalURL'] = 1 if len(re.findall(r'\.', url)) > 3 else 0
            features['WebsiteForwarding'] = 1 if len(url.split('//')) > 2 else 0
            features['StatusBarCust'] = 1 if re.search(r'status', url, re.IGNORECASE) else 0
            features['DisableRightClick'] = 1 if re.search(r'oncontextmenu', url, re.IGNORECASE) else 0
            features['AgeofDomain'] = len(url)
            features['DNSRecording'] = 1 if re.search(r'dns', url, re.IGNORECASE) else 0
            features['WebsiteTraffic'] = len(url)
            features['PageRank'] = 1 if re.search(r'page', url, re.IGNORECASE) else 0
            features['GoogleIndex'] = 1 if re.search(r'google', url, re.IGNORECASE) else 0
            features['StatsReport'] = 1 if re.search(r'stat', url, re.IGNORECASE) else 0
            features['InfoEmail'] = 1 if re.search(r'@', url) else 0
        except IndexError as e:
            raise ValueError(f"Error processing URL: {url}, {str(e)}")

        ordered_features = [features[name] for name in self.feature_names]
        return ordered_features

    def predict(self, urls):
        phishing_features = pd.DataFrame([self.extract_features(url) for url in urls], columns=self.feature_names)
        predictions = self.best_model.predict(phishing_features)
        return predictions

if __name__ == "__main__":
    detector = PhishingDetection()
    data_file = "model/phishing.csv"
    df = detector.load_data(data_file)
    X_train, X_test, y_train, y_test = detector.preprocess_data(df)
    model = detector.train_model(X_train, y_train)
    accuracy, confusion, classification = detector.evaluate_model(model, X_test, y_test)
    print(f"Accuracy: {accuracy}")
    print(f"Confusion Matrix:\n{confusion}")
    print(f"Classification Report:\n{classification}")
    detector.save_model(model, model_filename='Phishing_model.pkl')
