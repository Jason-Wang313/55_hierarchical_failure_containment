# Hostile Reviewer Response

The strongest criticism is correct: the original simulator made local retry too cheap, so the result looked monotone. V2 hardening shows that high retry budgets can mask persistent faults and lower utility.

The revised manuscript therefore makes a conditional architecture claim. Containment budgets are useful only if calibrated against retry cost, escalation cost, and masked-unsafe-state risk. This is workshop-only evidence.
