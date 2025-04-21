import os
import shutil
import pandas as pd
import time

def create_folders(base_path, folder_name):
    job_folder = os.path.join(base_path, folder_name)
    postal_folder = os.path.join(job_folder, "Postal")
    os.makedirs(postal_folder, exist_ok=True)
    print("Job folders created successfully.\n")
    return postal_folder

def convert_to_csv(file_path, destination_folder):
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
    csv_path = os.path.join(destination_folder, f"{file_name}.csv")
    
    if file_ext.lower() == ".csv":
        shutil.move(file_path, csv_path)
        return csv_path
    elif file_ext.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
        df.to_csv(csv_path, index=False)
        os.remove(file_path)  
        return csv_path
    elif file_ext.lower() == ".tsv":
        df = pd.read_csv(file_path, sep="\t")
        df.to_csv(csv_path, index=False)
        os.remove(file_path) 
        return csv_path
    else:
        print(f"Invalid file type: {file_name}{file_ext} - Deleting file.")
        os.remove(file_path)
        return None

def process_hotdata(source_folder, destination_folder):
    processed_files = []
    print("Processing hotdata folder...\n")
    
    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        if os.path.isfile(file_path):
            csv_file = convert_to_csv(file_path, destination_folder)
            if csv_file:
                processed_files.append(csv_file)
                print(f"Moved and converted: {file_name}")
    
    print("All valid files processed and moved successfully!\n")
    return processed_files

def rename_headers(file_path):
    df = pd.read_csv(file_path)
    print(f"\nProcessing file: {os.path.basename(file_path)}\n")
    
    bcc_fields = [
        "Full Name", "Delivery Address", "Alternate Address", "Alternate 2 Address", 
        "City", "State", "Zip", "First Name", "Last Name"
    ]
    
    new_columns = {}
    for col in df.columns:
        print(f"Current header: {col}")
        for i, field in enumerate(bcc_fields, 1):
            print(f"{i}) {field}")
        
        while True:
            try:
                choice = int(input("Enter the number corresponding to the correct field: "))
                if 1 <= choice <= len(bcc_fields):
                    new_columns[col] = bcc_fields[choice - 1]
                    break
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Please enter a valid number.")
    
    df.rename(columns=new_columns, inplace=True)
    
    if "First Name" in df.columns and "Last Name" in df.columns:
        df["Full Name"] = df["First Name"] + " " + df["Last Name"]
    
    job_date = time.strftime("%m%d%Y")

    job_number = input("Enter Job Number: ")
    account_number = input("Enter Account Number: ")
    mail_class = input("Enter Mail Class: ")
    piece_type = input("Enter Piece Type: ")

    df["Date"] = job_date
    df["JobNum"] = job_number
    df["CustNum"] = account_number
    df["MailClass"] = mail_class
    df["PieceType"] = piece_type

    df.to_csv(file_path, index=False)
    print("Headers renamed and metadata added successfully.\n")

def merge_csv_files(files, output_file):
    print("Merging files...\n")
    dfs = [pd.read_csv(f) for f in files]
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file created: {output_file}\n")

def main():
    print("\n=== Welcome to Scott's Job Assistant ===\n")
    base_path = r"GITHUB_UPLOAD_VERSION"
    hotdata_path = r"GITHUB_UPLOAD_VERSION"
    
    folder_name = input("Enter job folder name (e.g., 123456_ABC): ")
    postal_folder = create_folders(base_path, folder_name)
    
    processed_files = process_hotdata(hotdata_path, postal_folder)
    
    for file in processed_files:
        rename_headers(file)
    
    if len(processed_files) > 1:
        merged_file_path = os.path.join(postal_folder, f"{folder_name}_MERGED.csv")
        merge_csv_files(processed_files, merged_file_path)
    
    print("All files processed and moved successfully!\n")
    time.sleep(2)

if __name__ == "__main__":
    main()
