from pytrends.request import TrendReq
import time, json
pt = TrendReq(hl='pt-BR', tz=180, timeout=(10,30), retries=0)
def run(kws, tf, geo):
    for attempt in range(5):
        try:
            pt.build_payload(kws, timeframe=tf, geo=geo); return pt.interest_over_time().drop(columns=['isPartial'], errors='ignore')
        except Exception as e:
            print('ERR', kws, e, flush=True); time.sleep(40)
out={}
# 1) categorias 5 anos BR
df = run(['decant','perfume arabe','perfume de nicho','contratipo','perfume importado'], 'today 5-y', 'BR')
df.to_csv('trends/cat5y_BR.csv'); print(df.resample('YE').mean().round(1), flush=True)
time.sleep(10)
df = run(['decant','perfume arabe','perfume de nicho','contratipo','perfume importado'], 'today 5-y', 'BR-RS')
df.to_csv('trends/cat5y_RS.csv'); print(df.resample('YE').mean().round(1), flush=True)
time.sleep(10)
# 2) termos extras com a mesma âncora
ANCHOR='bleu de chanel'
extra = {
 'YSL Y / MYSLF': 'ysl y + myslf',
 'CH Bad Boy': 'bad boy carolina herrera + perfume bad boy',
 'Armani Code': 'armani code',
 'D&G Light Blue': 'light blue dolce + light blue perfume',
 'Paco Rabanne Phantom': 'phantom paco rabanne + perfume phantom',
 'Versace Dylan Blue': 'dylan blue',
 'Lattafa Asad Bourbon': 'asad bourbon',
 'Maison Alhambra Salvo': 'salvo maison alhambra + salvo intense',
 'Lattafa Musamam': 'musamam',
 'Lattafa Atheeri': 'atheeri',
 'Afnan Turathi': 'turathi',
 'Armaf CDN Untold': 'club de nuit untold',
}
res={}
names=list(extra)
base=None
for i in range(0,len(names),4):
    b=names[i:i+4]; kws=[ANCHOR]+[extra[n] for n in b]
    df=run(kws,'today 12-m','BR')
    if df is None: continue
    a=df[ANCHOR].mean()
    for n in b: res[n]={'raw_ratio_to_anchor': float(df[extra[n]].mean()/a), 'last_q_ratio': float(df[extra[n]].iloc[-13:].mean()/a), 'first_q_ratio': float(df[extra[n]].iloc[:13].mean()/a)}
    print('ok',b,flush=True); time.sleep(10)
json.dump(res,open('trends/extra_BR.json','w'),ensure_ascii=False,indent=1)
print(res)
