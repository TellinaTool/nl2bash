"""
Repair bad annotations in the existing dataset with fixed annotations.
Keep the original data split.

Usage: python3 repair_data.py [data_directory]
"""

import csv
import os, sys


def import_repairs(import_dir):
    repairs, errors, new_annotations = {}, {}, {}
    new_annotation = False
    for file_name in os.listdir(import_dir):
        print('reading {}...'.format(file_name))
        if file_name.endswith('.csv'):
            with open(os.path.join(import_dir, file_name)) as f:
                reader = csv.DictReader(f) 
                for i, row in enumerate(reader):
                    if i % 2 == 0:
                        command = row['Command'].strip()
                        old_description = row['Description'].strip()
                        print(command)
                        print(old_description)
                        print()
                        new_annotation = (old_description == '--')
                        example_sig = '{}<NL_Command>{}'.format(
                            old_description, command)
                    else:
                        description = row['Description'].strip()
                        if description == '<Type a new description here>':
                            continue
                        elif description == 'ERROR':
                            errors[example_sig] = None
                        else:
                            if new_annotation:
                                new_annotations[
                                    '{}<NL_Command>{}'.format(description, command)] = None
                            else:
                                repairs[example_sig] = description
    print('{} repairs, {} errors and {} new annotations loaded'.format(
        len(repairs), len(errors), len(new_annotations)))
    return repairs, errors, new_annotations


def repair_data(nl_path, cm_path, repairs, errors, new_annotations):
    with open(nl_path) as f:
        nls = [line.strip() for line in f.readlines()]
    with open(cm_path) as f:
        cms = [line.strip() for line in f.readlines()]

    repaired_data = []

    # Add data repairs
    for nl, cm in zip(nls, cms):
        example_sig = '{}<NL_Command>{}'.format(nl, cm)
        if example_sig in repairs:
            new_nl = repairs[example_sig]
            repaired_data.append((new_nl, cm))
        elif example_sig in errors:
            continue
        else:
            repaired_data.append((nl, cm))

    # Add new annotations
    for example_sig in new_annotations:
        repaired_data.append(tuple(example_sig.split('<NL_Command>')))

    repaired_data = sorted(list(set(repaired_data)))
    print('{} repaired data points in total'.format(len(repaired_data)))

    # Save repaired data to disk
    nl_out_path = nl_path + '.repaired'
    cm_out_path = cm_path + '.repaired'
    nl_out = open(nl_out_path, 'w')
    cm_out = open(cm_out_path, 'w')
    for nl, cm in repaired_data:
        nl_out.write('{}\n'.format(nl))
        cm_out.write('{}\n'.format(cm))
    nl_out.close()
    cm_out.close()


if __name__ == '__main__':
    data_dir = sys.argv[1]
    repairs, errors, new_annotations = \
        import_repairs(os.path.join(data_dir, 'repairs'))
    repair_data(os.path.join(data_dir, 'all.nl'),
                os.path.join(data_dir, 'all.cm'),
                repairs, errors, new_annotations)
