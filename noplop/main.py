import sys

from ast import parse, NodeVisitor


class NameCollector(NodeVisitor):
    def __init__(self):
        self.names = []

    def visit_Name(self, node):
        self.names.append(node.id)


class MutationChecker(NodeVisitor):
    def __init__(self):
        self.assignments = [set()]
        self.issues = []

    def is_defined(self, name):
        return any(name in a for a in self.assignments)

    def define(self, name):
        self.assignments[-1].add(name)

    def visit_Assign(self, node):
        for target in node.targets:
            for name in collect_names(target):
                if self.is_defined(name) and name != '_':
                    self.issues.append(node)

                self.define(name)

    def visit_FunctionDef(self, node):
        self.assignments.append(
            set(a.arg for a in node.args.args) |
            set(a.arg for a in node.args.kwonlyargs))
        self.generic_visit(node)
        self.assignments.pop()


def collect_names(node):
    collector = NameCollector()
    collector.visit(node)
    return collector.names


def collect_issues(code):
    m = MutationChecker()
    m.visit(parse(code))
    return m.issues


def run():
    filename = sys.argv[1]
    code = open(filename).read()
    lines = open(filename).readlines()
    issues = collect_issues(code)

    for node in issues:
        segment = lines[node.lineno - 1][node.col_offset:].strip()
        print(f'{filename}:{node.lineno} {segment}')

    sys.exit(bool(issues))
