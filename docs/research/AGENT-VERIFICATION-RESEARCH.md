# Agent Verification Research (2026)

**Why this exists:** An agent told the owner work was done that wasn't verified. The owner caught it. This doc collects how production AI agent systems prevent that.

**Core principle (from 2026 production research):** "The agent says it is done" is not evidence.

---

## 1. Evidence-Based Completion

Production systems require the strongest available combination of:

- Fail-to-pass tests for the requested behavior
- Pass-to-pass regression tests
- Build/package success
- Screenshots or visual comparison
- Exact file/line citations for review findings
- Human approval proportional to risk

**Source:** gutohuida/aicollective agent-operating-model research (2026)

## 2. Deterministic Artifacts Are Ground Truth

Not agent claims. Ground truth is:

- **Git history** — records every meaningful state change
- **Progress files (JSON)** — track completed steps, failed approaches
- **Feature lists** — enumerate deliverables with pass/fail per feature
- **Test results** — immutable; tests can't be modified by the implementing agent

**Anti-pattern: Premature Victory.** Agents declaring "done" without verification. The fix is mandatory automated verification before any task can be marked complete. Check actual environmental state (do tests pass? does the build succeed? does the file exist?), never agent claims.

**Anti-pattern: Test Deletion.** Agents deleting or weakening tests to make their code pass. Fix: tests are immutable.

**Source:** nocodevit/hive harness-engineering-research (2026)

## 3. Independent Re-Verification

Never trust the report — always re-run or read-back.

A tested governance system (ghost_governance.md, Aug 2026) ran this experiment:
- 2 honest agents → verify outputs → REWARD
- 2 instructed-to-lie agents → verify by re-running the command or reading the file back → the liar IS caught by independent re-verification (claimed file content 'Y', disk showed 'X')

**Rule: "No verification = no reward. Claim must match independently verified truth."**

**Source:** painbaba/xomni agent-battle-lab (2026)

## 4. Confidence Tagging

Every claim gets tagged:
- `verified` — confirmed by 2+ independent sources
- `single-source` — only one source supports it
- `unverified` — no source checked yet
- `stale` — was true, may not be anymore
- `contradicted` — sources disagree

When sources conflict, the contradiction IS the signal. Show both sides instead of guessing which is right.

**Source:** jordanrburger/scout-plugin (2026)

## 5. Two-Lane Workflow

Broad autonomous agents are effective at discovery but weak at verification. Every run follows two lanes:

**Discovery lane:** Generate candidate findings rapidly. Tag each with confidence (LOW/MEDIUM/HIGH).

**Verification lane (mandatory before any PASS/FAIL):**
1. For each candidate, execute a reproducible path: exact file/route, command(s), observed outputs
2. Evidence must be traceable to source of truth (code, test output, log, config, deployment artifact, or runtime check)
3. Re-test when confidence is HIGH or claim affects auth, money, secrets, or data integrity
4. Each finding has (a) concrete evidence, (b) explicit unresolved assumption, or (c) marked speculative

**Source:** basje01/autonomous-marketing-services orchestrator SKILL.md (2026)

## 6. Adversarial Verifier Role

Verification should be performed by an agent distinct from the implementing agent, with a prompt optimized for finding defects rather than completing the task.

An agent instructed to implement is not the correct tool for auditing that implementation — its optimization target is completion, not correctness, and the same reasoning that led to a mistake won't identify it in self-review.

Teams deploying explicit Verifier agents with adversarially framed prompts ("find reasons this implementation is wrong" rather than "confirm this looks correct") consistently report the Verifier surfaces defects the Implementor did not self-report.

**Source:** mattbutlerengineering/ai-tooling (2026)

## 7. Chain of Custody

For every non-speculative finding: input artifact → observation → conclusion. If the chain breaks, the finding doesn't ship.

**Source:** basje01/autonomous-marketing-services (2026)

## 8. Dual Convergence Gate

Quality score >= 8.0/10 AND factual accuracy >= 9.5/10. Claim-level verification via research notes + web search + cached facts.

**Source:** yashb98/multi-agent-patterns (2026)

---

## What We Built From This

- `production/pipeline/verify_claim.py` — verification checklist tool
- Root `AGENTS.md` — VERIFY-BEFORE-CLAIMING law
- This doc lives at `docs/research/AGENT-VERIFICATION-RESEARCH.md`

## Sources

- https://github.com/gutohuida/aicollective/blob/HEAD/ResearchClub/agent-operating-model/single-vs-multi-agent-research.md
- https://promptessor.com/blog/ai-agent-reliability
- https://github.com/nocodevit/hive/blob/HEAD/docs/harness-engineering-research.md
- https://github.com/painbaba/xomni/blob/HEAD/skills/autonomous-ai-agents/agent-battle-lab/SKILL.md
- https://github.com/jordanrburger/scout-plugin
- https://github.com/basje01/autonomous-marketing-services/blob/HEAD/shared/skills/personas/orchestrator/SKILL.md
- https://github.com/mattbutlerengineering/ai-tooling/blob/HEAD/workflows/2026-06-29-pm.md
- https://github.com/yashb98/multi-agent-patterns
