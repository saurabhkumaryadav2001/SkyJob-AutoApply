import json, requests
from pathlib import Path

def matches(title, location, keywords, locations):
    t=title.lower(); loc=location.lower()
    return any(k.lower() in t for k in keywords) and any(x.lower() in loc for x in locations)

def search_jobs(profile, stop_event):
    boards=json.loads(Path(__file__).with_name("boards.json").read_text(encoding="utf-8"))
    out=[]
    for b in boards:
        if stop_event.is_set(): break
        try:
            if b["type"]=="greenhouse":
                rows=requests.get(f'https://boards-api.greenhouse.io/v1/boards/{b["slug"]}/jobs?content=true',timeout=20).json().get("jobs",[])
                for x in rows:
                    title=x.get("title",""); loc=x.get("location",{}).get("name",""); url=x.get("absolute_url","")
                    if matches(title,loc,profile.get("keywords",[]),profile.get("locations",["Mumbai"])):
                        out.append(dict(title=title,company=b["company"],location=loc,source="Greenhouse",url=url))
            elif b["type"]=="lever":
                rows=requests.get(f'https://api.lever.co/v0/postings/{b["slug"]}?mode=json',timeout=20).json()
                for x in rows:
                    title=x.get("text",""); loc=x.get("categories",{}).get("location",""); url=x.get("hostedUrl","")
                    if matches(title,loc,profile.get("keywords",[]),profile.get("locations",["Mumbai"])):
                        out.append(dict(title=title,company=b["company"],location=loc,source="Lever",url=url))
        except Exception as e: print("Skipping",b.get("company"),e)
    seen=set(); return [j for j in out if j["url"] and not (j["url"] in seen or seen.add(j["url"]))]
