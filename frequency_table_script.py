# github.com/johnlloydpenamante

import os
import pandas as pd
import numpy as np

def run_stats(file_path='Master-Data.xlsx', out_csv='freq_stats_report.csv'):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} missing.")
        return

    excel = pd.ExcelFile(file_path)
    results = []

    print("=" * 60)
    print("FREQUENCY & STATS ANALYSIS")
    print("Copyright (c) 2026 JLandicho_2026-MYGITHUB")
    print("=" * 60)

    for sheet in excel.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(f"\n--- Sheet: {sheet} (Rows: {len(df)}) ---")

        for col in df.columns:
            s = df[col]
            
            if pd.api.types.is_numeric_dtype(s) and s.dropna().count() > 0:
                avg = round(s.mean(), 2)
                med = round(s.median(), 2)
            else:
                avg = med = "N/A"

            modes = s.mode().tolist()
            mod = ", ".join(map(str, modes[:3])) if modes else "N/A"

            print(f"\nColumn: [{col}]")
            print(f"Stats -> Mean: {avg} | Median: {med} | Mode: {mod}")

            cnt = s.value_counts(dropna=False)
            pct = (s.value_counts(normalize=True, dropna=False) * 100).round(2)

            res = pd.DataFrame({
                'Sheet': sheet,
                'Column': col,
                'Mean': avg,
                'Median': med,
                'Mode': mod,
                'Value': cnt.index,
                'Freq': cnt.values,
                'Pct(%)': pct.values
            })

            results.append(res)
            print(res[['Value', 'Freq', 'Pct(%)']].to_string(index=False))
            print("-" * 50)

    final_df = pd.concat(results, ignore_index=True)
    final_df.to_csv(out_csv, index=False)
    print(f"\nSaved report to '{out_csv}'")

if __name__ == "__main__":
    run_stats()

