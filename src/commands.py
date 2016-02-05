import collections

from model import scores, code_freqs

class ArgInfo(object):
    def __init__(self, type, *args):
        self.type = type
        self.info = args
    def score(self, word):
        if self.type == "seq":
            return sum(part.score(word) for part in self.info)
        elif self.type == "case":
            return max(part.score(word) for part in self.info)
        elif self.type == "empty":
            return 0
        elif self.type == "arg":
            argname = self.info[0]
            return scores.get(word, {}).get(argname, 0) * (1-code_freqs.get(argname, 0))
        elif self.type == "hole":
            return 0
    def propose_incantation(self, total_score, score_func):
        if self.type == "seq":
            return "".join(x.propose_incantation(total_score, score_func) for x in self.info)
        elif self.type == "case":
            empty_is_option = any(x.type == "empty" for x in self.info)
            best_option = max(((x, score_func(x)) for x in self.info), key=lambda x: x[1])
            if best_option[1] < total_score/10: # total hack
                return ""
            else:
                return best_option[0].propose_incantation(total_score, score_func)
        elif self.type == "empty":
            return ""
        elif self.type == "arg":
            argname = self.info[0]
            return " " + argname
        elif self.type == "hole":
            return " " + self.info[0].upper()

def mkarg(x):
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

TAR_ARGS = [dash + main_cmd + v + f
    for dash in ["-", ""]
    for main_cmd in "xct"
    for v in ["v", ""]
    for f in ["f", ""]]

TOOLS = [
    Tool("find"  , flags=seq(hole("path"),
        seq(
            optional(arg("-not")),
            case(
                seq(arg("-name"), hole("pattern")),
                seq(arg("-iname"), hole("pattern")),
                seq(arg("-mtime"), hole("time")),
                seq(arg("-size"), hole("n")),
                seq(arg("-exec"), hole("cmd ';'")))),
        case(
            empty(),
            arg("-delete")))),
    Tool("ls"    , flags=case("-l", "-la")),
    # Tool("sed"   , flags=hole("s/pat/repl/")),
    # Tool("awk"   , flags=hole("script")),
    Tool("grep"  , flags=seq(optional(arg("-e")), optional(arg("-i")), optional(arg("-v")), optional(arg("-r")), hole("regex"))),
    Tool("fgrep"  , flags=seq(optional(arg("-v")), optional(arg("-i")), optional(arg("-r")), hole("string"))),
    Tool("xargs" , flags=seq(optional("-0"), optional("-n1"), hole("cmd"))),
    Tool("rsync" , flags=empty()),
    Tool("scp"   , flags=optional("-R")),
    Tool("tar"   , flags=case(*[(seq(arg(a), optional(hole("archive.tar"))) if "f" in a else arg(a)) for a in TAR_ARGS])),
    Tool("sort"  , flags=seq(optional("-n"), optional("-u"))),
    Tool("head"  , flags=optional(seq("-n", hole("n")))),
    Tool("tail"  , flags=optional(seq("-n", hole("n")))),
    Tool("rm"    , flags=case(
        seq(arg("-f"),  hole("file")),
        seq(arg("-r"),  hole("file_or_dir")),
        seq(arg("-rf"), hole("file_or_dir")))),
    Tool("rmdir" , flags=empty()),
    Tool("mv"    , flags=empty()),
    Tool("cp"    , flags=optional("-R")),
    Tool("chmod" , flags=optional("-R")),
    Tool("git"   , flags=case("branch", "commit", "clone", "rebase", "merge", "checkout", "reset", "subtree"))]
