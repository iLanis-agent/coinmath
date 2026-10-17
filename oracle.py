#!/usr/bin/env python3
# Coin Math oracle - mirrors engine.js float-for-float.
import json, math

ROLLS = {
    "quarter": {"size": 40, "cents": 25, "plural": "quarters"},
    "dime":    {"size": 50, "cents": 10, "plural": "dimes"},
    "nickel":  {"size": 40, "cents": 5,  "plural": "nickels"},
    "penny":   {"size": 50, "cents": 1,  "plural": "pennies"},
}

def _fixed2(x):
    c = math.floor(x * 100 + 0.5)
    w, r = c // 100, c % 100
    return f"{w}.{r:02d}"

def jar_truth(q, d, n, p):
    for c in (q, d, n, p):
        if not math.isfinite(c) or c < 0:
            raise ValueError("coin counts must be zero or more")
    total_cents = 25 * q + 10 * d + 5 * n + p
    coins = q + d + n + p
    if coins == 0:
        return "The jar is empty - no coins, no math."
    coin_word = "coin" if coins == 1 else "coins"
    if q == 0:
        return f"${_fixed2(total_cents / 100)} across {coins} {coin_word} - no quarters in the jar at all."
    q_word = "quarter" if q == 1 else "quarters"
    return (f"${_fixed2(total_cents / 100)} across {coins} {coin_word} - the {q} {q_word} "
            f"{'carries' if q == 1 else 'carry'} ${_fixed2(25 * q / 100)} of the jar.")

def roll_truth(denom, count):
    spec = ROLLS.get(denom)
    if not spec:
        raise ValueError("pick quarter, dime, nickel, or penny")
    if not math.isfinite(count) or count < 0:
        raise ValueError("coin counts must be zero or more")
    full = math.floor(count / spec["size"])
    loose = count - full * spec["size"]
    roll_cents = spec["size"] * spec["cents"]
    if full == 0:
        return (f"{count} {spec['plural']} do not make a roll yet - {spec['size'] - count} more "
                f"and you have ${_fixed2(roll_cents / 100)}.")
    roll_word = "roll" if full == 1 else "rolls"
    if loose == 0:
        return (f"{count} {spec['plural']} are exactly {full} {roll_word} "
                f"(${_fixed2(full * roll_cents / 100)}) - nothing loose.")
    return (f"{count} {spec['plural']} are {full} full {roll_word} (${_fixed2(full * roll_cents / 100)}) "
            f"plus {loose} loose (${_fixed2(loose * spec['cents'] / 100)}) - the loose ones are the spendable ones.")

def machine_truth(total_dollars, fee_pct):
    if not math.isfinite(total_dollars) or total_dollars < 0:
        raise ValueError("the jar total must be zero or more")
    if not math.isfinite(fee_pct) or fee_pct < 0 or fee_pct > 100:
        raise ValueError("the fee must be between 0 and 100 percent")
    if fee_pct == 0:
        return f"At 0% the whole ${_fixed2(total_dollars)} survives - every cent."
    cut = total_dollars * fee_pct / 100
    keep = total_dollars - cut
    return (f"The machine's {fee_pct}% cut of ${_fixed2(total_dollars)} is ${_fixed2(cut)} - "
            f"you keep ${_fixed2(keep)}, and the quarters you roll yourself escape the fee.")

CASES = [
    ("jarTruth", (47, 23, 8, 112)),
    ("jarTruth", (0, 0, 0, 0)),
    ("jarTruth", (1, 1, 1, 1)),
    ("jarTruth", (0, 30, 0, 5)),
    ("rollTruth", ("quarter", 47)),
    ("rollTruth", ("dime", 23)),
    ("rollTruth", ("penny", 50)),
    ("rollTruth", ("quarter", -1)),
    ("machineTruth", (15.57, 11.9)),
    ("machineTruth", (15.57, 0)),
    ("machineTruth", (-5, 10)),
    ("machineTruth", (20, 120)),
]

FNS = {"jarTruth": jar_truth, "rollTruth": roll_truth, "machineTruth": machine_truth}

out = []
for name, args in CASES:
    try:
        expected = FNS[name](*args)
    except ValueError as e:
        expected = "ERR:" + str(e)
    out.append({"fn": name, "args": list(args), "expected": expected})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, indent=2) + "\n")
print(f"{len(out)} cases written")
