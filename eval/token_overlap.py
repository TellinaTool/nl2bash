import bashlex

class TokenOverlap(object):

    @staticmethod
    def compute(gt, pred):
        gt_cmd_list = TokenOverlap.get_command_list(gt)
        pred_cmd_list = TokenOverlap.get_command_list(pred)
        gt_num_cmds = len(gt_cmd_list)
        pred_num_cmds = len(pred_cmd_list)
        overlap_score = 0.0
        for i in xrange(min(gt_num_cmds, pred_num_cmds)):
            overlap_score += TokenOverlap.cmd_overlap_score(gt_cmd_list[i], pred_cmd_list[i])
        return overlap_score / max(gt_num_cmds, pred_num_cmds)

    @staticmethod
    def get_command_list(cmd):
        parse = bashlex.parse(cmd)
        command_list = []
        if parse[0].kind == "pipeline":
            for node in parse[0].parts:
                if node.kind == "command":
                    command_list.append(node)
        elif parse[0].kind == "command":
            command_list = [parse[0]]
        else:
            print "Unrecognized node type: " + parse[0].kind
        return command_list

    @staticmethod
    def cmd_overlap_score(gt, pred):
        gt_token_set = set([n.word for n in gt.parts if n.kind == "word"])
        pred_token_set = set([n.word for n in pred.parts if n.kind == "word"])
        return (len(gt_token_set & pred_token_set) + 0.0) / len(gt_token_set | pred_token_set)