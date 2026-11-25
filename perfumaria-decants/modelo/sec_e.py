from hb import *
from sec_a import E_BASE, E_CON, E_OTI, E_ROWS, B, ST1, ST2, INV0, PERF0
from sec_d import strip_pn, R, RR

CASES = ['Conservador', 'Base', 'Otimista']
ESC = N['esc']

def p22():
    h = '<h2>Projeções financeiras</h2>'
    h += f'<p class="lead">Plano escalonado, 3 cenários de demanda. Em todos, o caixa do negócio termina o semestre positivo e o capital do dono fica em {brl(INV0)} nos três, porque as etapas saem do caixa gerado. O que separa os cenários é volume, que só a operação real vai mostrar.</p>'
    h += '<h3>Premissas por cenário</h3>'
    C = m.CASES
    rows = [
        ['Pedidos por mês com o catálogo da versão 1 (dez a mai)'] + [', '.join(str(x) for x in C[c]['orders']) for c in CASES],
        ['Efeito do catálogo (elasticidade 0,3)'] + ['de ' + num(min(r['M'] for r in ESC[c][0]), 2) + '× a ' + num(max(r['M'] for r in ESC[c][0]), 2) + '×' for c in CASES],
        ['Pedidos de quem já comprou'] + ['0% a ' + pct(max(C[c]['rep'])) for c in CASES],
        ['Marketing pago por mês'] + ['R$ 0,00 a ' + brl(max(C[c]['mkt'])) for c in CASES],
        ['Mix (Descoberta / Trio / 2 × 5 ml / 10 ml / Dupla 10 ml)'] + [' / '.join(str(int(C[c]['mix'][o] * 100)) for o in m.OFFERS) for c in CASES],
        ['Etapas liberadas'] + ['; '.join(f'{x[2][0] and SK[x[2][0]]["nome"].split(" ", 1)[1].split(" ")[0]}… em {x[0]}' for x in ESC[c][1]['added']) or 'nenhuma' for c in CASES],
        ['Ticket médio'] + [brl(ESC[c][1]['ticket']) for c in CASES],
        ['Margem de contribuição por pedido'] + [f'{brl(ESC[c][1]["cmo"])} ({pct(ESC[c][1]["cmo"] / ESC[c][1]["ticket"], 1)})' for c in CASES],
    ]
    rows[5] = ['Etapas liberadas'] + [('; '.join(('etapa 2' if g == 25 else 'etapa 3') + ' em ' + mm for mm, g, ks, cst in ESC[c][1]['added']) or 'nenhuma') for c in CASES]
    h += table(['Premissa', 'Conservador', 'Base', 'Otimista'], rows)
    h += f'<p class="note">Volumes são {HI}. Comuns aos três: frete pago pelo cliente, frascos próprios com 40 ml úteis, reposição quando o estoque não cobre 1,5 mês e o caixa fica acima de R$ 150, preço por faixa.</p>'
    h += '<h3>90 dias e 6 meses</h3>'
    hd = ['Indicador'] + [f'{c}<br>{p}' for c in CASES for p in ['90 dias', '6 meses']]
    def two(f):
        out = []
        for c in CASES:
            r, t = ESC[c]
            out += f(r, t)
        return out
    rows = [
        ['Capital do dono'] + two(lambda r, t: [brl(r[2]['owner']), brl(t['owner'])]),
        ['Pedidos no período'] + two(lambda r, t: [num(t['q']['orders']), num(t['orders'])]),
        ['Faturamento'] + two(lambda r, t: [brl(t['q']['rev']), brl(t['rev'])]),
        ['Margem de contribuição'] + two(lambda r, t: [brl(t['q']['cm']), brl(t['cm'])]),
        ['Marketing pago'] + two(lambda r, t: [brl(t['q']['mkt']), brl(t['mkt'])]),
        ['Lucro operacional (− fixos − marketing)'] + two(lambda r, t: [brl(t['q']['op']), brl(t['op'])]),
        ['Horas de operação'] + two(lambda r, t: [num(t['q']['hours'], 1), num(t['hours'], 1)]),
        ['Lucro econômico (− horas a R$ 25)'] + two(lambda r, t: [brl(t['q']['op'] - t['q']['hours'] * 25), brl(t['econ'])]),
        ['Frascos de perfume recomprados'] + two(lambda r, t: [str(t['q']['bott']), str(t['bott'])]),
        ['Estoque final (perfume + embalagem, a custo)'] + two(lambda r, t: ['—', brl(t['stock_end'])]),
        ['Caixa do negócio ao fim'] + two(lambda r, t: [brl(t['q']['cash']), brl(t['cash_end'])]),
    ]
    h += table(hd, rows, align=['', 'r', 'r', 'r', 'r', 'r', 'r'], scroll=True)
    pb = ' · '.join(f'{c}: ' + (f'mês {ESC[c][1]["payback"]}' if ESC[c][1]['payback'] else 'após 6 meses') for c in CASES)
    h += f'<p class="note">Payback (lucro operacional acumulado ≥ capital do dono): {pb}. O caixa já desconta as compras das etapas 2 e 3 e a recompra de frascos; os frascos próprios entram no lucro pelo custo de reposição, sem saída de caixa.</p>'
    h += '<h3>Mês a mês</h3>'
    hd = ['Mês', 'Perfumes ativos', 'Pedidos', 'Novos clientes', 'Faturamento', 'Margem de contribuição', 'Marketing', 'CAC', 'Lucro operacional', 'Frascos recomprados (acum.)', 'Caixa ao fim do mês']
    rows = []; grp = []
    for c in CASES:
        grp.append(len(rows))
        rows.append([f'<b>{c}</b>'] + [''] * 10)
        for r in ESC[c][0]:
            rows.append([r['m'], str(r['nsku']), num(r['orders'], 1), num(r['newc'], 1), brl(r['rev']), brl(r['cm']), brl(r['mkt']), brl(r['cac']), brl(r['op']), str(r['bott']), brl(r['cash'])])
    t = table(hd, rows, align=['', 'c', 'c', 'c', 'r', 'r', 'r', 'r', 'r', 'c', 'r'], scroll=True)
    for gi in grp:
        t = t.replace(f'<tr><td><b>{rows[gi][0][3:-4]}</b></td>' + '<td></td>' * 10 + '</tr>', f'<tr class="grp"><td colspan="11"><b>{rows[gi][0][3:-4]}</b></td></tr>')
    h += t
    h += '<p class="note">"Perfumes ativos" cai quando um frasco próprio acaba (9pm, Liquid Brun ou Sauvage) e sobe quando uma etapa é liberada.</p>'
    h += '<h3>Sensibilidades (cenário base)</h3>'
    s0 = N['sens'][0]
    rows = [[s['label'], brl(s['cmo']), brl(s['op_mar']), brl(s['op_mar'] - s0['op_mar'], sign=(s['op_mar'] - s0['op_mar'] > 0)), brl(s['op6']), brl(s['cash']), brl(s['owner'])] for s in N['sens']]
    h += table(['Teste', 'Margem por pedido', 'Lucro operacional em mar/27', 'Variação contra o base', 'Lucro operacional em 6 meses', 'Caixa final', 'Capital do dono'], rows, align=['', 'r', 'r', 'r', 'r', 'r', 'r'], scroll=True)
    worst = N['sens'][-1]
    h += '<ul>'
    h += f'<li><b>O que mais pesa:</b> frete grátis (lucro de 6 meses cai para {brl(N["sens"][4]["op6"])}) e preço 10% menor ({brl(N["sens"][1]["op6"])}). Perda no envase pesa pouco.</li>'
    h += f'<li><b>Se o catálogo não atrair mais pedidos</b>, o lucro de 6 meses cai para {brl(N["sens"][8]["op6"])}, ainda positivo; nesse caso as etapas 2 e 3 não se pagam e os gatilhos devem segurá-las.</li>'
    h += f'<li><b>O que quebra o modelo:</b> preço menor, perfume mais caro e frete grátis juntos. O lucro de 6 meses fica em {brl(worst["op6"])} e o dono precisa aportar {brl(worst["owner"] - INV0)} a mais para as etapas; o caixa fecha em {brl(worst["cash"])}.</li></ul>'
    h += '<h3>Estoque girando em 30, 60 e 90 dias (ritmo de mar/27, base)</h3>'
    rows = [[f'{d} dias', f'{num(ml)} ml', num(fr, 1), brl(cap)] for d, ml, fr, cap in N['stock_cov']]
    h += table(['Cobertura de estoque', 'Perfume em estoque', 'Frascos de 100 ml equivalentes', 'Capital preso em perfume'], rows, align=['', 'c', 'c', 'r'])
    h += f'<p class="note">No ritmo de {num(N["orders_mar"])} pedidos por mês, com custo médio de {brl(N["cml_avg_mar"])} por ml (a grife sobe a média). Com 9 perfumes, cada um precisa de pelo menos um frasco aberto; a regra de 30 dias vale por perfume, não pelo total.</p>'
    h += '<div class="src"><b>Fonte:</b> modelo em Python deste plano, com as premissas da aba Metodologia.</div>'
    return h

