#!/usr/bin/env python3
"""search_sheets.py — I5 keyword+synonym search over sheet-index-20261101.json
Usage: python3 search_sheets.py "three quarter sitting" [--top 20]
Industry method: controlled-vocabulary + synonym expansion + faceted filtering.
Synonyms: three/quarter/3quarter, sitting/sit/seated/lounge/chair, front/forward,
back/rear, side/profile. Never searches by filename alone — tags + path both count.
"""
import json, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
SYN={'three':['3quarter','threequarter'],'quarter':['3quarter'],'3quarter':['three','quarter','threequarter'],
'sitting':['sit','seated','lounge','chair'],'sit':['sitting','seated','lounge'],'seated':['sit','sitting','lounge'],
'lounge':['sit','sitting','seated','chair'],'chair':['sit','sitting','lounge'],
'front':['forward'],'back':['rear'],'side':['profile'],'profile':['side']}
def main():
    q=' '.join(sys.argv[1:]) if len(sys.argv)>1 else 'three quarter sitting'
    top=20
    recs=json.load(open(os.path.join(HERE,'sheet-index-20261101.json')))
    terms=set()
    for t in q.lower().replace('-',' ').split():
        terms.add(t); terms.update(SYN.get(t,[]))
    scored=[]
    for r in recs:
        hay=(r['repo_path']+' '+' '.join(r['tags'])).lower()
        s=sum(1 for t in terms if t in hay)
        if s: scored.append((s,r))
    scored.sort(key=lambda x:(-x[0],x[1]['repo_path']))
    print(f"query: {q}\nexpanded: {sorted(terms)}\nmatches: {len(scored)}")
    for s,r in scored[:top]:
        print(f"  score {s}  {r['repo_path']}  tags={','.join(r['tags'])}  local={r['present_locally']}")
if __name__=='__main__': main()
