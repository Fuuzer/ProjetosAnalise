from hb import *
from sec_a import E_BASE, E_CON, E_OTI, E_ROWS, B, ST1, ST2, INV0, PERF0

MAR = E_ROWS[3]
CAC_MAR = MAR['cac']; FIX_SH = m.FIXED / MAR['orders']

def p14():
    h = '<h2>Precificação e kits</h2>'
    h += '<p class="lead">O preço passa a seguir o custo do perfume. Cada perfume pertence a uma faixa; os kits têm preço base para árabes e um adicional por perfume de faixa superior. Assim o cliente que escolhe grife paga a grife, e o que escolhe árabe não subsidia ninguém.</p>'
    h += '<h3>Faixas de preço</h3>'
    ex = {'A': 'Asad, Yara, Sabah Al Ward, Club de Nuit Intense Man, Fakhar Rose, Khamrah, Hawas, 9pm, Liquid Brun',
          'B': 'Sauvage EDT 200 ml, 212 VIP Men 200 ml, 1 Million 200 ml, Acqua di Giò 200 ml, Eros 200 ml',
          'C': 'La Vie Est Belle (refil 100 ml), Sauvage EDP 200 ml, Invictus 100 ml',
          'D': 'Bleu de Chanel EDP, Miss Dior Parfum, YSL Y EDP (só pré-venda)'}
    rows = []
    for t in m.TIERS:
        rows.append([m.TIER_NAME[t], f'até {brl(m.CAP[t])}', brl(m.P2ADD[t]), brl(m.P5[t]), brl(m.P10[t]),
                     ('—' if t == 'A' else '+' + brl(m.ADD_DESC[t])), ('—' if t == 'A' else '+' + brl(m.ADD_TRIO[t])), ('—' if t == 'A' else '+' + brl(m.ADD_DUPLA[t])), ex[t]])
    h += table(['Faixa', 'Custo do perfume por ml', '2 ml adicional', '5 ml', '10 ml', 'Adicional no Kit Descoberta (por 2 ml)', 'Adicional no Kit Trio (por 5 ml)', 'Adicional no Kit Dupla (por 10 ml)', 'Exemplos'], rows, align=['', 'r', 'r', 'r', 'r', 'r', 'r', 'r', ''], scroll=True, cls='wide')
    h += f'<p class="note">O teto de cada faixa é o maior custo por ml que ainda deixa 30% de margem no 5 ml. Grife começa na faixa B mesmo quando o custo cabe na A (ex.: Eros 200 ml a R$ 2,97 por ml), para não vender grife abaixo do valor de mercado. Acima de R$ 11,66 por ml (nicho, Bleu de Chanel Parfum), só pré-venda com preço calculado caso a caso {JU}.</p>'
    h += '<h3>Margem por faixa</h3>'
    rows = []
    for t in m.TIERS:
        c = N['wcml'][t]
        e = {ml: m.margin(p, m.decant_cost(ml, c)) for ml, p in [(5, m.P5[t]), (10, m.P10[t])]}
        e2 = m.margin(m.P2ADD[t], m.decant_cost(2, c))
        ecap = m.margin(m.P5[t], m.decant_cost(5, m.CAP[t]))
        rows.append([m.TIER_NAME[t], brl(c), f'{brl(e[5])} ({pct(e[5] / m.P5[t])})', f'{brl(e[10])} ({pct(e[10] / m.P10[t])})', f'{brl(e2)} ({pct(e2 / m.P2ADD[t])})', f'{brl(ecap)} ({pct(ecap / m.P5[t])})'])
    h += table(['Faixa', 'Custo por ml de referência', 'Margem 5 ml', 'Margem 10 ml', 'Margem 2 ml adicional', 'Margem 5 ml no teto da faixa'], rows, align=['', 'r', 'r', 'r', 'r', 'r'])
    h += '<p class="note">Custo de referência: média ponderada pela busca dos perfumes da faixa no portfólio (A: árabes; B: Sauvage EDT 200 ml e 212 VIP Men 200 ml; C: La Vie Est Belle; D: Bleu de Chanel EDP). Margem antes da embalagem do pedido e da mão de obra.</p>'
    h += '<h3>Por que o kit não pode ter preço fixo</h3>'
    def eco(keys, fixed):
        tl = [(SK[k]['tier'], SK[k]['cml']) for k in keys]
        e = m.offer_economics('trio', tl)
        if fixed:
            p = m.BASE['trio']
            cm = p - (e['perf'] + e['vials'] + e['labels'] + e['brinde'] + e['pack']) - p * (m.FEE + m.RES)
            return p, cm
        return e['price'], e['cm']
    rows = []
    for lab, keys in [('Asad, Yara, Sabah Al Ward', ['asad', 'yara', 'sabah']), ('Asad, Yara, Sauvage EDT', ['asad', 'yara', 'sauv']), ('Club de Nuit, Sauvage EDT, La Vie Est Belle', ['cdnim', 'sauv', 'lveb']), ('Sauvage EDT, 212 VIP Men, La Vie Est Belle', ['sauv', '212', 'lveb'])]:
        pf, cf = eco(keys, True); pv, cv = eco(keys, False)
        rows.append([lab, brl(pf), f'{brl(cf)} ({pct(cf / pf)})', brl(pv), f'{brl(cv)} ({pct(cv / pv)})'])
    h += table(['Kit Trio escolhido', 'Preço fixo', 'Margem com preço fixo', 'Preço por faixa', 'Margem com preço por faixa'], rows, align=['', 'r', 'r', 'r', 'r'])
    h += f'<p>Com preço fixo, o cliente racional escolhe os perfumes mais caros (seleção adversa) e o kit dá prejuízo. Com preço por faixa, a margem em reais fica estável e o cliente ainda paga menos que comprando os 5 ml avulsos (desconto de 7% a 14% no Trio, conforme a faixa, e de cerca de 8% na Dupla) {ES}.</p>'
    h += '<h3>Exemplos de kits com a regra nova</h3>'
    rows = []
    nm = {'desc': 'Kit Descoberta', 'trio': 'Kit Trio', 'dupla': 'Kit Dupla 10 ml'}
    for lab, o, keys, e in N['kit_ex']:
        e = m.offer_economics(o, [(SK[k]['tier'], SK[k]['cml']) for k in keys])
        comp = ' + '.join(f"{SK[k]['nome'].split(' ', 1)[1] if SK[k]['nome'].startswith(('Lattafa', 'Armaf', 'Afnan', 'Al Wataniah', 'French', 'Dior', 'Lancôme', 'Carolina', 'Rasasi')) else SK[k]['nome']} ({SK[k]['tier']})" for k in keys)
        rows.append([nm[o], comp, brl(e['price']), f'{brl(e["cm"])} ({pct(e["cm"] / e["price"])})'])
    h += table(['Kit', 'Composição (faixa)', 'Preço', 'Margem de contribuição'], rows, align=['', '', 'r', 'r'])
    h += '<p class="note">Como comunicar: "Kit Trio a partir de R$ 89,90. Perfumes de grife têm adicional: +R$ 12,90 (faixa B) e +R$ 34,90 (faixa C)." No WhatsApp, o atendente já informa o total ao montar o kit.</p>'
    h += '<h3>Custo completo, margem e pisos por oferta (faixa A)</h3>'
    cols = ['desc', 'trio', 'duo5', 'ml10', 'dupla']
    O = N['offA']
    def lucro(o): return O[o]['cm'] - O[o]['labor'] - CAC_MAR - FIX_SH
    def pmin(o):
        e = O[o]; vf = e['perf'] + e['vials'] + e['labels'] + e['brinde'] + e['pack']
        return vf / (1 - m.FEE - m.RES)
    def ppromo(o):
        e = O[o]; vf = e['perf'] + e['vials'] + e['labels'] + e['brinde'] + e['pack']
        return (vf + e['labor'] + CAC_MAR + FIX_SH) / (1 - m.FEE - m.RES)
    rws = [
        ['Preço de venda'] + [brl(O[o]['price']) for o in cols],
        ['Perfume (com perda de 5%)'] + [brl(O[o]['perf']) for o in cols],
        ['Frascos com spray'] + [brl(O[o]['vials']) for o in cols],
        ['Rótulo e lacre'] + [brl(O[o]['labels']) for o in cols],
        ['Brinde (1 ml do próximo perfume)'] + [brl(O[o]['brinde']) for o in cols],
        ['Caixa, envelope com bolha, cartão e proteção'] + [brl(O[o]['pack']) for o in cols],
        ['Taxa de pagamento (2,5%)'] + [brl(O[o]['fee']) for o in cols],
        ['Reserva para perdas, vazamentos e devoluções (3%)'] + [brl(O[o]['res']) for o in cols],
        ['Comissão de canal, imposto variável (MEI) e frete subsidiado'] + ['R$ 0,00'] * 5,
        ['<b>Margem de contribuição</b>'] + [f'<b>{brl(O[o]["cm"])}</b> ({pct(O[o]["cm"] / O[o]["price"], 1)})' for o in cols],
        ['Mão de obra (min × R$ 25/h)'] + [brl(O[o]['labor']) for o in cols],
        [f'CAC médio do cenário base em mar/27'] + [brl(CAC_MAR)] * 5,
        [f'Fixos rateados (R$ 112,05 ÷ {num(MAR["orders"])} pedidos)'] + [brl(FIX_SH)] * 5,
        ['<b>Lucro por pedido (após mão de obra, CAC e fixos)</b>'] + [f'<b>{brl(lucro(o))}</b>' for o in cols],
        ['Preço mínimo (margem de contribuição zero)'] + [brl(pmin(o)) for o in cols],
        ['Preço promocional mais baixo aceitável (lucro zero)'] + [brl(ppromo(o)) for o in cols],
        ['Desconto máximo sobre o preço cheio'] + [('nenhum' if ppromo(o) >= O[o]['price'] else pct(1 - ppromo(o) / O[o]['price'])) for o in cols],
        ['Papel no funil', 'Entrada: quem ainda não sabe o que quer', 'Carro-chefe e presente', 'Quem já sabe o que quer', 'Recompra do perfume que agradou', 'Recompra premium e presente'],
    ]
    h += table(['Componente', 'Kit Descoberta (5 × 2 ml)', 'Kit Trio (3 × 5 ml)', 'Dupla de 5 ml avulsos', '10 ml avulso', 'Kit Dupla 10 ml'], rws, align=['', 'r', 'r', 'r', 'r', 'r'], tot_rows=(9, 13), scroll=True)
    h += f'<p class="note">Perfume pelo custo médio da faixa A ponderado pela busca ({brl(N["wcml"]["A"])} por ml; era R$ 1,99 na versão 1, porque o Club de Nuit custa R$ 2,86). CAC e fixos valem para o plano escalonado, cenário base, em mar/27. Com grife, a margem em reais sobe (ver exemplos acima).</p>'
    h += '<h3>Preço por ml contra o mercado</h3>'
    pm = [
        ('3 fracionados de 5 ml no Mercado Livre', 60.0, 15, 'Piso do mercado, sem marca'),
        ('Kit 3 × 5 ml no Magalu', 89.24, 15, 'Concorrente direto em árabe'),
        ('Asad 5 ml no líder', 56.70, 5, 'Líder, árabe'),
        ('Sauvage EDT 5 ml no líder', 68.00, 5, 'Líder, grife'),
        ('Asad 2 ml na Tabs', 24.90, 2, 'Tabs, árabe'),
        ('Sauvage EDP 2 ml na Tabs', 34.90, 2, 'Tabs, grife'),
        ('<b>Kit Trio só árabes (este plano)</b>', 89.90, 15, 'Igual ao kit do Magalu, com brinde e curadoria'),
        ('<b>5 ml faixa A (este plano)</b>', m.P5['A'], 5, 'Abaixo do líder em 38%'),
        ('<b>5 ml faixa B (este plano)</b>', m.P5['B'], 5, 'Sauvage EDT 27% abaixo do líder'),
        ('<b>5 ml faixa C (este plano)</b>', m.P5['C'], 5, 'La Vie Est Belle 19% abaixo do líder'),
        ('<b>10 ml faixa A (este plano)</b>', m.P10['A'], 10, 'Premia a recompra'),
        ('<b>Kit Descoberta só árabes (este plano)</b>', 69.90, 10, 'Abaixo do 2 ml da Tabs'),
    ]
    h += table(['Oferta', 'Preço', 'R$ por ml', 'Referência'], [[a_, brl(p), brl(p / ml), r] for a_, p, ml, r in pm], align=['', 'r', 'r', ''])
    h += '<h3>Mesmo Kit Trio (só árabes) em outros canais</h3>'
    cm = O['trio']['cm']; P = O['trio']['price']
    ch = [('Canal próprio', '2,5% de pagamento', cm), ('Amazon', '12% + R$ 2 por item ' + ES, cm + 0.025 * P - (0.12 * P + 2)), ('Mercado Livre (clássico)', '12% + R$ 6,75 ' + ES, cm + 0.025 * P - (0.12 * P + 6.75)), ('Shopee', '20% + R$ 4,50', cm + 0.025 * P - (0.20 * P + 4.50))]
    h += table(['Canal', 'Tarifa considerada', 'Margem de contribuição'], [[c, t, brl(v)] for c, t, v in ch], align=['', '', 'r'])
    h += '<p class="note">Além da tarifa, o Mercado Livre exige número de notificação ou registro na Anvisa em anúncios de perfume, que o decant não tem. Marketplace fica fora da fase 1.</p>'
    h += '<h3>Regras de preço</h3><ul>'
    h += '<li>Preço por faixa, igual para todos os perfumes da faixa (simplifica a escolha). Um perfume muda de faixa se o custo de reposição passar do teto.</li>'
    h += '<li>Nunca cobrar acima do líder no mesmo tamanho; se a faixa ficar acima, o perfume não entra (ex.: Invictus 100 ml).</li>'
    h += '<li>Revisar se o custo do frasco subir mais de 10% ou se a margem média ficar abaixo de R$ 30 por pedido por 2 meses.</li>'
    h += f'<li>Desconto só em data do calendário e nunca abaixo do piso: Trio a {brl(ppromo("trio"))}, Dupla 10 ml a {brl(ppromo("dupla"))}, 10 ml a {brl(ppromo("ml10"))}. Kit Descoberta não tem desconto.</li>'
    h += '<li>Fim de frasco "até a última gota": 20% abaixo do preço por ml da faixa, só para o que sobrar abaixo de 30 ml.</li>'
    h += '<li>Frete grátis só acima de R$ 149 ou na retirada em Porto Alegre. Parcelamento em 3x sem juros só acima de R$ 150.</li></ul>'
    h += '<h3>Ponto de equilíbrio e retorno</h3>'
    t = E_BASE; tc = E_CON
    rows = [
        ['Ponto de equilíbrio sem marketing', f'{num(N["be_nomkt"], 1)} pedidos por mês', f'R$ 112,05 ÷ {brl(N["cmo"])}'],
        ['Ponto de equilíbrio com R$ 200 de marketing', f'{num(N["be_200"], 1)} pedidos por mês', f'(R$ 112,05 + R$ 200) ÷ {brl(N["cmo"])}'],
        ['Retorno sobre o capital do dono em 90 dias (base)', pct(t['q']['op'] / t['owner']), f'{brl(t["q"]["op"])} ÷ {brl(t["owner"])}'],
        ['Retorno sobre o capital do dono em 6 meses (base)', pct(t['op'] / t['owner']), f'{brl(t["op"])} ÷ {brl(t["owner"])}'],
        ['Retorno em 6 meses (conservador)', pct(tc['op'] / tc['owner']), f'{brl(tc["op"])} ÷ {brl(tc["owner"])}'],
    ]
    h += table(['Indicador', 'Valor', 'Conta'], rows)
    h += src(a(URL['ps_api'], 'Perfume Shopping, preços'), a(URL['tabs_busca'], 'Tabs, preços'), a('https://lista.mercadolivre.com.br/Asad%20Asad%20Attar%20Roll%20On', 'Mercado Livre, combos'), a('https://www.magazineluiza.com.br/busca/perfume+decant', 'Magalu, kit'), a('https://viniensina.com.br/?p=4707', 'tarifas do Mercado Livre 2026'), a('https://viniensina.com.br/?p=4619', 'tarifas da Shopee'), a('https://upseller.com/pt/blog-article-929', 'tarifas da Amazon'), a('https://global-selling.mercadolibre.com/help/1072', 'regra de anúncio de perfume no Mercado Livre'))
    return h