def p23():
    o = strip_pn(ORIG['p20'])
    o = R(o, '<td>Reserva de R$ 176,85; compras dentro do giro</td>', '<td>Caixa mínimo de R$ 150; etapas só com gatilho; compras dentro do giro</td>')
    new = ''.join([
        '<tr><td>Capital parado em grife ' + NOVO + '</td><td>Média</td><td>Alto</td><td>Frasco de grife com menos de 20 ml vendidos em 30 dias</td><td>Frasco de 200 ml só na etapa 3 e com 25% de grife no volume; La Vie Est Belle como teste</td><td>Vender por ml no "até a última gota"; não recomprar</td><td>Compras</td><td>Mensal</td></tr>',
        '<tr><td>Notificação de marca por uso de nome do original ' + NOVO + '</td><td>Média</td><td>Alto</td><td>Notificação extrajudicial; denúncia na plataforma</td><td>Nome do clone em título e anúncio; comparação só orgânica e aprovada</td><td>Remover o conteúdo; resposta pelo advogado</td><td>Jurídico</td><td>A cada conteúdo de clone</td></tr>',
        '<tr><td>Pré-venda que não fecha ' + NOVO + '</td><td>Média</td><td>Médio</td><td>Menos de 50% do frasco vendido em 10 dias</td><td>Termos claros; só 1 pré-venda por vez</td><td>Reembolso integral em 2 dias úteis</td><td>Financeiro</td><td>A cada pré-venda</td></tr>',
        '<tr><td>Preço do líder cair abaixo da faixa ' + NOVO + '</td><td>Média</td><td>Médio</td><td>Líder vende o mesmo 5 ml abaixo do nosso preço</td><td>Monitorar mensalmente os 10 perfumes do portfólio no líder e na Tabs</td><td>Trocar o perfume por outro da fila</td><td>Financeiro</td><td>Mensal</td></tr>',
        '<tr><td>Estourar o teto do MEI ' + NOVO + '</td><td>Baixa (só no otimista)</td><td>Médio</td><td>Receita acima de R$ 6.750 por mês por 2 meses</td><td>Acompanhar a receita acumulada do ano</td><td>Migrar para ME no Simples com o contador</td><td>Financeiro</td><td>Mensal</td></tr>',
        '<tr><td>Modismo de árabe viral ' + NOVO + '</td><td>Alta</td><td>Médio</td><td>Busca do perfume cai 2 trimestres seguidos (ex.: Asad caiu 64% no RS)</td><td>1 frasco por vez; lote do mês</td><td>Fim de frasco por ml; não recomprar</td><td>Marketing</td><td>Mensal</td></tr>',
    ])
    o = R(o, '<tr><td>Margem calculada errada</td>', new + '<tr><td>Margem calculada errada</td>')
    o = R(o, '<td>Combos abaixo de R$ 20 por 5 ml; concorrente local</td><td>Competir por kit, curadoria e confiança</td>', '<td>Combos abaixo de R$ 20 por 5 ml; concorrente local; cupons do líder</td><td>Competir por kit, curadoria, confiança e preço por faixa abaixo do líder</td>')
    return '<h2>Riscos</h2>' + o.replace('<h2>Riscos</h2>', '')

