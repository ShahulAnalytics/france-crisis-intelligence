"""Resilient ingestion helpers for public Eurostat and ECB data."""
from datetime import datetime,timezone
from pathlib import Path
from io import StringIO
import hashlib,json
import pandas as pd, requests
EUROSTAT='https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data'
ECB='https://data-api.ecb.europa.eu/service/data/EXR'
HEADERS={'User-Agent':'FranceCrisisIntelligence/1.0 public-interest research'}
def eurostat_json_to_frame(payload:dict,dataset_id:str,geography:str='FR')->pd.DataFrame:
 ids=payload.get('id',[]); sizes=payload.get('size',[]); dims=payload.get('dimension',{}); vals=payload.get('value',{})
 if not ids or not sizes or not dims or vals is None: raise ValueError('Invalid Eurostat JSON-stat response')
 labels=[]
 for i,name in enumerate(ids):
  idx=dims[name].get('category',{}).get('index',{}); ordered=[k for k,_ in sorted(idx.items(),key=lambda x:x[1])] if isinstance(idx,dict) else list(idx)
  if len(ordered)!=int(sizes[i]): raise ValueError('Dimension size mismatch: '+name)
  labels.append(ordered)
 rows=[]; total=1
 for n in sizes: total*=int(n)
 for flat in range(total):
  value=vals.get(str(flat),vals.get(flat))
  if value is None: continue
  rem=flat; coords=[0]*len(sizes)
  for i in range(len(sizes)-1,-1,-1): coords[i]=rem%int(sizes[i]); rem//=int(sizes[i])
  row={'dataset_id':dataset_id,'geo_requested':geography,'value':value}
  for name,pos,opts in zip(ids,coords,labels):
   code=opts[pos]; row[name]=code; row[name+'_label']=dims[name].get('category',{}).get('label',{}).get(code,code)
  rows.append(row)
 return pd.DataFrame(rows)
def _save_raw(data_dir:Path,name:str,raw:bytes,suffix:str):
 folder=Path(data_dir)/'raw'/'snapshots'; folder.mkdir(parents=True,exist_ok=True); path=folder/(name+'_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.'+suffix); path.write_bytes(raw); return path,hashlib.sha256(raw).hexdigest()
def fetch_eurostat_series(data_dir:Path,dataset_code:str,dataset_id:str,params:dict,meaning:str):
 url=EUROSTAT+'/'+dataset_code; response=requests.get(url,params=params,headers=HEADERS,timeout=30); response.raise_for_status(); payload=response.json(); raw=json.dumps(payload,ensure_ascii=False).encode(); path,digest=_save_raw(data_dir,dataset_id,raw,'json')
 frame=eurostat_json_to_frame(payload,dataset_id,params.get('geo','FR'))
 if 'time' not in frame: raise ValueError('Missing time dimension for '+dataset_id)
 frame['period']=frame['time'].astype(str); frame['value']=pd.to_numeric(frame['value'],errors='coerce'); frame['source_url']=response.url; frame['retrieved_at_utc']=datetime.now(timezone.utc).isoformat(); frame['series_definition']=meaning; frame=frame.dropna(subset=['value'])
 if frame.empty: raise ValueError('No observations for '+dataset_id)
 return frame,{'dataset_id':dataset_id,'publisher':'Eurostat','url':response.url,'rows':len(frame),'status':'ok','raw_file':str(path),'raw_sha256':digest,'series_definition':meaning}
def fetch_ecb_csv(data_dir:Path,currency:str,dataset_id:str):
 url=f'{ECB}/D.{currency}.EUR.SP00.A'; response=requests.get(url,params={'startPeriod':'2019-01-01','format':'csvdata'},headers=HEADERS,timeout=30); response.raise_for_status(); path,digest=_save_raw(data_dir,dataset_id,response.content,'csv'); raw=pd.read_csv(StringIO(response.text))
 t=next((c for c in raw if c.lower() in ('time_period','time','date')),None); v=next((c for c in raw if c.lower() in ('obs_value','observation_value','value')),None)
 if not t or not v: raise ValueError('Unexpected ECB CSV schema')
 frame=pd.DataFrame({'period':pd.to_datetime(raw[t],errors='coerce').dt.strftime('%Y-%m-%d'),'value':pd.to_numeric(raw[v],errors='coerce')}).dropna(); frame['dataset_id']=dataset_id; frame['currency_code']=currency; frame['quotation']=currency+' per EUR'; frame['source_url']=response.url; frame['retrieved_at_utc']=datetime.now(timezone.utc).isoformat()
 if frame.empty: raise ValueError('No ECB observations for '+currency)
 return frame,{'dataset_id':dataset_id,'publisher':'ECB','url':response.url,'rows':len(frame),'status':'ok','raw_file':str(path),'raw_sha256':digest}
def refresh_all(data_dir:Path,quiet_errors:bool=False)->dict:
 data_dir=Path(data_dir); processed=data_dir/'processed'; processed.mkdir(parents=True,exist_ok=True); manifest={'run_at_utc':datetime.now(timezone.utc).isoformat(),'feeds':[]}
 jobs=[('eurostat_hicp_all','prc_hicp_minr',{'freq':'M','geo':'FR','coicop':'CP00','unit':'RCH_A','sinceTimePeriod':'2019-01'},'HICP annual rate of change (%)'),('eurostat_hicp_food','prc_hicp_minr',{'freq':'M','geo':'FR','coicop':'CP01','unit':'RCH_A','sinceTimePeriod':'2019-01'},'Food HICP annual rate of change (%)')]
 for name,code,params,definition in jobs:
  try:
   frame,meta=fetch_eurostat_series(data_dir,code,name,params,definition); frame.to_csv(processed/(name+'.csv'),index=False); manifest['feeds'].append(meta)
  except Exception as exc: manifest['feeds'].append({'dataset_id':name,'status':'error','error':str(exc)})
 try:
  frame,meta=fetch_ecb_csv(data_dir,'USD','ecb_usd_eur'); frame.to_csv(processed/'ecb_usd_eur.csv',index=False); manifest['feeds'].append(meta)
 except Exception as exc: manifest['feeds'].append({'dataset_id':'ecb_usd_eur','status':'error','error':str(exc)})
 (processed/'refresh_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8'); return manifest
