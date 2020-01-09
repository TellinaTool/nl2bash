from src.bashlint import *


def batch_parse(input_file):
    """
    Parse the input_file each line of which is a bash command.
    """
    with open(input_file) as f:
        i = 0
        for cmd in f:
            print("{}. {}".format(i, cmd))
            ast = bash_parser(cmd)
            pretty_print(ast)
            i += 1

def test_bash_parser():
    while True:
        try:
            cmd = input("> ")
            norm_tree = bash_parser(cmd)
            # pruned_tree = normalizer.prune_ast(norm_tree)
            print()
            print("AST:")
            pretty_print(norm_tree, 0)
            # print("Pruned AST:")
            # pretty_print(pruned_tree, 0)
            # search_history = ast2list(norm_tree, 'dfs', list=[])
            # for state in search_history:
            #     print(state)
            print(get_utilities(norm_tree))
            print("Command Template:")
            print(ast2template(norm_tree, ignore_flag_order=False))
            print("Command: ")
            print(ast2command(norm_tree, ignore_flag_order=False))
            # print("Pruned Command Template:")
            # print(ast2template(pruned_tree, ignore_flag_order=False))
            print()
        except EOFError as ex:
            break


def test_bash_tokenizer():

    def test(cmd):
        tokens = bash_tokenizer(cmd)
        print('cmd: {}'.format(cmd))
        print('tokens: {}'.format(tokens))

    cmd1 = 'find . -name "*.andnav" | rename -vn "s/\.andnav$/.tile/"'
    test(cmd1)
    cmd2 = 'find /volume1/uploads -name "*.mkv" -exec mv \{\} \{\}.avi \;'
    test(cmd2)
    cmd3 = 'touch -d "$(date -r filename) - 2 hours" filename'
    test(cmd3)


if __name__ == "__main__":
    # input_file = sys.argv[1]
    # batch_parse(input_file)
    # test_bash_parser()
    test_bash_tokenizer()