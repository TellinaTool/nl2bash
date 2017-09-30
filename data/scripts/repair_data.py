"""
Repair bad annotations in the existing dataset with fixed annotations.
Keep the original data split.

Usage: python3 repair_data.py [data_directory]
"""

import csv
import os, sys

def import_repairs(import_dir):
    repairs, new_annotations = {}, {}
    new_annotation = False
    for file_name in os.listdir(import_dir):
        if file_name.endswith('.csv'):
            with open(os.path.join(import_dir, file_name)) as f:
                reader = csv.DictReader(f) 
                for i, row in enumerate(reader):
                    description = row['Description'].strip()
                    command = row['Command'].strip()
                    if i % 2 == 0:
                        new_annotation = (description == '--')
                        example_sig = '{}<NL_Command>{}'.format(
                            description, command)
                    else:
                        if description == '<Type a new description here>':
                            continue
                        else:
                            if new_annotation:
                                new_annotations[command] = description
                
if __name__ == '__main__':
    data_dir = sys.argv[1]
