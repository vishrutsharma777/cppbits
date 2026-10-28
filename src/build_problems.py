"""Merge the problem banks into problems.json (read by the grader and embedded in the page)."""
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import problems_a, problems_b, problems_c, problems_d, problems_e

probs = (problems_a.PROBLEMS + problems_b.PROBLEMS + problems_c.PROBLEMS
         + problems_d.PROBLEMS + problems_e.PROBLEMS)
ids = [p["id"] for p in probs]
assert len(ids) == len(set(ids)), "duplicate ids"
sections = []
for p in probs:
    if p["section"] not in sections:
        sections.append(p["section"])
check_h = open(os.path.join(here, "check.h"), encoding="utf-8").read()
out = {"sections": sections, "problems": probs, "check_h": check_h}
with open(os.path.join(here, "..", "build", "problems.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(len(probs), "problems in", len(sections), "sections")
for s in sections:
    print(" ", s, sum(p["section"] == s for p in probs))
