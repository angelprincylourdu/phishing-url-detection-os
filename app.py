from flask import Flask, render_template, request
import joblib
from feature_extraction import extract_features

app = Flask(__name__)

# Load the model trained with the same feature extractor
model_data = joblib.load("url_phishing_model_v2.pkl")
model = model_data["model"]
feature_names = model_data["features"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.form.get("url", "").strip()

    if not url:
        return render_template(
            "result.html",
            url="",
            result="Invalid URL",
            confidence=0,
            features={}
        )

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    extracted = extract_features(url)

    # Put features in exactly the same order used during training
    feature_values = [[extracted[name] for name in feature_names]]

    prediction = model.predict(feature_values)[0]
    probabilities = model.predict_proba(feature_values)[0]

    confidence = round(max(probabilities) * 100, 2)

    if prediction == 1:
        result = "Potentially Suspicious"
    else:
        result = "Potentially Legitimate"

    features = dict(zip(feature_names, feature_values[0]))

    return render_template(
        "result.html",
        url=url,
        result=result,
        confidence=confidence,
        features=features
    )


if __name__ == "__main__":
    app.run(debug=True)
