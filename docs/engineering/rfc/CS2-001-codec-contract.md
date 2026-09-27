# RFC-CS2-001 Codec, Projection, and Migration Contract

This companion contract deepens RFC-CS2-001 without changing its conformance ladder.

## Codec law
Canonical encoding is UTF-8 JSON with sorted object keys, no insignificant whitespace, and no NaN/Infinity. Set-like reference arrays are normalized lexicographically. Claim, source, and evidence arrays canonicalize by id.

The codec is bounded by explicit record-size, record-count, nesting-depth, and aggregate collection limits. A limit refusal is a transport refusal, not a claim about the subject.

## Stream law
JSONL is one complete CS2 bundle per nonblank line. A malformed record carries its record number. Processing may stop at that record without changing prior records. The stream has no authority semantics.

## Projection law
A portable projection preserves exact subject identity/revision, source/evidence/claim ids, standing, falsifiers, contradiction references, and the parent semantic fingerprint. Projection authority is always NONE. Extensions are opt-in because they may contain confidential producer data.

## Split law
Claim slicing computes transitive evidence/source closure: claim -> evidence_refs -> evidence.source_ref -> source, plus direct claim.source_refs. Missing references are refused; they are never silently dropped. Each slice records the parent semantic fingerprint and selected claim id.

## Merge law
Only bundles with the same (subject.id, subject.kind, subject.revision) may merge. Identical duplicate ids collapse. Conflicting ids default to refusal. Explicit compatibility modes may prefer existing or incoming values while emitting both digests. Divergent route/process objects move under merge extensions rather than being silently selected.

## Migration law
Legacy migration maps only explicit subject identity, preserves unprovenanced claims as UNKNOWN, never invents source/evidence bindings, retains unmapped predecessor data under extensions.migration.residue, binds predecessor identity and digest, and leaves absent revision absent/empty so C0 validation can refuse it.

## Failure vocabulary
INVALID_JSON, INVALID_ROOT, RECORD_TOO_LARGE, RECORD_LIMIT, DEPTH_LIMIT, COLLECTION_LIMIT, IDENTITY_MISSING, DUPLICATE_CONFLICT, MERGE_CONFLICT, SUBJECT_MISMATCH, BROKEN_REFERENCE, MIGRATION_UNSUPPORTED, INVALID_POLICY are stable machine failures.

## Executable surfaces
scripts/cs2_codec.py provides codec, JSONL, projection, merge, split, migration. scripts/cs2_corpus.py provides deterministic positive/negative/scale corpus generation. scripts/tests/test_cs2_codec.py provides executable contract examples. semantic/schemas/cs2-projection.schema.json defines portable projection shape. semantic/cs2/migration-map.json defines machine-readable migration law.

These surfaces are verification infrastructure and compatibility machinery. Their presence does not establish that checks were executed.
