import os
import datetime


def search_files(directory, file_name=None, extension=None, modified_after=None):
    matches = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file_name and file_name not in file:
                continue
            if extension and not file.endswith(extension):
                continue
            full_path = os.path.join(root, file)
            if modified_after:
                last_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
                if last_modified_date < modified_after:
                    continue
            matches.append(full_path)
    return matches


directory = input("Search in directory (ex: C:/): ")
file_name = input("Search for files containing (leave blank for any): ")
extension = input("File extension (leave blank for any): ")
date_input = input("Modified after (YYYY-MM-DD, leave blank for any): ")

modified_after = None
if date_input:
    year, month, day = map(int, date_input.split('-'))
    modified_after = datetime.datetime(year, month, day)

print("finding...")
found_files = search_files(directory, file_name, extension, modified_after)
print("\nFound files:")
for file in found_files:
    print(file)
