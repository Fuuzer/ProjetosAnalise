from hb import *
from sec_a import E_BASE, E_CON, E_OTI, E_ROWS, B, ST1, ST2, INV0, PERF0

BENCH = [
 # (decisão, serviço, quem faz e evidência, por quê, como entra no plano)
 ('Copiar', 'Preço por perfume, por faixa de custo', 'Perfume Shopping e Tabs: cada perfume tem preço próprio em todos os tamanhos', 'Grife e nicho custam de 2 a 30 vezes mais por ml que árabe; preço único dá prejuízo', 'Faixas A a D (aba Precificação)'),
 ('Copiar', 'Kits por ocasião, com preço pela composição', 'Perfume Shopping: Kit Date, Business, After, Ártico, Move, Tropical, Night, Assinatura; Kit Business 5 ml sai a R$ 124,40 no masculino e R$ 334,50 no feminino', 'Facilita a escolha e o presente; o preço acompanha os perfumes do kit', '4 kits temáticos (Encontro, Trabalho, Calor, Frio) com preço pela regra das faixas'),
 ('Copiar', 'Navegação por ocasião e por clima', 'Tabs: menus "Por ocasião" (dia a dia, encontros, festas) e "Por clima" (quente, frio, ameno)', 'O RS tem inverno e verão marcados; ajuda o cliente leigo', 'Catálogo do WhatsApp e destaques do Instagram organizados assim'),
 ('Copiar', 'Quiz de recomendação', 'Tabs: "Não sabe qual escolher? Responda nosso quiz"', 'Reduz a indecisão de quem chega pelo viral', 'Diagnóstico de 4 perguntas também em formulário e Stories'),
 ('Copiar', 'Frasco aberto ao vivo, vendido "até a última gota"', 'Tabs: R$ por ml com desconto e ml restantes (ex.: 1 Million Black a R$ 9/ml, 39% off, 182 de 200 ml)', 'Prova de origem, giro de estoque e urgência ao mesmo tempo', 'Live mensal de abertura; fim de frasco vendido por ml com 20% de desconto sobre a faixa'),
 ('Copiar', 'Escada de tamanhos com R$ por ml menor no maior', 'Perfume Shopping: Sauvage EDP 1 ml R$ 20,90, 5 ml R$ 79,50, 30 ml R$ 445,70', 'Puxa o cliente para o tamanho maior', '2, 5 e 10 ml; o 10 ml sai mais barato por ml que o 5 ml'),
 ('Copiar', 'Avaliação verificada com nota visível', 'Tabs: 4,8 estrelas em 569 avaliações, 92% com 5 estrelas', 'Confiança para quem não conhece a loja', 'Pedido de avaliação no D+7, com foto, publicada com autorização'),
 ('Copiar', 'Vídeo do processo e FAQ "é original?"', 'Perfume Shopping e Tabs', 'Responde à objeção nº 1', 'Destaque "Origem" com vídeo do envase e ficha de lote'),
 ('Copiar', 'Entrega no mesmo dia na cidade-sede', 'Tabs: motoboy em Campinas', 'Conveniência que loja nacional não tem', 'Porto Alegre no mesmo dia; retirada combinada'),
 ('Copiar', 'Brinde acima de um valor', 'Tabs: amostra brinde acima de R$ 179', 'Sobe o ticket sem dar desconto', '1 ml do próximo perfume a partir de R$ 89,90 (mantido)'),
 ('Copiar', 'Caixa de presente vendida à parte', 'Perfume Shopping: "Caixa de Presente para Decants (não acompanha decants)"', 'Venda adicional nas datas', f'Caixa presente a R$ 9,90 (custo estimado de R$ 3) {ES}'),
 ('Copiar', 'Porta-decant ou estojo', 'Tabs (porta-decants); Scentbird (estojo reutilizável no 1º pedido)', 'Acessório que puxa a recompra', 'Estojo como adicional; preço após cotação'),
 ('Copiar', 'Indicação e afiliados', 'Scent Split: programa de afiliados', 'Aquisição com custo conhecido', 'Indique e ganhe R$ 10 + R$ 10 (mantido); cupom para microafiliado'),
 ('Copiar', 'Frete grátis acima de um valor', 'Perfume Shopping e Tabs: acima de R$ 199', 'Sobe o ticket', 'Acima de R$ 149 (nosso ticket é menor); rever para R$ 199 se o ticket passar de R$ 130'),
 ('Eliminar', 'Originalidade só declarada', 'Tabs cita "selo ADIPEC" e um cliente reclama que "não existe selo algum"; reclamações de "não parece original" no líder, na Tabs e na Guido', 'Promessa sem prova vira reclamação pública', 'Ficha de lote verificável: vídeo, nota e lote no rótulo'),
 ('Eliminar', 'Resposta lenta no pós-venda', 'Perfume Shopping: 14 dias de média no Reclame Aqui; Tabs: cerca de 6 dias', 'Demora transforma problema simples em reclamação', 'Resposta em até 2 h no horário comercial'),
 ('Eliminar', 'Atraso e rastreio parado', 'Tema nº 1 de reclamação no líder, na Tabs, na Guido e na Casa dos Decants', 'É a reclamação mais frequente do setor', 'Despacho em 2 dias úteis, rastreio enviado no WhatsApp, crédito de R$ 10 por atraso'),
 ('Eliminar', 'Vazamento e quebra', 'Tabs e Scent Split (avaliações e reclamações)', 'Perde o produto e a confiança', 'Teste deitado de 30 min, lacre e envelope com bolha (mantido)'),
 ('Eliminar', 'Promessa de fixação "exatamente igual"', 'FAQ da Tabs: "É tudo exatamente igual: fragrância, fixação, projeção"', 'Fixação depende de pele e clima; gera reclamação de "não fixa"', 'Explicar o que muda a fixação; nunca prometer horas'),
 ('Eliminar', 'Descontos empilhados', 'Perfume Shopping: cupom de 8% + 5% no Pix + cashback de 10%', 'Corrói a margem e ensina o cliente a esperar promoção', 'Preço já abaixo do líder; desconto só no calendário e acima do piso'),
 ('Eliminar', 'Acessório com promessa difícil de provar', 'Perfume Shopping: "amplificador molecular" (2 itens entre os 40 mais vendidos)', 'Risco de publicidade enganosa (CDC, art. 37)', 'Não vender'),
 ('Eliminar', 'Vitrine com muitos tamanhos esgotados', 'Tabs: vários tamanhos "esgotado" na mesma página', 'Frustra e afasta', 'Mostrar só o que tem; "avise-me" para o resto'),
 ('Examinar', 'Assinatura ou clube', 'Clube Tabs (perfumes que nunca se repetem); Scentbird a US$ 17,95 por mês por 8 ml', '+ receita recorrente e previsão de estoque; − compromisso afasta quem só quer testar e exige base de clientes', 'Fase 2, com 100 clientes: piloto com 20 assinantes, 1 × 5 ml por mês das faixas A e B'),
 ('Examinar', 'Cashback', 'Perfume Shopping: 10% na 1ª compra e 5% nas seguintes', '+ recompra; − custa até 5% da receita e exige sistema', 'Trocar por crédito de R$ 10 na avaliação com foto e, na fase 2, pelo valor do decant abatido no frasco lacrado'),
 ('Examinar', 'Cupom de 1ª compra', 'Tabs: 10% (PRIMEIRACOMPRA)', f'+ conversão; − leva a margem do Trio de {brl(N["offA"]["trio"]["cm"])} para cerca de {brl(N["offA"]["trio"]["cm"] - 8.99)}', 'Usar brinde (1 ml extra) em vez de desconto'),
 ('Examinar', 'Desconto no Pix', 'Perfume Shopping e Tabs: 5%', '+ reduz taxa de cartão; − nosso Pix não tem taxa e o preço já é baixo', 'Pix como padrão, sem desconto'),
 ('Examinar', 'Catálogo amplo de nicho', 'Perfume Shopping: 578 nichos', '+ atrai o entusiasta; − Aventus custa R$ 3.320 e o líder vende o 5 ml a R$ 256, abaixo do nosso custo com margem', 'Nicho entra por clone ou por pré-venda'),
 ('Examinar', 'Rateio ou pré-venda de frasco', 'Modelo de "split" de grupos e lojas de fora', '+ permite faixa D e nicho sem capital; − espera e risco de não fechar', 'Teste com 1 frasco de faixa D após 60 pedidos; compra só quando a pré-venda pagar o frasco; reembolso se não fechar em 15 dias'),
 ('Examinar', 'Tamanho de 1 ml', 'Perfume Shopping: 1 ml sem spray a partir de cerca de R$ 10', '+ entrada barata; − frasco, rótulo e mão de obra quase iguais aos do 2 ml', 'Só como brinde'),
 ('Examinar', '30 ml e "30 ml no frasco original"', 'Perfume Shopping e Tabs', '+ ticket; − compete com o frasco, prende capital e consome um terço do frasco de origem', 'Não oferecer; acima de 20 ml, frasco sob encomenda (fase 2)'),
 ('Examinar', 'Parcelamento em 3x sem juros', 'Perfume Shopping e Tabs, acima de R$ 150', '+ converte ticket alto de grife; − taxa maior', 'Só acima de R$ 150'),
 ('Examinar', 'Influenciador ou "garoto-propaganda"', 'Tabs (citado em avaliação de cliente)', '+ confiança e alcance; − custo e risco de imagem', 'Microinfluenciador local por permuta, após 20 vendas, com roteiro de prova de origem'),
 ('Examinar', 'Marketplace', 'Combos no Mercado Livre e Magalu; Gold Glow em farmácias', '+ tráfego; − exige número da Anvisa no anúncio e briga com R$ 20 por 5 ml', 'Fora da fase 1 (mantido)'),
 ('Examinar', 'Aplicativo próprio', 'Tabs', '+ recompra; − custo e manutenção', 'Não; o WhatsApp cumpre o papel'),
]

