// Coin Math engine - coin jar honesty.
// Mirrored float-for-float by oracle.py; keep the op order identical.

var ROLLS = {
  quarter: { size: 40, cents: 25, plural: "quarters" },
  dime:    { size: 50, cents: 10, plural: "dimes" },
  nickel:  { size: 40, cents: 5, plural: "nickels" },
  penny:   { size: 50, cents: 1, plural: "pennies" }
};

function _fixed2(x) {
  var c = Math.floor(x * 100 + 0.5);
  var w = Math.floor(c / 100), r = c - w * 100;
  return w + "." + (r < 10 ? "0" + r : "" + r);
}

function _rollValueCents(denom) {
  return ROLLS[denom].size * ROLLS[denom].cents;
}

// The jar truth: what the counts actually add up to.
function jarTruth(q, d, n, p) {
  var counts = [q, d, n, p];
  for (var i = 0; i < counts.length; i++) {
    if (!isFinite(counts[i]) || counts[i] < 0) throw new Error("coin counts must be zero or more");
  }
  var totalCents = 25 * q + 10 * d + 5 * n + p;
  var coins = q + d + n + p;
  if (coins === 0) return "The jar is empty - no coins, no math.";
  var coinWord = coins === 1 ? "coin" : "coins";
  if (q === 0) {
    return "$" + _fixed2(totalCents / 100) + " across " + coins + " " + coinWord +
      " - no quarters in the jar at all.";
  }
  var qWord = q === 1 ? "quarter" : "quarters";
  return "$" + _fixed2(totalCents / 100) + " across " + coins + " " + coinWord + " - the " +
    q + " " + qWord + " " + (q === 1 ? "carries" : "carry") + " $" + _fixed2(25 * q / 100) + " of the jar.";
}

// The roll truth: full rolls versus loose coins, by the published roll counts.
function rollTruth(denom, count) {
  var spec = ROLLS[denom];
  if (!spec) throw new Error("pick quarter, dime, nickel, or penny");
  if (!isFinite(count) || count < 0) throw new Error("coin counts must be zero or more");
  var full = Math.floor(count / spec.size);
  var loose = count - full * spec.size;
  var rollCents = _rollValueCents(denom);
  if (full === 0) {
    return count + " " + spec.plural + " do not make a roll yet - " + (spec.size - count) +
      " more and you have $" + _fixed2(rollCents / 100) + ".";
  }
  var rollWord = full === 1 ? "roll" : "rolls";
  if (loose === 0) {
    return count + " " + spec.plural + " are exactly " + full + " " + rollWord + " ($" +
      _fixed2(full * rollCents / 100) + ") - nothing loose.";
  }
  return count + " " + spec.plural + " are " + full + " full " + rollWord + " ($" +
    _fixed2(full * rollCents / 100) + ") plus " + loose + " loose ($" +
    _fixed2(loose * spec.cents / 100) + ") - the loose ones are the spendable ones.";
}

// The machine truth: what the counting machine's fee actually eats.
function machineTruth(totalDollars, feePct) {
  if (!isFinite(totalDollars) || totalDollars < 0) throw new Error("the jar total must be zero or more");
  if (!isFinite(feePct) || feePct < 0 || feePct > 100) throw new Error("the fee must be between 0 and 100 percent");
  if (feePct === 0) {
    return "At 0% the whole $" + _fixed2(totalDollars) + " survives - every cent.";
  }
  var cut = totalDollars * feePct / 100;
  var keep = totalDollars - cut;
  return "The machine's " + feePct + "% cut of $" + _fixed2(totalDollars) + " is $" +
    _fixed2(cut) + " - you keep $" + _fixed2(keep) + ", and the quarters you roll yourself escape the fee.";
}
