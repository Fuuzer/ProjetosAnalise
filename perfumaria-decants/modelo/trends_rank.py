from pytrends.request import TrendReq
import time, json, sys
geo = sys.argv[1] if len(sys.argv) > 1 else 'BR'
tf = sys.argv[2] if len(sys.argv) > 2 else 'today 12-m'
pt = TrendReq(hl='pt-BR', tz=180, timeout=(10,30), retries=0)
ANCHOR = 'bleu de chanel'
items = {
 # designer masculino
 'Dior Sauvage': 'sauvage',
 'Creed Aventus': 'aventus',
 'Paco Rabanne Invictus': 'invictus',
 'Carolina Herrera 212 VIP': '212 vip',
 'JPG Le Male / Ultra Male': 'le male + ultra male',
 'Versace Eros': 'eros versace + versace eros',
 'Paco Rabanne 1 Million': '1 million + one million',
 'Armani Acqua di Gio': 'acqua di gio',
 'Armani Stronger With You': 'stronger with you',
 'JPG Le Beau': 'le beau',
 'Valentino Born in Roma': 'born in roma',
 'Azzaro Wanted': 'azzaro wanted + the most wanted',
 # designer feminino
 'Lancome La Vie Est Belle': 'la vie est belle',
 'CH Good Girl': 'good girl carolina herrera + perfume good girl',
 'YSL Libre': 'libre ysl + perfume libre',
 'JPG Scandal': 'scandal perfume + perfume scandal',
 'Chanel Coco Mademoiselle': 'coco mademoiselle',
 'Miss Dior': 'miss dior',
 'Paco Rabanne Olympea': 'olympea',
 'Burberry Goddess': 'burberry goddess',
 'Dior J adore': 'jadore + j adore',
 # nicho
 'MFK Baccarat Rouge 540': 'baccarat rouge',
 'PDM Delina': 'delina',
 'Xerjoff Erba Pura': 'erba pura',
 'Kilian Angels Share': 'angels share',
 'PDM Layton': 'layton',
 'PDM Althair': 'althair',
 'Tom Ford Tobacco Vanille': 'tobacco vanille',
 # arabes
 'Lattafa Asad': 'asad lattafa + perfume asad + asad perfume',
 'Lattafa Yara': 'yara lattafa + perfume yara + yara perfume',
 'Lattafa Khamrah': 'khamrah',
 'Armaf Club de Nuit': 'club de nuit',
 'Afnan 9pm': '9pm afnan + perfume 9pm + 9pm perfume',
 'Al Wataniah Sabah Al Ward': 'sabah al ward + perfume sabah',
 'French Avenue Liquid Brun': 'liquid brun',
 'Lattafa Fakhar': 'fakhar',
 'Rasasi Hawas': 'hawas',
 'Lattafa Badee Al Oud': 'badee al oud + bade e al oud',
 'Armaf Odyssey': 'odyssey armaf + armaf odyssey',
 'Al Haramain Amber Oud': 'amber oud',
 'Queen of Arabia': 'queen of arabia',
 'French Avenue Vulcan Feu': 'vulcan feu',
 'Lattafa Eclaire': 'eclaire',
 'Lattafa Hayaati': 'hayaati',
 'Al Wataniah Eqaab': 'eqaab',
 'Lattafa Qaed Al Fursan': 'qaed al fursan',
 'Lattafa His Confession': 'his confession',
 'Lattafa Ana Abiyedh': 'ana abiyedh',
 'Afnan Supremacy': 'supremacy afnan + afnan supremacy',
}
names = list(items)
res = {}
anchor_base = None
for i in range(0, len(names), 4):
    batch = names[i:i+4]
    kws = [ANCHOR] + [items[n] for n in batch]
    for attempt in range(4):
        try:
            pt.build_payload(kws, timeframe=tf, geo=geo)
            df = pt.interest_over_time()
            break
        except Exception as e:
            print('ERR', batch, e, flush=True); time.sleep(30)
    else:
        continue
    df = df.drop(columns=['isPartial'], errors='ignore')
    a = df[ANCHOR].mean()
    if anchor_base is None: anchor_base = a
    for n in batch:
        s = df[items[n]]
        k = anchor_base / a if a else float('nan')
        last3 = s.iloc[-13:].mean(); first3 = s.iloc[:13].mean()
        res[n] = {'mean12m': float(s.mean()*k), 'last_q': float(last3*k), 'first_q': float(first3*k), 'peak_week': str(s.idxmax().date())}
    print('ok', batch, flush=True)
    time.sleep(7)
res['_anchor'] = {'term': ANCHOR, 'mean': float(anchor_base)}
json.dump(res, open(f'trends/rank_{geo}_{tf.replace(" ","_")}.json','w'), ensure_ascii=False, indent=1)
rows = sorted([(n, v) for n, v in res.items() if not n.startswith('_')], key=lambda x: -x[1]['mean12m'])
for n, v in rows:
    print(f"{n:32s} {v['mean12m']:8.2f}  ult.trim {v['last_q']:7.2f}  1o.trim {v['first_q']:7.2f}  pico {v['peak_week']}")
