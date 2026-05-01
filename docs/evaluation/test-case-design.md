# Test Case Design

Traps are necessary because realistic profiling signals are ambiguous and can trigger overconfident wrong-grain decisions.

Exact string matching is insufficient; semantic outputs vary in phrasing. Golden checks use semantic constraints (required inclusions, forbidden grains, risk keywords, governance flags).

Grain/fact/dimension decisions require domain context (retail lines, snapshots, bridge entities, SCD drift, factless facts).

Case mapping highlights real modeling failures: header-line mixing, snapshot misclassification, identity conflicts, noisy events, bridge omission, degenerate dimensions, and premature SCD finalization.


## Trap design principles
1. transaction_id alone
2. order_id header-line ambiguity
3. product descriptor vs snapshot fact
4. customer_id with cross-source conflict
5. event_id weak uniqueness
6. lifecycle dates vs accumulating snapshot
7. no measures vs factless fact
8. many-to-many bridge
9. invoice number degenerate dimension
10. product attribute drift vs final SCD choice
