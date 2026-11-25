"""Modelo financeiro do plano de decants (versão 2).
Todas as premissas ficam explícitas aqui; as tabelas do HTML saem deste arquivo."""
import json, math, os, copy

D = os.path.dirname(os.path.abspath(__file__))
TR_BR = json.load(open(os.path.join(D, 'trends/rank_BR_today_12-m.json')))
TR_RS = json.load(open(os.path.join(D, 'trends/rank_BR-RS_today_12-m.json')))
A_BR = TR_BR['_anchor']['mean']; A_RS = TR_RS['_anchor']['mean']

def tw(key):
    """Peso de demanda: média de BR e RS em 'unidades Bleu de Chanel' (âncora = 1)."""
    br = TR_BR[key]['mean12m'] / A_BR
    rs = TR_RS[key]['mean12m'] / A_RS
    return 0.5 * br + 0.5 * rs, br, rs

# ---------------- premissas gerais ----------------
LOSS = 0.05            # perda no envase
FEE = 0.025            # taxa média de pagamento
RES = 0.03             # reserva para perdas, vazamentos e devoluções
VIAL = {2: 2.97, 5: 2.69, 10: 2.78}
LABEL = 0.38
BRINDE = 2.86          # 1 ml do próximo perfume (flaconete + perfume + rótulo)
PACK = 3.81            # caixa, envelope com bolha, cartão e proteção por pedido
FIXED = 112.05         # DAS 82,05 + 30 de consumíveis
HOUR = 25.0
MIN_DECANT, MIN_ORDER = 4, 5
CASH_MIN = 150.0

# faixas de preço (por custo por ml do frasco de reposição)
TIERS = ['A', 'B', 'C', 'D']
TIER_NAME = {'A': 'Faixa A (árabes e clones)', 'B': 'Faixa B (grife de giro)', 'C': 'Faixa C (grife premium)', 'D': 'Faixa D (luxo, só pré-venda)'}
P5 = {'A': 34.90, 'B': 49.90, 'C': 69.90, 'D': 99.90}
P10 = {'A': 59.90, 'B': 89.90, 'C': 129.90, 'D': 189.90}
P2ADD = {'A': 12.90, 'B': 19.90, 'C': 24.90, 'D': 36.90}       # 2 ml adicional em pedido
ADD_DESC = {'A': 0.0, 'B': 6.90, 'C': 12.90, 'D': 22.90}         # por 2 ml no Kit Descoberta
ADD_TRIO = {'A': 0.0, 'B': 12.90, 'C': 34.90, 'D': 55.90}        # por 5 ml no Kit Trio
ADD_DUPLA = {'A': 0.0, 'B': 27.90, 'C': 64.90, 'D': 119.90}      # por 10 ml no Kit Dupla
BASE = {'desc': 69.90, 'trio': 89.90, 'dupla': 109.90}

def tier_cap(p5):
    """Maior custo por ml que mantém 30% de margem no 5 ml."""
    return (p5 * (1 - FEE - RES - 0.30) - VIAL[5] - LABEL) * (1 - LOSS) / 5
CAP = {t: tier_cap(P5[t]) for t in TIERS}

def tier_for(cml, linha):
    for t in TIERS:
        if cml <= CAP[t] + 1e-9:
            if linha == 'Grife' and t == 'A':
                return 'B'  # piso: grife começa na faixa B
            return t
    return 'E'

