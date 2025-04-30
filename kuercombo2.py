import pandas as pd
import os
import glob

folder_path = r"GITHUB_DEMO"
excel_files = glob.glob(os.path.join(folder_path, "GITHUB*.xlsx"))
if not excel_files:
    raise FileNotFoundError("No GITHUB Excel file found in the folder.")

excel_file = excel_files[0]
print(f"Found Excel file: {excel_file}")
sheets = pd.read_excel(excel_file, sheet_name=None)
for sheet_name, df in sheets.items():
    for col in df.select_dtypes(include='number').columns:
        df[col] = df[col].round(0).astype('Int64')

    csv_file = os.path.join(folder_path, f"{sheet_name}.csv")
    df.to_csv(csv_file, index=False)
    print(f"Saved cleaned {csv_file}")

for r_file in ["R2.csv", "R3.csv", "R4.csv"]:
    r_path = os.path.join(folder_path, r_file)

    if os.path.exists(r_path):
        df = pd.read_csv(r_path, header=None, skiprows=1)
        df.to_csv(r_path, index=False, header=False)
        print(f"Removed header and cleaned {r_file}")
    else:
        print(f"{r_file} not found, skipping.")

combined_df = pd.DataFrame()

for r_file in ["R1.csv", "R2.csv", "R3.csv", "R4.csv"]:
    r_path = os.path.join(folder_path, r_file)

    if os.path.exists(r_path):
        df = pd.read_csv(r_path, header=None)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
        print(f"Added {r_file} to combo")
    else:
        print(f"{r_file} not found, skipping.")

combo_path = os.path.join(folder_path, "GITHUBCOMBO.csv")
combined_df.to_csv(combo_path, index=False, header=False)
print(f"Saved combined file as {combo_path}")

