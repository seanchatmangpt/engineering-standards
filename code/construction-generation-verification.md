# Construction, Generation, and Verification Contract

This contract applies across all language/framework profiles.

## Construction order

```text
admitted semantics
-> capability closure
-> reuse / compose / extend
-> generator or irreducible handwritten mechanism
-> narrow verifier
-> integration verifier
-> consequence authority
-> execution
-> receipt / replay
```

## Generated vs handwritten

Every adopting repository should classify changed artifacts as:

- **canonical source** — admitted semantic/source authority;
- **generated projection** — reproducible consequence of canonical source + generator identity;
- **handwritten irreducible mechanism** — behavior the admitted generator/tooling cannot express;
- **handwritten bootstrap residue** — temporary setup awaiting formal manufacture;
- **external artifact** — dependency/tool output with immutable identity.

Do not edit a generated projection directly. Repair the source, generator, or generator capability.

## Generator capability refusal

If the preferred generator cannot represent the required semantics, record:

```text
UNSUPPORTED(generator-capability)
generator=<identity>
subject=<exact required semantic>
missing=<specific capability>
fallback=<bounded handwritten residue or alternate generator>
```

"Generator unavailable" is not evidence that hand-writing is inherently required.

## Verification

Every verifier claim declares:
- exact subject;
- source/candidate identity;
- toolchain/config identity;
- observed command/run;
- consequence tested;
- falsifier class;
- evidence ceiling.

Static/type/schema checks cannot be promoted to runtime standing. Integration checks cannot automatically prove deployment. CI cannot prove a different head.

## Learning

A repeated successful handwritten transform is a candidate for formalization. Promote it to a template, generator, ontology, schema, rule, verifier, or process control and remove the need to purchase the same reasoning again.
