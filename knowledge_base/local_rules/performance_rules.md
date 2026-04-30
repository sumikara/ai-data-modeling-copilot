This file defines binding rules for the AI Copilot.

# Performance Rules

- Performance tuning MUST follow correctness and traceability, not precede them.
- Indexing MUST align with actual access paths:
  - lineage-driven joins,
  - foreign-key lookups,
  - incremental validation,
  - time-bound fact queries.
- Large fact structures SHOULD use range partitioning on temporal grain columns.
- Partition pruning MUST be enabled through compatible query/filter design.
- Lightweight index options (e.g., BRIN for ordered large date domains) SHOULD be used when workload-appropriate.
- Surrogate key generation SHOULD use explicit sequences for control and portability.
- Indexes MUST support join cost reduction; they MUST NOT be used to mask poor query/model design.
