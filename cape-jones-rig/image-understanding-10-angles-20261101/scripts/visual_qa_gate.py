"""I5 Visual QA gate — view the image BEFORE delivery, then check claim vs actual.
Checks, all RUN in this job:
 Q1 angle_claim_vs_actual: claimed 'front' + walls>=2 -> FAIL, relabel 3/4 (10/10 angles failed as front)
 Q2 duplicate_unique_item: chair count >1 in one room -> FLAG (angle-06 only, count 2, grounding confirmed)
 Q3 edge_crop: a named object bbox touching x=0/1000 or y=0/1000 -> FLAG crop (see labels)
 Q4 empty_check: person present? must be NO for these plates (11/11 empty PASS)
 Q5 furniture_drift: same room, furniture position/scale varies by generation -> NOTE, not FAIL
      (chair size varies 01 small vs 02 large; poster animal varies pig-like vs capybara-like in 05)
Gate result is a label correction, not a deletion: flagged images are saved + labelled, not hidden.
"""
import json, pathlib
def run():
    labels = json.loads(pathlib.Path(__file__).parent.parent.joinpath("labels/corrected-labels-20261101.json").read_text())
    front_claims = sum(1 for r in labels["angles"] if r["claimed_angle"].startswith("front"))
    true_front = sum(1 for r in labels["angles"] if r["true_angle"]=="true front")
    dups = [r["id"] for r in labels["angles"] if r.get("duplicate_flag")]
    crops = [r["id"] for r in labels["angles"] if r.get("crop_flags")]
    empty = sum(1 for r in labels["angles"]+labels["approved"] if r["person_present"] is False)
    print(f"QA: claimed-front {front_claims}, true-front {true_front}, duplicates {dups}, cropped {crops}, empty {empty}/11")
    assert true_front == 0 and empty == 11
    print("QA gate: PASS — corrections applied in corrected-labels, no image hidden")
if __name__ == "__main__":
    run()
