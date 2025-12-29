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

    # Distinct counts
    n1 = len(operators)          # distinct operators
    n2 = len(operands)           # distinct operands

    # Total counts
    N1 = sum(operators.values()) # total operators
    N2 = sum(operands.values())  # total operands

    vocabulary = n1 + n2
    program_length = N1 + N2

    volume = program_length * math.log2(vocabulary) if vocabulary > 0 else 0
    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
    effort = volume * difficulty
    bugs = volume / 3000 if volume > 0 else 0

    return {
        "n1": n1,
        "n2": n2,
        "N1": N1,
        "N2": N2,
        "Vocabulary": vocabulary,
        "ProgramLength": program_length,
        "Volume": round(volume, 2),
        "Difficulty": round(difficulty, 2),
        "Effort": round(effort, 2),
        "Estimated Bugs": round(bugs, 3)
    }
