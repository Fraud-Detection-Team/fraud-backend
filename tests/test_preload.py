from app import preload
import pandas as pd

def test_transactions_loaded():
    assert isinstance(preload.transactions_df, pd.DataFrame)
    assert not preload.transactions_df.empty

def test_users_loaded():
    assert isinstance(preload.users_df, pd.DataFrame)
    assert not preload.users_df.empty

def test_cards_loaded():
    assert isinstance(preload.cards_df, pd.DataFrame)
    assert not preload.cards_df.empty

def test_fraud_labels_loaded():
    assert isinstance(preload.fraud_labels, dict)
    assert len(preload.fraud_labels) > 0

def test_mcc_dict_loaded():
    assert isinstance(preload.mcc_dict, dict)
    assert len(preload.mcc_dict) > 0
