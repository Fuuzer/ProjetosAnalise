from hb import *

E_BASE = N['esc']['Base'][1]; E_CON = N['esc']['Conservador'][1]; E_OTI = N['esc']['Otimista'][1]
E_ROWS = N['esc']['Base'][0]
B = N['budgets']
ST1, ST2 = N['esc_stage_cost']
INV0 = N['esc_inv0']; PERF0 = N['esc_perf0']
TIER_PRICE_TXT = f"5 ml a {brl(m.P5['A'])} (faixa A), {brl(m.P5['B'])} (B), {brl(m.P5['C'])} (C)"

def p1():
    t = E_BASE
    h = '<h2>Resumo executivo</h2>'
    h += (f'<p class="lead">Vale abrir, e com um portfólio diferente do proposto na versão anterior. Os dados novos (Google Trends, catálogo e ranking de mais vendidos do maior concorrente, preços de frasco no varejo) mostram que a demanda por decant está concentrada em <b>perfumes de grife e clones de nicho</b>, não em árabes "puros". '
          f'A recomendação passa a ser um <b>plano escalonado com teto de R$ 3.000</b>: aporte inicial de <b>{brl(INV0)}</b> (árabes + 1 grife comprada + os 3 frascos que você já tem), com duas etapas de compra liberadas por metas de venda e pagas, de preferência, com o caixa do próprio negócio.</p>')
    h += '<div class="kpis">'
    for v, l in [
        (brl(INV0), 'aporte inicial (teto de R$ 3.000 em etapas)'),
        ('A, B, C e D', 'faixas de preço por custo do perfume; kit varia com a escolha'),
        (f"a partir de {brl(m.BASE['trio'])}", 'Kit Trio (3 × 5 ml); sobe conforme a faixa escolhida'),
        (num(t['orders']), 'pedidos em 6 meses no cenário base'),
        (brl(t['op']), 'lucro operacional em 6 meses (base)'),
        (brl(N['cac_max']), 'CAC máximo por cliente novo'),
    ]:
        h += f'<div><b>{v}</b><span>{l}</span></div>'
    h += '</div>'
    h += '<h3>O que mudou e por quê</h3><ul>'
    h += (f'<li><b>Grife entra, por faixa de preço.</b> A versão anterior excluiu grife porque calculou o Sauvage com frasco de 100 ml a R$ 819 e preço de 5 ml a R$ 59,90. Com frasco de 200 ml (R$ 1.002,51 na Época, R$ 5,01 por ml) e preço de mercado, o 5 ml de Sauvage deixa margem. No maior concorrente, <b>72 dos 100 decants mais vendidos são de grife, 10 de nicho e 16 de árabes</b> {FA}.</li>')
    h += (f'<li><b>Sua hipótese se confirma, com uma ressalva.</b> Decant vende mais quando o frasco é caro: o 5 ml de Sauvage EDP custa 9% do frasco; o 5 ml de Asad custa 21% do frasco, e quem gosta de árabe costuma comprar o frasco inteiro. Nicho original (Aventus, Baccarat Rouge) não fecha conta com custo de varejo; a demanda de nicho entra pelos <b>clones</b> (Club de Nuit Intense Man, Khamrah, Asad) {JU}.</li>')
    h += (f'<li><b>Google Trends medido.</b> Nos últimos 12 meses, no Brasil, os mais buscados da lista foram Invictus, Sauvage, Club de Nuit, 1 Million e 212 VIP. "Perfume árabe" cresceu 43% contra os 12 meses anteriores e já tem cerca de 8 vezes o volume de busca de "decant", que cresceu 32% {FA}.</li>')
    h += (f'<li><b>Kits com preço variável.</b> Preço fixo com grife no cardápio é seleção adversa: um Kit Trio a {brl(m.BASE["trio"])} montado com Sauvage, 212 VIP e La Vie Est Belle dá prejuízo de {brl(-N["fixed_adverse"][1])} por pedido. A regra nova é "a partir de" {brl(m.BASE["trio"])}, com adicional por perfume das faixas B e C.</li>')
    h += (f'<li><b>Orçamento maior ajuda só se comprar grife.</b> Subir de R$ 1.000 para R$ 1.500 colocando mais 2 árabes quase não muda o lucro; colocando La Vie Est Belle no lugar, o lucro de 6 meses do cenário base vai de {brl(B[1000]["res_cases"]["Base"][1]["op"])} para {brl(B[1500]["res_cases"]["Base"][1]["op"])} {ES}.</li>')
    h += (f'<li><b>Concorrentes: copiar a estrutura, eliminar as falhas.</b> Os três maiores têm reclamações de suspeita de falsificação e de atraso; o líder leva 14 dias, em média, para responder no Reclame Aqui. O diferencial continua sendo prova de origem por lote, resposta rápida e entrega local; o que se copia deles é preço por faixa, kits por ocasião, quiz, venda "até a última gota" do frasco aberto e avaliação verificada.</li>')
    h += (f'<li><b>Riscos que continuam na frente:</b> parecer jurídico sobre fracionamento (Anvisa), aceite escrito de transportadora e uso de marca de terceiro na comunicação de clones.</li>')
    h += '</ul>'
    h += '<h3>Números do plano escalonado (6 meses)</h3>'
    rows = []
    for case in ['Conservador', 'Base', 'Otimista']:
        r, tt = N['esc'][case]
        rows.append([('<b>Base</b>' if case == 'Base' else case), num(tt['orders']), brl(tt['rev']), brl(tt['ticket']), brl(tt['op']), brl(tt['cash_end']), brl(tt['owner']), num(tt['hours'])])
    h += table(['Cenário', 'Pedidos', 'Faturamento', 'Ticket médio', 'Lucro operacional', 'Caixa final', 'Capital do dono', 'Horas'], rows, align=['', 'c', 'r', 'r', 'r', 'r', 'r', 'c'])
    h += (f'<p class="note">Volumes são {HI}; preços de compra, preços de concorrentes e dados de busca são {FA} com data de 25/11/2026. "Capital do dono" é o que sai do seu bolso; no conservador, a etapa 3 não é liberada em 6 meses. O caixa final já desconta a recompra de frascos.</p>')
    h += src(a(URL['trends'], 'Google Trends, categorias'), a(URL['ps_api'], 'Perfume Shopping, ranking de popularidade'), a(URL['tabs'], 'Tabs Perfumes'), a(URL['epoca_api'], 'Época Cosméticos, preços de frasco'), a(URL['ra_ps'], 'Reclame Aqui'), 'demais fontes nas abas seguintes')
    return h

