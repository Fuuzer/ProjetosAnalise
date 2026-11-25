import requests,json,time,re,sys
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'}
qs=sys.argv[1:]
out={}
for q in qs:
    try:
        r=requests.get('https://www.epocacosmeticos.com.br/api/catalog_system/pub/products/search',params={'ft':q,'_from':0,'_to':24},headers=UA,timeout=30)
        d=r.json()
    except Exception as e:
        print('ERR',q,e,r.status_code if 'r' in dir() else ''); continue
    rows=[]
    for p in d:
        for it in p.get('items',[]):
            offers=[s['commertialOffer'] for s in it.get('sellers',[]) if s.get('commertialOffer',{}).get('AvailableQuantity',0)>0]
            if not offers: continue
            o=offers[0]
            rows.append((p['productName'], it.get('name'), o.get('Price'), o.get('ListPrice'), p.get('link')))
    out[q]=rows
    print('==',q)
    for r_ in rows[:8]: print('   ',r_[0][:70],'|',r_[1],'|',r_[2],'|',r_[3])
    time.sleep(0.6)
json.dump(out,open('epoca/'+re.sub(r'\W','_',qs[0])+'.json','w'),ensure_ascii=False)
