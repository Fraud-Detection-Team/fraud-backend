import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from data.loader import load_transactions, load_fraud_labels


def prepare_data():
    transactions = load_transactions()
    labels_dict = load_fraud_labels()

    # Convert labels to DataFrame
    labels_df = pd.DataFrame({
        "id": list(labels_dict.keys()),
        "is_fraud": [1 if v.strip().lower() == "yes" else 0 for v in labels_dict.values()]
    })

    # Merge
    df = transactions.merge(labels_df, on="id", how="inner")

    # Feature selection
    features = df[["amount", "use_chip", "errors", "mcc"]]
    features["use_chip"] = features["use_chip"].astype("category").cat.codes
    features["mcc"] = features["mcc"].astype("category").cat.codes
    features["errors"] = features["errors"].astype("category").cat.codes

    labels = df["is_fraud"]

    return features, labels


def train_and_save_model():
    X, y = prepare_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    joblib.dump(clf, "models/fraud_model_v2.pkl")
    print("✅ Model saved at models/fraud_model_v2.pkl")


if __name__ == "__main__":
    train_and_save_model()
