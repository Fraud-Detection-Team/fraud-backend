from data import loader

# Load once at app startup
transactions_df = loader.load_transactions()
users_df = loader.load_users()
cards_df = loader.load_cards()
fraud_labels = loader.load_fraud_labels()
mcc_dict = loader.load_mcc_codes()