def p2():
    h = '<h2>Decisão recomendada</h2>'
    h += (f'<div class="box ok"><b>Abrir com o plano escalonado.</b> Etapa 1 (agora, após o sinal do advogado): insumos + Lattafa Asad, Lattafa Yara e Lancôme La Vie Est Belle, somando {brl(INV0)}, mais os decants dos frascos que você já tem (Afnan 9pm, Liquid Brun e Sauvage EDT). '
          f'Etapa 2 ({brl(ST1)}): Sabah Al Ward e Club de Nuit Intense Man, com 25 pedidos acumulados. Etapa 3 ({brl(ST2)}): 212 VIP Men 200 ml e Fakhar Rose, com 60 pedidos. Teto total de R$ 3.000.</div>')
    rows = [
        ['Modelo', 'Curadoria híbrida: árabes e clones (faixa A) + grife de giro (faixas B e C) + pré-venda para luxo; frasco lacrado sob encomenda na fase 2', f'Concentra a demanda medida (Trends e ranking do líder) e mantém a margem por faixa {JU}'],
        ['Público principal', 'Entusiasta que quer provar grife antes do frasco e curioso de árabe e clone; 20 a 40 anos; Porto Alegre e RS', 'É quem compra decant: o frasco caro é o motivo da compra'],
        ['Produtos de largada', 'Asad, Yara e La Vie Est Belle (comprados) + 9pm, Liquid Brun e Sauvage EDT (frascos próprios)', '3 masculinos, 2 femininos e 1 unissex; 2 grifes entre os 6'],
        ['Preço', f'Faixas por custo do ml: {TIER_PRICE_TXT}; faixa D só em pré-venda', 'O preço acompanha o custo; nenhum perfume vendido com prejuízo'],
        ['Kits', f'Descoberta a partir de {brl(m.BASE["desc"])}, Trio a partir de {brl(m.BASE["trio"])}, Dupla 10 ml a partir de {brl(m.BASE["dupla"])}; adicional por perfume de faixa superior', 'Fixo para árabes, variável quando entra grife'],
        ['Investimento', f'{brl(INV0)} na etapa 1; etapas 2 e 3 ({brl(ST1)} e {brl(ST2)}) com o caixa gerado; aporte extra só se o caixa não cobrir e a meta tiver sido batida', 'Expõe menos capital antes de provar demanda'],
        ['Caixa mínimo', f'{brl(m.CASH_MIN)} sempre; nenhuma compra que deixe o caixa abaixo disso', 'Cobre o DAS e um frete de reposição'],
        ['Canal de largada', 'Instagram + WhatsApp (lista VIP) + link de pagamento; retirada e entrega em Porto Alegre; envio nacional só com aceite escrito', 'Sem tarifa de canal; marketplace exige número da Anvisa'],
        ['Frete', 'Cliente paga; grátis acima de R$ 149 ou na retirada', f'Subsídio de R$ 15 por pedido corta o lucro de 6 meses de {brl(N["sens"][0]["op6"])} para {brl(N["sens"][4]["op6"])}'],
    ]
    h += table(['Decisão', 'Escolha', 'Por quê'], rows)
    h += '<h3>O que fica proibido no início</h3><ul>'
    h += '<li>Comprar nicho original (Aventus, Baccarat Rouge, Delina) para estoque; comprar frasco de grife de 100 ml quando existe o de 200 ml com custo por ml menor; pagar anúncio antes de 10 vendas orgânicas; anunciar em marketplace; caixa personalizada com pedido mínimo de 500 unidades.</li>'
    h += '<li>Usar "réplica", "contratipo", "igualzinho ao" ou "dupe" em título, anúncio pago ou nome de produto. Clone se apresenta pelo próprio nome e pelas notas; a comparação com o original fica para conteúdo orgânico, nos limites da aba Jurídico.</li>'
    h += '<li>Prometer fixação ou projeção em horas, como fazem concorrentes com reclamação de "não fixa".</li></ul>'
    h += '<h3>Condições para interromper ou reformular</h3><ul>'
    h += '<li>Parecer jurídico apontar risco sanitário alto para a venda de fracionado: migrar para a estrutura alternativa (aba Jurídico).</li>'
    h += '<li>Menos de 20 pedidos em 90 dias, ou margem média abaixo de R$ 28 por pedido por 2 meses seguidos.</li>'
    h += '<li>Grife abaixo de 20% do volume vendido depois de 60 dias: a tese de grife não se confirmou; parar na etapa 2 e voltar ao foco em árabes.</li>'
    h += '<li>Nenhuma transportadora aceitar o envio por escrito: operar só em Porto Alegre até resolver.</li></ul>'
    return h

def bench_counts():
    from sec_b import BENCH
    c = {k: sum(1 for x in BENCH if x[0] == k) for k in ['Copiar', 'Eliminar', 'Examinar']}
    return f'A aba <b>Benchmark de serviços</b> avalia {len(BENCH)} serviços: {c["Copiar"]} para copiar, {c["Eliminar"]} para eliminar e {c["Examinar"]} neutros examinados um a um.'

