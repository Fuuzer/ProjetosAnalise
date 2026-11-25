from pytrends.request import TrendReq
import time, json, pandas as pd
pt = TrendReq(hl='pt-BR', tz=180, timeout=(10,30), retries=0)
out = {}
for kw in ['decant', 'perfume arabe', 'perfume arabe masculino', 'perfume importado', 'contratipo', 'perfume masculino', 'perfume feminino']:
    for tf in ['today 12-m']:
        for attempt in range(3):
            try:
                pt.build_payload([kw], timeframe=tf, geo='BR')
                rq = pt.related_queries()[kw]
                out[kw] = {k: (v.to_dict('records') if v is not None else None) for k, v in rq.items()}
                reg = pt.interest_by_region(resolution='REGION', inc_low_vol=True)
                out[kw]['region'] = reg[kw].sort_values(ascending=False).to_dict()
                break
            except Exception as e:
                print('ERR', kw, e); time.sleep(20)
        time.sleep(8)
json.dump(out, open('trends/related.json','w'), ensure_ascii=False, indent=1)
for kw, d in out.items():
    print('=====', kw)
    print('TOP:', [(r['query'], r['value']) for r in (d.get('top') or [])][:25])
    print('RISING:', [(r['query'], r['value']) for r in (d.get('rising') or [])][:25])
    print('REGION top 8:', list(d['region'].items())[:8], ' RS=', d['region'].get('Rio Grande do Sul'))