def p24():
    h = '<h2>Plano de ação</h2>'
    rows = []
    def g(t): rows.append(('grp', t))
    def r(*x): rows.append(('row', x))
    g('48 horas (até 27/11/2026)')
    r('26/11', 'Medir o volume restante dos 4 frascos próprios (9pm, Liquid Brun, Sauvage EDT, Bleu de Chanel Parfum)', 'Seringa graduada ou proveta; anotar em ml', 'R$ 0', 'Nenhuma', 'Saber quanto dá para vender sem comprar', 'ml por frasco', '40 ml ou mais em 9pm, Liquid Brun e Sauvage')
    r('26/11', 'Enviar as perguntas ao advogado (12) e ao contador (7)', 'E-mail com as listas da aba Jurídico', 'Honorários a combinar', 'Nenhuma', 'Retorno preliminar', 'Dias até a resposta', 'Resposta em até 7 dias')
    r('26/11', 'Checar o nome Gota Rara', 'Busca de @ no Instagram e TikTok, registro.br, INPI (classes 3 e 35)', 'R$ 0', 'Nenhuma', 'Nome confirmado ou troca', 'Disponibilidade', '@ e domínio livres; sem marca igual na classe 3')
    r('27/11', 'Comprar os insumos da etapa 1', 'Carrinhos no Mercado Livre, Magalu e Shopee; cotar caixa em pacote de 20', brl(m.INSUMOS_TOTAL), 'Medição dos frascos', 'Insumos em casa até 03/12', 'Pedidos feitos', 'Entrega em até 7 dias')
    r('27/11', 'Black Friday: só cotar La Vie Est Belle, Asad e Yara', 'Salvar preço e loja; comprar só se o advogado já tiver respondido', 'R$ 0', 'Parecer', 'Referência de preço', 'Preço por ml', 'La Vie Est Belle abaixo de R$ 6,55 por ml')
    r('27/11', 'Criar perfil e WhatsApp Business', 'Bio, catálogo por faixa, mensagem automática, tabela de kits "a partir de"', 'R$ 0', 'Nome', 'Canais prontos', 'Perfil publicado', '3 posts fixados')
    g('1 semana (até 02/12/2026)')
    r('30/11', 'Abrir o MEI', 'Portal do Empreendedor, CNAE 4772-5/00', 'R$ 82,05 por mês', 'Resposta do contador sobre o CNAE', 'CNPJ ativo', 'CNPJ', 'Antes da 1ª venda')
    r('02/12', 'Aceite de transporte', 'Escrever para 2 transportadoras com a descrição do produto', 'R$ 0', 'Nenhuma', 'Envio nacional liberado', 'Respostas escritas', 'Pelo menos 1 aceite')
    r('02/12', 'Tabela de distribuidor', 'Rebaj (Lattafa), BIM (Al Wataniah, Armaf), BR Brand Import', 'R$ 0', 'CNPJ', 'Custo de reposição menor', 'R$ por ml', '10% abaixo do varejo')
    r('02/12', 'Envase piloto', '10 decants de 9pm, Liquid Brun e Sauvage, cronometrados', 'Insumos já comprados', 'Insumos', 'Tempo e perda reais', 'Min por decant; perda', 'Até 4 min e até 5%')
    r('02/12', 'Lista de espera', 'Conteúdos dos dias 1 e 2 e aviso aos contatos próximos', 'R$ 0', 'Perfil', 'Demanda inicial', 'Inscritos', '30 pessoas')
    r('02/12', 'Comprar os perfumes da etapa 1', 'Asad, Yara e La Vie Est Belle (refil 100 ml), com nota', brl(PERF0), 'Retorno do advogado + 30 na lista ou 5 pedidos', 'Portfólio de largada completo', 'Frascos recebidos', 'Chegada até 09/12')
    g('30 dias (até 25/12/2026)')
    r('01 a 30/12', 'Calendário de conteúdo', 'Aba Marketing', 'R$ 0', 'Perfil', 'Audiência e confiança', 'Publicações', '25 de 30 feitas')
    r('07/12', 'Políticas, fichas de lote e tabela de faixas nos destaques', 'Textos da aba Operação', 'R$ 0', 'Fichas', 'Objeção de origem e de preço respondidas', 'Destaques', 'Publicado')
    r('10/12', 'Liberar 10 ml e Kit Dupla', 'Comprar 50 frascos de 10 ml e 100 de 1 ml com a receita', 'R$ 196,91', '5 pedidos pagos', 'Escada de recompra completa', 'Pedidos de 10 ml', 'Primeiro 10 ml vendido')
    r('até 23/12', 'Vendas de Natal', 'Lista VIP, Instagram, entrega local', 'R$ 0', 'Perfumes', 'Primeiras vendas', 'Pedidos', '12 ou mais')
    r('20/12', '1 parceiro local com tester', 'Barbearia ou estúdio; comissão de 10% a 15%', 'Frascos de teste', 'Perfumes', 'Canal presencial', 'Pedidos do parceiro', '2 pedidos em 30 dias')
    g('60 dias (até 24/01/2027)')
    r('21/12', '1ª live de frasco aberto', 'Abertura com nota e lote; fim de frasco por ml', 'R$ 0', 'Estoque', 'Prova de origem e giro', 'ml vendidos na live', '20 ml')
    r('30/12', 'Programa de indicação', 'Códigos individuais; planilha de créditos', 'R$ 20 por cliente novo', 'Clientes satisfeitos', 'Aquisição barata', 'Clientes por indicação', '20% dos novos')
    r('jan/27', '1º teste de anúncio', 'R$ 150 em 15 dias; regras da aba Marketing', 'R$ 150', '10 vendas orgânicas', 'CAC medido', 'CAC', f'Até {brl(N["cac_max"])}')
    r('jan a fev/27', 'Etapa 2', 'Sabah Al Ward e Club de Nuit Intense Man', brl(ST1), '25 pedidos, margem de R$ 30, pedidos por esses perfumes', 'Árabes de giro', 'Pedidos acumulados', 'Gatilho batido')
    r('15/01', 'Revisar preço e faixas', 'Margem real por perfume e oferta; preços do líder', 'R$ 0', 'Dados de dezembro', 'Faixas ajustadas', 'Margem por pedido', 'R$ 35 ou mais')
    g('90 dias (até 23/02/2027)')
    r('23/02', 'Revisão de 90 dias', 'Metas e regras da aba Indicadores', 'R$ 0', 'Painel em dia', 'Decisão sobre etapa 3 e fase 2', 'Metas atingidas', '4 de 6')
    r('fev a mar/27', 'Etapa 3', '212 VIP Men 200 ml e Fakhar Rose', brl(ST2), '60 pedidos e grife com 25% do volume', 'Grife masculina de giro', 'Pedidos acumulados', 'Gatilho batido')
    g('6 meses (até 25/05/2027)')
    r('mar a mai/27', 'Fase 2', 'Loja virtual, lacrado sob encomenda, 1ª pré-venda de faixa D (Bleu de Chanel EDP)', 'Plano da loja', '60 pedidos e parecer favorável', 'Mais ticket e mais canais', 'Pedidos por mês', '35 ou mais')
    r('mai/27', 'Escala controlada', 'Dia das Mães; lote do mês da fila; clube piloto com mais de 100 clientes', 'Dentro do giro', 'Fase 2', f'{num(E_ROWS[-1]["orders"])} pedidos por mês (base)', 'Lucro operacional', f'{brl(E_ROWS[-1]["op"])} por mês')
    g('12 meses (até 25/11/2027)')
    r('nov/27', 'Decisões estruturais', 'Regime tributário (teto do MEI); marketplace só com respaldo jurídico; ajuda na expedição acima de 60 pedidos por mês', 'A definir', 'Resultados do ano', 'Negócio estável', 'Lucro e horas', 'Lucro por hora acima de R$ 25')
    h += '<div class="scroll"><table class="wide"><thead><tr><th>Prazo</th><th>O que</th><th>Como</th><th>Custo</th><th>Dependência</th><th>Resultado esperado</th><th>Indicador</th><th>Critério de sucesso</th></tr></thead><tbody>'
    for k, x in rows:
        if k == 'grp': h += f'<tr class="grp"><td colspan="8"><b>{x}</b></td></tr>'
        else: h += '<tr>' + ''.join(f'<td>{c}</td>' for c in x) + '</tr>'
    h += '</tbody></table></div>'
    return h

