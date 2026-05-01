This file defines binding rules for the AI Copilot.

# Entity Business Key Decisions

## Purpose
This document records entity-by-entity business key decisions derived from profiling evidence for the Retail DWH reference project.

## AI Copilot Usage Rules
For each entity recommendation, the AI must explicitly output:
- raw key,
- candidate business key,
- engineered `*_src_id` rule,
- caveats,
- decision confidence,
- whether human approval is required.

The AI must not silently resolve unresolved identity conflicts.

## Decision Summary Table
| Entity | Recommended Business Key (Current Project) | Confidence | Human Approval Required |
|---|---|---|---|
| Product | `product_category + product_name + product_brand + product_material` | Medium | No |
| Store | `store_location + store_city + store_state` | Medium | No |
| Geography - State | `state` | High | No |
| Geography - City | `city + state` | High | No |
| Geography - Address | `city + state + zip` | Medium | No |
| Employee | `employee_name` (or normalized `employee_src_id`) | Low/Medium | Yes |
| Engagement | Decision gate: event key vs profile key | Medium | Yes |
| Delivery | Analytical key `delivery_type + shipping_partner`; instance/profile gate required | Medium | Yes |
| Promotion | `promotion_type + promotion_channel + promotion_start_dt + promotion_end_dt` | Medium | No |
| Customer | `DECISION_REQUIRED` | Low | Yes |

## Product
### Profiling Findings
- `product_name` is reused across categories.
- `product_name` alone is not sufficiently meaningful.
- `product_category + product_name + product_brand` is still too coarse.
- Adding `product_material` increases variant separation.

### Recommended Business Key
`product_category + product_name + product_brand + product_material`

### Rationale
`product_material` affects product identity in this synthetic dataset; omitting it collapses distinct variants.

### Caveat
In production retail systems, SKU (or equivalent catalog master identifier) is typically preferred.

## Store
### Profiling Findings
- `store_location + city + state + zip` inflates store-key cardinality.
- `zip` behaves like noisy or transaction-varying detail.
- `store_location + city + state` yields more realistic store cardinality.

### Recommended Business Key
`store_location + store_city + store_state`

### Rationale
This reduces artificial store explosion caused by zip variation.

## Geography
### State Key
`state`

### City Key
`city + state`

### Address Key
`city + state + zip`

### Rule
`city` alone is unsafe because city names can repeat across states.

## Employee
### Profiling Findings
- The synthetic dataset includes 100 employee names.
- `employee_name` behaves as a stable identifier in this dataset.
- In real operations, employee names are not robust natural keys.

### Recommended Business Key for This Dataset
`employee_name` (or normalized `employee_src_id` derived from employee name)

### Caveat
Real systems should use HR employee number (or equivalent authoritative employee identifier).

## Engagement
### Profiling Findings
- `engagement_id` is unique at row/event level.
- Descriptive engagement combinations are much smaller than event-level rows.

### Interpretation
Two valid modeling paths exist:
- `engagement_id` as event/instance key,
- `order_channel + support_method + issue_status + app_usage + social_media_engagement` as reusable profile/segment key.

### Recommendation
AI should emit an explicit decision gate: event entity vs reusable engagement profile dimension.

## Delivery
### Profiling Findings
- `delivery_id` behaves like an instance key.
- `delivery_type + delivery_status + shipping_partner` creates a small profile set.
- `delivery_status` may change over time and can be volatile.

### Recommended Analytical Key
`delivery_type + shipping_partner`

### Delivery Status Rule
Treat `delivery_status` as descriptive/latest known state, not a structural key component.

### Gate Required
Delivery instance vs delivery profile modeling must be human-approved.

## Promotion
### Profiling Findings
- `promotion_type + promotion_channel` is too broad.
- Adding start/end dates moves toward occurrence-level uniqueness.
- Raw `promotion_id` alone is not trusted as stable identity.

### Practical Key
`promotion_type + promotion_channel + promotion_start_dt + promotion_end_dt`

### Interpretation
This key acts as an occurrence/version-level identifier, not a pure reusable promotion master key.

### Modeling Rule
Treat promotions as immutable promotion versions/business events.

### SCD Type
Type 0 (insert-only).

## Customer
### Conflict / Decision Required
Conflicting notes exist:
1. `customer_id` is unique and can be used as business key.
2. `customer_id` is unreliable, so `customer_src_id` should be engineered from demographic + geography attributes.

Required unresolved marker:
- `DECISION_REQUIRED: Customer identity strategy.`

Possible interpretations:
- `customer_id` as source-native unique key,
- `customer_src_id` as demographic-profile key,
- customer as a derived profile entity due to anonymized/incomplete source characteristics.

AI must not choose one interpretation silently.

## Cross-Document Harmonization Notes
- `DECISION_REQUIRED`: Confirm whether the customer identity resolution policy should be codified here as the canonical local rule, or deferred to a dedicated customer-identity governance artifact.
