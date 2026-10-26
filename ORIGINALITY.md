# Mechanism comparison

Judgment: Does a proposed public commitment entail the current one, while adding an obligation within exactly the same service and beneficiary scope?

Participants: An issuer creates and may strengthen or seal a promise. Readers may inspect versions. Validators independently judge the two directed entailment relations and scope. There are no funds or outside sources.

State change: An accepted stronger promise becomes the only active version and links to its parent hash. Previous versions remain queryable. Weak, equivalent, ambiguous, stale, or out-of-scope proposals cannot advance state.

Invariant: The issuer cannot use a later accepted version to dilute a previously registered obligation. Each accepted step must entail its parent, be strictly stronger, and preserve scope. This is a semantic guard subject to validator judgment, not a mathematical proof of real-world performance.

Closest workspace mechanisms:

- MeaningSeal asks whether two frozen texts are equivalent under a materiality policy. It does not keep an active version or enforce a strengthening relation.
- PolicyAmendmentChain classifies the impact of an amendment, then lets a member quorum approve it. It permits substantive changes after quorum; PromiseRatchet has no amendment vote and rejects any weakening.
- Scope Change Check classifies project requests and permits mutually approved scope changes. PromiseRatchet is unilateral issuer revision with an irreversible non-weakening condition.
- VersionMerge performs a three-way section merge. PromiseRatchet has no branch merge, conflict choice, or bilateral resolution.
- ShelfPulse and ChangePointWatch operate on time-ordered observations and threshold changes. PromiseRatchet has no measurement stream, threshold, or replenishment state.

Residual review risk: This workspace contains several semantic comparison and versioning contracts. The directed entailment ratchet is the distinct mechanism; a reviewer still decides originality across their full review cohort.