# ---------------- SKUs ----------------
# preco: frasco de reposição (R$), ml: volume do frasco de reposição; util0: ml disponíveis no início
SKUS = {
 'asad':   dict(nome='Lattafa Asad', linha='Árabe', gen='Masculino', fam='Âmbar especiado', preco=185.43, ml=100, fonte='Magalu (lojista com NF), plano anterior', proprio=False, tkey='Lattafa Asad', compara='Dior Sauvage Elixir'),
 'yara':   dict(nome='Lattafa Yara', linha='Árabe', gen='Feminino', fam='Gourmand atalcado', preco=160.46, ml=100, fonte='Magalu, plano anterior', proprio=False, tkey='Lattafa Yara', compara=None),
 'sabah':  dict(nome='Al Wataniah Sabah Al Ward', linha='Árabe', gen='Feminino', fam='Floral frutado', preco=128.61, ml=100, fonte='Magalu (Pix), plano anterior', proprio=False, tkey='Al Wataniah Sabah Al Ward', compara=None),
 'cdnim':  dict(nome='Armaf Club de Nuit Intense Man', linha='Árabe', gen='Masculino', fam='Amadeirado frutado defumado', preco=299.90, ml=105, fonte='Época Cosméticos (105 ml)', proprio=False, tkey='Armaf Club de Nuit', compara='Creed Aventus'),
 'fakhar': dict(nome='Lattafa Fakhar Rose', linha='Árabe', gen='Feminino', fam='Floral frutado', preco=224.01, ml=100, fonte='Magalu, plano anterior', proprio=False, tkey='Lattafa Fakhar', compara=None),
 'khamrah':dict(nome='Lattafa Khamrah', linha='Árabe', gen='Unissex', fam='Gourmand especiado', preco=269.90, ml=100, fonte='Época Cosméticos', proprio=False, tkey='Lattafa Khamrah', compara="Kilian Angels' Share"),
 'p9pm':   dict(nome='Afnan 9pm', linha='Árabe', gen='Masculino', fam='Âmbar adocicado', preco=222.27, ml=100, fonte='Frasco próprio; reposição no Magalu', proprio=True, util0=40, repor='so_se_vender', tkey='Afnan 9pm', compara=None),
 'brun':   dict(nome='French Avenue Liquid Brun', linha='Árabe', gen='Unissex', fam='Gourmand amadeirado', preco=296.70, ml=100, fonte='Frasco próprio; reposição no Magalu', proprio=True, util0=40, repor='nao_tri1', tkey='French Avenue Liquid Brun', compara=None),
 'sauv':   dict(nome='Dior Sauvage EDT', linha='Grife', gen='Masculino', fam='Aromático fresco', preco=1002.51, ml=200, fonte='Frasco próprio; reposição: Época, 200 ml', proprio=True, util0=40, repor='se_caixa', tkey='Dior Sauvage', compara=None),
 'lveb':   dict(nome='Lancôme La Vie Est Belle EDP', linha='Grife', gen='Feminino', fam='Gourmand floral', preco=654.90, ml=100, fonte='Época Cosméticos (refil 100 ml)', proprio=False, tkey='Lancome La Vie Est Belle', compara=None),
 'hawas':  dict(nome='Rasasi Hawas for Him', linha='Árabe', gen='Masculino', fam='Aromático aquático', preco=279.90, ml=100, fonte='Época Cosméticos', proprio=False, tkey='Rasasi Hawas', compara=None),
 '212':    dict(nome='Carolina Herrera 212 VIP Men EDT', linha='Grife', gen='Masculino', fam='Especiado amadeirado', preco=718.53, ml=200, fonte='Época Cosméticos (200 ml)', proprio=False, tkey='Carolina Herrera 212 VIP', compara=None),
}
for k, s in SKUS.items():
    s['cml'] = s['preco'] / s['ml']
    s['tier'] = tier_for(s['cml'], s['linha'])
    s['w'], s['w_br'], s['w_rs'] = tw(s['tkey'])

