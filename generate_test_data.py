import pandas as pd
import os

def create_sample_csv():
    # Ensure the data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    data = {
        'date': [
            '2026-01-05', '01/05/2026', # Duplicate pair (different formats)
            '2026-01-10', '2026-01-12', # Groceries
            '2026-01-15', '2026-01-20', # Dining
            '2026-01-25',                # Entertainment (One-off)
            '2026-02-01', '2026-02-05', # Feb Utilities
            '2026-02-10'                 # Uncategorized/Other
        ],
        'amount': [
            '1200.00', '1200.00',       # Rent (Duplicate)
            '$45.50', '82.30',          # Groceries
            '(15.00)', '25.00',         # Dining (Accounting format)
            '1.500,00 €',               # One-off Large Expense (Euro format)
            '120.00', '85.00',          # Utilities
            '99.99'                     # Random shop
        ],
        'description': [
            'Apartment MGMT Rent', 'Apartment MGMT Rent',
            'WAL-MART #1234', 'Whole Foods Market',
            'Starbucks Coffee', 'Uber Eats',
            'VIP CONCERT TICKETS',      # One-off
            'Verizon Wireless', 'City Water Dept',
            'Steam Games'
        ]
    }

    df = pd.DataFrame(data)
    file_path = 'data/sample_transactions.csv'
    df.to_csv(file_path, index=False)
    print(f"✅ Created sample data at: {file_path}")

if __name__ == "__main__":
    create_sample_csv()