def alt_run(port):
    import math
    inv0 = round(sum(SK[x]['preco'] for x in port) + m.INSUMOS_TOTAL, 2)
    k = math.ceil(inv0 / 500) * 500 + 0.001  # orçamento nominal da faixa (reserva igual à dos cenários)
    m.BUDGETS[k] = port
    perf, ins, inv, res = m.invest(k)
    out = {}
    for e in [0, 0.3]:
        for case in ['Conservador', 'Base']:
            out[(e, case)] = m.simulate(k, case, elasticity=e)[1]['op']
    del m.BUDGETS[k]
    return inv, out

def p15():
    h = '<h2>Cenários de investimento: R$ 1.000 a R$ 3.000</h2>'
    h += f'<p class="lead">Testei 5 orçamentos em 3 níveis de demanda e 3 hipóteses sobre quanto um catálogo maior atrai de pedidos. A conclusão não é "quanto mais, melhor": o que aumenta o resultado é <b>incluir grife</b>. O plano recomendado é escalonado: {brl(INV0)} agora, até R$ 3.000 por etapas.</p>'
    h += '<h3>O que cada orçamento compra</h3>'
    rows = []
    for b, d in B.items():
        comp = ', '.join(SK[k]['nome'].replace('Al Wataniah ', '').replace('Lattafa ', '').replace('Armaf ', '').replace('Lancôme ', '').replace('Carolina Herrera ', '') for k in m.BUDGETS[b])
        rows.append([f'<b>R$&nbsp;{num(b)}</b>', comp, str(d['nsku']), str(d['ngrife']), brl(d['perf']), brl(d['ins']), brl(d['inv']), brl(d['res']), num(d['M'], 2) + '×'])
    h += table(['Orçamento', 'Perfumes comprados', 'Perfumes no total (com 9pm, Liquid Brun e Sauvage próprios)', 'Grifes', 'Perfume', 'Insumos', 'Total investido', 'Reserva', 'Efeito do catálogo nos pedidos'], rows, align=['', '', 'c', 'c', 'r', 'r', 'r', 'r', 'c'], scroll=True, cls='wide')
    h += f'<p class="note">Em R$ 2.500 o Asad sai para caber o 212 VIP Men com reserva acima de R$ 150; o Club de Nuit cobre o masculino árabe. "Efeito do catálogo" = (peso de busca do catálogo ÷ peso do catálogo da versão 1)<sup>0,3</sup>, enquanto todos os perfumes estão em estoque {HI}.</p>'
    h += '<h3>Resultado em 6 meses por orçamento</h3>'
    rows = []
    for b, d in B.items():
        rc = d['res_cases']
        tb = rc['Base'][1]
        rows.append([f'<b>R$&nbsp;{num(b)}</b>', ' / '.join(num(rc[c][1]['orders']) for c in ['Conservador', 'Base', 'Otimista']), brl(tb['ticket']), brl(rc['Conservador'][1]['op']), brl(tb['op']), brl(rc['Otimista'][1]['op']), brl(tb['cash_end']), (f'mês {tb["payback"]}' if tb['payback'] else 'após 6 meses'), (f'mês {rc["Conservador"][1]["payback"]}' if rc['Conservador'][1]['payback'] else 'após 6 meses'), pct(tb['grife_share'])])
    tb = E_BASE
    rows.append(['<b>Escalonado (recomendado)</b>', ' / '.join(num(N['esc'][c][1]['orders']) for c in ['Conservador', 'Base', 'Otimista']), brl(tb['ticket']), brl(E_CON['op']), brl(tb['op']), brl(E_OTI['op']), brl(tb['cash_end']), (f'mês {tb["payback"]}' if tb['payback'] else 'após 6 meses'), (f'mês {E_CON["payback"]}' if E_CON['payback'] else 'após 6 meses'), pct(tb['grife_share'])])
    h += table(['Orçamento', 'Pedidos (cons. / base / otim.)', 'Ticket médio (base)', 'Lucro conservador', 'Lucro base', 'Lucro otimista', 'Caixa final (base)', 'Payback (base)', 'Payback (conservador)', 'Grife no volume vendido (base)'], rows, align=['', 'c', 'r', 'r', 'r', 'r', 'r', 'c', 'c', 'c'], tot_rows=(5,), scroll=True, cls='wide')
    h += '<p class="note">Lucro = lucro operacional (margem de contribuição − fixos − marketing). Payback = mês em que o lucro acumulado cobre o capital do dono. No escalonado, o capital do dono é ' + brl(INV0) + '; as etapas 2 e 3 saem do caixa do negócio.</p>'
    h += '<h3>E se um catálogo maior não trouxer mais pedidos?</h3>'
    rows = []
    for b, d in B.items():
        s = d['sens']
        rows.append([f'R$&nbsp;{num(b)}'] + [brl(s[e][1]['op']) + ' / ' + brl(s[e][0]['op']) for e in [0, 0.3, 0.5]])
    s = N['esc_sens_e']
    rows.append(['<b>Escalonado</b>'] + [brl(s[e][1]['op']) + ' / ' + brl(s[e][0]['op']) for e in [0, 0.3, 0.5]])
    h += table(['Orçamento', 'Elasticidade 0: catálogo não atrai (cons. / base)', 'Elasticidade 0,3: premissa do plano', 'Elasticidade 0,5: catálogo atrai muito'], rows, align=['', 'r', 'r', 'r'], tot_rows=(5,))
    h += (f'<p>Se o catálogo não atrair pedido nenhum (elasticidade 0), o melhor orçamento é o de R$ 1.500 com La Vie Est Belle: a grife sobe o ticket mesmo sem pedido a mais. Nesse caso, as etapas 2 e 3 não deveriam acontecer, e por isso os gatilhos exigem pedidos e pedidos dos perfumes novos, não só tempo {JU}.</p>')
    h += '<h3>A composição pesa mais que o valor</h3>'
    alts = [
        ('R$ 1.500 só com árabes (Asad, Yara, Sabah, Club de Nuit, Fakhar Rose)', ['asad', 'yara', 'sabah', 'cdnim', 'fakhar']),
        ('R$ 1.500 com 1 grife (Asad, Yara, La Vie Est Belle)', ['asad', 'yara', 'lveb']),
        ('R$ 2.000 com 212 VIP Men no lugar de La Vie Est Belle', ['asad', 'yara', 'sabah', 'cdnim', '212']),
        ('R$ 2.500 com Fakhar Rose e Hawas, sem 212 VIP', ['asad', 'yara', 'sabah', 'cdnim', 'lveb', 'fakhar', 'hawas']),
    ]
    rows = []
    for lab, port in alts:
        inv, out = alt_run(port)
        rows.append([lab, brl(inv), brl(out[(0.3, 'Conservador')]), brl(out[(0.3, 'Base')]), brl(out[(0, 'Base')])])
    h += table(['Alternativa', 'Investimento', 'Lucro conservador', 'Lucro base', 'Lucro base sem efeito do catálogo'], rows, align=['', 'r', 'r', 'r', 'r'])
    h += '<p class="note">Cada alternativa parte do mesmo orçamento nominal da linha (R$ 1.500, R$ 2.000 ou R$ 2.500): o que não vai para perfume e insumos fica em caixa.</p>'
    h += '<p class="note">Com o mesmo dinheiro, trocar dois árabes por uma grife rende mais em todos os casos. Mais árabes acrescentam variedade, mas dividem a mesma demanda e têm custo por ml maior que o Asad e o Yara (Club de Nuit a R$ 2,86).</p>'
    h += '<h3>Análise marginal: o que cada R$ a mais compra</h3>'
    rows = []
    base0 = B[1000]
    for b in [1500, 2000, 2500, 3000]:
        d = B[b]
        dcap = d['inv'] - base0['inv']
        db = d['res_cases']['Base'][1]['op'] - base0['res_cases']['Base'][1]['op']
        dc = d['res_cases']['Conservador'][1]['op'] - base0['res_cases']['Conservador'][1]['op']
        rows.append([f'De R$ 1.000 para R$ {num(b)}', brl(dcap), brl(db, sign=True), brl(dc, sign=True), pct(db / dcap), pct(dc / dcap)])
    h += table(['Passo', 'Capital a mais', 'Lucro a mais (base)', 'Lucro a mais (conservador)', 'Retorno marginal (base)', 'Retorno marginal (conservador)'], rows, align=['', 'r', 'r', 'r', 'r', 'r'])
    h += '<h3>Recomendação: plano escalonado com teto de R$ 3.000</h3>'
    rows = [
        ['1. Largada', f'Insumos ({brl(m.INSUMOS_TOTAL)}) + Asad, Yara e La Vie Est Belle ({brl(PERF0)})', brl(INV0), 'Insumos já; perfumes após o retorno preliminar do advogado e 30 pessoas na lista ou 5 pedidos pagos', 'Seu capital', 'Operar com 9pm, Liquid Brun e Sauvage próprios'],
        ['2. Árabes de giro', 'Sabah Al Ward e Club de Nuit Intense Man', brl(ST1), '25 pedidos acumulados, margem média de R$ 30 ou mais e pelo menos 5 pedidos ou pedidos de clientes por esses perfumes', 'Caixa do negócio', 'Esperar; vender o fim dos frascos'],
        ['3. Grife masculina e feminino árabe', '212 VIP Men 200 ml e Fakhar Rose', brl(ST2), '60 pedidos acumulados, grife com 25% ou mais do volume vendido e caixa acima de R$ 150 depois da compra', 'Caixa do negócio; aporte só se a meta bater e o caixa não cobrir', 'Parar na etapa 2'],
        ['Reposição do Sauvage', 'Sauvage EDT 200 ml', brl(SK['sauv']['preco']), 'Frasco próprio acabou, venda de 20 ml ou mais no mês e caixa acima de R$ 1.152,51', 'Caixa do negócio', 'Ficar sem Sauvage; oferecer 212 VIP e Club de Nuit'],
        ['Teto', '—', 'R$ 3.000,00', 'Soma de capital do dono e aportes', '—', '—'],
    ]
    h += table(['Etapa', 'O que compra', 'Valor', 'Gatilho', 'De onde vem o dinheiro', 'Se o gatilho não vier'], rows, align=['', '', 'r', '', '', ''], scroll=True, cls='wide')
    h += '<h3>Critérios da escolha</h3>'
    h += table(['Critério', 'R$ 1.000', 'R$ 1.500 (com grife)', 'R$ 3.000 de uma vez', 'Escalonado'], [
        ['Capital exposto antes de provar demanda', brl(B[1000]['inv']), brl(B[1500]['inv']), brl(B[3000]['inv']), brl(INV0)],
        ['Lucro em 6 meses, base', brl(B[1000]['res_cases']['Base'][1]['op']), brl(B[1500]['res_cases']['Base'][1]['op']), brl(B[3000]['res_cases']['Base'][1]['op']), brl(E_BASE['op'])],
        ['Lucro em 6 meses, conservador', brl(B[1000]['res_cases']['Conservador'][1]['op']), brl(B[1500]['res_cases']['Conservador'][1]['op']), brl(B[3000]['res_cases']['Conservador'][1]['op']), brl(E_CON['op'])],
        ['Perfumes na prateleira', '6', '6', '10', '6 → 10'],
        ['Grife', 'Só o Sauvage próprio', 'Sauvage + La Vie Est Belle', '3', '2 → 3'],
        ['Estoque parado se a demanda não vier', 'Baixo', 'Médio', 'Alto', 'Médio'],
    ], align=['', 'r', 'r', 'r', 'r'])
    h += f'<div class="box ok"><b>Escolha: escalonado.</b> Tem quase o lucro do R$ 3.000 no cenário base com menos da metade do capital exposto, e no cenário conservador fica no nível do R$ 1.500. A diferença entre os dois só aparece se a demanda responder, e é exatamente isso que os gatilhos medem {JU}.</div>'
    h += '<h3>O que não comprar agora</h3><ul>'
    h += '<li>Nicho original (Aventus R$ 3.320,84, Delina R$ 3.635, Baccarat Rouge R$ 4.064,10) e faixa D para estoque (Bleu de Chanel EDP R$ 1.149).</li>'
    h += '<li>Grife em frasco de 100 ml quando houver o de 200 ml; mais de 1 frasco do mesmo perfume antes de vender 60 ml dele.</li>'
    h += '<li>Caixa personalizada com logo (pedido mínimo de 500 a 2.000 peças); frascos de 30 ml, de plástico ou porta-perfume de bolso.</li>'
    h += '<li>Site pago, domínio, ferramentas de automação e anúncios antes de 10 vendas orgânicas; balança de precisão, seladora e impressora térmica antes de 40 pedidos por mês.</li></ul>'
    h += src('modelo em Python deste plano', a(URL['epoca_api'], 'preços de frasco (Época)'), a(URL['trends_rank'], 'pesos de busca (Google Trends)'))
    return h