def p9():
    h = '<h2>Benchmark de serviços</h2>'
    c = {k: sum(1 for x in BENCH if x[0] == k) for k in ['Copiar', 'Eliminar', 'Examinar']}
    h += f'<p class="lead">{len(BENCH)} serviços observados nos maiores concorrentes e em duas referências de fora. {c["Copiar"]} entram no plano como estão ou adaptados; {c["Eliminar"]} são falhas que geram reclamação e o plano evita; {c["Examinar"]} são neutros, com prós e contras, e cada um recebeu uma decisão.</p>'
    h += '<div class="scroll"><table class="wide"><thead><tr><th>Serviço</th><th>Quem faz e evidência</th><th>Por quê (prós e contras)</th><th>Como entra no plano</th></tr></thead><tbody>'
    lab = {'Copiar': 'Copiar: pontos positivos', 'Eliminar': 'Eliminar: pontos negativos', 'Examinar': 'Examinar: neutros, bons por um lado e ruins por outro'}
    for dec in ['Copiar', 'Eliminar', 'Examinar']:
        h += f'<tr class="grp"><td colspan="4"><b>{lab[dec]} ({c[dec]})</b></td></tr>'
        for d, s, q, w, p in BENCH:
            if d == dec:
                h += f'<tr><td><b>{s}</b></td><td>{q}</td><td>{w}</td><td>{p}</td></tr>'
    h += '</tbody></table></div>'
    h += '<h3>Os 5 itens que mais mudam o negócio</h3><ol>'
    h += '<li><b>Preço por faixa</b> (copiado): é o que permite ter grife sem dar prejuízo.</li>'
    h += '<li><b>Prova de origem verificável</b> (contra a falha nº 1 do setor): é o diferencial que o cliente procura, como mostram as buscas "decant perfume original".</li>'
    h += '<li><b>Frasco aberto ao vivo, até a última gota</b> (copiado): conteúdo, prova e giro de estoque numa ação só.</li>'
    h += '<li><b>Resposta em até 2 horas</b> (contra a falha nº 2): custo zero, efeito direto na reputação.</li>'
    h += '<li><b>Pré-venda para faixa D</b> (neutro, testado com regras): abre Bleu de Chanel EDP e Miss Dior sem capital parado.</li></ol>'
    h += src(a(URL['ps'], 'Perfume Shopping'), a(URL['tabs'], 'Tabs Perfumes'), a(URL['ra_ps'], 'Reclame Aqui, Perfume Shopping'), a(URL['ra_tabs'], 'Reclame Aqui, Tabs'), a(URL['ra_guido'], 'Reclame Aqui, Guido'), a(URL['scentbird'], 'Scentbird'), a(URL['scentsplit'], 'Scent Split'), a(URL['scentsplit_aff'], 'Scent Split, afiliados'), a('https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm', 'CDC'))
    return h