# frascos fora do portfólio comprado, para a tabela de faixas (custo de reposição observado)
REF_BOTTLES = [
 ('Paco Rabanne 1 Million EDT', 'Grife', 729.00, 200, 'Época'),
 ('Versace Eros EDT', 'Grife', 594.00, 200, 'Época (lojista parceiro)'),
 ('Armani Acqua di Giò EDT', 'Grife', 877.00, 200, 'Época'),
 ('JPG Le Male Le Parfum', 'Grife', 821.70, 200, 'Época'),
 ('Armani Stronger With You EDT', 'Grife', 496.53, 100, 'Época'),
 ('Dior Sauvage EDP', 'Grife', 1168.41, 200, 'Época'),
 ('Paco Rabanne Invictus EDT', 'Grife', 689.56, 100, 'Época'),
 ('YSL Y EDP', 'Grife', 858.00, 100, 'Época'),
 ('Carolina Herrera Good Girl EDP', 'Grife', 829.90, 80, 'Época'),
 ('Miss Dior Parfum', 'Grife', 891.91, 80, 'Época'),
 ('Chanel Bleu de Chanel EDP', 'Grife', 1149.00, 100, 'Droga Raia (via busca)'),
 ('Chanel Bleu de Chanel Parfum', 'Grife', 2132.72, 100, 'Drogasil, plano anterior'),
 ('Xerjoff Erba Pura', 'Nicho', 1427.00, 100, 'Época'),
 ('Creed Aventus', 'Nicho', 3320.84, 100, 'Época'),
 ('PDM Delina', 'Nicho', 3635.00, 75, 'Época'),
 ('MFK Baccarat Rouge 540 EDP', 'Nicho', 4064.10, 70, 'Época'),
]

# ---------------- economia por decant e por oferta ----------------
def decant_cost(ml, cml):
    return ml * cml / (1 - LOSS) + VIAL[ml] + LABEL

def margin(price, cost):
    return price * (1 - FEE - RES) - cost

OFFERS = ['desc', 'trio', 'duo5', 'ml10', 'dupla']
OFFER_NAME = {'desc': 'Kit Descoberta (5 × 2 ml)', 'trio': 'Kit Trio (3 × 5 ml)', 'duo5': 'Dupla de 5 ml avulsos', 'ml10': '10 ml avulso', 'dupla': 'Kit Dupla 10 ml'}
SLOTS = {'desc': (5, 2), 'trio': (3, 5), 'duo5': (2, 5), 'ml10': (1, 10), 'dupla': (2, 10)}
HAS_BRINDE = {'desc': False, 'trio': True, 'duo5': False, 'ml10': False, 'dupla': True}

def slot_price(offer, tier):
    if offer == 'desc': return ADD_DESC[tier]
    if offer == 'trio': return ADD_TRIO[tier]
    if offer == 'dupla': return ADD_DUPLA[tier]
    if offer == 'duo5': return P5[tier]
    if offer == 'ml10': return P10[tier]

def offer_base(offer):
    return BASE.get(offer, 0.0)

def offer_economics(offer, tiers_cml):
    """tiers_cml: lista de (tier, custo_ml) por slot. Retorna dicionário com preço e custos."""
    n, ml = SLOTS[offer]
    price = offer_base(offer) + sum(slot_price(offer, t) for t, _ in tiers_cml)
    perf = sum(ml * c / (1 - LOSS) for _, c in tiers_cml)
    vials = n * VIAL[ml]; labels = n * LABEL
    brinde = BRINDE if HAS_BRINDE[offer] else 0.0
    fee = price * FEE; res = price * RES
    cm = price - perf - vials - labels - brinde - PACK - fee - res
    mins = n * MIN_DECANT + MIN_ORDER
    return dict(price=price, perf=perf, vials=vials, labels=labels, brinde=brinde, pack=PACK, fee=fee, res=res, cm=cm, labor=mins / 60 * HOUR, mins=mins)

