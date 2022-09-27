import numpy as np
from re import split, sub, search
import sys

ALPHA = "abcdefghijklmnopqrstuvwxyz"
toFixed = lambda n,f: round(n * 10**f) / 10**f
getLetterFromString = lambda s: next((c for c in s if c in ALPHA), "_")
isolate_terms = lambda equation: list(filter(lambda x: x != "", split(r"[\+=]", sub("-", "+-", sub(r"\s+", "", equation)))))
def toDictionary(terms_list):
    d = {}
    for term in terms_list:
        s = search(r"(-*\d+)\**([a-z]{1}(\^\d+)?)?", term)
        co, var = int(s.group(1)), s.group(2)
        d[var] = co
    return d

def main():
    # Acquire equations
    equations = None
    with open("equations.txt", "r") as f:
        equations = f.readlines()
    if equations is None:
        raise Exception("input file is empty")
    # Process equations
    x = list(map(toDictionary, map(isolate_terms, equations)))
    s = set(k for d in x for k in d)
    if (len(s) - 1 if None in s else 0) > len(x):
        raise Exception("too many terms, too few equations")
    v = [[k] for k in list(x[0])[:-1]]
    c = [[d[k] for k in [e[0] for e in v]] for d in x]
    a = [[d[k] for k in list(d)[-1:]] for d in x]
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