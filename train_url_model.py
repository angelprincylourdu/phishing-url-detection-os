import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from feature_extraction import extract_features


DATASET = "PhiUSIIL_Phishing_URL_Dataset.csv"

FEATURE_NAMES = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsHTTPS"
]

print("Loading dataset...")

df = pd.read_csv(DATASET)
df = df.drop_duplicates(subset=["URL"]).reset_index(drop=True)

print("Rows:", len(df))
print("Extracting URL features...")

X = []

for url in df["URL"]:
    values = extract_features(url)
    X.append([values[name] for name in FEATURE_NAMES])

X = pd.DataFrame(X, columns=FEATURE_NAMES)

y = 1 - df["label"]

print("Features:", len(FEATURE_NAMES))

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Random Forest...")

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n===== URL MODEL RESULTS =====")
print("Accuracy:", round(accuracy, 4))

print("\n===== CLASSIFICATION REPORT =====")

print(
    classification_report(
        y_test,
        predictions,
        target_names=["Legitimate", "Phishing"]
    )
)

model_data = {
    "model": model,
    "features": FEATURE_NAMES
}

joblib.dump(model_data, "url_phishing_model_v2.pkl")

print("\nSaved: url_phishing_model_v2.pkl")