# ---------------- cenários de demanda ----------------
CASES = {
 'Conservador': dict(orders=[6, 9, 10, 11, 12, 13], rep=[0, .055, .10, .10, .15, .15], mkt=[0, 50, 100, 100, 100, 100], mix={'desc': .35, 'trio': .25, 'duo5': .20, 'ml10': .15, 'dupla': .05}),
 'Base':        dict(orders=[12, 18, 22, 25, 28, 30], rep=[0, .10, .15, .20, .25, .25], mkt=[0, 150, 150, 200, 200, 200], mix={'desc': .25, 'trio': .35, 'duo5': .15, 'ml10': .15, 'dupla': .10}),
 'Otimista':    dict(orders=[20, 30, 38, 45, 50, 55], rep=[0, .15, .20, .25, .30, .30], mkt=[0, 250, 300, 300, 350, 350], mix={'desc': .20, 'trio': .35, 'duo5': .15, 'ml10': .15, 'dupla': .15}),
}
MONTHS = ['dez/26', 'jan/27', 'fev/27', 'mar/27', 'abr/27', 'mai/27']

# ---------------- cenários de orçamento ----------------
INSUMOS = [
 ('Frascos de vidro 5 ml com spray (pacote de 20)', 1, 53.85),
 ('Frascos de vidro 2 ml com spray (pacote de 30)', 1, 89.00),
 ('Caixas kraft para presente (pacote de 20)', 1, 45.00),
 ('Envelopes de segurança com bolha 19×25 (pacote de 50)', 1, 38.00),
 ('Etiquetas de vinil personalizadas 4×4 (100 un)', 2, 18.90),
 ('Cartões impressos (50 un)', 1, 25.00),
 ('Kit de envase: seringas, adaptador, funil, pipetas', 1, 40.00),
 ('Álcool 70%, luvas nitrílicas, papel toalha', 1, 20.00),
]
INSUMOS_TOTAL = round(sum(q * p for _, q, p in INSUMOS), 2)
PACK_STOCK0 = round(INSUMOS_TOTAL - 40 - 20, 2)  # material de embalagem consumível

BUDGETS = {
 1000: ['asad', 'yara', 'sabah'],
 1500: ['asad', 'yara', 'lveb'],
 2000: ['asad', 'yara', 'sabah', 'cdnim', 'lveb'],
 2500: ['yara', 'sabah', 'cdnim', 'lveb', '212'],
 3000: ['asad', 'yara', 'sabah', 'cdnim', 'lveb', '212', 'fakhar'],
}
OWN = ['p9pm', 'brun', 'sauv']

def portfolio(b):
    return BUDGETS[b] + OWN

def invest(b):
    perf = round(sum(SKUS[k]['preco'] for k in BUDGETS[b]), 2)
    return perf, INSUMOS_TOTAL, round(perf + INSUMOS_TOTAL, 2), round(b - perf - INSUMOS_TOTAL, 2)

PORT_V1 = ['asad', 'yara', 'sabah', 'p9pm', 'brun']  # portfólio da versão anterior (referência dos volumes)
W_REF = sum(SKUS[k]['w'] for k in PORT_V1)
ELAST = 0.3

STAGED = dict(start=['asad', 'yara', 'lveb'],
              stages=[(25, ['sabah', 'cdnim']), (60, ['212', 'fakhar'])],
              cap=3000.0)

