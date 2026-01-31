import pandas as pd
import os
from datetime import datetime

def export_to_excel(summary_df, categorized_df, output_dir="data/reports"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    file_path = os.path.join(output_dir, f"spending_report_{timestamp}.xlsx")

    try:
        # 1. Prepare Summary Data (with Total Column)
        summary_with_total = summary_df.copy()
        summary_with_total['TOTAL'] = summary_with_total.sum(axis=1)
        
        if isinstance(summary_with_total.index, pd.PeriodIndex):
            summary_with_total.index = summary_with_total.index.astype(str)

        # 2. Calculate Executive Metrics
        income = summary_with_total[summary_with_total > 0].sum()
        expenses = summary_with_total[summary_with_total < 0].sum()
        net_flow = income + expenses
        status = net_flow.apply(lambda x: "PROFIT" if x > 0 else "LOSS")

        exec_summary = pd.DataFrame([
            [""] * len(summary_with_total.columns),
            income, expenses, net_flow, status
        ], index=["---", "TOTAL INCOME", "TOTAL EXPENSES", "NET FLOW", "STATUS"], columns=summary_with_total.columns)

        final_summary = pd.concat([summary_with_total, exec_summary])

        # 3. Deep Dive: Top 5 Largest Expenses
        deep_dive = categorized_df.sort_values(by='amount', ascending=True).head(5)
        deep_dive = deep_dive[['date', 'description', 'category', 'amount']]

        # 4. Write to Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            final_summary.to_excel(writer, sheet_name='Monthly Summary')
            
            start_row = len(final_summary) + 4
            worksheet = writer.sheets['Monthly Summary']
            worksheet.cell(row=start_row, column=1, value="DEEP DIVE: TOP 5 LARGEST EXPENSES")
            
            deep_dive.to_excel(writer, sheet_name='Monthly Summary', startrow=start_row)

        print(f"Executive Report and Deep Dive saved: {file_path}")
        return file_path
        
    except Exception as e:
        print(f"Export failed: {e}")
        raise