def p25():
    o = strip_pn(ORIG['p22'])
    r = E_ROWS
    o = R(o, '<td>12, 18, 22 (dez a fev)</td>', f'<td>{num(r[0]["orders"])}, {num(r[1]["orders"])}, {num(r[2]["orders"])} (dez a fev)</td>')
    o = R(o, '<td>R$ 79 ou mais</td><td>Abaixo de R$ 70</td><td>Puxar Kit Trio e adicional de 2 ml</td>', '<td>R$ 100 ou mais</td><td>Abaixo de R$ 85</td><td>Puxar Kit Trio com grife e adicional de 2 ml</td>')
    o = R(o, '<td>R$ 33 ou mais</td><td>Abaixo de R$ 28</td>', '<td>R$ 37 ou mais</td><td>Abaixo de R$ 30</td>')
    o = R(o, '<tr><td>CAC</td><td>Até R$ 12</td><td>Acima de R$ 21,22</td></tr>', f'<tr><td>CAC</td><td>Até R$ 12</td><td>Acima de {brl(N["cac_max"])}</td></tr><tr><td>Grife no volume vendido</td><td>25% ou mais</td><td>Menos de 20%</td></tr>')
    o = R(o, '<td>Até R$ 12</td><td>Acima de R$ 21,22</td>', f'<td>Até R$ 12</td><td>Acima de {brl(N["cac_max"])}</td>')
    o = R(o, '<td>R$ 176,85 ou mais</td><td>Abaixo de R$ 150</td>', '<td>R$ 300 ou mais</td><td>Abaixo de R$ 150</td>')
    o = R(o, '<td>R$ 482 em fev/27 (base)</td>', f'<td>{brl(r[2]["op"])} em fev/27 (base)</td>')
    new = ('<tr><td>Grife no volume vendido ' + NOVO + '</td><td>ml de grife vendidos ÷ ml vendidos</td><td>Mensal</td><td>Fichas de lote</td><td>25% ou mais</td><td>Abaixo de 20% depois de 60 dias</td><td>Segurar a etapa 3; voltar o foco para árabes</td></tr>'
           '<tr><td>Pedidos por perfume fora do catálogo ' + NOVO + '</td><td>Contagem de pedidos e perguntas no WhatsApp</td><td>Semanal</td><td>Etiquetas do WhatsApp</td><td>Registro de todos</td><td>—</td><td>Ordenar a fila de entrada</td></tr>'
           '<tr><td>Preço do líder nos perfumes do portfólio ' + NOVO + '</td><td>Preço do 5 ml no líder ÷ nosso preço</td><td>Mensal</td><td>Site do líder</td><td>Acima de 1,1</td><td>Abaixo de 1,0</td><td>Trocar o perfume ou revisar a faixa</td></tr>')
    o = R(o, '<tr><td>Faturamento</td>', new + '<tr><td>Faturamento</td>')
    o = R(o, '<td>Restarem 35 ml e ele tiver vendido 20 ml ou mais nos últimos 30 dias</td>', '<td>Restarem 35 ml (60 ml nos frascos de 200 ml) e ele tiver vendido 20 ml ou mais nos últimos 30 dias</td>')
    o = R(o, '<td>Só a partir de R$ 149; baixar para R$ 129 apenas com ticket médio de R$ 95 e margem de R$ 40 por pedido</td>', '<td>Só a partir de R$ 149; subir para R$ 199 se o ticket médio passar de R$ 130</td>')
    o = R(o, '<td>Começar após 10 vendas orgânicas; escalar com CAC até R$ 12; pausar acima de R$ 21,22</td>', f'<td>Começar após 10 vendas orgânicas; escalar com CAC até R$ 12; pausar acima de {brl(N["cac_max"])}</td>')
    o = R(o, '<td>40 pedidos acumulados e todos os perfumes vendendo 20 ml ou mais por mês; 1 novo por mês</td>', '<td>Etapa 2: 25 pedidos, margem de R$ 30 e pedidos pelos perfumes novos. Etapa 3: 60 pedidos e grife com 25% do volume. Depois: 1 novo por mês, só com vaga aberta</td>')
    o = R(o, 'margem abaixo de R$ 25 por 2 meses; ou lucro operacional negativo por 3 meses', 'margem abaixo de R$ 28 por 2 meses; ou lucro operacional negativo por 3 meses')
    o = R(o, '<tr><td>Margem média por pedido</td><td>R$ 30 ou mais</td><td>Menos de R$ 25</td></tr>', '<tr><td>Margem média por pedido</td><td>R$ 35 ou mais</td><td>Menos de R$ 28</td></tr>')
    o = R(o, '4 ou 5 metas: liberar a fase 2. 3 metas: estender a validação por 30 dias. 2 ou menos: rever preço, mix e conteúdo antes de investir mais.', '5 ou 6 metas: liberar a fase 2 e a etapa 3, se ainda não liberada. 4 metas: estender a validação por 30 dias. 3 ou menos: rever preço, faixas, mix e conteúdo antes de investir mais.')
    return o

