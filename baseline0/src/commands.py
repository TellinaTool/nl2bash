import collections

from model import scores, code_freqs
import common

class ArgInfo(object):
    def __init__(self, type, *args):
        self.type = type
        self.info = args
    def score(self, root_cmd, word):
        if self.type == "seq":
            return sum(part.score(root_cmd, word) for part in self.info)
        elif self.type == "case":
            return max(part.score(root_cmd, word) for part in self.info)
        elif self.type == "empty":
            return 0
        elif self.type == "arg":
            argname = common.mangle_arg(root_cmd, self.info[0])
            return scores.get(word, {}).get(argname, 0) * (1-code_freqs.get(argname, 0))
        elif self.type == "hole":
            return 0
    def propose_incantation(self, root_cmd, total_score, score_func):
        if self.type == "seq":
            return "".join(x.propose_incantation(root_cmd, total_score, score_func) for x in self.info)
        elif self.type == "case":
            empty_is_option = any(x.type == "empty" for x in self.info)
            best_option = max(((x, score_func(x)) for x in self.info), key=lambda x: x[1])
            if best_option[1] < total_score/10: # total hack
                return ""
            else:
                return best_option[0].propose_incantation(root_cmd, total_score, score_func)
        elif self.type == "empty":
            return ""
        elif self.type == "arg":
            argname = self.info[0]
            return " " + argname
        elif self.type == "hole":
            return " " + self.info[0].upper()

def mkarg(x):
    if x is None:
        return empty()
    if isinstance(x, ArgInfo):
        return x
    if isinstance(x, str):
        return ArgInfo("arg", x)
    raise ValueError(x)

def seq(*args):
    if len(args) == 0:
        return empty()
    if len(args) == 1:
        return mkarg(args[0])
    return ArgInfo("seq", *[mkarg(x) for x in args])

def case(*args):
    if len(args) == 1:
        return mkarg(args[0])
    return ArgInfo("case", *[mkarg(x) for x in args])

def empty():
    return ArgInfo("empty")

def optional(arg):
    return case(arg, empty())

def arg(name):
    return ArgInfo("arg", name)

def hole(name):
    return ArgInfo("hole", name)

Tool = collections.namedtuple("Tool", ["name", "flags"])

TAR_ARGS_NO_F = seq(optional("-v"), optional(case("-z", "-j")))
TAR_F = optional(seq("-f", hole("file.tar")))
TAR_ARGS = seq(TAR_ARGS_NO_F, TAR_F)

TOOLS = [
    Tool("find"  , flags=seq(hole("path"),
        seq(
            optional("-not"),
            case(
                seq("-name", hole("pattern")),
                seq("-iname", hole("pattern")),
                seq("-mtime", hole("time")),
                seq("-size", hole("n")),
                seq("-exec", hole("cmd ';'")))),
        case(
            empty(),
            "-delete"))),
    Tool("ls"    , flags=case("-l", "-la")),
    # Tool("sed"   , flags=hole("s/pat/repl/")),
    # Tool("awk"   , flags=hole("script")),
    Tool("grep"  , flags=seq(optional("-e"), optional("-i"), optional("-v"), optional("-r"), hole("regex"))),
    Tool("fgrep"  , flags=seq(optional("-v"), optional("-i"), optional("-r"), hole("string"))),
    Tool("xargs" , flags=seq(optional("-0"), optional("-n1"), hole("cmd"))),
    Tool("rsync" , flags=empty()),
    Tool("scp"   , flags=optional("-R")),
    Tool("tar"   , flags=case(
        seq("-c", TAR_ARGS, "PATH"),
        seq(case("-r", "-u"), TAR_ARGS_NO_F, TAR_F, "PATH"),
        seq(case("-x", "-t"), TAR_ARGS))),
    Tool("sort"  , flags=seq(optional("-n"), optional("-u"))),
    Tool("head"  , flags=optional(seq("-n", hole("n")))),
    Tool("tail"  , flags=optional(seq("-n", hole("n")))),
    Tool("rm"    , flags=case(
        seq("-f",  hole("file")),
        seq("-r",  hole("file_or_dir")),
        seq("-rf", hole("file_or_dir")))),
    Tool("rmdir" , flags=empty()),
    Tool("mv"    , flags=empty()),
    Tool("cp"    , flags=optional("-R")),
    Tool("chmod" , flags=optional("-R")),
    Tool("git"   , flags=case("branch", "commit", "clone", "rebase", "merge", "checkout", "reset", "subtree"))]
