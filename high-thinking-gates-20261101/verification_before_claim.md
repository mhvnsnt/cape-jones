# Conversation gate 5: Verification-before-claim
Before saying landed / approved / built / verified in chat:
- [ ] Landed: file present on remote main AND PR merged, size+SHA verified — a PR number or push receipt alone is NOT landed
- [ ] Approved: Mars said perfect/approved for that exact version, 1/1 — a prediction ("it'll be perfect") is NOT approval
- [ ] Built: file exists on disc with frame count / size measured, not just a submission receipt
- [ ] If any check above is unmet, say the unmet check plainly, do not upgrade the claim
Test: verification_check.py <claim-file.json> — JSON must contain {"claim":..,"evidence":..,"verified_on_main":true/false}
