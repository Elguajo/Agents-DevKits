> Integrated from the v0.1 prompt/skill prototype `related-bug-hunt`. Load this reference only when its trigger applies.

# Related Bug / Pattern Hunt
## Goal
Find other locations that share the same failure mechanism, not merely similar syntax.

## Workflow
1. Define the confirmed root-cause pattern and the conditions that make it unsafe.
2. Search structurally and semantically across the repository.
3. Inspect each candidate in context.
4. Classify each as: SAME BUG / POTENTIALLY VULNERABLE / INTENTIONAL & SAFE / FALSE POSITIVE.
5. Recommend action only for confirmed or credible risks.
6. Add shared regression coverage if a common abstraction is responsible.

## Rules
- Similar code is not automatically the same bug.
- Explain why each match is or is not vulnerable.
- Avoid repository-wide replacements without context.

## Output
Candidate list, classification, evidence, recommended action, and whether a shared fix is preferable.