def p3():
    h = '<h2>Respostas às suas perguntas</h2>'
    h += '<p class="lead">As cinco perguntas desta revisão, com a resposta curta e onde está o detalhe.</p>'
    qa = [
        ('Quem são os maiores e o que copiar, eliminar ou examinar?',
         f'A maior loja de decants do país é a Perfume Shopping (desde 2012, diz ter mais de 150 mil clientes e 2.136 decants no catálogo). A Tabs Perfumes (desde 2023, mais de 70 mil clientes) é a que mais inova em serviço. Guido, Casa dos Decants, Gold Glow (farmácias) e combos de marketplace completam o quadro. ' + bench_counts()),
        ('Os kits têm preço fixo? Não deveriam variar com a escolha?',
         f'Na versão anterior, sim, eram fixos, e fazia sentido porque os 5 perfumes custavam de R$ 1,29 a R$ 2,97 por ml. Com grife no cardápio, preço fixo quebra: o cliente escolhe os mais caros e o pedido dá prejuízo (perda de {brl(-N["fixed_adverse"][1])} no Trio com 3 grifes). A regra nova: preço base para árabes e adicional por perfume das faixas B e C. Detalhe na aba <b>Precificação e kits</b>.'),
        ('Pouca variedade: e se o orçamento subir?',
         f'Rodei 5 cenários (R$ 1.000, 1.500, 2.000, 2.500 e 3.000) em 3 níveis de demanda. Conclusão: o que aumenta o resultado é <b>colocar grife</b>, não mais árabes. O plano recomendado chega a 10 perfumes (6 na largada + 4 nas etapas 2 e 3) com aporte inicial de {brl(INV0)} e teto de R$ 3.000. Detalhe na aba <b>Cenários de R$ 1.000 a R$ 3.000</b>.'),
        ('O que o Google Trends mostra? Sauvage, Bleu de Chanel e Aventus deveriam estar?',
         'Sim para Sauvage (2º mais buscado no Brasil e no RS na lista medida; o Sauvage EDP é o decant mais vendido do líder e o EDT, o 9º). Bleu de Chanel aparece no meio da lista e o EDP custa R$ 11,49 por ml: entra só em pré-venda (faixa D). Aventus original custa R$ 33 por ml no varejo e o líder vende o 5 ml a R$ 256: a demanda de Aventus entra pelo Club de Nuit Intense Man, 3º mais buscado da lista. Detalhe na aba <b>Google Trends</b>.'),
        ('Decant é comprado para testar antes do frasco caro?',
         'Os dados apoiam: grife e nicho são 82% dos 100 decants mais vendidos do líder; o próprio líder vende o decant como "prove antes de comprar o frasco"; e as buscas por "contratipo" giram em torno de grife (Delina, Bleu de Chanel, La Vie Est Belle, Good Girl). A ressalva: em árabe, o frasco é barato e o decant compete com ele. Detalhe na aba <b>Cliente e posicionamento</b>.'),
    ]
    h += '<dl class="qa">' + ''.join(f'<dt>{q}</dt><dd>{a_}</dd>' for q, a_ in qa) + '</dl>'
    h += '<h3>O que mudou em cada aba</h3>'
    rows = [
        ['Resumo, Decisão, Respostas executivas, Se eu estivesse começando', 'Reescritas para o plano escalonado com grife'],
        ['Google Trends, Benchmark de serviços, Cenários de R$ 1.000 a R$ 3.000', 'Abas novas'],
        ['Metodologia', 'Trends acessado; API pública do catálogo do líder; limites revistos'],
        ['Mercado, Concorrência, Cliente', 'Dados de busca, ranking de vendas do líder, preços por tamanho, Reclame Aqui atualizado'],
        ['Modelo de negócio, Portfólio, Fornecedores', 'Grife reavaliada; ranking com peso de busca; fontes de frasco de 200 ml'],
        ['Precificação e kits', 'Faixas A a D; kits "a partir de"; prova da seleção adversa'],
        ['Projeções, Indicadores, Riscos, Plano de ação, Lista de compras, Decisões', 'Recalculadas no modelo novo'],
        ['Canais, Operação, Jurídico, Marca, Marketing, Retenção, Checklist', 'Ajustes pontuais: clones, pré-venda, "até a última gota", textos'],
    ]
    h += table(['Abas', 'Mudança'], rows)
    return h

def p4():
    o = ORIG['p3']
    o = o.replace('<h2>Auditoria do estudo anterior</h2>', '<h2>Auditoria das versões anteriores</h2>')
    o = o.replace('<p class="lead">O estudo anterior acertou', '<h3>Versão 1 contra o primeiro estudo (mantido para referência)</h3><p class="lead">O estudo anterior acertou')
    o = re.sub(r'<div class="pn">.*?</div>\s*$', '', o, flags=re.S)
    h = o.split('<div class="src">')[0]
    src_old = '<div class="src">' + o.split('<div class="src">')[1] if '<div class="src">' in o else ''
    new = '<h3>Versão 2 contra a versão 1 (esta revisão)</h3>'
    rows = [
        ['1', '"Grife não entra": Sauvage EDT deixa R$ 10,43 e Bleu de Chanel Parfum dá prejuízo', 'Conta feita com frasco de 100 ml a preço cheio (R$ 8,19/ml) e 5 ml a R$ 59,90; ignorou o frasco de 200 ml e o preço do líder (R$ 68 a R$ 79,50)', 'Grife entra por faixa: Sauvage EDT 200 ml a R$ 5,01/ml, 5 ml a R$ 49,90 (faixa B); Bleu de Chanel Parfum segue fora (R$ 21,33/ml)'],
        ['2', '"Volume de busca: não encontrado"', 'Google Trends não foi acessado', 'Trends medido: categorias em 5 anos, ranking de 62 perfumes no Brasil e no RS, buscas relacionadas e em alta'],
        ['3', 'Preço único por formato', 'Funciona só com custo por ml parecido; com grife, o cliente escolhe o mais caro', 'Faixas A a D e kits "a partir de"'],
        ['4', 'Portfólio de 5 árabes', 'Deixou fora o 3º perfume mais buscado (Club de Nuit) e toda a grife; Asad caiu 29% no Brasil e 64% no RS entre o 1º e o último trimestre', 'Até 11 perfumes, com 3 grifes, por etapas'],
        ['5', 'Concorrência descrita por nome e reputação', 'Sem preço por tamanho, sem lista de serviços, sem dado de vendas', 'Catálogo e ranking do líder pela API pública; 30 serviços avaliados'],
        ['6', 'Guido Decants "Bom (7,8), 110 reclamações"', 'Dado antigo', 'Reclame Aqui de mai a out/2026: nota 8,5 ("Ótimo"), 31 reclamações'],
        ['7', 'Teto de R$ 1.000 como restrição fixa', 'O pedido atual pede cenários até R$ 3.000', '5 orçamentos × 3 demandas × 3 elasticidades'],
        ['8', 'Ticket médio de R$ 79,38 (base)', 'Sem grife', f'Ticket de {brl(E_BASE["ticket"])} no plano escalonado (base) {ES}'],
        ['9', 'Payback "em caixa" no mês 2', 'Critério favorecia o caixa porque o estoque inicial ainda não tinha sido recomprado', 'Payback = mês em que o lucro operacional acumulado cobre o capital do dono'],
    ]
    new += table(['#', 'O que a versão 1 dizia', 'Problema', 'Correção nesta versão'], rows)
    new += f'<p class="note">O que se manteve da versão 1: foco em prova de origem por lote, venda local primeiro, frete pago pelo cliente, parecer jurídico antes de comprar perfume, 2 ml só em kit ou como adicional.</p>'
    return new + h + src_old

