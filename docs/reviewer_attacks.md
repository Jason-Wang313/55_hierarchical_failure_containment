# Reviewer Attacks

## Attack: The v1 simulator makes retries free.

Sustained historically. V2 added retry cost and persistent faults. V3 keeps this as a negative control and changes the claim to risk-calibrated containment.

## Attack: More containment can hide stale unsafe state.

Sustained and central. Unlimited retry has propagation 0.074 but masked unsafe 0.231, stale exposure 0.333, and utility -0.096 in the full-scale benchmark.

## Attack: This is only a synthetic benchmark.

Partly sustained. The final paper explicitly claims a deterministic mechanism benchmark and reporting discipline, not real-robot safety.

## Attack: Fixed retry baselines are strong.

Sustained. Fixed one retry has utility 0.492 and fixed two retries has utility 0.470. Risk-calibrated containment still wins as the best non-oracle policy with utility 0.547.

## Attack: The paper should not claim universal superiority over runtime assurance or behavior trees.

Sustained. The claim is narrowed to a containment-budget reporting and architecture mechanism.
