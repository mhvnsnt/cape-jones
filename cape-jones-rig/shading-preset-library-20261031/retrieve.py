#!/usr/bin/env python3
"""Retrieve a shading preset by tier / light / pose / finish / status / id / free-text.
Usage: python3 retrieve.py --tier CLEAN --pose ARMS_UP
       python3 retrieve.py --light RIGHT --finish CEL
       python3 retrieve.py --id CORE-V9
       python3 retrieve.py --query "smooth blender apose"
Refuses TEST_ONLY / ARCHIVE production use unless --allow-test is given, and prints that refusal.
Catalog: shading-preset-catalog-20261031.json (same folder). Paths are source paths; library does not duplicate preset PNGs."""
import json, os, sys, argparse
HERE=os.path.dirname(os.path.abspath(__file__))
CAT=json.load(open(os.path.join(HERE,"shading-preset-catalog-20261031.json")))
def show(x):
    print(f"{x['id']} | {x['name']} | tier={x['tier']} status={x['status']}")
    print(f"  file: {os.path.join(os.path.expanduser('~/workspace/cape-jones-rig'), x['source_folder'], x['source_file'])}")
    print(f"  half={x['half_mean_delta_R']} edge={x['edge_delta_R']} plate={x['plate']} light={x['light_direction']} finish={x['finish']} run={x['run']}")
    print(f"  method: {x['method']}")
    if x['notes']: print(f"  note: {x['notes']}")
    print(f"  {x['normals']}. {x['lighting_axis_note']}.")
def main():
    a=argparse.ArgumentParser(); a.add_argument("--tier"); a.add_argument("--light"); a.add_argument("--pose"); a.add_argument("--finish"); a.add_argument("--id"); a.add_argument("--query"); a.add_argument("--allow-test",action="store_true"); a.add_argument("--status")
    args=a.parse_args(); hits=CAT["entries"]
    if args.id: hits=[x for x in hits if x["id"]==args.id]
    if args.tier: hits=[x for x in hits if x["tier"]==args.tier.upper()]
    if args.light: hits=[x for x in hits if x["light_direction"]==args.light.upper()]
    if args.pose: hits=[x for x in hits if x["plate"]==args.pose.upper()]
    if args.finish: hits=[x for x in hits if args.finish.lower() in x["finish"].lower()]
    if args.status: hits=[x for x in hits if args.status.lower() in x["status"].lower()]
    if args.query:
        q=args.query.lower(); hits=[x for x in hits if q in (x["name"]+" "+x["method"]+" "+" ".join(x["tags"])).lower() or all(w in (x["name"]+" "+x["method"]+" "+" ".join(x["tags"])).lower() for w in q.split())]
    if not hits: print("NO MATCH — try --tier CLEAN, --pose ARMS_UP, --light LEFT, or --query smooth"); return 2
    blocked=[x for x in hits if x["tier"] in ("TEST_ONLY","ARCHIVE")]
    if blocked and not args.allow_test and not args.id:
        print("REFUSED for production: the following are TEST_ONLY/ARCHIVE and are shown for reference only (use --allow-test to list them, or --id for one record):")
        for x in blocked: print(f"  {x['id']} {x['name']} tier={x['tier']}")
        hits=[x for x in hits if x["tier"] not in ("TEST_ONLY","ARCHIVE")]
        if not hits: return 2
    for x in hits: show(x)
    print(f"RETURNED {len(hits)} preset(s).")
    return 0
if __name__=="__main__": sys.exit(main())
