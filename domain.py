"""Incident Timeline Builder domain retrieval and answer rules."""
NAME = '09-incident-timeline-builder'

import re
from datetime import datetime,timezone
from common import norm,require
FIELDS=("incident","time","event")

def instant(value):
    dt=datetime.fromisoformat(value)
    require(dt.tzinfo is not None,"timestamp needs UTC offset")
    return dt.astimezone(timezone.utc)

def validate(rows):
    for r in rows: instant(r["time"])

def solve(rows,q):
    interval=re.fullmatch(r"elapsed time from (.+?) to (.+?) for (.+)",q.rstrip("?"))
    if interval:
        start,end,incident=interval.groups()
        records=[r for r in rows if norm(r["incident"])==incident]
        pairs=[[r for r in records if norm(r["event"])==name] for name in (start,end)]
        if start==end or any(len(matches)!=1 for matches in pairs):return
        first,last=(matches[0] for matches in pairs)
        seconds=(instant(last["time"])-instant(first["time"])).total_seconds()
        if seconds<0:return
        return f"{seconds:.6f}".rstrip("0").rstrip(".")+" seconds",[first,last],"named event interval"
    m=re.fullmatch(r"(timeline|first event|last event|elapsed time) for (.+)",q.rstrip("?"))
    if not m: return
    action,incident=m.groups()
    hits=sorted((r for r in rows if norm(r["incident"])==incident),key=lambda r:(instant(r["time"]),r["id"]))
    if not hits: return
    if action=="elapsed time":
        if len(hits)<2: return
        delta=(instant(hits[-1]["time"])-instant(hits[0]["time"])).total_seconds()
        return f"{format(delta,'.6f').rstrip('0').rstrip('.')} seconds",[hits[0],hits[-1]],action
    if action=="first event": hits=hits[:1]
    if action=="last event": hits=hits[-1:]
    return "\n".join(instant(r["time"]).isoformat().replace("+00:00","Z")+" "+r["event"] for r in hits),hits,action
