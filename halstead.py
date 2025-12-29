import tokenize
import math
from collections import Counter

def halstead_metrics(file_path):
    operators = Counter()
    operands = Counter()

    with open(file_path, "rb") as f:
        for tok in tokenize.tokenize(f.readline):
            if tok.type == tokenize.OP:
                operators[tok.string] += 1
            elif tok.type in (tokenize.NAME, tokenize.NUMBER, tokenize.STRING):
                operands[tok.string] += 1

    n1 = len(operators)
    n2 = len(operands)
    N1 = sum(operators.values())
    N2 = sum(operands.values())

    vocabulary = n1 + n2
    length = N1 + N2

    volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
    effort = volume * difficulty
    bugs = volume / 3000 if volume > 0 else 0

    return {
        "Halstead Volume": round(volume, 2),
        "Halstead Difficulty": round(difficulty, 2),
        "Halstead Effort": round(effort, 2),
        "Estimated Bugs": round(bugs, 3)
    }
