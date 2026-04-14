import pandas as pd
import os

# ✅ Set correct input path
file_path = r"C:\Users\sharan\OneDrive\Desktop\MGNREGA-Karnataka-Analytics\data\Karnataka_mgnrega_FY2023_24.xlsx"

# ✅ Load Excel data
df = pd.read_excel(file_path)
print("✅ File Loaded Successfully — Rows:", len(df))

# ✅ Clean column names
df.columns = [c.strip() for c in df.columns]

# ✅ Convert numerical columns safely
num_cols = [
    'Total_Individuals_Worked', 'Total_Households_Worked', 'Total_No_of_Active_Workers',
    'Total_Exp', 'Wages', 'Average_Wage_rate_per_day_per_person',
    'Total_No_of_HHs_completed_100_Days_of_Wage_Employment',
    'Women_Persondays', 'SC_persondays', 'ST_persondays'
]

for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

# ✅ Compute district-level KPIs
district_kpis = df.groupby('district_name')[num_cols].sum().reset_index()

# ✅ Save output file
output_path = r"C:\Users\sharan\OneDrive\Desktop\MGNREGA-Karnataka-Analytics\data\district_kpis_FY2023_24.csv"
district_kpis.to_csv(output_path, index=False)

print("✅ District KPI CSV saved to:", output_path)