def p10():
    o = ORIG['p7']
    o = re.sub(r'<div class="pn">.*?</div>\s*$', '', o, flags=re.S)
    o = o.replace('<h2>Cliente e posicionamento</h2>', '')
    h = '<h2>Cliente e posicionamento</h2>'
    h += '<h3>Por que as pessoas compram decant: teste da sua hipótese</h3>'
    h += '<p>Hipótese: a maior parte da compra de decant acontece porque o frasco inteiro é caro e o cliente quer provar antes. Quatro evidências independentes:</p>'
    ev = [
        ['O que o líder vende', '82 dos 100 decants mais vendidos são de grife ou nicho; 16 são árabes', FA, 'Apoia'],
        ['Como o líder e a Tabs vendem', '"Prove antes de comprar o frasco"; "vale para quem quer provar um perfume caro sem pagar o frasco inteiro"', FA, 'Apoia'],
        ['O que se busca junto de "contratipo"', 'Delina, Bleu de Chanel, La Vie Est Belle, Good Girl', FA, 'Apoia: a referência é sempre o perfume caro'],
        ['Custo do teste em relação ao frasco', 'Grife: o 5 ml custa de 6% a 9% do frasco; árabe: de 17% a 25%', FA + ' + ' + ES, 'Apoia, com ressalva para árabe'],
    ]
    h += table(['Evidência', 'Dado', 'Tipo', 'Leitura'], ev)
    rows = [
        ['Creed Aventus', 'R$ 3.320,84 (100 ml)', brl(PS5['aventus']), pct(PS5['aventus'] / 3320.84, 1)],
        ['Dior Sauvage EDP', 'R$ 841,35 (100 ml)', brl(PS5['sauv_edp']), pct(PS5['sauv_edp'] / 841.35, 1)],
        ['Armani Acqua di Giò EDT', 'R$ 800,00 (100 ml)', brl(PS5['adg']), pct(PS5['adg'] / 800.0, 1)],
        ['Carolina Herrera 212 VIP Men', 'R$ 739,00 (100 ml)', brl(PS5['212men']), pct(PS5['212men'] / 739.0, 1)],
        ['Armaf Club de Nuit Intense Man', 'R$ 299,90 (105 ml)', brl(PS5['cdnim']), pct(PS5['cdnim'] / 299.90, 1)],
        ['Lattafa Asad', 'R$ 268,72 (100 ml)', brl(PS5['asad']), pct(PS5['asad'] / 268.72, 1)],
        ['Al Wataniah Sabah Al Ward', 'R$ 239,90 (100 ml)', brl(PS5['sabah']), pct(PS5['sabah'] / 239.90, 1)],
        ['Lattafa Yara', 'R$ 259,90 (100 ml)', brl(PS5['yara']), pct(PS5['yara'] / 259.90, 1)],
    ]
    h += '<h3>Quanto custa testar, em relação ao frasco</h3>'
    h += table(['Perfume', 'Frasco (Época, 25/11/2026)', '5 ml no líder', '5 ml ÷ frasco'], rows, align=['', 'r', 'r', 'r'])
    h += (f'<div class="box"><b>Conclusão:</b> a hipótese está certa para grife e nicho. Para árabe, o decant de 5 ml custa um quinto do frasco, e boa parte de quem gosta compra o frasco inteiro; o decant árabe vende como <b>variedade</b> (provar vários) e como <b>clone</b> ("como é o árabe que lembra o Aventus?"). '
          f'Isso muda o portfólio: grife de giro para quem testa antes do frasco caro, clones para quem quer o cheiro do nicho a preço de árabe, árabes virais para descoberta. Onde você pode estar errado: nicho original não fecha conta com custo de varejo (Aventus a R$ 33 por ml), e o líder já ocupa esse espaço {JU}.</div>')
    # segmentos: ajusta textos e acrescenta o caçador de clone
    o = o.replace('<td>Testar sem gastar R$ 160 a R$ 300 num frasco</td>', '<td>Testar o viral sem gastar R$ 250 a R$ 400 num frasco</td>')
    o = o.replace('<td>Variedade, novidade, 10 ml para usar de verdade</td>', '<td>Provar grife e nicho antes do frasco caro; variedade; 10 ml para usar de verdade</td>')
    o = o.replace('<tr><td>Presenteador</td>', '<tr><td>Caçador de clone</td><td>20 a 35 anos, quer o cheiro de um nicho caro</td><td>Saber qual árabe chega perto do Aventus, do Angels\' Share ou do Sauvage Elixir</td><td>Kit Trio com o clone e, se possível, o original em 2 ml</td><td>1</td></tr><tr><td>Presenteador</td>')
    o = o.replace('<p><b>Situação:</b> 31 anos, coleciona perfumes, participa de grupos.<br><b>Dor:</b> quer variedade sem lotar a prateleira de frascos.', '<p><b>Situação:</b> 31 anos, coleciona perfumes, participa de grupos.<br><b>Dor:</b> quer provar o Sauvage, o 212 ou o La Vie Est Belle antes de gastar R$ 700 num frasco, e variedade sem lotar a prateleira.')
    o = o.replace('<b>Oferta:</b> 10 ml avulso e Kit Dupla 10 ml; aviso de lote novo no grupo VIP.', '<b>Oferta:</b> 5 ml de grife (faixas B e C), 10 ml avulso e Kit Dupla 10 ml; aviso de lote novo e de pré-venda no grupo VIP.')
    o = o.replace('<div class="box">Acerte o perfume árabe antes de pagar o frasco: decants com origem comprovada por lote, curadoria pelo seu perfil e entrega no mesmo dia em Porto Alegre.</div>',
                  '<div class="box">Prove o perfume antes de pagar o frasco: decants de grife, clones e árabes com origem comprovada por lote, curadoria pelo seu perfil e entrega no mesmo dia em Porto Alegre.</div>')
    o = o.replace('O cliente sabe que o frasco custa R$ 160; a mensagem de luxo soa falsa.', 'O cliente sabe que o decant é a versão acessível; a mensagem de luxo soa falsa.')
    o = o.replace('<div class="src"><b>Fontes:</b> ', '<div class="src"><b>Fontes:</b> ' + a(URL['ps_api'], 'Perfume Shopping, popularidade') + ' &middot; ' + a(URL['ps'], 'FAQ do líder') + ' &middot; ' + a(URL['trends_rel'], 'Trends, "contratipo"') + ' &middot; ' + a(URL['epoca'], 'Época Cosméticos') + ' &middot; ')
    return h + o

