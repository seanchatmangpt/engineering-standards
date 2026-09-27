#!/usr/bin/env python3
"""RFC-CS2-001 portable projection, split, merge, and conservative migration."""
from __future__ import annotations
import copy, hashlib, json
from dataclasses import dataclass, asdict
from typing import Any, Mapping, Sequence

STANDARD="RFC-CS2-001"; FORMAT="cs2.conformance.v1"

class CodecError(ValueError):
    def __init__(self, code:str, message:str):
        super().__init__(message); self.code=code

def canonical(value:Any)->str:
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)

def digest(value:Any)->str:
    return "sha256:"+hashlib.sha256(canonical(value).encode()).hexdigest()

def semantic(bundle:Mapping[str,Any])->dict[str,Any]:
    out=copy.deepcopy(dict(bundle)); c=out.get("conformance")
    if isinstance(c,dict):
        for key in ("actual_level","semantic_fingerprint","issues"): c.pop(key,None)
    return out

def fingerprint(bundle:Mapping[str,Any])->str:
    return digest(semantic(bundle))

def normalize(bundle:Mapping[str,Any])->dict[str,Any]:
    out=copy.deepcopy(dict(bundle))
    out.setdefault("schema_version",FORMAT); out.setdefault("standard",STANDARD)
    out.setdefault("sources",[]); out.setdefault("evidence",[]); out.setdefault("claims",[])
    out.setdefault("conformance",{"requested_level":"C0"})
    for key in ("sources","evidence","claims"):
        if not isinstance(out[key],list): raise CodecError("INVALID_SHAPE",key+" must be array")
        out[key].sort(key=lambda x:(str(x.get("id","")),canonical(x)))
    for claim in out["claims"]:
        for key in ("source_refs","evidence_refs","contradicts"):
            if key in claim:
                if not isinstance(claim[key],list): raise CodecError("INVALID_SHAPE",key+" must be array")
                claim[key]=sorted(set(claim[key]))
    return out

def project(bundle:Mapping[str,Any], include_extensions:bool=False)->dict[str,Any]:
    src=normalize(bundle); subject=src.get("subject",{})
    claims=[]
    for claim in src["claims"]:
        item={key:copy.deepcopy(claim.get(key)) for key in ("id","predicate","object","standing","source_refs","evidence_refs")}
        for key in ("falsifier","contradicts"):
            if key in claim:item[key]=copy.deepcopy(claim[key])
        claims.append(item)
    out={"schema_version":FORMAT,"standard":STANDARD,
         "subject":{key:subject.get(key) for key in ("id","kind","revision")},
         "sources":[{key:x[key] for key in ("id","kind","locator","revision") if key in x} for x in src["sources"]],
         "evidence":[{key:x[key] for key in ("id","kind","subject_ref","source_ref","locator","digest") if key in x} for x in src["evidence"]],
         "claims":claims,"semantic_fingerprint":fingerprint(src),"projection_authority":"NONE"}
    for key in ("route","process"):
        if key in src:out[key]=copy.deepcopy(src[key])
    if "route" in out:out["route"]["projection_authority"]="NONE"
    if include_extensions and "extensions" in src:out["extensions"]=copy.deepcopy(src["extensions"])
    return out

def split_by_claim(bundle:Mapping[str,Any]):
    src=normalize(bundle); sources={x["id"]:x for x in src["sources"]}; evidence={x["id"]:x for x in src["evidence"]}
    for claim in src["claims"]:
        ev=[]; source_ids=set(claim.get("source_refs",[]))
        for ref in claim.get("evidence_refs",[]):
            if ref not in evidence:raise CodecError("BROKEN_REFERENCE","unknown evidence "+ref)
            item=evidence[ref]; ev.append(copy.deepcopy(item)); source_ids.add(item.get("source_ref"))
        ss=[]
        for ref in sorted(x for x in source_ids if x):
            if ref not in sources:raise CodecError("BROKEN_REFERENCE","unknown source "+ref)
            ss.append(copy.deepcopy(sources[ref]))
        out={"schema_version":FORMAT,"standard":STANDARD,"subject":copy.deepcopy(src["subject"]),
             "sources":ss,"evidence":ev,"claims":[copy.deepcopy(claim)],
             "conformance":copy.deepcopy(src["conformance"]),
             "extensions":{"slice":{"parent_fingerprint":fingerprint(src),"claim_id":claim.get("id")}}}
        for key in ("route","process"):
            if key in src:out[key]=copy.deepcopy(src[key])
        yield normalize(out)

