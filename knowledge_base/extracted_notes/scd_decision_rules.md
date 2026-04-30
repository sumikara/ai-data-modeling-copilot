# SLOWLY CHANGING DIMENSIONS (SCD) & KEY DESIGN

> **AI Copilot Usage Note:** Use this document to govern key strategy, SCD behavior, default-row handling, and historical integrity decisions.

---

## 1. Key Concepts

### Primary Key (PK)
- Uniquely identifies each row.
- Must remain stable and non-null.

### Foreign Key (FK)
- References a PK in another table.
- Preserves relational integrity across layers.

### Natural Key (NK)
- Originates from source systems.
- Reflects business identity.
- May drift, collide, or be missing across sources.

### Surrogate Key (SK)
- Warehouse-generated identifier.
- Preferred PK pattern for dimensions in DWH.
- Immutable and integration-friendly.

---

## 2. Why Surrogate Keys Are Required

Natural keys are often insufficient because they can:
- change over time,
- fail uniqueness across systems,
- be null or malformed.

Surrogate keys address:
- key stability,
- cross-source integration,
- robust SCD implementation.

```text
Copilot rule:
Use NK for mapping/lineage.
Use SK for dimensional joins and history control.
```

---

## 3. Slowly Changing Dimensions (SCD)

SCD policy determines how attribute changes are represented over time in dimensions.

No SCD recommendation is valid without explicit business and audit context.

---

## 4. SCD Type 0 (Fixed)

- No post-load changes.
- Attribute remains constant.

Use when:
- attribute is treated as permanently fixed.

---

## 5. SCD Type 1 (Overwrite)

- Replace old value in-place.
- No historical version retained.

Use when:
- correction/current-state reporting is sufficient.

Typical case:
- typo/data correction where history has no analytic value.

---

## 6. SCD Type 2 (History Tracking)

- Insert a new row for each tracked change.
- Preserve prior versions.

Required control columns:
- `start_date`
- `end_date`
- `is_active`

---

## 7. SCD Type 2 Rules

- Do not overwrite current historical row for tracked attributes.
- Close old version (`end_date`, deactivate).
- Insert new active version.
- Keep SK-based version identity.

```text
Type 2 invariant:
one active row per business key at a point in time
```

---

## 8. SCD Type 3 (Limited History)

- Store current and previous value in separate columns.
- Limited history only.

Use when:
- short lookback is enough and full versioning is unnecessary.

---

## 9. Hybrid SCD

- Different attributes in same entity may use different SCD policies.

Example pattern:
- Type 2 for high-impact identity/location attributes
- Type 1 for low-impact correction attributes

---

## 10. SCD Decision Logic

SCD selection must be driven by:
- business semantics,
- audit/compliance requirements,
- reporting/history needs.

Copilot must provide evidence and alternatives, not unconditional finalization.

---

## 11. Dimension Versioning Strategy

Each tracked change should:
- preserve previous state,
- create a new version,
- retain lineage to source/business key.

Versioning must be deterministic and rerunnable.

---

## 12. Surrogate Key Generation

Allowed strategies (platform-dependent):
- sequence
- identity
- UUID

Selection criteria:
- stability
- performance
- operational compatibility

---

## 13. Key Mapping Strategy

Mapping bridge is required:

```text
Natural Key -> Surrogate Key
```

Used in:
- dimension load/upsert control
- fact FK resolution
- cross-layer conformance

---

## 14. Composite Keys

Use composite business keys when one source attribute is insufficient for uniqueness.

Example pattern:
- `transaction_id + product_id`

Composite keys are mapping identities; dimensional joins should still resolve to SK.

---

## 15. Business Key vs Technical Key

### Business Key
- Semantically meaningful in business processes.

### Technical Key
- System-managed identifier for storage/join/version control.

Copilot should preserve both roles explicitly.

---

## 16. Key Stability Rules

Keys used for core modeling must be:
- unique (within defined scope),
- stable,
- non-null,
- consistent across pipeline layers.

---

## 17. Default Row Strategy (Critical)

When FK resolution fails, use controlled default member routing.

Common defaults:
- numeric key: `-1`
- text value: `'n.a.'`
- date fallback: `'1900-01-01'` (or approved project baseline)

---

## 18. Handling Missing Dimensions

Do not leave unresolved FKs as uncontrolled NULLs.

Required behavior:
- link fact to approved default row,
- preserve load continuity and referential integrity,
- log unresolved mapping event.

---

## 19. Late Arriving Dimensions

Scenario:
- fact event arrives before corresponding dimension member is available.

Strategy:
- route to default member first,
- reconcile/update via controlled backfill when dimension arrives.

---

## 20. Early Arriving Facts

Scenario:
- fact depends on future/unknown descriptive context.

Strategy:
- use placeholder/default dimension member,
- maintain correction workflow once true dimension context is available.

---

## 21. Degenerate Keys

A degenerate key is stored in fact without separate dimension table.

Typical example:
- `order_id` / `transaction_id`

Use when identifier is analytically useful but has no stable descriptive attribute set.

---

## 22. Surrogate Key Propagation

SK discipline must be consistent through:
- staging resolution steps,
- core/integration models,
- dimensional publications.

Broken SK propagation causes join inconsistency and historical drift.

---

## 23. Key Integrity Constraints

Integrity checks must ensure:
- no unintended duplicates,
- valid FK-to-dimension resolution,
- stable join behavior across reruns.

---

## 24. Key Conflict Handling

On key conflicts:
- apply trusted-source priority policy,
- apply business conflict rules,
- log discrepancies for audit and remediation.

No silent conflict suppression.

---

## 25. SCD Pitfalls

Avoid:
- overwriting when Type 2 versioning is required,
- losing historical states,
- mixing SCD policies without attribute-level rules,
- inconsistent NK/SK assignment logic.

---

## 26. AI Copilot Rules (Important)

The Copilot must:
- never assign SCD type without evidence,
- never overwrite history unless Type 1 is explicitly approved,
- require human approval for Type 2 policy finalization,
- preserve key lineage and key-mapping traceability,
- surface ambiguity and risk when SCD evidence is incomplete.

```text
Approval gate:
No final SCD policy is published until business owner + data architect approval is recorded.
```
