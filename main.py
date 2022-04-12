import numpy as np
from re import split, sub, search
import sys

ALPHA = "abcdefghijklmnopqrstuvwxyz"
toFixed = lambda n,f: round(n * 10**f) / 10**f
def getLetterFromString(s):
    for c in s:
        if c in ALPHA:
            return c
    return "_"
isolate_terms = lambda equation: list(filter(lambda x: x != "", split(r"[\+=]", sub("-", "+-", sub(r"\s+", "", equation)))))
def toDictionary(terms_list):
    d = {}
    for term in terms_list:
        s = search(r"(-*\d+)\**([a-z]{1}(\^\d+)?)?", term)
        co, var = int(s.group(1)), s.group(2)
        d[var] = co
    return d
processEquations = lambda equations: map(toDictionary, map(isolate_terms, equations))
def countTerms(equations):
    s = set(k for d in equations for k in d)
    return len(s) - 1 if None in s else 0
def makeMatrices(equations_dict):
    v = [[k] for k in list(equations_dict[0])[:-1]]
    c = [[d[k] for k in [e[0] for e in v]] for d in equations_dict]
    a = [[d[k] for k in list(d)[-1:]] for d in equations_dict]
    return c, v, a

def main():
    # Acquire equations
    equations = None
    with open("equations.txt", "r") as f:
        equations = f.readlines()
    if equations is None:
        raise Exception("input file is empty")
    # Process equations
    x = list(processEquations(equations))
    if countTerms(x) > len(x):
        raise Exception("too many terms, too few equations")
    c, v, a = makeMatrices(x)
    # Solve equations
    # out = c^-1 * a
    out = [e[0] for e in np.matmul(np.linalg.inv(c),a)]
    var = [e[0] for e in v]
    for i in range(len(v)):
        v = search(r"^[a-z]{1}", var[i]).group()
        s = search(r"\^{1}(\d+)", var[i])
        exp = float(s.group(1)) if s else 1
        print(f"{v} = {toFixed(out[i]**(1/exp),5)}")

if __name__ == "__main__":
    main()