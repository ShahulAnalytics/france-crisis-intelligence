"""RSS metadata collector; headlines are leads, not verified claims."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
import requests
DEFAULT_FEEDS=[{'publisher':'ECB','url':'https://www.ecb.europa.eu/rss/press.html'},{'publisher':'Eurostat','url':'https://ec.europa.eu/eurostat/news/rss'}]
def _local(tag): return tag.rsplit('}',1)[-1].lower()
def parse_rss(xml_text:str,publisher:str,feed_url:str)->list[dict]:
 root=ET.fromstring(xml_text); records=[]
 for item in root.iter():
  if _local(item.tag) not in ('item','entry'): continue
  fields={_local(c.tag):' '.join(''.join(c.itertext()).split()) for c in item}; link=fields.get('link','')
  if not link:
   for c in item:
    if _local(c.tag)=='link': link=c.attrib.get('href','')
  title=fields.get('title','')
  if title: records.append({'publisher':publisher,'title':title,'url':link or feed_url,'summary':fields.get('description',fields.get('summary',''))[:1500],'published_at':fields.get('pubdate',fields.get('published',fields.get('updated',''))),'feed_url':feed_url,'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'record_id':hashlib.sha256((publisher+title+(link or '')).encode()).hexdigest()})
 return records
def collect_rss(feeds:list[dict]|None=None,output_dir:Path=Path('data'),timeout:int=15,max_records:int=2000)->dict:
 records=[]; statuses=[]
 for feed in (feeds or DEFAULT_FEEDS):
  try:
   response=requests.get(feed['url'],headers={'User-Agent':'FranceCrisisIntelligence/1.0'},timeout=timeout); response.raise_for_status(); items=parse_rss(response.text,feed.get('publisher','Unknown'),feed['url']); records.extend(items); statuses.append({'publisher':feed.get('publisher'),'status':'ok','records':len(items)})
  except Exception as exc: statuses.append({'publisher':feed.get('publisher'),'status':'error','error':str(exc)})
 unique={r['record_id']:r for r in records}; records=sorted(unique.values(),key=lambda x:x.get('published_at',''),reverse=True)[:max_records]; target=Path(output_dir)/'processed'; target.mkdir(parents=True,exist_ok=True); output=target/'news_metadata.json'; output.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
 return {'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'feed_status':statuses,'article_count':len(records),'output':str(output),'caveat':'RSS metadata is a research lead, not independent verification.'}
def cluster_near_duplicate_articles(records:list[dict],threshold:float=0.88,max_days_apart:int=7)->list[dict]:
 groups={}
 for item in records:
  key=' '.join(''.join(c.lower() if c.isalnum() else ' ' for c in item.get('title','')).split()); groups.setdefault(key,[]).append(item)
 return [{'normalized_title':key,'count':len(items),'articles':items} for key,items in groups.items()]
