"""Calcula todos os números usados no HTML a partir do model.py."""
import json, os
import model as m

D = os.path.dirname(os.path.abspath(__file__))

def brl(x, sign=False):
    neg = x < 0
    s = f"{abs(x):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return ('-R$ ' if neg else ('+R$ ' if sign else 'R$ ')) + s

def num(x, d=0):
    s = f"{x:,.{d}f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return s

def pct(x, d=0):
    return num(x * 100, d) + '%'

N = {}
SK = m.SKUS

# ---------- faixas ----------
N['caps'] = m.CAP
N['tiers'] = m.TIERS

def tier_econ(t, cml):
    out = {}
    for ml, p in [(5, m.P5[t]), (10, m.P10[t])]:
        c = m.decant_cost(ml, cml)
        mg = m.margin(p, c)
        out[ml] = dict(price=p, cost=c, mg=mg, mgp=mg / p)
    # 2 ml adicional
    c2 = m.decant_cost(2, cml)
    mg2 = m.margin(m.P2ADD[t], c2)
    out[2] = dict(price=m.P2ADD[t], cost=c2, mg=mg2, mgp=mg2 / m.P2ADD[t])
    return out

# custo médio ponderado (peso Trends) dos SKUs de cada faixa no portfólio de R$ 3.000 + próprios
port_all = m.portfolio(3000)
def wavg_cml(t):
    ks = [k for k in port_all if SK[k]['tier'] == t]
    if not ks: return None
    w = sum(SK[k]['w'] for k in ks)
    return sum(SK[k]['w'] * SK[k]['cml'] for k in ks) / w
N['wcml'] = {t: wavg_cml(t) for t in m.TIERS}
N['wcml']['D'] = 11.49  # Bleu de Chanel EDP como referência da faixa D

# ---------- economia por oferta, faixa A (tabela principal, como na versão anterior) ----------
cA = N['wcml']['A']
offers = {}
for o in m.OFFERS:
    n, ml = m.SLOTS[o]
    e = m.offer_economics(o, [('A', cA)] * n)
    offers[o] = e
N['offA'] = offers

def offer_min_price(o, e):
    # preço mínimo: margem de contribuição zero (custos variáveis fixos em R$ + % sobre preço)
    var_fixed = e['perf'] + e['vials'] + e['labels'] + e['brinde'] + e['pack']
    return var_fixed / (1 - m.FEE - m.RES)

# ---------- exemplos de kits ----------
def kit_example(o, keys):
    tl = [(SK[k]['tier'], SK[k]['cml']) for k in keys]
    e = m.offer_economics(o, tl)
    return e
N['kit_ex'] = []
for label, o, keys in [
    ('Trio só árabes (Asad, Yara, Sabah Al Ward)', 'trio', ['asad', 'yara', 'sabah']),
    ('Trio com 1 grife (Asad, Yara, Sauvage EDT)', 'trio', ['asad', 'yara', 'sauv']),
    ('Trio misto (Club de Nuit, Sauvage EDT, La Vie Est Belle)', 'trio', ['cdnim', 'sauv', 'lveb']),
    ('Trio só grife (Sauvage EDT, 212 VIP Men, La Vie Est Belle)', 'trio', ['sauv', '212', 'lveb']),
    ('Descoberta só árabes (5 árabes)', 'desc', ['asad', 'yara', 'sabah', 'cdnim', 'p9pm']),
    ('Descoberta com 2 grifes (3 árabes + Sauvage + La Vie Est Belle)', 'desc', ['asad', 'yara', 'cdnim', 'sauv', 'lveb']),
    ('Dupla 10 ml árabe (Asad + Yara)', 'dupla', ['asad', 'yara']),
    ('Dupla 10 ml grife (Sauvage EDT + La Vie Est Belle)', 'dupla', ['sauv', 'lveb']),
]:
    e = kit_example(o, keys)
    N['kit_ex'].append((label, o, keys, e))

# preço fixo (seleção adversa): Trio a R$ 89,90 com 3 grifes, cobrando como faixa A
def fixed_price_trio(keys):
    tl = [(SK[k]['tier'], SK[k]['cml']) for k in keys]
    e = m.offer_economics('trio', tl)
    price = m.BASE['trio']
    cm = price - (e['perf'] + e['vials'] + e['labels'] + e['brinde'] + e['pack']) - price * (m.FEE + m.RES)
    return price, cm
N['fixed_adverse'] = fixed_price_trio(['sauv', '212', 'lveb'])
N['fixed_adverse_mix'] = fixed_price_trio(['cdnim', 'sauv', 'lveb'])

# ---------- tabela de frascos de referência ----------
N['ref'] = []
for nome, linha, preco, ml, fonte in m.REF_BOTTLES:
    cml = preco / ml
    t = m.tier_for(cml, linha)
    N['ref'].append((nome, linha, preco, ml, fonte, cml, t))

# ---------- SKUs ----------
N['sku_econ'] = {}
for k, s in SK.items():
    N['sku_econ'][k] = tier_econ(s['tier'], s['cml']) if s['tier'] in m.TIERS else None

