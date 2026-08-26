import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Load dataset
print("Loading dataset...")
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

print("Original rows:", len(df))

# Remove duplicate URLs
df = df.drop_duplicates(subset=["URL"]).reset_index(drop=True)

print("Rows after removing duplicate URLs:", len(df))

# Dataset label:
# Original: 0 = Phishing, 1 = Legitimate
# Our model: 1 = Phishing, 0 = Legitimate
y = 1 - df["label"]

# Select numeric features only
X = df.drop(columns=["label"])
X = X.select_dtypes(include=["number"])

print("Features used:", len(X.columns))

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# Random Forest
print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training completed!")

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n===== FINAL MODEL EVALUATION =====")
print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1-Score :", round(f1, 4))

print("\n===== CLASSIFICATION REPORT =====")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Legitimate", "Phishing"]
    )
)

print("===== CONFUSION MATRIX =====")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Save model and feature names
model_data = {
    "model": model,
    "features": list(X.columns)
}

joblib.dump(model_data, "phishing_model.pkl")

print("\nFinal model saved as phishing_model.pkl")
