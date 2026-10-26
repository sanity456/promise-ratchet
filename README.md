# PromiseRatchet

PromiseRatchet is a reusable GenLayer intelligent contract for public service commitments. An issuer creates a promise for a fixed service context. Each later version must preserve every earlier obligation and add a real obligation for the same service and beneficiaries. An issuer cannot replace a promise with weaker, merely equivalent, or unclear wording. Each accepted version links cryptographically to the previous version; sealing makes the final wording immutable.

GenLayer validators independently compare the current and proposed commitments. They return three closed judgments: whether the new text implies the old, whether the old implies the new, and whether the scope remains the same. Deterministic code advances the version only for `YES`, `NO`, `YES` respectively and stores the exact agreed judgments. A stale version, repeated text, or unauthorized account cannot advance the promise.

One deployment supports many independent issuer-scoped promises. This is an on-chain public commitment record, not proof that an issuer can perform, a legal guarantee, or a way to authenticate off-chain services. All promise wording is public. There is no external evidence collection: the two registered texts and fixed context are the complete evidence for the semantic comparison.

## Interface

Writes: `open_promise`, `tighten_promise`, `seal_promise`.

Views: `get_promise`, `get_revision`.

## Local verification

```text
genvm-lint check contracts/promise_ratchet.py
genvm-lint typecheck contracts/promise_ratchet.py
python -m pytest tests/direct -q -p no:cacheprovider
```

See `ORIGINALITY.md` for the mechanism comparison and `AUDIT.md` for release status. StudioNet evidence will be recorded only after the deployed source is checked against the public Git commit.