def p26():
    h = '<h2>Decisões que ainda dependem de validação</h2>'
    rows = [
        ['1', 'Vender perfume fracionado', 'Parecer sobre RDC 108/2005, nova norma e licença sanitária', 'Advogado', '02/12', 'Estrutura alternativa (aba Jurídico)'],
        ['2', 'CNAE e regime', 'Confirmar se o fracionamento cabe no MEI e quando sair dele', 'Contador', '30/11', 'Outro enquadramento antes de vender'],
        ['3', 'Envio nacional', 'Aceite por escrito de uma transportadora', 'Transportadoras', '02/12', 'Operar só em Porto Alegre (o RS tem busca abaixo da média)'],
        ['4', 'Uso dos frascos próprios', 'Medir o volume restante dos 4', 'Dono', '26/11', 'Comprar a etapa 1 sem a ajuda deles'],
        ['5', 'Conteúdo de clone', 'Roteiro de comparação aprovado', 'Advogado', '09/12', 'Clone só pelo próprio nome e notas'],
        ['6', 'Nome Gota Rara', '@, domínio, INPI', 'Dono', '26/11', 'Casa Mirra ou novo nome'],
        ['7', 'Custo de reposição de árabes', 'Tabela de distribuidor', 'Rebaj, BIM, BR Brand Import', '02/12', 'Seguir no varejo com nota'],
        ['8', 'Preço de La Vie Est Belle na Black Friday', 'Cotação de 27/11', 'Dono', '27/11', 'Comprar após o parecer pelo preço de 25/11'],
        ['9', 'Demanda local e efeito da grife', '30 pessoas na lista; participação da grife nas primeiras 20 vendas', 'Dono', '31/12', 'Segurar etapas; foco em árabe'],
        ['10', 'Tempo e perda reais do envase', 'Envase piloto cronometrado', 'Dono', '02/12', 'Revisar preço do Kit Descoberta'],
        ['11', 'Elasticidade do catálogo', 'Pedidos antes e depois da etapa 2', 'Painel', '28/02/2027', 'Não liberar a etapa 3'],
        ['12', 'Entrega local por aplicativo', 'Termos de uso sobre inflamáveis', 'Dono', '02/12', 'Só retirada combinada'],
    ]
    h += table(['#', 'Decisão', 'O que falta', 'Quem valida', 'Prazo', 'Se a resposta for negativa'], rows, scroll=True, cls='wide')
    return h