def simulate(b, case, elasticity=None, price_mult=1.0, cost_mult=1.0, ship_sub=0.0, desc_heavy=False, loss=None, mkt_mult=1.0, staged=None):
    """b: orçamento (chave de BUDGETS) ou 'esc' para o plano escalonado."""
    global LOSS
    if elasticity is None: elasticity = ELAST
    old_loss = LOSS
    if loss is not None: LOSS = loss
    C = CASES[case]
    mix = dict(C['mix'])
    if desc_heavy:
        mix = {'desc': .50, 'trio': .20, 'duo5': .10, 'ml10': .12, 'dupla': .08}
    if b == 'esc':
        st = STAGED
        port = list(st['start']) + OWN
        perf0 = round(sum(SKUS[k]['preco'] for k in st['start']), 2)
        inv = round(perf0 + INSUMOS_TOTAL, 2)
        cash = 0.0           # o caixa do negócio começa zerado; o dono aporta só o necessário
        owner = inv
        pending = list(st['stages'])
        budget_ref = st['cap']
    else:
        port = portfolio(b)
        perf0, ins0, inv, cash = invest(b)
        owner = float(b)
        pending = []
        budget_ref = b
    stock = {k: (SKUS[k]['util0'] if SKUS[k]['proprio'] else SKUS[k]['ml']) for k in port}
    pack_stock = PACK_STOCK0
    rows = []
    bottles = {k: 0 for k in SKUS}
    sold_ml = {k: 0.0 for k in SKUS}
    last_ml = {k: 0.0 for k in SKUS}
    added = []
    cum_orders = 0.0
    tot = dict(orders=0, rev=0, cm=0, gross=0, mkt=0, op=0, hours=0, newc=0, bott=0, bott_cash=0, decants=0)
    for t in range(6):
        # etapas do plano escalonado: liberadas no início do mês seguinte ao gatilho
        while pending and cum_orders >= pending[0][0]:
            gate, new = pending.pop(0)
            costn = sum(SKUS[k]['preco'] * cost_mult for k in new)
            if cash - costn < CASH_MIN:
                top = min(budget_ref - owner, CASH_MIN + costn - cash)
                if top > 0:
                    cash += top; owner += top
            if cash - costn >= CASH_MIN - 1e-6:
                cash -= costn
                for k in new:
                    port.append(k); stock[k] = SKUS[k]['ml']
                added.append((MONTHS[t], gate, new, costn))
            else:
                pending.insert(0, (gate, new)); break
        avail = [k for k in port if stock[k] > 0.5]
        W = sum(SKUS[k]['w'] for k in avail)
        M = (W / W_REF) ** elasticity if W > 0 else 0
        O = C['orders'][t] * M
        share = {k: SKUS[k]['w'] / W for k in avail}
        ml_per_order = sum(mix[o] * SLOTS[o][0] * SLOTS[o][1] for o in OFFERS)
        need = {k: O * ml_per_order * share[k] / (1 - LOSS) for k in avail}
        for k in avail:
            s_ = SKUS[k]
            rule = s_.get('repor', 'sempre')
            while stock[k] < 1.5 * need[k]:
                ok = False
                if rule == 'sempre': ok = True
                elif rule == 'so_se_vender': ok = last_ml[k] >= 20
                elif rule == 'nao_tri1': ok = t >= 3 and last_ml[k] >= 20
                elif rule == 'se_caixa': ok = last_ml[k] >= 20
                if ok and cash - s_['preco'] * cost_mult >= CASH_MIN:
                    cash -= s_['preco'] * cost_mult; stock[k] += s_['ml']; bottles[k] += 1
                    tot['bott'] += 1; tot['bott_cash'] += s_['preco'] * cost_mult
                else:
                    break
        lost_frac = 0.0
        use = {}
        for k in avail:
            u = min(need[k], stock[k]); use[k] = u
            if need[k] > 0: lost_frac += share[k] * (1 - u / need[k]) * 0.5
        O_eff = O * (1 - lost_frac)
        e_add = {o: sum(share[k] * slot_price(o, SKUS[k]['tier']) for k in avail) for o in OFFERS}
        e_cml = sum(share[k] * SKUS[k]['cml'] for k in avail) * cost_mult
        rev = cm = gross = mins = decs = 0.0
        for o in OFFERS:
            n, ml = SLOTS[o]
            q = O_eff * mix[o]
            price = (offer_base(o) + n * e_add[o]) * price_mult
            perf = n * ml * e_cml / (1 - LOSS)
            vial = n * (VIAL[ml] + LABEL)
            br = BRINDE if HAS_BRINDE[o] else 0
            g = price - perf - vial - br - PACK
            c = g - price * (FEE + RES) - ship_sub
            rev += q * price; gross += q * g; cm += q * c
            mins += q * (n * MIN_DECANT + MIN_ORDER); decs += q * n
        for k in avail:
            stock[k] -= use[k]
            sold = use[k] * (1 - LOSS)
            sold_ml[k] += sold; last_ml[k] = sold
        pack_cost = sum(O_eff * mix[o] * (SLOTS[o][0] * (VIAL[SLOTS[o][1]] + LABEL) + PACK + (BRINDE * 0.6 if HAS_BRINDE[o] else 0)) for o in OFFERS)
        from_stock = min(pack_stock, pack_cost); pack_stock -= from_stock
        mkt = C['mkt'][t] * mkt_mult
        op = cm - FIXED - mkt
        newc = O_eff * (1 - C['rep'][t])
        cash += rev * (1 - FEE - RES) - (pack_cost - from_stock) - FIXED - mkt - O_eff * ship_sub
        cum_orders += O_eff
        rows.append(dict(m=MONTHS[t], orders=O_eff, newc=newc, rev=rev, cm=cm, gross=gross, mkt=mkt, cac=(mkt / newc if newc else 0), op=op, cash=cash, bott=sum(bottles.values()), hours=mins / 60, M=M, nsku=len(avail), owner=owner))
        for kk, v in [('orders', O_eff), ('rev', rev), ('cm', cm), ('gross', gross), ('mkt', mkt), ('op', op), ('hours', mins / 60), ('newc', newc), ('decants', decs)]:
            tot[kk] += v
    stock_val = sum(stock[k] * SKUS[k]['cml'] for k in stock if not (SKUS[k]['proprio'] and bottles[k] == 0)) + pack_stock
    tot.update(stock_end=stock_val, cash_end=cash, wc_end=cash + stock_val, econ=tot['op'] - tot['hours'] * HOUR,
               inv=inv, owner=owner, ticket=(tot['rev'] / tot['orders'] if tot['orders'] else 0),
               cmo=(tot['cm'] / tot['orders'] if tot['orders'] else 0), bottles=bottles, sold_ml=sold_ml, added=added,
               nsku_end=len([k for k in stock]))
    acc = 0; pb = None
    for i, r in enumerate(rows):
        acc += r['op']
        if pb is None and acc >= owner: pb = i + 1
    tot['payback'] = pb
    tot['q'] = {kk: sum(r[kk] for r in rows[:3]) for kk in ['orders', 'rev', 'cm', 'mkt', 'op', 'hours']}
    tot['q']['cash'] = rows[2]['cash']
    tot['q']['bott'] = rows[2]['bott']
    # participação da grife no volume vendido
    gml = sum(v for k, v in sold_ml.items() if SKUS[k]['linha'] == 'Grife'); aml = sum(sold_ml.values())
    tot['grife_share'] = gml / aml if aml else 0
    LOSS = old_loss
    return rows, tot

if __name__ == '__main__':
    print('INSUMOS', INSUMOS_TOTAL, 'CAPS', {t: round(c, 2) for t, c in CAP.items()})
    for b in list(BUDGETS) + ['esc']:
        for case in CASES:
            rows, t = simulate(b, case)
            print(f"{str(b):5s} {case:12s} ped={t['orders']:.0f} fat={t['rev']:.0f} ticket={t['ticket']:.2f} cm/ped={t['cmo']:.2f} op={t['op']:.0f} caixa={t['cash_end']:.0f} estoque={t['stock_end']:.0f} frascos={t['bott']} pb={t['payback']} dono={t['owner']:.0f} grife={t['grife_share']*100:.0f}% add={[(a[0],a[1]) for a in t['added']]}")
    for e in [0, 0.3, 0.5]:
        print('elasticidade', e, [round(simulate(b, 'Base', elasticity=e)[1]['op']) for b in list(BUDGETS) + ['esc']], [round(simulate(b, 'Conservador', elasticity=e)[1]['op']) for b in list(BUDGETS) + ['esc']])
