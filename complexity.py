import ast

class CyclomaticVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1

    def generic_visit(self, node):
        if isinstance(node, (ast.If, ast.For, ast.While,
                             ast.And, ast.Or, ast.ExceptHandler)):
            self.complexity += 1
        super().generic_visit(node)

def cyclomatic_complexity(file_path):
    tree = ast.parse(open(file_path).read())
    visitor = CyclomaticVisitor()
    visitor.visit(tree)
    return visitor.complexity
