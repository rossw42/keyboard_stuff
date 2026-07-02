import csv
import os

csv_path = r'D:\GitHub\keyboard_stuff\scripts\vial-research\vial_keyboard_pairs.csv'
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    for i, row in enumerate(reader):
        print(f"Row {i+1}: {row}")
        if i >= 10:
            break
