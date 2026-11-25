import requests, json, time, html, sys
from concurrent.futures import ThreadPoolExecutor
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'}
B='https://www.perfumeshopping.com.br/wp-json/wc/store/v1/products/'
pop=json.load(open('ps/popular.json')); allp=json.load(open('ps/all.json'))
kits=[p for p in allp if any(c['name']=='KITS' for c in p['categories'])]
targets=pop[:120]+kits
def fv(v):
    for i in range(3):
        try:
            r=requests.get(B+str(v['id']),headers=UA,timeout=30)
            if r.status_code==200:
                d=r.json(); return v['attributes'][0]['value'] if v['attributes'] else '', int(d['prices']['price'])/100, d.get('is_in_stock')
        except Exception as e: pass
        time.sleep(2)
    return None
out=[]
with ThreadPoolExecutor(6) as ex:
    for rank,p in enumerate(targets):
        vs=p.get('variations',[])
        res=list(ex.map(fv,vs)) if vs else []
        cats=[html.unescape(c['name']) for c in p['categories']]
        out.append({'rank':rank+1 if rank<120 else None,'name':html.unescape(p['name']),'type':p['type'],'cats':cats,
                    'price':int(p['prices']['price'])/100,'range':[int(p['prices']['price_range']['min_amount'])/100,int(p['prices']['price_range']['max_amount'])/100] if p['prices'].get('price_range') else None,
                    'vars':[r for r in res if r],'link':p['permalink'],'short':html.unescape(p.get('short_description',''))[:400]})
        if rank%20==0: print(rank, flush=True)
json.dump(out,open('ps/top_vars.json','w'),ensure_ascii=False,indent=0)
print('done',len(out))
