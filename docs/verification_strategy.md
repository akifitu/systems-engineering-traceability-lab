# Verification Strategy

## Verification Methods

The repository supports four classic methods:

- `analysis`
- `inspection`
- `demonstration`
- `test`

## Verification Logic

- Each system and subsystem requirement must declare at least one verification method.
- Each system and subsystem requirement must link to at least one verification case.
- Each linked test must point back to the requirement it claims to verify.
- The verification case method must be compatible with the requirement's declared methods.

## Validation Goals

The automated audit answers the review questions below:

1. Are all engineering requirements traceable to parents and tests?
2. Are all interfaces valid between declared producers and consumers?
3. Are risks scored consistently and linked to affected requirements?
4. Can a reviewer export summary evidence without inspecting raw JSON manually?