# ---------- cenários por orçamento ----------
N['budgets'] = {}
for b in m.BUDGETS:
    perf, ins, inv, res = m.invest(b)
    W = sum(SK[k]['w'] for k in m.portfolio(b))
    r = {}
    for case in m.CASES:
        rows, t = m.simulate(b, case)
        r[case] = (rows, t)
    sens = {e: (m.simulate(b, 'Base', elasticity=e)[1], m.simulate(b, 'Conservador', elasticity=e)[1]) for e in [0, 0.3, 0.5]}
    N['budgets'][b] = dict(perf=perf, ins=ins, inv=inv, res=res, W=W, M=(W / m.W_REF) ** m.ELAST, res_cases=r, sens=sens,
                           skus=m.portfolio(b), nsku=len(m.portfolio(b)), ngrife=len([k for k in m.portfolio(b) if SK[k]['linha'] == 'Grife']))
# plano escalonado
esc = {}
for case in m.CASES:
    esc[case] = m.simulate('esc', case)
N['esc'] = esc
N['esc_sens_e'] = {e: (m.simulate('esc', 'Base', elasticity=e)[1], m.simulate('esc', 'Conservador', elasticity=e)[1]) for e in [0, 0.3, 0.5]}
N['esc_inv0'] = esc['Base'][1]['inv']
N['esc_perf0'] = round(sum(SK[k]['preco'] for k in m.STAGED['start']), 2)
N['esc_stage_cost'] = [round(sum(SK[k]['preco'] for k in ks), 2) for g, ks in m.STAGED['stages']]

# sensibilidades do plano escalonado (cenário base)
base_rows, base_t = esc['Base']
def sens(label, **kw):
    rows, t = m.simulate('esc', 'Base', **kw)
    mar = rows[3]
    return dict(label=label, cmo=t['cmo'], op_mar=mar['op'], op6=t['op'], cash=t['cash_end'], owner=t['owner'])
N['sens'] = [
    sens('Plano escalonado, cenário base'),
    sens('Preço 10% menor', price_mult=0.9),
    sens('Custo do perfume 15% maior', cost_mult=1.15),
    sens('Marketing dobrado', mkt_mult=2.0),
    sens('Frete grátis subsidiado: R$ 15 por pedido', ship_sub=15.0),
    sens('Perda de 10% no envase', loss=0.10),
    sens('Perda de 15% no envase', loss=0.15),
    sens('Mix de menor margem (50% Kit Descoberta)', desc_heavy=True),
    sens('Catálogo não atrai mais pedidos (elasticidade zero)', elasticity=0.0),
    sens('Tudo ruim junto: preço −10%, perfume +15%, frete R$ 15', price_mult=0.9, cost_mult=1.15, ship_sub=15.0),
]

# ---------- indicadores derivados (plano escalonado, base) ----------
cmo = base_t['cmo']
N['cmo'] = cmo
N['ticket'] = base_t['ticket']
m10A = tier_econ('A', cA)[10]['mg']
N['m10A'] = m10A
N['client_value'] = cmo + 0.30 * m10A
N['cac_max'] = N['client_value'] * 0.5
N['be_nomkt'] = m.FIXED / cmo
N['be_200'] = (m.FIXED + 200) / cmo
# estoque em 30/60/90 dias no ritmo de mar/27 (cenário base)
mar = base_rows[3]
mix = m.CASES['Base']['mix']
ml_per_order = sum(mix[o] * m.SLOTS[o][0] * m.SLOTS[o][1] for o in m.OFFERS)
ml_month = mar['orders'] * ml_per_order / (1 - m.LOSS)
port_mar = m.STAGED['start'] + [k for g, ks in m.STAGED['stages'] for k in ks] + m.OWN
wtot = sum(SK[k]['w'] for k in port_mar)
cml_avg = sum(SK[k]['w'] * SK[k]['cml'] for k in port_mar) / wtot
N['stock_cov'] = [(d, ml_month * d / 30, ml_month * d / 30 / 100, ml_month * d / 30 * cml_avg) for d in (30, 60, 90)]
N['ml_month_mar'] = ml_month
N['cml_avg_mar'] = cml_avg
N['orders_mar'] = mar['orders']

# teto do MEI
N['mei_month'] = 81000 / 12
oti_rows = esc['Otimista'][0]
N['oti_last_month_rev'] = oti_rows[-1]['rev']
N['base_last_month_rev'] = base_rows[-1]['rev']

if __name__ == '__main__':
    print('wcml', N['wcml'])
    for o, e in N['offA'].items():
        print(o, {k: round(v, 2) for k, v in e.items()}, 'min', round(offer_min_price(o, e), 2))
    for l, o, ks, e in N['kit_ex']:
        print(l, round(e['price'], 2), round(e['cm'], 2), pct(e['cm'] / e['price'], 1))
    print('fixed adverse', N['fixed_adverse'], N['fixed_adverse_mix'])
    for r in N['ref']: print(r[0], round(r[5], 2), r[6])
    for s in N['sens']: print(s['label'], round(s['cmo'], 2), round(s['op_mar'], 2), round(s['op6'], 2), round(s['cash'], 2), round(s['owner'], 2))
    print('cmo', cmo, 'ticket', N['ticket'], 'cac_max', N['cac_max'], 'be', N['be_nomkt'], N['be_200'])
    print('stock', N['stock_cov'])
    print('mei', N['mei_month'], 'oti last', N['oti_last_month_rev'], 'base last', N['base_last_month_rev'])
    for case in m.CASES:
        rows, t = esc[case]
        print(case, [(r['m'], round(r['orders'], 1), round(r['rev']), round(r['op']), round(r['cash']), r['nsku']) for r in rows], t['added'])
