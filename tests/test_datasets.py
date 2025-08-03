from app.data.loader import (
    load_transactions, load_users, load_cards,
    load_mcc_codes, load_fraud_labels, load_zip_coordinates
)


def test_load_transactions():
    df = load_transactions()
    assert not df.empty
    assert "id" in df.columns
    assert df["amount"].dtype == float
    assert df["id"].dtype == object or df["id"].dtype == "string"
    assert df["amount"].notnull().all()


def test_load_users():
    df = load_users()
    assert not df.empty
    assert "id" in df.columns
    assert "yearly_income" in df.columns
    assert df["yearly_income"].dtype == float
    assert df["id"].dtype == object or df["id"].dtype == "string"


def test_load_cards():
    df = load_cards()
    assert not df.empty
    assert "id" in df.columns
    assert "is_compromised" in df.columns
    assert df["is_compromised"].dtype == bool


def test_load_mcc_codes():
    mcc = load_mcc_codes()
    assert isinstance(mcc, dict)
    assert len(mcc) > 0
    sample_key = list(mcc.keys())[0]
    sample_val = mcc[sample_key]
    assert isinstance(sample_key, str)
    assert isinstance(sample_val, str)


def test_load_fraud_labels():
    labels = load_fraud_labels()
    assert isinstance(labels, dict)
    assert all(isinstance(k, str) for k in labels.keys())
    assert all(isinstance(v, str) for v in labels.values())


def test_load_zip_coordinates():
    coords = load_zip_coordinates()
    assert isinstance(coords, dict)
    assert len(coords) > 0
    sample_key = list(coords.keys())[0]
    assert isinstance(sample_key, str)
    sample_val = coords[sample_key]
    assert "latitude" in sample_val and "longitude" in sample_val
    assert isinstance(sample_val["latitude"], float)
    assert isinstance(sample_val["longitude"], float)
