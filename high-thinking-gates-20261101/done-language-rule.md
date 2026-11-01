# DONE-LANGUAGE RULE (Mars, 2026-11-01 09:28 CST, standing)
Correction: "Stop saying done when you haven't done anything. You keep saying
done and all you did was respond to me."

## The rule, in one line
"Done" means: a step I personally completed AND verified by a tool result,
a file, or a repo check in this turn. Nothing else gets the word "done".

## Status words — use exactly these
- STARTED: I began the step (tool call, file write, spawn, browser task).
  Never "done" at this point.
- RUNNING / WAITING ON X: a delegated agent, browser task, or Mars is
  working, or a result has not returned yet. Name X.
- RECEIVED, NOT YET VERIFIED: a subagent/browser result arrived, but its
  files/PR/merge have not been checked yet.
- COMPLETED + VERIFIED: tool output, file bytes, or repo main check
  (size + SHA, merge SHA) proves it. This is the only state that may be
  reported with "done", and only for that specific step.
- FAILED / BLOCKED: tool or agent returned failure, or a named blocker
  stops it. State the error/blocker, not a success word.

## Banned
- "Done" as an acknowledgement ("Done: I understand", "Done: noted").
- "Done" for a spawned subagent, a browser task accepted, a file merely
  planned, or a reply that only summarises someone else's report.
- "Done" for landing before: branch -> PR -> mergeable clean/GREEN ->
  merge SHA -> size+SHA verified on main. A PR number or push receipt
  is NOT done.

## Pre-send self-audit (every reply, before sending)
1. Did I do it, or did I delegate it, or did I just reply?
2. For each claim: what tool output / file / repo check proves it?
   If none, downgrade the claim to started / running / pending / unverified.
3. Any number, date, PR, file, or size I cannot point to? Mark it
   UNVERIFIED / OWED / UNKNOWN — never invent it.
4. Run check_done_language.py on the draft when a "done" claim is made.

## The 5 industry-standard systems wired here
1. Status honesty (state machine, not free text) — tkmd-style:
   a task may not jump to done; it passes through started -> pending-close
   (automated verification) -> verified. See status-state-machine.md.
2. Evidence gate (citation-before-claim) — every key claim carries its
   source: tool output, file path + bytes, or repo blob SHA. No source =
   uncertainty log entry, not a claim. See evidence-gate.md.
3. Acknowledgement vs completion language — the status words above;
   acknowledgement is "received / started", never "done".
   See acknowledgement-vs-completion.md.
4. Calibration (confidence + "why not 100%") — CLAIM-CAL-style atomic
   claims, each labelled Supported / Contradicted / Unknown, plus a
   confidence % and what stops it reaching 100%. See calibration.md.
5. Hallucination / bullshit guard — automated draft scan
   (check_done_language.py) + a rule: no invented numbers, dates, PRs,
   files, or sizes; unverified items are marked, never smoothed over.
   See hallucination-guard.md.

Sources (public, fetched 2026-11-01): confidence-honesty skill
(https://eliteai.tools/agent-skills/confidence-honesty); CLAIM-CAL
decomposition + adversarial verification probes
(https://scienmag.com/ai-learns-to-check-itself-new-framework-makes-language-models-honest-about-their-own-confidence/);
tkmd pending-close + human sign-off gates
(https://www.clawdbytes.com/article/2026-10-20-tkmd-a-local-cli-task-manager-and-mcp-server-with-ai-agent-review-gates);
citation-before-claim QA checklist
(https://gotranscript.com/en/blog/ai-summarization-in-research-prevent-hallucinations-rules-qa-checklist).
