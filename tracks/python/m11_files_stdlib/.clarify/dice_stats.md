# dice_stats: clarifications

Pattern: injected-rng

The answers an interviewer would give if asked. Compare them with the edge cases
you listed yourself before reading this.

- The same seed in random.Random(seed) must give the same rolls; the module-level
  random state (random.seed) must have no effect on the result.
- Each roll is an int from 1 to `sides`, both included.
- n = 0 returns an empty list; summarise of an empty list returns an empty dict.
- n below 0, or `sides` below 1, raises ValueError.
- summarise lists only faces that appeared (no zero counts), in ascending face order;
  the counts add up to the number of rolls.
- summarise does not change the list it is given.