def p5():
    h = '<h2>Metodologia e fontes</h2>'
    h += '<h3>Como os dados foram levantados</h3><ul>'
    h += f'<li><b>Google Trends:</b> consultado em 25/11/2026 pela interface pública (biblioteca pytrends), Brasil e Rio Grande do Sul, 12 meses e 5 anos. Para comparar mais de 5 termos, todos os lotes trazem "bleu de chanel" como âncora e os valores são reescalados por ela; nesta versão, os índices aparecem com Sauvage = 100.</li>'
    h += '<li><b>Concorrentes:</b> catálogo completo e ranking de popularidade da Perfume Shopping pela API pública da loja (WooCommerce Store API), com preço de cada tamanho dos 120 mais vendidos; páginas de busca e da home da Tabs Perfumes; Reclame Aqui por resumos de busca.</li>'
    h += '<li><b>Preço de frasco:</b> API pública de catálogo da Época Cosméticos (VTEX), preços com estoque em 25/11/2026; preços da versão anterior (Magalu, Pague Menos, Drogasil) mantidos onde não houve dado novo.</li>'
    h += '<li><b>Referências internacionais:</b> Scentbird e Scent Split (sites e páginas de avaliação).</li>'
    h += '<li><b>Modelo financeiro:</b> script em Python com premissas explícitas; todas as tabelas numéricas desta versão saem dele.</li></ul>'
    h += '<h3>Limites honestos</h3><ul>'
    h += '<li><b>Reclame Aqui, Magalu, Sephora, Beleza na Web, Drogasil e Fragrantica</b> bloquearam a leitura automática (proteção anti-robô). Não contornei o bloqueio: os dados de Reclame Aqui vêm de resumos de busca e podem variar conforme a data de captura.</li>'
    h += '<li><b>Trends mede interesse relativo, não volume.</b> Termos ambíguos ("invictus" também é filme, "1 million" é genérico, "delina" é nome próprio) ficam inflados; a tabela sinaliza cada caso.</li>'
    h += '<li><b>Ranking do líder</b> é a ordenação "popularidade" da própria loja (vendas acumuladas); não traz unidades nem período.</li>'
    h += '<li><b>Custo de grife no varejo</b> é maior que o de lojas grandes: o líder vende Good Girl 5 ml a R$ 66,40, abaixo do nosso custo de reposição. Itens assim ficam de fora até haver tabela de distribuidor.</li>'
    h += '<li>Não verifiquei @ no Instagram, domínio ou INPI; caixa kraft em pacote de 20, cartões e kit de envase seguem estimados.</li></ul>'
    h += '<h3>Legenda usada no documento</h3>'
    h += f'<p>{FA} dado com fonte. {ES} número calculado ou aproximado sem fonte direta. {HI} premissa de comportamento a testar. {JU} opinião fundamentada. {VA} depende de checagem externa antes de agir.</p>'
    h += '<h3>Premissas centrais do modelo</h3>'
    rows = [
        ['Perda na transferência', '5% (sensibilidade com 10% e 15%)', HI],
        ['Taxa de pagamento média', '2,5% (60% Pix sem taxa, 40% cartão)', ES],
        ['Reserva para perdas, vazamentos, reenvios e devoluções', '3% da receita', HI],
        ['Tempo de operação', '4 min por decant + 5 min por pedido', HI],
        ['Valor da hora do dono', 'R$ 25', JU],
        ['Custos fixos', 'R$ 112,05 por mês (DAS R$ 82,05 + R$ 30)', FA + ' + ' + ES],
        ['Pedidos por mês (base)', '12, 18, 22, 25, 28, 30 com o portfólio da versão 1, ajustados pelo catálogo (linha abaixo)', HI],
        ['Efeito do catálogo na demanda', 'Pedidos × (peso de busca do catálogo disponível ÷ peso do catálogo da versão 1)<sup>0,3</sup>; sensibilidade com 0 e 0,5', HI],
        ['Peso de busca de cada perfume', 'Média do índice do Trends no Brasil e no RS, em unidades de Bleu de Chanel', FA + ' + ' + ES],
        ['Escolha do perfume dentro do pedido', 'Proporcional ao peso de busca entre os perfumes em estoque', HI],
        ['Faixa de preço', 'Maior custo por ml que mantém 30% de margem no 5 ml: A até R$ 3,69; B até R$ 5,53; C até R$ 7,98; D até R$ 11,66; acima disso, só pré-venda. Grife começa na B', JU],
        ['Frascos próprios (9pm, Liquid Brun, Sauvage EDT)', '40 ml úteis cada; custo pelo preço de reposição', VA],
        ['Reposição', 'Compra quando o estoque não cobre 1,5 mês, se o caixa ficar acima de R$ 150; 9pm, Liquid Brun e Sauvage só se venderem 20 ml ou mais no mês', JU],
        ['Frete', 'Pago pelo cliente (subsídio testado na sensibilidade)', JU],
    ]
    h += table(['Premissa', 'Valor', 'Tipo'], rows)
    h += '<h3>Fórmulas</h3>'
    h += ('<p class="formula">Custo do decant = ml × custo do ml ÷ (1 − perda) + frasco + rótulo e lacre<br>'
          'Preço do kit = preço base + Σ adicional da faixa de cada perfume escolhido<br>'
          'Margem de contribuição do pedido = preço − perfume − frascos − rótulos − brinde − embalagem do pedido − 2,5% × preço − 3% × preço − frete subsidiado<br>'
          'Lucro do pedido = margem de contribuição − mão de obra − CAC − fixos rateados<br>'
          'Teto da faixa (custo por ml) = (preço do 5 ml × (1 − 2,5% − 3% − 30%) − frasco − rótulo) × (1 − perda) ÷ 5<br>'
          'Índice Trends (Sauvage = 100) = média semanal de 12 meses do termo ÷ média do Sauvage × 100</p>')
    h += '<p class="note">As fontes, com links, ficam no rodapé de cada aba. Todos os links foram consultados em 25/11/2026.</p>'
    return h