@dataclass
class MergeReport:
    inputs:int=0; identical:int=0; added:int=0; conflicts:int=0
    def to_dict(self):return asdict(self)

def merge(bundles:Sequence[Mapping[str,Any]], policy:str="error"):
    if not bundles:raise CodecError("EMPTY_INPUT","at least one bundle required")
    items=[normalize(x) for x in bundles]; first=items[0]
    identity=tuple(first.get("subject",{}).get(k) for k in ("id","kind","revision"))
    report=MergeReport(inputs=len(items))
    out={"schema_version":FORMAT,"standard":STANDARD,"subject":copy.deepcopy(first["subject"]),
         "sources":[],"evidence":[],"claims":[],"conformance":copy.deepcopy(first["conformance"]),
         "extensions":{"merge":{"inputs":[fingerprint(x) for x in items],"policy":policy}}}
    for item in items:
        if tuple(item.get("subject",{}).get(k) for k in ("id","kind","revision"))!=identity:
            raise CodecError("SUBJECT_MISMATCH","merge subjects differ")
        for namespace in ("sources","evidence","claims"):
            index={x["id"]:x for x in out[namespace]}
            for incoming in item[namespace]:
                key=incoming.get("id")
                if not key:raise CodecError("IDENTITY_MISSING",namespace+" id missing")
                old=index.get(key)
                if old is None:out[namespace].append(copy.deepcopy(incoming));report.added+=1;continue
                if canonical(old)==canonical(incoming):report.identical+=1;continue
                report.conflicts+=1
                if policy=="error":raise CodecError("MERGE_CONFLICT",namespace+" id "+key)
                if policy=="prefer-incoming":old.clear();old.update(copy.deepcopy(incoming))
                elif policy!="prefer-existing":raise CodecError("INVALID_POLICY",policy)
    out["extensions"]["merge"]["report"]=report.to_dict()
    return normalize(out)

def migrate_legacy(value:Mapping[str,Any], predecessor:str="legacy")->dict[str,Any]:
    if value.get("standard")==STANDARD and value.get("schema_version")==FORMAT:return normalize(value)
    raw=value.get("subject")
    if isinstance(raw,dict):
        subject={"id":str(raw.get("id","")),"kind":str(raw.get("kind",value.get("subject_kind","Unknown"))),"revision":str(raw.get("revision",value.get("revision","")))}
    else:
        subject={"id":str(raw if isinstance(raw,str) else value.get("subject_id","")),"kind":str(value.get("subject_kind","Unknown")),"revision":str(value.get("revision",""))}
    claims=value.get("claims",[])
    if isinstance(claims,dict):claims=[{"id":k,"predicate":k,"object":v} for k,v in claims.items()]
    if not isinstance(claims,list):raise CodecError("MIGRATION_UNSUPPORTED","claims must be array or object")
    mapped=[]
    for n,claim in enumerate(claims):
        if not isinstance(claim,dict):claim={"object":claim}
        mapped.append({"id":str(claim.get("id","legacy:claim:"+str(n))),"predicate":str(claim.get("predicate",claim.get("name","legacy_claim"))),
          "object":copy.deepcopy(claim.get("object",claim.get("value"))),"source_refs":[],"evidence_refs":[],"standing":"UNKNOWN",
          "falsifier":{"observation":"An admitted observation contradicts this migrated claim."},"contradicts":[]})
    known={"standard","schema_version","subject","subject_id","subject_kind","revision","claims","sources","evidence","extensions"}
    residue={k:copy.deepcopy(v) for k,v in value.items() if k not in known}
    ext=copy.deepcopy(value.get("extensions",{})) if isinstance(value.get("extensions"),dict) else {}
    ext.update({"predecessor":predecessor,"migration":{"strategy":"conservative-no-invented-provenance","legacy_digest":digest(value),"residue":residue}})
    return normalize({"schema_version":FORMAT,"standard":STANDARD,"subject":subject,
      "sources":copy.deepcopy(value.get("sources",[])) if isinstance(value.get("sources"),list) else [],
      "evidence":copy.deepcopy(value.get("evidence",[])) if isinstance(value.get("evidence"),list) else [],
      "claims":mapped,"conformance":{"requested_level":"C0"},"extensions":ext})
