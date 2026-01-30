import pandas as pd

def summarize_by_month(df):
    """
    Groups transactions by month and category, summing the amounts.
    Returns a Pivot Table where index is Month and columns are Categories.
    """
    if df.empty:
        return pd.DataFrame()

    df = df.copy()

    # 1. Create a Period column (e.g., '2026-01') for monthly grouping
    # This ignores the specific day of the month for the aggregation
    df['month'] = df['date'].dt.to_period('M')

    # 2. Pivot the data
    # index = rows (Months)
    # columns = headers (Categories)
    # values = what we are summing (Amount)
    summary = df.pivot_table(
        index='month',
        columns='category',
        values='amount',
        aggfunc='sum'
    )

    # 3. Clean up the output
    summary = summary.fillna(0.0)

    return summary