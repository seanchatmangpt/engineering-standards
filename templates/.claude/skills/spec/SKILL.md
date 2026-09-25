# /spec — Project a specification from admitted intent

Create or update a human specification without manufacturing a parallel authority surface.

## Root references

Fetch:
- https://raw.githubusercontent.com/seanchatmangpt/engineering-standards/main/process/semantic-engineering-protocol.md
- https://raw.githubusercontent.com/seanchatmangpt/engineering-standards/main/process/documentation-standards.md

Read local `AGENTS.md` and project semantic/work source first.

## Procedure

1. Resolve mode: Semantic Work Mode or Documentation Mode.
2. Resolve the exact feature/decision subject, constraints, acceptance criteria, falsifiers, evidence boundary, and out-of-scope space.
3. In Semantic Work Mode, conserve the WorkOrder/contract identities and treat the document as a projection. Do not invent semantics missing from the canonical source; surface the gap.
4. In Documentation Mode, the spec may be the practical contract.
5. Draft the appropriate product spec, technical design, or ADR.
6. Make acceptance criteria falsifiable and identify the verification boundary.
7. Write the document to the project-standard path.

## Constraints

- Generated/projection docs carry no DO authority.
- A spec approval is not authority.
- Prefer links/queries to duplicated semantic facts.
- If a stable projection can be generated, route it to the project generator rather than maintaining a hand copy.
