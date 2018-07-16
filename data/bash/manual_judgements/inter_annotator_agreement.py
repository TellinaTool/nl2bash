"""
Compute the inter-annotator agreement.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import csv
import os
import sys

from bashlint import data_tools
from eval.eval_tools import load_cached_evaluations_from_file
from eval.eval_tools import get_example_nl_key, get_example_cm_key
from eval.eval_tools import normalize_judgement

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
            command_eval = normalize_judgement(row['correct command'].strip())
            template_eval = normalize_judgement(row['correct template'].strip())
            command_judgements.append(command_eval)
            template_judgements.append(template_eval)
    return command_judgements, template_judgements

def inter_annotator_agreement(input_files1, input_files2):
    command_judgements1, template_judgements1 = [], []
    command_judgements2, template_judgements2 = [], []
    for input_file in input_files1:
        cj, tj = read_annotations(input_file)
        command_judgements1.extend(cj)
        template_judgements1.extend(tj)
    for input_file in input_files2:
        cj, tj = read_annotations(input_file)
        command_judgements2.extend(cj)
        template_judgements2.extend(tj)
    print('IAA-F: {}'.format(iaa(command_judgements1, command_judgements2)))
    print('IAA-T: {}'.format(iaa(template_judgements1, template_judgements2)))

def combine_annotations_multi_files():
    """
    Combine multiple annotations files and discard the annotations that has a conflict.
    """

    input_dir = sys.argv[1]

    template_evals = {}
    command_evals = {}
    discarded_keys = set({})

    for in_csv in os.listdir(input_dir):
        in_csv_path = os.path.join(input_dir, in_csv)
        with open(in_csv_path) as f:
            reader = csv.DictReader(f)
            current_description = ''
            for row in reader:
                template_eval = normalize_judgement(row['correct template'])
                command_eval = normalize_judgement(row['correct command'])
                description = get_example_nl_key(row['description'])
                if description.strip():
                    current_description = description
                else:
                    description = current_description
                prediction = row['prediction']
                example_key = '{}<NL_PREDICTION>{}'.format(description, prediction)
                if example_key in template_evals and template_evals[example_key] != template_eval:
                    discarded_keys.add(example_key)
                    continue
                if example_key in command_evals and command_evals[example_key] != command_eval:
                    discarded_keys.add(example_key)
                    continue
                template_evals[example_key] = template_eval
                command_evals[example_key] = command_eval
            print('{} read ({} manually annotated examples, {} discarded)'.format(in_csv_path, len(template_evals), len(discarded_keys)))

    # Write to new file
    assert(len(template_evals) == len(command_evals))
    with open('manual_annotations.additional', 'w') as o_f:
        o_f.write('description,prediction,template,correct template,correct comand\n')
        for key in sorted(template_evals.keys()):
            if key in discarded_keys:
                continue
            description, prediction = key.split('<NL_PREDICTION>')
            template_eval = template_evals[example_key]
            command_eval = command_evals[example_key]
            pred_tree = data_tools.bash_parser(prediction)
            pred_temp = data_tools.ast2template(pred_tree, loose_constraints=True)
            o_f.write('"{}","{}","{}",{},{}\n'.format(
                description.replace('"', '""'),
                prediction.replace('"', '""'),
                pred_temp.replace('"', '""'),
                template_eval,
                command_eval
            ))

    
def combine_annotations_multi_annotators():
    """
    Combine the annotations input by three annotators.

    :param input_file1: main annotation file 1.
    :param input_file2: main annotation file 2 (should contain the same number of
        lines as input_file1).
    :param input_file3: supplementary annotation file which contains annotations
        of lines in input_file1 and input_file2 that contain a disagreement.
    :param output_file: file that contains the combined annotations.
    """
    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    input_file3 = sys.argv[3]
    output_file = sys.argv[4]
    o_f = open(output_file, 'w')
    o_f.write('description,prediction,template,correct template,correct command,'
              'correct template A,correct command A,'
              'correct template B,correct command B,'
              'correct template C,correct command C\n')
    sup_structure_eval, sup_command_eval = load_cached_evaluations_from_file(
        input_file3, treat_empty_as_correct=True)

    with open(input_file1) as f1:
        with open(input_file2) as f2:
            reader1 = csv.DictReader(f1)
            reader2 = csv.DictReader(f2)
            current_desp = ''
            for row1, row2 in zip(reader1, reader2):
                row1_template_eval = normalize_judgement(row1['correct template'].strip())
                row1_command_eval = normalize_judgement(row1['correct command'].strip())
                row2_template_eval = normalize_judgement(row2['correct template'].strip())
                row2_command_eval = normalize_judgement(row2['correct command'].strip())
                if row1['description']:
                    current_desp = row1['description'].strip()
                sc_key = get_example_nl_key(current_desp)
                pred_cmd = row1['prediction'].strip()
                if not pred_cmd:
                    row1_template_eval, row1_command_eval = 'n', 'n'
                    row2_template_eval, row2_command_eval = 'n', 'n'
                pred_temp = data_tools.cmd2template(pred_cmd, loose_constraints=True)
                structure_example_key = '{}<NL_PREDICTION>{}'.format(sc_key, pred_temp)
                command_example_key = '{}<NL_PREDICTION>{}'.format(sc_key, pred_cmd)
                row3_template_eval, row3_command_eval = None, None
                if structure_example_key in sup_structure_eval:
                    row3_template_eval = sup_structure_eval[structure_example_key]
                if command_example_key in sup_command_eval:
                    row3_command_eval = sup_command_eval[command_example_key]
                if row1_template_eval != row2_template_eval or row1_command_eval != row2_command_eval:
                    if row1_template_eval != row2_template_eval:
                        if row3_template_eval is None:
                            print(structure_example_key)
                        assert(row3_template_eval is not None)
                        template_eval = row3_template_eval
                    else:
                        template_eval = row1_template_eval
                    if row1_command_eval != row2_command_eval:
                        # if row3_command_eval is None:
                        #     print(command_example_key)
                        assert(row3_command_eval is not None)
                        command_eval = row3_command_eval
                    else:
                        command_eval = row1_command_eval
                else:
                    template_eval = row1_template_eval
                    command_eval = row1_command_eval
                if row3_template_eval is None:
                    row3_template_eval = ''
                if row3_command_eval is None:
                    row3_command_eval = ''
                o_f.write('"{}","{}","{}",{},{},{},{},{},{},{},{}\n'.format(
                    current_desp.replace('"', '""'), pred_cmd.replace('"', '""'), pred_temp.replace('"', '""'),
                    template_eval, command_eval,
                    row1_template_eval, row1_command_eval,
                    row2_template_eval, row2_command_eval,
                    row3_template_eval, row3_command_eval))
    o_f.close()

def print_error_analysis_sheet():
    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    input_file3 = sys.argv[3]
    output_file = sys.argv[4]
    o_f = open(output_file, 'w')
    o_f.write('description,model,prediction,correct template,correct command,'
              'correct template A,correct command A,'
              'correct template B,correct command B,'
              'correct template C,correct command C\n')
    sup_structure_eval, sup_command_eval = load_cached_evaluations_from_file(
        input_file3, treat_empty_as_correct=True)
    # for key in sup_structure_eval:
    #     print(key)
    # print('------------------')
    with open(input_file1) as f1:
        with open(input_file2) as f2:
            reader1 = csv.DictReader(f1)
            reader2 = csv.DictReader(f2)
            current_desp = ''
            for row_id, (row1, row2) in enumerate(zip(reader1, reader2)):
                if row1['description']:
                    current_desp = row1['description'].strip()
                model_name = row2['model']
                if not model_name in ['partial.token-copynet', 'tellina']:
                    continue
                if row_id % 3 != 0:
                    continue
                row1_template_eval = normalize_judgement(row1['correct template'].strip())
                row1_command_eval = normalize_judgement(row1['correct command'].strip())
                row2_template_eval = normalize_judgement(row2['correct template'].strip())
                row2_command_eval = normalize_judgement(row2['correct command'].strip())
                sc_key = get_example_nl_key(current_desp)
                pred_cmd = row1['prediction'].strip()
                if not pred_cmd:
                    row1_template_eval, row1_command_eval = 'n', 'n'
                    row2_template_eval, row2_command_eval = 'n', 'n'
                pred_temp = data_tools.cmd2template(pred_cmd, loose_constraints=True)
                structure_example_key = '{}<NL_PREDICTION>{}'.format(sc_key, pred_temp)
                command_example_key = '{}<NL_PREDICTION>{}'.format(sc_key, pred_cmd)
                row3_template_eval, row3_command_eval = None, None
                if structure_example_key in sup_structure_eval:
                    row3_template_eval = sup_structure_eval[structure_example_key]
                if command_example_key in sup_command_eval:
                    row3_command_eval = sup_command_eval[command_example_key]
                if row1_template_eval != row2_template_eval or row1_command_eval != row2_command_eval:
                    if row1_template_eval != row2_template_eval:
                        if row3_template_eval is None:
                            print(pred_cmd, structure_example_key)
                        assert (row3_template_eval is not None)
                        template_eval = row3_template_eval
                    else:
                        template_eval = row1_template_eval
                    if row1_command_eval != row2_command_eval:
                        # if row3_command_eval is None:
                        #     print(command_example_key)
                        assert (row3_command_eval is not None)
                        command_eval = row3_command_eval
                    else:
                        command_eval = row1_command_eval
                else:
                    template_eval = row1_template_eval
                    command_eval = row1_command_eval
                if row3_template_eval is None:
                    row3_template_eval = ''
                if row3_command_eval is None:
                    row3_command_eval = ''
                o_f.write('"{}","{}","{}",{},{},{},{},{},{},{},{}\n'.format(
                    current_desp.replace('"', '""'), model_name, pred_cmd.replace('"', '""'),
                    template_eval, command_eval,
                    row1_template_eval, row1_command_eval,
                    row2_template_eval, row2_command_eval,
                    row3_template_eval, row3_command_eval))
    o_f.close()

def compute_error_overlap():
    input_file = sys.argv[1]
    template_judgements = []
    command_judgements = []
    with open(input_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            template_eval = row['correct template']
            command_eval = row['correct command']
            if row['model'] == 'tellina':
                template_judgements.append([template_eval])
                command_judgements.append([command_eval])
            else:
                template_judgements[-1].append(template_eval)
                command_judgements[-1].append(command_eval)
    temp_error_hist = [0, 0, 0, 0]
    for t1, t2 in template_judgements:
        if t1 == 'y' and t2 == 'y':
            temp_error_hist[0] += 1
        elif t1 == 'y' and t2 == 'n':
            temp_error_hist[1] += 1
        elif t1 == 'n' and t2 == 'y':
            temp_error_hist[2] += 1
        elif t1 == 'n' and t2 == 'n':
            temp_error_hist[3] += 1
    print('Template Judgements:')
    print('\ty y: {}'.format(temp_error_hist[0]))
    print('\ty n: {}'.format(temp_error_hist[1]))
    print('\tn y: {}'.format(temp_error_hist[2]))
    print('\tn n: {}'.format(temp_error_hist[3]))
    command_error_hist = [0, 0, 0, 0]
    for c1, c2 in command_judgements:
        if c1 == 'y' and c2 == 'y':
            command_error_hist[0] += 1
        elif c1 == 'y' and c2 == 'n':
            command_error_hist[1] += 1
        elif c1 == 'n' and c2 == 'y':
            command_error_hist[2] += 1
        elif c1 == 'n' and c2 == 'n':
            command_error_hist[3] += 1
    print('Command Judgements"')
    print('\ty y: {}'.format(command_error_hist[0]))
    print('\ty n: {}'.format(command_error_hist[1]))
    print('\tn y: {}'.format(command_error_hist[2]))
    print('\tn n: {}'.format(command_error_hist[3]))

def compute_error_category():
    input_file = sys.argv[1]
    tellina_error_hist = collections.defaultdict(int)
    pc_error_hist = collections.defaultdict(int)
    with open(input_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            error_cat = row['error category']
            if error_cat:
                if row['model'] == 'tellina':
                    tellina_error_hist[error_cat] += 1
                elif row['model'] == 'partial.token-copynet':
                    pc_error_hist[error_cat] += 1
                else:
                    raise ValueError
    print('Tellina errors:')
    for ec, freq in sorted(tellina_error_hist.items(), key=lambda x:x[1], reverse=True):
        print(ec, freq)
    print()
    print('Sub-token CopyNet errors:')
    for ec, freq in sorted(pc_error_hist.items(), key=lambda x:x[1], reverse=True):
        print(ec, freq)

def export_annotation_differences(input_file1, input_file2, output_file, command_header):
    o_f = open(output_file, 'w')
    o_f.write('description,{},correct template A,correct command A,correct template B,correct command B\n'.format(
        command_header))
    with open(input_file1) as f1:
        with open(input_file2) as f2:
            reader1 = csv.DictReader(f1)
            reader2 = csv.DictReader(f2)
            current_desp = ''
            desp_written = False
            for row1, row2 in zip(reader1, reader2):
                if row1['description']:
                    current_desp = row1['description']
                    desp_written = False
                if not row1[command_header]:
                    continue
                row1_template_eval = normalize_judgement(row1['correct template'].strip())
                row1_command_eval = normalize_judgement(row1['correct command'].strip())
                row2_template_eval = normalize_judgement(row2['correct template'].strip())
                row2_command_eval = normalize_judgement(row2['correct command'].strip())
                if (row1_template_eval != row2_template_eval) or \
                        (row1_command_eval != row2_command_eval):
                    if not desp_written:
                        o_f.write('"{}","{}",{},{},{},{}\n'.format(
                            current_desp.replace('"', '""'), row1[command_header].replace('"', '""'),
                            row1_template_eval, row1_command_eval, row2_template_eval, row2_command_eval))
                        desp_written = True
                    else:
                        o_f.write(',"{}",{},{},{},{}\n'.format(row1[command_header].replace('"', '""'),
                            row1_template_eval, row1_command_eval, row2_template_eval, row2_command_eval))
    o_f.close()

def main():
    # print_error_analysis_sheet()
    # combine_annotations_multi_annotators()
    # input_files1 = ['unreleased_files/manual.evaluations.test.stc.annotator.1.csv', 'unreleased_files/manual.evaluations.test.tellina.annotator.1.csv']
    # input_files2 = ['unreleased_files/manual.evaluations.test.stc.annotator.2.csv', 'unreleased_files/manual.evaluations.test.tellina.annotator.2.csv']
    # input_files1 = ['unreleased_files/NL-Cmd Judgement (Hamid) - pc.csv', 'unreleased_files/NL-Cmd Judgement (Hamid) - tellina.csv']
    # input_files2 = ['unreleased_files/NL-Cmd Judgement (Shridhar) - pc.csv', 'unreleased_files/NL-Cmd Judgement (Shridhar) - tellina.csv']
    # input_files1 = ['unreleased_files/manual.evaluations.dev.samples.annotator.1.csv']
    # input_files2 = ['unreleased_files/manual.evaluations.dev.samples.annotator.2.csv']
    # inter_annotator_agreement(input_files1, input_files2)
    # compute_error_overlap()
    # compute_error_category()
    combine_annotations_multi_files()    

if __name__ == '__main__':
    main()
