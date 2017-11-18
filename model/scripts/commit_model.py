#!/usr/bin/python3

import os, sys
import subprocess

def strip_quotes(s):
    assert(len(s) >= 2 and s[0] == '"' and s[-1] == '"')
    return s[1:-1]

def commit_model_files(model_subdir):
    cpt_path = os.path.join(model_subdir, 'checkpoint')
    temp_cpt_path = os.path.join(model_subdir, 'checkpoint.temp')
    assert(os.path.exists(cpt_path))
    model_cpt_file = None
    with open(temp_cpt_path, 'w') as o_f:
        with open(cpt_path) as f:
            for line in f:
                path_name, path = line.strip().split(': ', 1)
                if path_name == 'model_checkpoint_path':
                    model_cpt_file = os.path.basename(
                        strip_quotes(path))
                file_name = os.path.basename(strip_quotes(path))
                o_f.write('{}: "{}"\n'.format(path_name, file_name))
    # subprocess.Popen('git add {}'.format(cpt_path))
    assert(model_cpt_file)

    bak_cpt_path = os.path.join(model_subdir, 'checkpoint.bak')
    os.rename(cpt_path, bak_cpt_path)
    print()
    print('old checkpoint file saved to {}'.format(bak_cpt_path))
    os.rename(temp_cpt_path, cpt_path)
    print('new checkpoint file saved to {}'.format(cpt_path))
    print()
    subprocess.call(['git', 'add', cpt_path])
    subprocess.call(['git', 'add',
        os.path.join(model_subdir, 
            '{}.data-00000-of-00001'.format(
                model_cpt_file))])
    subprocess.call(['git', 'add',
        os.path.join(model_subdir, '{}.index'.format(model_cpt_file))])
    if model_subdir.endswith('normalized'):
        subprocess.call(['git', 'add',
            os.path.join(model_subdir, 'train.mappings.X.Y.npz')])
    if os.path.exists(os.path.join(model_subdir, 
            'predictions.beam_search.100.dev.latest')):
        subprocess.call(['git', 'add',
            os.path.join(model_subdir, 
                'predictions.beam_search.100.dev.latest')])
    subprocess.call(['git', 'commit', '-m', '"check in model {}"'.format(
        model_subdir)])
    subprocess.call(['git', 'push'])

if __name__ == '__main__':
    model_subdir = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))), sys.argv[1])
    commit_model_files(model_subdir)

   