def p27():
    h = '<h2>Lista final de compras</h2>'
    h += '<h3>Etapa 1: agora (insumos já; perfumes após o sinal do advogado)</h3>'
    rows = []
    for nome, q, p in m.INSUMOS:
        rows.append([nome, 'Insumos', str(q), brl(p), brl(q * p), 'Mercado Livre, Shopee ou compra local' + (' (estimado)' if nome.startswith(('Caixas', 'Cartões', 'Kit de envase', 'Álcool')) else '')])
    for k in m.STAGED['start']:
        s = SK[k]
        rows.append([f'{s["nome"]} {s["ml"]} ml', 'Perfume', '1', brl(s['preco']), brl(s['preco']), s['fonte']])
    rows.append(['<b>Total da etapa 1</b>', '', '', '', f'<b>{brl(INV0)}</b>', f'Insumos {brl(m.INSUMOS_TOTAL)} + perfumes {brl(PERF0)}'])
    h += table(['Item', 'Tipo', 'Quantidade', 'Preço unitário', 'Total', 'Fornecedor'], rows, align=['', '', 'c', 'r', 'r', ''], tot_rows=(len(rows) - 1,), scroll=True, cls='wide')
    h += f'<p class="note">Caixa mínimo do negócio: R$ 150, que pode vir das primeiras vendas com os frascos próprios. Se quiser começar com folga, separe {brl(1500 - INV0)} a mais (o orçamento de R$ 1.500 do cenário equivalente).</p>'
    h += '<h3>Com a receita das primeiras vendas</h3>'
    h += table(['Item', 'Quantidade', 'Fornecedor', 'Preço', 'Gatilho'], [
        ['Frascos de vidro âmbar 10 ml com spray', '50', 'Magalu', 'R$ 139,00', '5 pedidos pagos'],
        ['Flaconetes de vidro 1 ml (brinde)', '100', 'Mercado Livre', 'R$ 57,91', '5 pedidos pagos'],
        ['Frascos de vidro 5 ml com spray', '20', 'Mercado Livre', 'R$ 53,85', 'Restarem 15'],
        ['Caixa presente (adicional de R$ 9,90)', '20', 'A cotar', 'Estimado R$ 60,00', '10 pedidos'],
        [f'Etapa 2: {SK["sabah"]["nome"]} e {SK["cdnim"]["nome"]}', '1 de cada', 'Magalu e Época', brl(ST1), '25 pedidos, margem de R$ 30, pedidos por eles'],
        [f'Etapa 3: {SK["212"]["nome"]} 200 ml e {SK["fakhar"]["nome"]}', '1 de cada', 'Época e Magalu', brl(ST2), '60 pedidos, grife com 25% do volume'],
        ['Reposição do Sauvage EDT (200 ml)', '1', 'Época', brl(SK['sauv']['preco']), 'Frasco próprio acabou e venda de 20 ml ou mais no mês'],
        ['Reposição de perfume', '1 por vez', 'Distribuidor ou varejo com nota', 'R$ 128,61 a R$ 718,53', 'Regra de recompra (aba Indicadores)'],
        ['Caixas kraft 12 × 19 × 4 cm', '100', 'Sekai Embalagens', 'R$ 189,75', '40 pedidos acumulados'],
    ], align=['', 'c', '', 'r', ''])
    h += '<h3>Não comprar</h3>'
    h += '<p>Nicho original e faixa D para estoque; grife em frasco de 100 ml quando houver o de 200 ml; mais de 1 frasco do mesmo perfume antes de vender 60 ml dele; frasco sem nota ou muito abaixo do varejo; caixa personalizada com pedido mínimo; frascos de 30 ml, de plástico ou porta-perfume de bolso; site pago, domínio e anúncios antes de 10 vendas orgânicas; "amplificador" de fixação; equipamentos (balança, seladora, impressora térmica) antes de 40 pedidos por mês.</p>'
    return h

