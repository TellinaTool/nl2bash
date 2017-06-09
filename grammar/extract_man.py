import os
import subprocess

top_cmd_list_file = "top100.txt"
out_dir = "gnu_man_synopsis"


def main():
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    top_cmds = map(lambda x: x.strip(), open(top_cmd_list_file,"r").readlines())
    for cmd in top_cmds:
        f = open(os.path.join(out_dir, cmd), "w")
        out = subprocess.call([cmd, "--help"], stdout=f)

if __name__ == '__main__':
    main()