import bashlex

from common.bash import bash_tokenizer

class TokenOverlap(object):

    @staticmethod
    def compute(gt, pred, verbose=False):
        try:
            gt_cmd_list = TokenOverlap.get_command_list(gt, verbose)
        except bashlex.errors.ParsingError, e:
            gt_cmd_list = TokenOverlap.get_command_list_rule_based(gt)
        except bashlex.tokenizer.MatchedPairError, e:
            gt_cmd_list = TokenOverlap.get_command_list_rule_based(gt)
        except NotImplementedError, e:
            gt_cmd_list = TokenOverlap.get_command_list_rule_based(gt)
        pred_cmd_list = TokenOverlap.get_command_list_rule_based(pred)

        gt_num_cmds = len(gt_cmd_list)
        if gt_num_cmds == 0:
            # ignore ground truth that contains a list of commands
            return -1
        else:
            pred_num_cmds = len(pred_cmd_list)
            overlap_score = 0.0
            for i in xrange(min(gt_num_cmds, pred_num_cmds)):
                overlap_score += TokenOverlap.cmd_overlap_score(gt_cmd_list[i], pred_cmd_list[i])
            return overlap_score / max(gt_num_cmds, pred_num_cmds)

    @staticmethod
    def get_command_list(cmd, verbose=False):
        parse = bashlex.parse(cmd)
        command_list = []
        if parse[0].kind == "pipeline":
            for node in parse[0].parts:
                if node.kind == "command":
                    command_list.append(node)
        elif parse[0].kind == "command":
            command_list = [parse[0]]
        elif parse[0].kind == "list":
            if len(parse[0].parts) == 2:
                # command + operator
                for node in parse[0].parts:
                    if node.kind == "command":
                        command_list.append(node)
            else:
                if verbose:
                    print "Skipped: ground truth contains multiple statements"
                    print
        else:
            if verbose:
                print "Unrecognized node type: " + parse[0].kind
                print 
        return command_list

    @staticmethod
    def get_command_list_rule_based(cmd):
        return cmd.split('|')

    @staticmethod
    def cmd_overlap_score(gt, pred):
        if hasattr(gt, 'parts'):
            gt_token_set = set([n.word for n in gt.parts if n.kind == "word"])
        else:
            gt_token_set = set(bash_tokenizer(gt))
        pred_token_set = set(bash_tokenizer(pred))
        return (len(gt_token_set & pred_token_set) + 0.0) / len(gt_token_set | pred_token_set)