MATRIX = [
 ('Curadoria híbrida v2: árabes e clones + grife de giro por faixa + pré-venda de luxo; lacrado sob encomenda na fase 2', [4, 4, 4, 5, 2, 3, 5], 'novo'),
 ('Híbrido v1: decants árabes + kits + lacrado sob encomenda + curadoria no WhatsApp', [4, 4, 4, 5, 2, 3, 4], ''),
 ('Decants árabes + kits', [4, 4, 5, 4, 2, 3, 4], ''),
 ('Só decants árabes', [5, 4, 5, 2, 2, 3, 4], ''),
 ('Decants árabes + grife (reavaliado: era 2,80)', [4, 4, 4, 4, 2, 3, 4], 'rev'),
 ('Curadoria personalizada (diagnóstico + venda)', [4, 4, 3, 5, 3, 1, 3], ''),
 ('Clube de assinatura', [3, 4, 2, 4, 2, 4, 5], ''),
 ('Decants + lacrados sob encomenda', [4, 3, 4, 3, 2, 3, 3], ''),
 ('Pré-venda / compra coletiva de lacrados', [5, 3, 3, 3, 3, 2, 2], ''),
 ('Alternativa mais segura: lacrados + miniaturas de fábrica + bar de testes presencial', [3, 2, 3, 3, 5, 3, 2], ''),
 ('Decants de nicho original (Aventus, Baccarat Rouge, Delina)', [1, 2, 3, 4, 2, 2, 3], 'novo'),
]
WM = [.20, .15, .15, .15, .15, .10, .10]