def p6():
    o = ORIG['p5']
    o = re.sub(r'<div class="pn">.*?</div>\s*$', '', o, flags=re.S)
    # remove o bloco "Últimos 90 dias" e a tabela de demanda por perfume; substitui por versões novas
    i1 = o.index('<h3>Últimos 90 dias')
    i2 = o.index('<h3>Sazonalidade')
    top = o[:i1]
    rest = o[i2:]
    top = top.replace('<p class="lead">O perfume árabe é a categoria que mais cresce na perfumaria brasileira, e o decant virou a porta de entrada barata. O mercado é real; o que está saturado é o produto, não a demanda.</p>',
                      '<p class="lead">O perfume árabe é a categoria de busca que mais cresce, mas quem compra decant procura sobretudo grife. As duas coisas convivem: o árabe traz o público novo; a grife paga a conta do decant.</p>')
    import pandas as pd
    df = pd.read_csv(os.path.join(D, 'trends/cat5y_BR.csv'), parse_dates=['date'], index_col='date')
    dr = pd.read_csv(os.path.join(D, 'trends/cat5y_RS.csv'), parse_dates=['date'], index_col='date')
    yb = df.groupby(df.index.year).mean(); yr = dr.groupby(dr.index.year).mean()
    chg = (df.iloc[-52:].mean() / df.iloc[-104:-52].mean() - 1)
    chr_ = (dr.iloc[-52:].mean() / dr.iloc[-104:-52].mean() - 1)
    cols = ['decant', 'perfume arabe', 'perfume de nicho', 'contratipo', 'perfume importado']
    lab = {'decant': '"decant"', 'perfume arabe': '"perfume árabe"', 'perfume de nicho': '"perfume de nicho"', 'contratipo': '"contratipo"', 'perfume importado': '"perfume importado"'}
    rows = []
    for c in cols:
        rr = [lab[c]] + [num(yb.loc[y, c], 1) for y in range(2021, 2027)]
        cb = chg[c]; cr = chr_[c]
        rr += [('+' if cb >= 0 else '') + pct(cb), ('n/d' if cr != cr or cr == float('inf') else ('+' if cr >= 0 else '') + pct(cr))]
        rows.append(rr)
    blk = '<h3>Busca por categoria no Google (Brasil, 5 anos)</h3>'
    blk += table(['Termo', '2021', '2022', '2023', '2024', '2025', '2026*', '12 meses contra 12 anteriores (BR)', 'Idem (RS)'], rows, align=['', 'c', 'c', 'c', 'c', 'c', 'c', 'r', 'r'], scroll=True)
    blk += (f'<p class="note">Índice do Google Trends com os 5 termos na mesma consulta (100 = maior semana do período). *2026 até 22/11. "Perfume árabe" saiu de quase zero em 2022 para o maior volume da cesta, cerca de 8 vezes o de "decant". "Perfume importado" está estável ou em queda: o interesse migrou para árabe e nicho {FA}.</p>')
    blk += '<h3>Últimos 90 dias, últimos 30 dias e mês atual</h3><ul>'
    blk += f'<li><b>Set a nov/2026 (90 dias):</b> imprensa trata o decant como tendência e o perfume como "nova paixão" do brasileiro. No Trends, "decant" cresceu 32% no Brasil e 119% no RS na comparação de 12 meses {FA}.</li>'
    blk += f'<li><b>Out e nov/2026 (30 dias):</b> buscas em alta ligadas a "perfume árabe": Queen of Arabia (+1.750%), Vulcan Feu (+700%), Liquid Brun (+250%), Club de Nuit Intense Man (+80%). Também sobem apelidos visuais ("perfume da abelha", "da cobra", "do pavão", "da fada"): sinal de público iniciante, que busca pelo frasco e não pelo nome {FA}.</li>'
    blk += f'<li><b>Mês atual:</b> Black Friday em 27/11/2026. O líder roda cupom de 8% e cashback; o frasco cheio fica mais barato, o que reduz a vantagem do decant de árabe e aumenta a do decant de grife. Não é semana para lançar; pode ser semana para comprar o primeiro frasco de grife, se o parecer jurídico já tiver vindo {JU}.</li>'
    blk += '</ul>'
    blk += '<h3>Demanda por perfume (evidência pública)</h3>'
    dem = [
        ['Dior Sauvage', '2º mais buscado no Brasil e no RS na lista medida; EDP é o nº 1 em vendas no líder e EDT o nº 9', 'Grife de maior giro; entra pelo frasco próprio e depois pelo 200 ml'],
        ['Armaf Club de Nuit Intense Man', '3º mais buscado no Brasil (linha inteira); nº 7 em vendas no líder; "club de nuit intense man" em alta (+80%)', 'Clone mais procurado; serve a demanda de Aventus'],
        ['Paco Rabanne Invictus, 1 Million, 212 VIP', 'Topo do Trends (termos com ambiguidade); 212 VIP Black nº 4 no líder', 'Grife de giro; 212 VIP Men 200 ml entra na etapa 3'],
        ['Lancôme La Vie Est Belle', 'Feminino mais buscado da lista (6º geral); L\'Eau de Parfum nº 25 no líder', 'Grife feminina da etapa 1'],
        ['Lattafa Asad e Yara', 'Árabes mais buscados depois do Club de Nuit; Asad nº 17 e Yara nº 67 no líder; Asad em queda no RS', 'Base árabe da etapa 1'],
        ['Al Wataniah Sabah Al Ward, Lattafa Fakhar', 'Meio da lista; Fakhar Rose nº 45 e Sabah nº 65 no líder', 'Etapas 2 e 3'],
        ['Rasasi Hawas', 'Subiu 129% no Brasil entre o 1º e o último trimestre', 'Fila: candidato forte'],
        ['Creed Aventus, PDM Delina, MFK Baccarat Rouge', 'Aventus nº 2 e Delina nº 69 no líder; buscas de "contratipo" citam Delina', 'Só clone ou pré-venda: custo de R$ 33 a R$ 58 por ml'],
        ['Afnan 9pm', 'Pouca busca no Trends (termo ambíguo); fora dos 120 mais vendidos do líder', 'Frasco próprio; não repor sem pedido'],
    ]
    blk += table(['Perfume', 'Evidência', 'Leitura'], dem)
    rest = rest.replace('Lançar o 6º perfume (âmbar)', 'Lote do mês: âmbar ou gourmand (ex.: Khamrah)')
    rest = rest.replace('<div class="src"><b>Fontes:</b> links na tabela', '<div class="src"><b>Fontes:</b> ' + a(URL['trends'], 'Google Trends, categorias') + ' &middot; ' + a(URL['trends_rel'], 'Trends, buscas relacionadas') + ' &middot; ' + a(URL['ps_api'], 'Perfume Shopping, popularidade') + ' &middot; links na tabela')
    return top + blk + rest

