import ast

class OOMetrics(ast.NodeVisitor):
    def __init__(self):
        self.classes = {}
        self.inheritance = {}

    def visit_ClassDef(self, node):
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        self.classes[node.name] = len(methods)

        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        self.inheritance[node.name] = bases

        self.generic_visit(node)

def compute_oo_metrics(file_path):
    tree = ast.parse(open(file_path).read())
    visitor = OOMetrics()
    visitor.visit(tree)

    noc = {cls: 0 for cls in visitor.classes}
    for bases in visitor.inheritance.values():
        for base in bases:
            if base in noc:
                noc[base] += 1

    return visitor.classes, noc
