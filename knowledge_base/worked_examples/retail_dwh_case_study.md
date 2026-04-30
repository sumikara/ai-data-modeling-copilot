This file is an example implementation, not a universal rule.

# Retail DWH Case Study (Worked Example)

This is a worked example. Not universal modeling truth.

## Context
- Domain: retail transactions
- Sources: two synthetic CSV feeds
  - online channel
  - offline/in-store channel
- Approximate volume profile used in the case:
  - bulk: ~500k rows per source
  - incremental: smaller append feeds

## Architecture Used in This Example
- SQL-native ELT on PostgreSQL + PL/pgSQL
- Source-specific landing schemas for online/offline
- Mapping/lineage layer (stg)
- 3NF normalized integration layer (nf)
- Star-schema dimensional layer (dim)
- Logging/orchestration tables for batch and step observability

## Retail-Specific Entities Mentioned
- customer
- product
- store
- promotion
- delivery
- engagement
- employee
- transaction
- date

## Retail Pipeline Flow (Example)
1. CSV accessed via foreign table interface
2. Raw landing persisted per source
3. Standardized source tables created
4. Mapping tables build lineage and derived keys
5. Normalized entity/fact integration loaded
6. Dimensional stars and partitioned fact published
7. Batch/step logging captures run status and row counts

## Retail-Specific Modeling Artifacts
- Snowflake-style normalized nf model
- Star schema in dim model
- Bus matrix combining online and offline business processes
- Partitioned fact table by transaction date
- Employee SCD Type 2 handling

## ERD Interpretation (Example)
- Geographic hierarchy represented via state → city → address relationships.
- Transactions reference multiple domain entities via foreign keys.
- Product/promotion/delivery taxonomies represented as separate controlled entities.
- Online/offline source semantics unified in integrated transaction structures.

## Grain and Dedup in This Example
- Fact grain: one row per retail transaction event.
- Duplicate protection: row signature (MD5) plus incremental exclusion logic.
- Source triplet lineage preserved to avoid unsafe cross-source ID assumptions.

## Worked Example Caveat
- This retail case demonstrates one concrete implementation path.
- Reuse requires adapting entities, key semantics, and SCD policies to the new domain.