def p7():
    h = '<h2>Google Trends: o que o brasileiro procura</h2>'
    h += '<p class="lead">Medi 62 perfumes (50 no ranking abaixo e 12 em consulta complementar) e 5 categorias no Brasil e no RS. Grife lidera, o clone Club de Nuit está colado nela e os árabes "puros" ficam no meio da tabela. Índice com Sauvage = 100 (média de 12 meses).</p>'
    rb = trends_rank('BR')
    vmax = max(v for _, v in rb)
    rows = []
    for i, (k, v) in enumerate(rb[:30]):
        rs = t_idx(k, 'RS')
        ch = t_chg(k, 'BR') if k != 'Chanel Bleu de Chanel' else None
        lin = 'Grife' if k == 'Chanel Bleu de Chanel' else linha_of(k)
        nm = 'Chanel Bleu de Chanel (âncora)' if k == 'Chanel Bleu de Chanel' else TNAME.get(k, k)
        if k in AMBIG: nm += f' <span class="tag">{AMBIG[k]}</span>'
        rows.append([str(i + 1), nm, lin, bar(v, vmax, num(v)), num(rs), ('' if ch is None else (('+' if ch >= 0 else '') + pct(ch)))])
    h += '<h3>Ranking no Brasil (30 primeiros)</h3>'
    h += table(['#', 'Perfume', 'Linha', 'Índice BR (Sauvage = 100)', 'Índice RS', 'Último trimestre contra o 1º (BR)'], rows, align=['c', '', '', '', 'c', 'r'], scroll=True)
    # resumo por linha
    import collections
    agg = collections.defaultdict(list)
    for k, v in rb:
        agg['Grife' if k == 'Chanel Bleu de Chanel' else linha_of(k)].append(v)
    top20 = collections.Counter(('Grife' if k == 'Chanel Bleu de Chanel' else linha_of(k)) for k, _ in rb[:20])
    h += '<h3>Leitura por linha</h3>'
    h += table(['Linha', 'Perfumes medidos', 'Entre os 20 mais buscados', 'Soma do índice', 'Mais buscado'],
               [[l, str(len(agg[l])), str(top20.get(l, 0)), num(sum(agg[l])), TNAME.get(next(k for k, v in rb if (('Grife' if k == 'Chanel Bleu de Chanel' else linha_of(k)) == l)), '')] for l in ['Grife', 'Árabe', 'Nicho']], align=['', 'c', 'c', 'r', ''])
    h += '<h3>Ranking no RS (15 primeiros)</h3>'
    rr = trends_rank('RS')
    vmr = max(v for _, v in rr)
    rows = [[str(i + 1), TNAME.get(k, 'Chanel Bleu de Chanel (âncora)' if k == 'Chanel Bleu de Chanel' else k), ('Grife' if k == 'Chanel Bleu de Chanel' else linha_of(k)), bar(v, vmr, num(v)), ('' if t_chg(k, 'RS') is None or k == 'Chanel Bleu de Chanel' else (('+' if t_chg(k, 'RS') >= 0 else '') + pct(t_chg(k, 'RS'))))] for i, (k, v) in enumerate(rr[:15])]
    h += table(['#', 'Perfume', 'Linha', 'Índice RS (Sauvage = 100)', 'Último trimestre contra o 1º (RS)'], rows, align=['c', '', '', '', 'r'], scroll=True)
    h += f'<p class="note">No RS a grife pesa ainda mais: Invictus, Sauvage, 1 Million e 212 VIP vêm antes do primeiro árabe (Club de Nuit). Asad caiu 64% entre o 1º e o último trimestre no RS. Volumes baixos no RS deixam vários árabes com índice próximo de zero {FA}.</p>'
    h += '<h3>Buscas relacionadas (Brasil, 12 meses)</h3>'
    rel = [
        ['"decant"', 'perfume decant (100), decant de perfume (30), decant perfumes (21), decant perfume árabe (6), the king of decant (6), decant in the box (6), decant perfume original (4), guido decant (4)', '—', 'Quem busca decant também busca nome de loja e "original": confiança é o critério de escolha'],
        ['"perfume árabe"', 'feminino árabe (100), masculino árabe (60), lattafa (37), yara (22), asad (18), sabah (17), "cobra" (13), melhor perfume árabe (12), club de nuit (8)', 'Queen of Arabia (+1.750%), Vulcan Feu (+700%), "fada" (+650%), "abelha" (+600%), Liquid Brun (+250%), "pavão" (+180%), Club de Nuit Intense Man (+80%)', 'Público novo, que escolhe pelo frasco e pelo viral'],
        ['"contratipo"', 'contratipo Delina, contratipo Bleu de Chanel, La Vie Est Belle contratipo, contratipo Good Girl', 'perguntas "é contratipo de qual perfume"', 'A referência de quem busca clone é sempre um perfume de grife ou nicho'],
        ['"perfume importado"', 'feminino, masculino, wepink, árabe, 212, Chanel', 'wepink (+170%), perfume árabe (+70%), Delina (+70%), Burberry Goddess (+60%)', 'Concorrência de marcas nacionais baratas no topo do funil'],
        ['"perfume feminino"', 'feminino árabe (100), boticário, natura, importado', 'perfume de nicho feminino (+120%), lattafa feminino (+50%)', 'Nicho feminino começa a aparecer'],
    ]
    h += table(['Termo pesquisado', 'Mais buscados junto', 'Em alta', 'Leitura'], rel)
    h += '<h3>Onde se busca (índice por estado, 12 meses)</h3>'
    h += table(['Termo', 'Estados com mais interesse', 'RS'], [
        ['"decant"', 'SP (100), DF (96), PR (91), SC (89), MG (86), ES (82)', '59'],
        ['"perfume árabe"', 'MS (100), PR (99), MT (86), RO (76), SP (72), GO (71)', '46'],
        ['"perfume masculino"', 'SP (100), PR (93), GO (91), MT (87), MG (87)', '69'],
        ['"perfume feminino"', 'PR (100), SP (100), GO (95), MG (93), DF (91)', '75'],
    ], align=['', '', 'c'])
    h += f'<p class="note">O RS tem interesse abaixo da média em "decant" e "perfume árabe": a venda local sozinha não sustenta volume. O envio nacional (com aceite da transportadora) é condição para passar do cenário base {JU}.</p>'
    h += '<h3>Conclusões para o plano</h3><ol>'
    h += '<li>Grife e clone de grife puxam a busca; o portfólio precisa de pelo menos 1 grife masculina (Sauvage) e 1 feminina (La Vie Est Belle) desde o início.</li>'
    h += '<li>Club de Nuit Intense Man é o árabe com mais busca e serve quem quer Aventus: entra na etapa 2.</li>'
    h += '<li>Asad e Yara continuam fortes no Brasil, mas Asad perde fôlego; não comprar 2 frascos de Asad de uma vez.</li>'
    h += '<li>Lançamentos virais (Queen of Arabia, Vulcan Feu, Hawas) sobem rápido e caem rápido: tratar como "lote do mês", 1 frasco por vez.</li>'
    h += '<li>"Original" aparece junto de "decant": a prova de origem por lote continua sendo o diferencial que o cliente procura.</li></ol>'
    h += src(a(URL['trends_rank'], 'Google Trends, ranking com âncora Bleu de Chanel'), a(URL['trends_rel'], 'Trends, "perfume árabe"'), a(URL['trends_dec'], 'Trends, "decant"'), a(URL['trends'], 'Trends, categorias 5 anos'))
    return h

