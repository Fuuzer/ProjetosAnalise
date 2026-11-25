import requests, json, time, sys
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'}
B='https://www.perfumeshopping.com.br/wp-json/wc/store/v1/products'
def get(params):
    for i in range(3):
        try:
            r=requests.get(B,params=params,headers=UA,timeout=40)
            if r.status_code==200: return r.json(), r.headers
            print('status',r.status_code, file=sys.stderr)
        except Exception as e: print(e, file=sys.stderr)
        time.sleep(3)
    return None, None
# popularity ranking
pop=[]
for p in range(1,4):
    d,h=get({'orderby':'popularity','order':'desc','per_page':100,'page':p})
    if not d: break
    pop+=d
    print('pop page',p,len(d),h.get('X-WP-Total'), flush=True)
json.dump(pop,open('ps/popular.json','w'),ensure_ascii=False)
# full catalog
allp=[]
p=1
while True:
    d,h=get({'per_page':100,'page':p})
    if not d: break
    allp+=d
    tot=int(h.get('X-WP-TotalPages','1'))
    print('cat page',p,'/',tot, flush=True)
    if p>=tot: break
    p+=1
    time.sleep(0.5)
json.dump(allp,open('ps/all.json','w'),ensure_ascii=False)
print('total',len(allp))