def p28():
    o = strip_pn(ORIG['p25'])
    o = R(o, '<li>Caixa mínimo de R$ 176,85 separado</li>', '<li>Caixa mínimo de R$ 150 separado</li><li>Gatilhos das etapas 2 e 3 anotados no painel</li>')
    o = R(o, '<li>Link de pagamento e Pix na conta do negócio</li>', '<li>Link de pagamento e Pix na conta do negócio</li><li>Tabela de faixas e de kits "a partir de" no catálogo e nos destaques</li>')
    o = R(o, '<li>Volume dos frascos já disponíveis medido</li>', '<li>Volume dos 4 frascos próprios medido</li><li>Preço do líder anotado para os 6 perfumes da largada</li>')
    o = R(o, '<li>Modelo de rótulo revisado</li>', '<li>Modelo de rótulo revisado</li><li>Roteiro de conteúdo de clone aprovado</li>')
    return o

def p29():
    t = E_BASE
    h = '<h2>Respostas executivas</h2><dl class="qa">'
    qa = [
        ('Eu deveria abrir?', f'Sim, em etapas. A conta fecha com poucos pedidos ({num(N["be_200"], 1)} por mês pagam fixos e R$ 200 de marketing). O que pode impedir é o parecer jurídico sobre fracionamento e o aceite do transporte; os dois vêm antes de comprar perfume.'),
        ('Qual modelo?', 'Curadoria híbrida v2: árabes e clones na faixa A, grife de giro nas faixas B e C, faixa D só em pré-venda. Fase 2, após 60 pedidos e parecer favorável: frasco lacrado sob encomenda e loja virtual.'),
        ('Qual público?', 'Quem quer provar grife antes do frasco caro, quem procura o clone de um nicho e o curioso do árabe viral; 20 a 40 anos; Porto Alegre e envio nacional. Presenteadores nas datas.'),
        ('Quais produtos primeiro?', 'Asad, Yara e La Vie Est Belle (comprados) + 9pm, Liquid Brun e Sauvage EDT (próprios). Etapa 2: Sabah Al Ward e Club de Nuit Intense Man. Etapa 3: 212 VIP Men 200 ml e Fakhar Rose.'),
        ('Os kits têm preço fixo?', f'Não mais. Kit Trio a partir de {brl(m.BASE["trio"])} com árabes; cada perfume de grife soma o adicional da faixa (+R$ 12,90 na B, +R$ 34,90 na C). Com preço fixo, um Trio de grifes daria prejuízo de {brl(-N["fixed_adverse"][1])}.'),
        ('Quanto investir agora?', f'{brl(INV0)}: {brl(m.INSUMOS_TOTAL)} de insumos já e {brl(PERF0)} em perfumes após o retorno do advogado e 30 pessoas na lista. Teto de R$ 3.000, com as etapas 2 ({brl(ST1)}) e 3 ({brl(ST2)}) pagas pelo caixa do negócio.'),
        ('Quanto manter em caixa?', 'Nunca abaixo de R$ 150. Nenhuma compra de etapa ou de reposição que deixe o caixa abaixo disso.'),
        ('Quanto cobrar?', f'5 ml: {brl(m.P5["A"])} (A), {brl(m.P5["B"])} (B), {brl(m.P5["C"])} (C). 10 ml: {brl(m.P10["A"])}, {brl(m.P10["B"])}, {brl(m.P10["C"])}. Kit Descoberta a partir de {brl(m.BASE["desc"])}, Trio a partir de {brl(m.BASE["trio"])}, Dupla 10 ml a partir de {brl(m.BASE["dupla"])}. Frete pago pelo cliente, grátis acima de R$ 149.'),
        ('Sauvage, Bleu de Chanel e Aventus entram?', 'Sauvage sim (frasco próprio agora, 200 ml depois). Bleu de Chanel EDP só em pré-venda (R$ 11,49 por ml). Aventus original não: R$ 33 por ml e o líder vende abaixo do que daria margem; a demanda de Aventus vai para o Club de Nuit Intense Man.'),
        ('Onde vender primeiro?', 'Instagram (com live de frasco aberto) e WhatsApp, com Pix ou link e retirada ou entrega em Porto Alegre. Envio nacional só com aceite escrito da transportadora. Marketplace não.'),
        ('O que fazer nas próximas 48 horas?', 'Medir os 4 frascos, mandar as perguntas ao advogado e ao contador, checar o nome, comprar os insumos, criar perfil e WhatsApp Business e só cotar (não comprar) os perfumes na Black Friday.'),
        ('Que resultados esperar em 30, 60 e 90 dias?', f'No cenário base: {num(E_ROWS[0]["orders"])} pedidos em dezembro, {num(E_ROWS[0]["orders"] + E_ROWS[1]["orders"])} acumulados em janeiro e {num(t["q"]["orders"])} em fevereiro, com faturamento de {brl(t["q"]["rev"])} e lucro operacional de {brl(t["q"]["op"])} em 90 dias. No conservador, {num(E_CON["q"]["orders"])} pedidos em 90 dias; no otimista, {num(E_OTI["q"]["orders"])}.'),
        ('Quando investir mais?', 'Pelos gatilhos: etapa 2 com 25 pedidos, margem de R$ 30 e pedidos pelos perfumes novos; etapa 3 com 60 pedidos e grife com 25% do volume. Fase 2 na revisão de 90 dias, com 5 de 6 metas e parecer favorável.'),
        ('Quando interromper ou reformular?', 'Parecer jurídico desfavorável (migrar para lacrados, miniaturas e teste presencial); menos de 20 pedidos em 90 dias; margem abaixo de R$ 28 por 2 meses; lucro operacional negativo por 3 meses; grife abaixo de 20% do volume depois de 60 dias (parar na etapa 2).'),
    ]
    h += ''.join(f'<dt>{q}</dt><dd>{a_}</dd>' for q, a_ in qa) + '</dl>'
    return h

