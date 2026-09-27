#!/usr/bin/env python3
import argparse,copy,hashlib,json
from pathlib import Path
def bundle(i):
 s="repo:corpus/service-"+str(i)
 return {"schema_version":"cs2.conformance.v1","standard":"RFC-CS2-001","subject":{"id":s,"kind":"Repository","revision":format(i,"040x")},"sources":[{"id":"src:"+str(i),"kind":"Corpus","locator":"corpus://source/"+str(i)}],"evidence":[{"id":"ev:"+str(i),"kind":"Observation","subject_ref":s,"source_ref":"src:"+str(i),"locator":"corpus://evidence/"+str(i),"value":i}],"claims":[{"id":"claim:"+str(i),"predicate":"corpus_value","object":i,"source_refs":["src:"+str(i)],"evidence_refs":["ev:"+str(i)],"standing":"OBSERVED","falsifier":{"observation":"A deterministic corpus observation differs."},"contradicts":[]}],"route":{"consumer":"corpus","workflow":"qualification","projection_id":"corpus-v1","minimum_level":"C3","delivery_semantics":"SNAPSHOT","projection_authority":"NONE"},"process":{"ocel_ref":"corpus://ocel/"+str(i),"receipt_schema":"semantic/schemas/evidence-receipt.schema.json","replay_binding":"corpus://replay/"+str(i),"episode_id":"episode:"+str(i),"event_refs":["event:"+str(i)],"consequence_class":"NONE"},"conformance":{"requested_level":"C4"}}
def main():
 p=argparse.ArgumentParser();p.add_argument("output",type=Path);p.add_argument("--count",type=int,default=1000);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);manifest=[]
 for i in range(a.count):
  b=bundle(i);extra=(i%32)+1;t=b["claims"][0];b["claims"]=[]
  for j in range(extra):
   c=copy.deepcopy(t);c["id"]="claim:"+str(i)+":"+str(j);c["object"]={"n":j,"bucket":j%7};b["claims"].append(c)
  raw=json.dumps(b,sort_keys=True,indent=2)+"\n";fn="scale__"+str(i)+".json";(a.output/fn).write_text(raw);manifest.append({"id":"scale:"+str(i),"file":fn,"expected_actual":"C4","sha256":hashlib.sha256(raw.encode()).hexdigest()})
 (a.output/"manifest.json").write_text(json.dumps({"schema":"cs2.corpus.v1","cases":manifest},sort_keys=True,indent=2)+"\n");return 0
if __name__=="__main__":raise SystemExit(main())