def p8():
    h = '<h2>Concorrência</h2>'
    h += '<p class="lead">O líder vende volume e grife; a Tabs vende serviço; os pequenos vendem preço. Todos têm reclamações de origem e entrega. O espaço livre continua sendo curadoria com prova de origem verificável, resposta rápida e entrega local, agora com grife no cardápio.</p>'
    rows = [
        ['Perfume Shopping', 'Maior loja de decants (desde 2012; diz ter mais de 150 mil clientes)', '2.136 decants (846 grife, 578 nicho, 170 árabes); 1, 2,5, 5, 8, 10 e 30 ml; preço por perfume; kits por ocasião; cashback; frete grátis acima de R$ 199', 'Catálogo, ranking de vendas, preço decrescente por ml', 'Reclame Aqui sem reputação: 22 reclamações (mai–out/2026), 77% respondidas, resposta média de 14 dias; temas: não recebido, "não parece original", atraso, não fixa'],
        ['Tabs Perfumes', 'Loja de decants em Campinas (desde 2023; mais de 70 mil clientes)', '2, 5, 10 e 30 ml e "30 ml no frasco original"; quiz; navegação por ocasião e clima; "Até a Última Gota" (venda por ml de frasco aberto ao vivo); Clube Tabs (assinatura); entrega no mesmo dia em Campinas', 'Serviço e conteúdo; 4,8 estrelas em 569 avaliações', 'Reclame Aqui nota 7,8 a 7,9; temas: atraso, vazamento e quebra, suspeita de falsificação, "não existe selo"'],
        ['Guido Decants', 'Loja de decants', 'Decants de grife e nicho', 'Reclame Aqui 8,5 ("Ótimo") de mai a out/2026, 31 reclamações, todas respondidas', 'Atraso; reclamações antigas de falsificação'],
        ['Casa dos Decants', 'Loja de decants', 'Decants', 'Volume', '190 reclamações no 1º semestre de 2026, sem reputação calculada; não entrega e produto adulterado'],
        ['Gold Glow', 'Decants em marketplace de farmácia (Drogasil, Droga Raia)', 'Creed Aventus 8 ml a R$ 402,32; Orientica 1 ml a R$ 16', 'Confiança do canal', 'Preço por ml alto'],
        ['Combos de marketplace', 'Mercado Livre e Magalu', '3 × 5 ml a R$ 60; kit Yara + Fakhar + Sabah a R$ 89,24 no Pix', 'Preço', 'Sem marca e sem prova de origem'],
        ['Âmbar Perfumes, Samadi, Lattafa Brasil', 'Lojas de árabes lacrados', 'Frasco cheio original', 'Concorrem com o "upgrade" para o frasco', 'Não vendem teste barato'],
        ['Scentbird (EUA)', 'Assinatura de decants', 'US$ 17,95 por mês por 8 ml; fila de perfumes; estojo reutilizável; cancela quando quiser', 'Recorrência', 'Compromisso mensal; catálogo de grife'],
        ['Scent Split (EUA)', 'Decants de grife e nicho', 'Garantia de autenticidade; decant feito no pedido; frete grátis acima de US$ 70; programa de afiliados; nível VIP', 'Escala e programa de afiliados', 'Avaliações citam vazamento e tamanho menor que o da foto'],
    ]
    h += table(['Concorrente', 'Tipo', 'Oferta observada', 'Força', 'Ponto fraco observado'], rows, scroll=True, cls='wide')
    h += '<h3>O que o líder vende: 100 decants mais vendidos</h3>'
    h += table(['Corte do ranking', 'Grife', 'Nicho', 'Árabes', 'Acessórios'], [
        ['10 primeiros', '6', '2', '1', '1'], ['20 primeiros', '14', '3', '2', '1'], ['50 primeiros', '37', '6', '5', '2'], ['100 primeiros', '72', '10', '16', '2']], align=['', 'c', 'c', 'c', 'c'])
    h += f'<p class="note">Top 5: Sauvage EDP, Creed Aventus, Acqua di Giò, 212 VIP Black e um acessório ("PS Booster"). Primeiro árabe: Club de Nuit Intense Man (nº 7). Mediana do 5 ml: grife R$ 67,60, nicho R$ 256,00, árabe R$ 59,70 {FA}.</p>'
    h += '<h3>Preço do decant: líder, Tabs e este plano</h3>'
    comp = [
        ('Dior Sauvage EDT', 'sauv_edt', 'sauv'), ('Dior Sauvage EDP', 'sauv_edp', None), ('Lancôme La Vie Est Belle', 'lveb', 'lveb'),
        ('Carolina Herrera 212 VIP Men', '212men', '212'), ('Armaf Club de Nuit Intense Man', 'cdnim', 'cdnim'), ('Lattafa Asad', 'asad', 'asad'),
        ('Lattafa Yara', 'yara', 'yara'), ('Al Wataniah Sabah Al Ward', 'sabah', 'sabah'), ('Lattafa Fakhar Rose', 'fakhar', 'fakhar'),
        ('French Avenue Liquid Brun', 'brun', 'brun'), ('Lattafa Khamrah', 'khamrah', None), ('Creed Aventus', 'aventus', None),
    ]
    rows = []
    for nome, pk, sk in comp:
        ours5 = brl(m.P5[SK[sk]['tier']]) + f' ({SK[sk]["tier"]})' if sk else ('R$ 69,90 (C, frasco de 200 ml)' if pk == 'sauv_edp' else 'só clone ou pré-venda')
        if pk == 'khamrah': ours5 = brl(m.P5['A']) + ' (A)'
        rows.append([nome, brl(PS5[pk]) if pk in PS5 else '—', brl(TABS2[pk]) if pk in TABS2 else '—', ours5])
    h += table(['Perfume', 'Líder: 5 ml', 'Tabs: 2 ml', 'Este plano: 5 ml (faixa)'], rows, align=['', 'r', 'r', 'r'])
    h += f'<p class="note">O plano fica abaixo do líder em todos os itens e perto da Tabs no custo por ml. O espaço de preço existe porque o líder cobra 3 a 5 vezes o custo do ml em árabe (Asad: R$ 56,70 por 5 ml de um frasco de R$ 185 a R$ 340) {FA} + {JU}.</p>'
    h += '<h3>Mapa de posição</h3><ul>'
    h += '<li><b>Preço baixo, sem marca:</b> combos de marketplace. Não competir aqui.</li>'
    h += '<li><b>Catálogo gigante:</b> Perfume Shopping. Não competir em amplitude; competir em curadoria e preço por faixa.</li>'
    h += '<li><b>Serviço e conteúdo:</b> Tabs. Copiar o que funciona (quiz, ocasião, frasco aberto ao vivo) com operação local.</li>'
    h += '<li><b>Espaço livre:</b> prova de origem verificável por lote, resposta em até 2 horas e entrega no mesmo dia em Porto Alegre, com grife e clones a preço abaixo do líder.</li></ul>'
    h += '<h3>Diferenciação concreta e difícil de copiar</h3><ol>'
    h += '<li><b>Ficha de lote pública.</b> Vídeo de abertura do lacre, foto da nota (dados cobertos), lote e data; o rótulo do decant traz o código da ficha. Responde à reclamação nº 1 dos concorrentes ("não parece original").</li>'
    h += '<li><b>Entrega no mesmo dia em Porto Alegre e retirada combinada.</b></li>'
    h += '<li><b>Garantia de acerto no Kit Descoberta.</b> Se nenhum agradar, o cliente escolhe outro 2 ml grátis no próximo pedido.</li>'
    h += '<li><b>Diagnóstico olfativo em 4 perguntas pelo WhatsApp</b>, com resposta de pessoa em até 2 horas.</li>'
    h += '<li><b>Mapa de clones honesto:</b> conteúdo que compara o clone com o original nas notas, inclusive onde ele não se parece. Concorrente grande evita esse tipo de conteúdo por risco de marca.</li></ol>'
    h += src(a(URL['ps'], 'Perfume Shopping'), a(URL['ps_api'], 'API de popularidade'), a(URL['tabs'], 'Tabs Perfumes'), a(URL['ra_ps'], 'Reclame Aqui, Perfume Shopping'), a(URL['ra_tabs'], 'Reclame Aqui, Tabs'), a(URL['ra_guido'], 'Reclame Aqui, Guido'), a(URL['ra_casa'], 'Reclame Aqui, Casa dos Decants'), a(URL['drogaraia_aventus'], 'Droga Raia, Gold Glow'), a(URL['scentbird'], 'Scentbird'), a(URL['scentsplit'], 'Scent Split'), a('https://lista.mercadolivre.com.br/Asad%20Asad%20Attar%20Roll%20On', 'Mercado Livre, combos'), a('https://jornaldebrasilia.com.br/brasil-7/8-lojas-online-para-comprar-perfume-arabe-feminino-original/', 'Jornal de Brasília'))
    return h
