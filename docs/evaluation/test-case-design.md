# Test Case Design

Traps are necessary because realistic profiling signals are ambiguous and can trigger overconfident wrong-grain decisions.

Exact string matching is insufficient; semantic outputs vary in phrasing. Golden checks use semantic constraints (required inclusions, forbidden grains, risk keywords, governance flags).

Grain/fact/dimension decisions require domain context (retail lines, snapshots, bridge entities, SCD drift, factless facts).

Case mapping highlights real modeling failures: header-line mixing, snapshot misclassification, identity conflicts, noisy events, bridge omission, degenerate dimensions, and premature SCD finalization.
