# Python script to generate district-level plots

import pandas as pd
import matplotlib.pyplot as plt
import os

# ✅ Paths
data_path = r"C:\Users\sharan\OneDrive\Desktop\MGNREGA-Karnataka-Analytics\data\district_kpis_FY2023_24.csv"
output_dir = r"C:\Users\sharan\OneDrive\Desktop\MGNREGA-Karnataka-Analytics\visuals"

# ✅ Create output folder if not exists
os.makedirs(output_dir, exist_ok=True)

# ✅ Load KPI data
df = pd.read_csv(data_path)
print("✅ Data Loaded for Visualization:", df.shape)

# Helper function to create bar charts
def plot_top_bottom(df, column, title):
    top10 = df.nlargest(10, column)
    bottom10 = df.nsmallest(10, column)

    plt.figure(figsize=(10, 6))
    plt.barh(top10['district_name'], top10[column], color='green')
    plt.title(f"Top 10 Districts - {title}")
    plt.xlabel(column)
    plt.tight_layout()
    top_path = os.path.join(output_dir, f"{column}_top10.png")
    plt.savefig(top_path)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.barh(bottom10['district_name'], bottom10[column], color='red')
    plt.title(f"Bottom 10 Districts - {title}")
    plt.xlabel(column)
    plt.tight_layout()
    bottom_path = os.path.join(output_dir, f"{column}_bottom10.png")
    plt.savefig(bottom_path)
    plt.close()

    print(f"✅ Saved charts for {column}")

# ✅ Generate charts for each key metric
metrics = [
    ("Total_Individuals_Worked", "Individuals Worked"),
    ("Total_Households_Worked", "Households Worked"),
    ("Total_Exp", "Total Expenditure (in Lakhs)"),
    ("Wages", "Total Wages (in Lakhs)"),
    ("Average_Wage_rate_per_day_per_person", "Average Daily Wage Rate"),
    ("Total_No_of_HHs_completed_100_Days_of_Wage_Employment", "HHs Completed 100 Days"),
]

for col, title in metrics:
    if col in df.columns:
        plot_top_bottom(df, col, title)

print("🎉 All visualization charts saved to:", output_dir)
