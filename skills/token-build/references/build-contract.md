# Token build contract

A token build should declare:

- canonical input locations and schema;
- target artifacts and whether they are committed or generated at build time;
- alias-resolution and theme-override rules;
- deterministic command(s) and stale-output detection;
- validation for malformed inputs and target-specific constraints;
- ownership of tooling and CI changes.

Generated artifacts must be traceable to the token source; manually editing both sources creates drift.