def p11():
    o = ORIG['p8']
    o = re.sub(r'<div class="pn">.*?</div>\s*$', '', o, flags=re.S)
    i1 = o.index('<table>'); i2 = o.index('</table>', i1) + len('</table>')
    i3 = o.index('<h3>Business Model Canvas')
    head = '<h2>Modelo de negócio</h2><h3>Matriz de 11 modelos</h3><p>Notas de 1 a 5 (5 = melhor); risco jurídico recebe 5 quando o risco é menor ' + JU + '.</p>'
    hd = ['Modelo', 'Cabe no orçamento (até R$ 3.000, em etapas)<br>20%', 'Margem<br>15%', 'Velocidade de validação<br>15%', 'Diferenciação<br>15%', 'Risco jurídico e sanitário (5 = menor)<br>15%', 'Escala com pouco tempo<br>10%', 'Recorrência<br>10%', 'Nota']
    rows = []
    sc = sorted(MATRIX, key=lambda x: -sum(w * v for w, v in zip(WM, x[1])))
    for nome, v, tag in sc:
        score = sum(w * x for w, x in zip(WM, v))
        t = f' <span class="tag">{"novo" if tag == "novo" else "reavaliado"}</span>' if tag else ''
        rows.append([f'<b>{nome}</b>{t}'] + [str(x) for x in v] + [f'<b>{num(score, 2)}</b>'])
    mt = table(hd, rows, align=[''] + ['c'] * 8)
    leit = '<h3>Leitura da matriz</h3><ul>'
    leit += '<li><b>A v2 lidera (3,85)</b> porque soma a diferenciação da curadoria com a recorrência da grife (recompra de 10 ml e, na fase 2, frasco lacrado). A fase 1 dela é o plano escalonado.</li>'
    leit += '<li><b>"Árabes + grife" subiu de 2,80 para 3,60</b> na reavaliação: com frasco de 200 ml e preço por faixa, a margem deixa de ser negativa e o plano em etapas cabe no orçamento.</li>'
    leit += '<li><b>Nicho original fica em último (2,35):</b> capital de R$ 3.300 a R$ 4.800 por frasco e preço que não bate o líder.</li>'
    leit += '<li><b>Todos os modelos com decant levam 2 em risco jurídico.</b> A alternativa mais segura segue como plano B se o parecer vier negativo.</li>'
    leit += '<li><b>Clube de assinatura</b> tem a melhor recorrência, mas exige base: entra como piloto após 100 clientes.</li></ul>'
    canvas = o[i3:]
    canvas = canvas.replace('Distribuidores oficiais (Rebaj e importadoras de Al Wataniah e Afnan), varejistas com nota fiscal,', 'Distribuidores oficiais (Rebaj e importadoras de Al Wataniah, Armaf e Afnan), varejistas de grife com nota fiscal (Época, Sephora, Beleza na Web),')
    canvas = canvas.replace('Acertar o perfume árabe antes de pagar o frasco, com origem comprovada por lote, curadoria e entrega rápida local', 'Provar o perfume antes de pagar o frasco: grife, clones e árabes com origem comprovada por lote, curadoria e entrega rápida local')
    canvas = canvas.replace('Curioso do viral e entusiasta (principal); presenteador e quem busca perfume assinatura (secundário)', 'Entusiasta que prova grife, caçador de clone e curioso do viral (principal); presenteador e quem busca perfume assinatura (secundário)')
    canvas = canvas.replace('Kits (Descoberta, Trio, Dupla 10 ml), avulsos de 5 e 10 ml, adicional de 2 ml; na fase 2, margem do frasco lacrado sob encomenda', 'Kits com preço por faixa (Descoberta, Trio, Dupla 10 ml, kits por ocasião), avulsos de 5 e 10 ml, adicional de 2 ml, caixa presente, fim de frasco por ml; pré-venda de faixa D; na fase 2, frasco lacrado sob encomenda')
    canvas = canvas.replace('Perfume (maior custo variável), frascos e embalagem', 'Perfume (maior custo variável; grife em frasco de 200 ml), frascos e embalagem')
    canvas = canvas.replace('<div class="src"><b>Fontes:</b> notas da matriz são julgamento sobre os dados das abas Mercado, Concorrência, Precificação e Jurídico.</div>', '<div class="src"><b>Fontes:</b> notas da matriz são julgamento sobre os dados das abas Mercado, Google Trends, Concorrência, Precificação, Cenários e Jurídico.</div>')
    return head + mt + leit + canvas

