# Comparative Solution Audit

## Goal

Use analogous solutions to challenge a repository's technical direction and
identify evidence-backed improvements without mistaking competitor conventions
for requirements.

## Use when

- The user explicitly asks to compare the repository with similar products,
  open-source projects, or established implementations.
- External examples can test a concrete concern already observed in the
  repository: architecture, reliability, security, performance, data handling,
  developer experience, or verification.

## Workflow

1. Establish a repository baseline first: product purpose, maturity, target
   users, architecture, constraints, and the concern to challenge.
2. State comparison criteria before researching. Use criteria tied to the
   current project, such as failure handling, data integrity, extension cost,
   operational burden, testability, performance, or security.
3. Select two to four genuinely analogous solutions. Prefer maintained,
   production-proven, primary-source implementations or official technical
   documentation. Record why each is comparable and where it differs.
4. Inspect the relevant mechanism in context rather than feature lists or
   marketing claims. Cite the exact source for each material comparison.
5. Compare the repository and examples against the declared criteria. For every
   difference, explain whether it is a confirmed gap, a credible risk, an
   intentional trade-off, or irrelevant to this project's constraints.
6. Convert only applicable findings into recommendations. Name the smallest
   next action, expected benefit, cost, confidence, and the evidence supporting
   it.
7. Produce a verdict: retain the current approach, improve specific areas, or
   reconsider a design. Identify what remains unverified.

## Rules

- Never research external code before understanding the local repository.
- Do not copy code, architecture, naming, or product scope merely because a
  comparable project uses it.
- Do not treat popularity, GitHub stars, or feature count as quality evidence.
- Do not compare unrelated scale, deployment model, regulatory constraints, or
  target users without explicitly discounting the difference.
- Distinguish repository evidence, external-source evidence, inference, and
  recommendation.
- Prefer official documentation, source repositories, and maintainers' design
  records over secondary summaries. If browsing is unavailable, say so and
  limit the verdict to repository evidence.
- Do not implement broad fixes during the audit.

## Output

Return:

1. **Scope and baseline** — what was inspected and the comparison criteria.
2. **Analogues considered** — each analogue, why it is comparable, and its
   relevant constraints.
3. **Comparison matrix** — criterion, current repository, analogue evidence,
   implication, and confidence.
4. **Findings** — confirmed gaps, credible risks, intentional trade-offs, and
   rejected comparisons.
5. **Verdict and roadmap** — retain / improve / reconsider, prioritized
   Now/Next/Later actions, expected value, effort, and verification needed.

Each material claim must link to local evidence or an external primary source.