def p30():
    h = '<h2>Se eu estivesse começando amanhã</h2><ol class="steps">'
    steps = [
        '<b>Manhã do dia 1:</b> medir o volume que resta nos 4 frascos próprios e anotar.',
        'Mandar as 12 perguntas ao advogado (incluindo conteúdo de clone e pré-venda) e as 7 ao contador, pedindo retorno preliminar em até 7 dias.',
        'Checar @gotarara no Instagram e TikTok, o domínio no registro.br e a busca de marca no INPI; garantir o @.',
        f'Comprar os insumos da etapa 1 ({brl(m.INSUMOS_TOTAL)}).',
        'Na Black Friday (27/11), só anotar o preço de La Vie Est Belle, Asad e Yara; comprar apenas se o advogado já tiver respondido.',
        'Criar o perfil e o WhatsApp Business com bio, catálogo por faixa, kits "a partir de" e mensagem automática; fixar 3 posts (quem somos, como funciona, políticas e faixas).',
        'Mandar mensagem individual para 30 contatos próximos convidando para a lista de espera.',
        'Dia 2: abrir o MEI depois da resposta do contador sobre o CNAE.',
        'Escrever para 2 transportadoras pedindo aceite por escrito para perfume fracionado.',
        'Quando os insumos chegarem: envase piloto de 10 decants de 9pm, Liquid Brun e Sauvage, com cronômetro e teste de vazamento.',
        'Publicar os conteúdos dos dias 1 a 6 do calendário.',
        '<b>Primeira venda:</b> oferecer à lista o Kit Trio com 9pm, Liquid Brun e Sauvage (R$ 102,80, com o adicional do Sauvage), retirada em Porto Alegre e Pix.',
        f'Com retorno do advogado e 30 pessoas na lista: comprar Asad, Yara e La Vie Est Belle ({brl(PERF0)}) com nota.',
        'Filmar a abertura de cada frasco e publicar as fichas de lote nos destaques.',
        'Abrir a pré-venda de Natal em 07/12 com os 6 perfumes.',
        'No 5º pedido pago: comprar os frascos de 10 ml e os flaconetes de 1 ml e liberar o 10 ml e o Kit Dupla.',
        'Em cada entrega: cartão escrito à mão; mensagem no D+2; pedido de avaliação no D+7 com crédito de R$ 10; anotar a frequência de uso e o perfume preferido.',
        'Em 21/12: primeira live de frasco aberto, com o fim do frasco do 9pm ou do Liquid Brun vendido por ml.',
        'Com 25 pedidos: conferir margem e pedidos por Club de Nuit e Sabah; se bater, comprar a etapa 2 com o caixa do negócio.',
        'Todo domingo, atualizar o painel (incluindo grife no volume); em 23/02/2027, fazer a revisão de 90 dias e decidir etapa 3 e fase 2 pelas regras.',
    ]
    h += ''.join(f'<li>{s}</li>' for s in steps) + '</ol>'
    return h
