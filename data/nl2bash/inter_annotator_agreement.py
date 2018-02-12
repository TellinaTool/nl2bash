"""
Compute the inter-annotator agreement.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import csv

def iaa(a1, a2):
    assert(len(a1) == len(a2))
    num_agree = 0
    for i in range(len(a1)):
        if a1[i].lower() == a2[i].lower():
            num_agree += 1
    return float(num_agree) / len(a1)

def read_annotations(input_file):
    command_judgements, template_judgements = [], []
    with open(input_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            command_eval = row['correct command'].strip()
            if not command_eval or command_eval.lower() == 'y':
                command_eval = 'y'
            else:
                command_eval = 'n'
            template_eval = row['correct template'].strip()
            if not template_eval or command_eval.lower() == 'y':
                template_eval = 'y'
            else:
                command_eval = 'n'
            command_judgements.append(command_eval)
            template_judgements.append(template_eval)
    return command_judgements, template_judgements

def combine_annotations(input_file1, input_file2):
    o_f = open('manual.evaluations.1119.copy-partial.csv', 'w')
    o_f.write('description,prediction,template,correct template,correct command\n')
    with open(input_file1) as f1:
        with open(input_file2) as f2:
            reader1 = csv.DictReader(f1)
            reader2 = csv.DictReader(f2)
            for row1, row2 in zip(reader1, reader2):
                if row1['correct template'] == row2['correct template']:
                    row = copy.deepcopy(row1)
                    if row1['correct command'] != row2['correct command']:
                        row['correct command'] = ''
                    row_template =
                    o_f.write('"{}","{}","{}",{},{}\n'.format(row['description'].replace('"', '""'),
                                                              row['command'].replace('"', '""'),
                                                              row_template.replace('"', '""'),
                                                              row['correct template'],
                                                              row['correct command']))

def main():
    """shridhar_pc = read_annotations('NL-Cmd Judgement (Shridhar) - pc.csv')
    shridhar_tellina = read_annotations('NL-Cmd Judgement (Shridhar) - tellina.csv')
    hamid_pc = read_annotations('NL-Cmd Judgement (Hamid) - pc.csv')
    hamid_tellina = read_annotations('NL-Cmd Judgement (Hamid) - tellina.csv')
    eric_pc = read_annotations('NL-Cmd Judgement (Eric) - pc.csv')
    eric_tellina = read_annotations('NL-Cmd Judgement (Eric) - tellina.csv')
    # serge_pc = read_annotations('NL-Cmd Judgement Batch II (Serge) - pc.csv')
    # serge_tellina = read_annotations('NL-Cmd Judgement Batch II (Serge) - tellina.csv')

    shridhar_command_judgements = shridhar_pc[0] + shridhar_tellina[0]
    shridhar_template_judgements = shridhar_pc[1] + shridhar_tellina[1]
    hamid_command_judgements = hamid_pc[0] + hamid_tellina[0]
    hamid_template_judgements = hamid_pc[1] + hamid_tellina[1]
    eric_command_judgements = eric_pc[0] + eric_tellina[0]
    eric_template_judgements = eric_pc[1] + eric_tellina[1]
    # serge_command_judgements = serge_pc[0] + serge_tellina[0]
    # serge_template_judgements = serge_pc[1] + serge_tellina[1]

    print('Command inter-annotator agreement')
    print('Shridhar vs. Hamid', iaa(shridhar_command_judgements, hamid_command_judgements))
    print('Shridhar vs. Eric', iaa(shridhar_command_judgements, eric_command_judgements))
    print('Hamid vs. Eric', iaa(hamid_command_judgements, eric_command_judgements))
    print()

    print('Template inter-annotator agreement')
    print('Shridhar vs. Hamid', iaa(shridhar_template_judgements, hamid_template_judgements))
    print('Shridhar vs. Eric', iaa(shridhar_template_judgements, eric_template_judgements))
    print('Hamid vs. Eric', iaa(hamid_template_judgements, eric_template_judgements))
    print()
    """

    combine_annotations('NL-Cmd Judgement (Shridhar) - pc.csv', 'NL-Cmd Judgement (Hamid) - pc.csv')

if __name__ == '__main__':
    main()