STAGE_OF = {'asad': 'Etapa 1', 'yara': 'Etapa 1', 'lveb': 'Etapa 1', 'p9pm': 'Etapa 1 (frasco próprio)', 'brun': 'Etapa 1 (frasco próprio)', 'sauv': 'Etapa 1 (frasco próprio); repor com 200 ml',
            'sabah': 'Etapa 2 (25 pedidos)', 'cdnim': 'Etapa 2 (25 pedidos)', '212': 'Etapa 3 (60 pedidos)', 'fakhar': 'Etapa 3 (60 pedidos)', 'hawas': 'Fila (lote do mês)', 'khamrah': 'Fila (lote do mês)'}
PSKEY = {'asad': 'asad', 'yara': 'yara', 'lveb': 'lveb', 'brun': 'brun', 'sauv': 'sauv_edt', 'sabah': 'sabah', 'cdnim': 'cdnim', '212': '212men', 'fakhar': 'fakhar', 'khamrah': 'khamrah'}

def p12():
    h = '<h2>Portfólio</h2>'
    h += '<p class="lead">Do ranking de busca e de vendas para a prateleira: 6 perfumes na largada (3 comprados e 3 próprios), mais 4 em duas etapas, com fila para lotes do mês e pré-venda para a faixa D.</p>'
    h += '<h3>Ranking dos candidatos</h3>'
    order = ['sauv', 'cdnim', '212', 'lveb', 'yara', 'asad', 'fakhar', 'sabah', 'hawas', 'khamrah', 'brun', 'p9pm']
    rows = []
    for i, k in enumerate(sorted(order, key=lambda k: -SK[k]['w'])):
        s = SK[k]; e = N['sku_econ'][k]
        br = t_idx(s['tkey'], 'BR'); rs = t_idx(s['tkey'], 'RS')
        rk = PS_RANK.get(PSKEY.get(k, ''), None)
        rows.append([str(i + 1), f'<b>{s["nome"]}</b>' + (f'<br><span class="note">lembra {s["compara"]}</span>' if s.get('compara') else ''), s['linha'], num(br), num(rs), (f'nº {rk}' if rk else 'fora dos 120'),
                     brl(s['cml']), s['tier'], brl(e[5]['price']), f'{brl(e[5]["mg"])} ({pct(e[5]["mgp"], 0)})', STAGE_OF.get(k, '')])
    h += table(['#', 'Perfume', 'Linha', 'Busca BR (Sauvage = 100)', 'Busca RS', 'Vendas no líder', 'Custo por ml', 'Faixa', '5 ml', 'Margem 5 ml', 'Decisão'], rows, align=['c', '', '', 'c', 'c', 'c', 'r', 'c', 'r', 'r', ''], scroll=True, cls='wide')
    h += f'<p class="note">Ordem pelo peso de busca (média de Brasil e RS). Margem por decant = preço − custo do decant − 2,5% de taxa − 3% de reserva, antes da embalagem do pedido e da mão de obra. Frascos próprios entram a preço de reposição. "Lembra" indica a comparação mais citada em guias de perfumaria; não é afirmação da marca e não vai para título ou anúncio {JU}.</p>'
    h += '<h3>Grife e nicho fora da largada: o que fazer com cada um</h3>'
    rows = []
    for nome, linha, preco, ml, fonte, cml, t in N['ref']:
        if t == 'B': dec = 'Fila: entra quando um B sair ou na etapa 3+'
        elif t == 'C': dec = 'Fila: entra se o 5 ml ficar abaixo do líder'
        elif t == 'D': dec = 'Só pré-venda'
        else: dec = 'Fora: só clone ou pré-venda com custo menor'
        if 'Invictus' in nome: dec = f'Fora por enquanto: faixa C ({brl(m.P5["C"])}) acima do líder ({brl(PS5["invictus"])}); buscar frasco de 200 ml'
        if 'Good Girl' in nome: dec = f'Fora: o líder vende o 5 ml a {brl(PS5["goodgirl"])}, abaixo do nosso custo com margem'
        if 'Bleu de Chanel Parfum' in nome: dec = 'Frasco próprio: conteúdo e teste olfativo; 2 ml a R$ 49,90 só para gerar caixa, sem repor'
        if 'Bleu de Chanel EDP' in nome: dec = 'Pré-venda após 60 pedidos (teste do rateio)'
        if 'Sauvage EDP' in nome: dec = 'Fila: alternativa ao Sauvage EDT quando o frasco próprio acabar'
        rows.append([nome, linha, f'{brl(preco)} ({ml} ml)', fonte, brl(cml), ('E (acima da D)' if t == 'E' else t), dec])
    h += table(['Perfume', 'Linha', 'Frasco', 'Fonte do preço', 'Custo por ml', 'Faixa', 'Decisão'], rows, align=['', '', 'r', '', 'r', 'c', ''], scroll=True, cls='wide')
    h += '<h3>Clones: o que dá para afirmar</h3>'
    h += table(['Clone (árabe)', 'Original que costuma ser comparado', 'Preço do original', 'Fonte da comparação', 'Situação no plano'], [
        ['Armaf Club de Nuit Intense Man', 'Creed Aventus', 'R$ 3.320,84 (100 ml)', a(URL['dupe_cdnim'], 'Perfumania, guia de dupes 2026'), 'Etapa 2'],
        ['Lattafa Khamrah', "Kilian Angels' Share", 'não pesquisado', a(URL['scento_khamrah'], 'Scento, guia do Khamrah'), 'Fila'],
        ['Lattafa Asad', 'Dior Sauvage Elixir', 'R$ 1.421,21 (100 ml)', a(URL['scento_sauvage'], 'Scento, dupes do Sauvage Elixir'), 'Etapa 1'],
    ])
    h += f'<p class="note">Outras comparações circulam (Liquid Brun, Hawas, Yara), mas não encontrei fonte para citar; ficam fora do conteúdo até haver referência {VA}. A comparação é conteúdo, não nome de produto (aba Jurídico).</p>'
    h += '<h3>Portfólio por etapa</h3>'
    wide = '<div class="scroll"><table class="wide"><thead><tr><th>Perfume</th><th>Etapa</th><th>Público</th><th>Perfil olfativo</th><th>Frasco e preço de compra</th><th>Fornecedor</th><th>Custo por ml</th><th>Faixa</th><th>2 ml adicional</th><th>5 ml</th><th>10 ml</th><th>Custo do decant 5 / 10 ml</th><th>Margem 5 ml</th><th>Margem 10 ml</th><th>Reposição</th></tr></thead><tbody>'
    prof = {'asad': 'Âmbar especiado (pimenta, baunilha, tabaco)', 'yara': 'Gourmand atalcado (orquídea, baunilha, frutas)', 'lveb': 'Gourmand floral (íris, praliné, baunilha)', 'p9pm': 'Âmbar adocicado (maçã, canela, baunilha)', 'brun': 'Gourmand amadeirado (canela, baunilha, praliné)', 'sauv': 'Aromático fresco (bergamota, pimenta, ambroxan)', 'sabah': 'Floral frutado doce (rosa, frutas vermelhas)', 'cdnim': 'Frutado amadeirado defumado (abacaxi, bétula, âmbar)', '212': 'Especiado fresco (maracujá, menta, couro)', 'fakhar': 'Floral frutado'}
    rep = {'asad': 'Quando restarem 35 ml', 'yara': 'Quando restarem 35 ml', 'lveb': 'Quando restarem 35 ml', 'p9pm': 'Só se vender 20 ml ou mais em 30 dias', 'brun': 'Não repor no 1º trimestre', 'sauv': 'Sauvage EDT 200 ml quando vender 20 ml no mês e o caixa permitir', 'sabah': 'Quando restarem 35 ml', 'cdnim': 'Quando restarem 35 ml', '212': 'Quando restarem 60 ml', 'fakhar': 'Quando restarem 35 ml'}
    for k in ['asad', 'yara', 'lveb', 'p9pm', 'brun', 'sauv', 'sabah', 'cdnim', '212', 'fakhar']:
        s = SK[k]; e = N['sku_econ'][k]
        tag = ' <span class="tag">frasco próprio</span>' if s['proprio'] else ''
        wide += (f'<tr><td><b>{s["nome"]}</b>{tag}</td><td>{STAGE_OF[k]}</td><td>{s["gen"]}</td><td>{prof[k]}</td><td class="r">{brl(s["preco"])} ({s["ml"]} ml)</td><td>{s["fonte"]}</td><td class="r">{brl(s["cml"])}</td><td class="c">{s["tier"]}</td>'
                 f'<td class="r">{brl(e[2]["price"])}</td><td class="r">{brl(e[5]["price"])}</td><td class="r">{brl(e[10]["price"])}</td><td class="r">{brl(e[5]["cost"])} / {brl(e[10]["cost"])}</td>'
                 f'<td class="r">{brl(e[5]["mg"])} ({pct(e[5]["mgp"], 1)})</td><td class="r">{brl(e[10]["mg"])} ({pct(e[10]["mgp"], 1)})</td><td>{rep[k]}</td></tr>')
    wide += '</tbody></table></div>'
    h += wide
    h += '<p class="note">Fica com 5 masculinos, 4 femininos e 1 unissex depois da etapa 3 (o Liquid Brun é o unissex; La Vie Est Belle, Yara, Sabah e Fakhar Rose são os femininos). Preços de compra de 25/11/2026; tabela de distribuidor deve baixar o custo dos árabes ' + VA + '.</p>'
    h += '<h3>O que não vender sozinho</h3>'
    h += table(['Formato', 'Por quê', 'Como usar'], [
        ['2 ml avulso', 'Margem de R$ 3 a R$ 9 por unidade não paga a embalagem do pedido (R$ 3,81) nem a mão de obra', 'Só no Kit Descoberta ou como adicional dentro de outro pedido'],
        ['1 ml', 'Custo de frasco e etiqueta quase igual ao do 2 ml', 'Só como brinde em pedidos a partir de R$ 89,90'],
        ['30 ml ou mais', 'Prende capital, compete com o frasco cheio e consome um terço do frasco de origem', 'Não oferecer; quem quer mais de 20 ml recebe o frasco sob encomenda (fase 2)'],
        ['Faixa D em estoque', 'R$ 9 a R$ 12 por ml; 1 frasco prende mais de R$ 800', 'Só pré-venda'],
        ['Nicho original', 'R$ 14 a R$ 58 por ml; o líder vende abaixo do nosso preço com margem', 'Clone na prateleira; original só em pré-venda, se houver custo menor'],
    ])
    h += '<h3>Fila de entrada</h3>'
    h += f'<p>Ordem: Rasasi Hawas (subiu 129% na busca), 1 Million EDT 200 ml (faixa B, {brl(729.00)}), Lattafa Khamrah (clone de nicho), Versace Eros EDT 200 ml (faixa B), Le Male Le Parfum 200 ml (faixa B), virais do mês (Vulcan Feu, Queen of Arabia). Entra o que o grupo VIP mais pedir; cada entrada exige vaga aberta por um perfume que vendeu menos de 20 ml em 30 dias.</p>'
    h += src(a(URL['trends_rank'], 'Google Trends'), a(URL['ps_api'], 'Perfume Shopping, popularidade e preços'), a(URL['epoca_api'], 'Época Cosméticos'), a('https://m.magazineluiza.com.br/busca/lattafa+arabe/', 'Magalu, Asad'), a('https://m.magazineluiza.com.br/busca/yara/', 'Magalu, Yara'), a('https://m.magazineluiza.com.br/busca/watani+perfume', 'Magalu, Sabah Al Ward'), a('https://m.magazineluiza.com.br/busca/perfumes+arabes/', 'Magalu, Fakhar Rose'), a(URL['drogaraia_bdc'], 'Droga Raia, Bleu de Chanel EDP'), a('https://www.drogasil.com.br/perfume-chanel-bleu-de-chanel-parfum-masculino-100-ml-683814.html', 'Drogasil, Bleu de Chanel Parfum'))
    return h

