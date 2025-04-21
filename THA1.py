import os
import shutil
from datetime import datetime

input_folder = r"GITHUB_REPO_VERSION"
archive_base = r"GITHUB_REPO_VERSION"
date_folder = datetime.now().strftime("%m%d%Y")
postal_folder = os.path.join(archive_base, date_folder, "Postal")

os.makedirs(postal_folder, exist_ok=True)
input_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

if not input_files:
    raise Exception("No files found in the input folder.")
elif len(input_files) > 1:
    raise Exception("More than one file found in the input folder. Please clean it up.")

file_name = input_files[0]
src_file_path = os.path.join(input_folder, file_name)

dst_file_path = os.path.join(postal_folder, file_name)
shutil.copy2(src_file_path, dst_file_path)  # Keeps metadata

new_name = "THA_INPUT" + os.path.splitext(file_name)[1]  # Keep original extension
new_path = os.path.join(input_folder, new_name)

# Delete if THA_INPUT already exists to avoid error
if os.path.exists(new_path):
    os.remove(new_path)

os.rename(src_file_path, new_path)

print("File copied to archive and input file renamed.")
