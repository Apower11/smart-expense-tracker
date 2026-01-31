import pandas as pd
import json
import os

def load_categories(config_path='config/categories.json'):
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r') as f:
        return json.load(f)

def apply_categories(df):
    """
    Categorizes transactions based on keywords and ensures 
    correct mathematical signs for Net Spend logic.
    """
    df = df.copy()
    categories = load_categories()
    
    df['category'] = 'Other'
    
    for category, keywords in categories.items():
        for keyword in keywords:
            mask = df['description'].str.contains(keyword, case=False, na=False)
            df.loc[mask, 'category'] = category

    income_categories = ['Income', 'Salary', 'Refund', 'Deposit']

    # 1. Ensure all amounts are treated as absolute values first to reset
    df['amount'] = df['amount'].abs()

    # 2. If category is NOT in income_categories, make it negative (Expense)
    is_expense = ~df['category'].isin(income_categories)
    df.loc[is_expense, 'amount'] = df.loc[is_expense, 'amount'] * -1
    
    return df