def p13():
    o = ORIG['p10']
    o = re.sub(r'<div class="pn">.*?</div>\s*$', '', o, flags=re.S)
    o = o.replace('<p class="lead">Perfume só com nota fiscal e, assim que houver volume, direto de distribuidor oficial. Insumos podem vir de marketplace, com amostra antes de lote grande.</p>',
                  '<p class="lead">Perfume só com nota fiscal. Árabe: varejo agora e distribuidor oficial assim que houver volume. Grife: frasco de 200 ml ou refil, comprado em varejista grande, de preferência em data promocional. Insumos de marketplace, com amostra antes de lote grande.</p>')
    new_rows = ('<tr><td>Época Cosméticos (loja e lojistas parceiros)</td><td>Varejista e marketplace</td><td>Sauvage EDT 200 ml R$ 1.002,51; 212 VIP Men 200 ml R$ 718,53; La Vie Est Belle refil 100 ml R$ 654,90; Club de Nuit Intense Man 105 ml R$ 299,90; Khamrah R$ 269,90</td><td>Varejo, com promoções</td><td>1 unidade</td><td>Ver no carrinho</td><td>Exigir do lojista</td><td>Rede grande</td><td>Baixo a médio</td></tr>'
                '<tr><td>Sephora, Beleza na Web, Droga Raia</td><td>Varejista</td><td>Grife (ex.: Bleu de Chanel EDP 100 ml R$ 1.149 na Droga Raia)</td><td>Varejo, com promoções</td><td>1 unidade</td><td>Ver no carrinho</td><td>Sim</td><td>Redes grandes</td><td>Baixo</td></tr>'
                '<tr><td>Frasco de grife muito abaixo do varejo (tester, importação informal, "Paraguai")</td><td>Não verificado</td><td>Grife diversa</td><td>30% a 50% abaixo</td><td>—</td><td>—</td><td>Sem nota</td><td>—</td><td>Alto: não comprar</td></tr>')
    o = o.replace('<tr><td>Pague Menos, Drogasil, Beleza na Web</td>', new_rows + '<tr><td>Pague Menos, Drogasil, Beleza na Web</td>')
    o = o.replace('<h3>Procedimento de verificação de fornecedor e autenticidade</h3>', '<h3>Regras de compra de grife</h3><ul><li>Comprar o maior frasco disponível (200 ml) ou o refil: o custo por ml cai de 15% a 40% (Sauvage EDT: R$ 6,34 por ml no 100 ml e R$ 5,01 no 200 ml).</li><li>Comprar em datas promocionais (Black Friday, Beauty November, Dia do Consumidor) e só com nota fiscal em nome do comprador.</li><li>Não comprar grife para estoque de mais de 60 dias: um frasco de 200 ml de faixa B rende cerca de 38 decants de 5 ml.</li><li>Refil sem válvula facilita o envase e reduz a perda.</li></ul><h3>Procedimento de verificação de fornecedor e autenticidade</h3>')
    o = o.replace('<div class="src"><b>Fontes:</b> ', '<div class="src"><b>Fontes:</b> ' + a(URL['epoca_api'], 'Época Cosméticos (API de catálogo)') + ' &middot; ' + a(URL['drogaraia_bdc'], 'Droga Raia') + ' &middot; ')
    return o
