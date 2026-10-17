# Coin Math

Coin jar honesty. The machine's cut is the most expensive coffee you never drank. Coin Math counts the jar, splits rolls from loose change, and prices the counting machine's fee.

## What it computes

- **The jar truth** - quarters, dimes, nickels, and pennies to a dollar total, plus which denomination carries the jar.
- **The roll truth** - full rolls versus loose coins by the published roll counts (40 quarters, 50 dimes, 40 nickels, 50 pennies).
- **The machine truth** - the counting machine's fee in dollars, and what survives it.

## Boundary

Counting arithmetic only. Your counts, the published roll standards, and the fee you enter. Coin Math never guesses what a coin is worth to a collector.

## Files

- `index.html` - landing page with the honesty pitch and the boundary.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic, shared by the app and the tests.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (12 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/coinmath/
Repo: https://github.com/iLanis-agent/coinmath
