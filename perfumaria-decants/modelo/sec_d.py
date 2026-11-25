from hb import *
from sec_a import E_BASE, E_CON, E_OTI, E_ROWS, B, ST1, ST2, INV0, PERF0

def strip_pn(o):
    return re.sub(r'<div class="pn">.*?</div>\s*$', '', o, flags=re.S)

def R(o, old, new):
    assert old in o, 'não encontrado: ' + old[:80]
    return o.replace(old, new)

def RR(o, pattern, new):
    o2, n = re.subn(pattern, new, o, flags=re.S)
    assert n == 1, 'regex não casou: ' + pattern[:60]
    return o2

def p16():
    o = strip_pn(ORIG['p13'])
    o = R(o, '<p class="lead">Começar onde vender não custa tarifa: Instagram para mostrar, WhatsApp para vender e recomprar, link de pagamento para receber. Marketplace fica fora até o parecer jurídico.</p>',
          '<p class="lead">Começar onde vender não custa tarifa: Instagram para mostrar (com live de abertura de frasco), WhatsApp para vender e recomprar, link de pagamento para receber. Marketplace fica fora até o parecer jurídico.</p>')
    o = R(o, 'CAC de R$ 20, abaixo do máximo de R$ 21,22', f'CAC de R$ 20, abaixo do máximo de {brl(N["cac_max"])}')
    o = R(o, '<tr><td>TikTok</td>', '<tr><td>Live de abertura de frasco (Instagram) ' + NOVO + '</td><td>Prova de origem, venda do fim de frasco por ml</td><td>R$ 0</td><td>Conteúdo, prova e giro numa ação; copia o "Até a Última Gota" da Tabs</td><td>Exige estoque e roteiro</td><td>Semana 3, depois mensal</td></tr><tr><td>Quiz no Stories e formulário ' + NOVO + '</td><td>Diagnóstico para quem não chama no WhatsApp</td><td>R$ 0</td><td>Captura o lead indeciso</td><td>Resposta manual</td><td>Semana 2</td></tr><tr><td>TikTok</td>')
    o = R(o, 'Onde o perfume árabe viraliza', 'Onde o árabe e o "clone de nicho" viralizam')
    o = R(o, '<li><b>Dias 4 a 10:</b> 6 conteúdos de prova de origem e diagnóstico; primeira venda local.</li>', '<li><b>Dias 4 a 10:</b> 6 conteúdos de prova de origem e diagnóstico; primeira venda local com 9pm, Liquid Brun e Sauvage próprios.</li>')
    return o

def p17():
    o = strip_pn(ORIG['p14'])
    mar = E_ROWS[3]
    per_sku = N['ml_month_mar'] / 9
    o = R(o, 'Repor perfume quando restarem 35 ml (cenário base: cerca de 69 ml por perfume por mês e 7 dias de entrega).', f'Repor perfume quando restarem 35 ml (60 ml no 212 VIP Men de 200 ml). No cenário base de mar/27 saem cerca de {num(per_sku)} ml por perfume por mês, com 9 perfumes ativos e 7 dias de entrega.')
    sc = N['stock_cov']
    o = R(o, 'Estoque máximo de perfume para 30 dias: com 25 pedidos por mês, 60 dias de estoque prendem R$ 1.265,33 e 90 dias, R$ 1.739,83.', f'Estoque máximo de perfume para 30 dias por perfume: com {num(N["orders_mar"])} pedidos por mês, 30 dias de estoque somam cerca de {brl(sc[0][3])}; 60 dias prendem {brl(sc[1][3])} e 90 dias, {brl(sc[2][3])}.')
    o = R(o, '<tr><td>Domingo</td>', '<tr><td>1ª segunda do mês</td><td>Live de abertura de frasco e venda do fim de frasco por ml</td><td>30 a 45 min</td></tr><tr><td>Domingo</td>')
    o = R(o, '<li>Transferir com adaptador de borrifo (sem violar frascos crimpados) ou seringa graduada exclusiva daquele perfume.</li>', '<li>Transferir com adaptador de borrifo (sem violar frascos crimpados, caso de quase toda grife) ou seringa graduada exclusiva daquele perfume; refil sem válvula (La Vie Est Belle) vai direto com seringa.</li>')
    o = R(o, '<li><b>Garantia de acerto do Kit Descoberta:</b> se nenhum agradar, um 2 ml à escolha no próximo pedido.</li>', '<li><b>Garantia de acerto do Kit Descoberta:</b> se nenhum agradar, um 2 ml de faixa A à escolha no próximo pedido.</li><li><b>Pré-venda (faixa D):</b> prazo de envio informado antes do pagamento; se a pré-venda não pagar o frasco em 15 dias, reembolso integral em até 2 dias úteis.</li><li><b>Fixação:</b> o texto de cada produto explica que fixação e projeção variam com pele, clima e aplicação; nenhuma promessa em horas.</li>')
    return o

def p18():
    o = strip_pn(ORIG['p15'])
    oti_m6 = N['oti_last_month_rev']
    o = R(o, '<tr><td>Teto do MEI</td><td>R$ 81 mil por ano; o cenário otimista chega a cerca de R$ 19,4 mil em 6 meses</td><td><span class="b fa">Permitido</span></td>',
          f'<tr><td>Teto do MEI</td><td>R$ 81 mil por ano (R$ 6.750 por mês em média). No plano escalonado, o cenário base chega a {brl(N["base_last_month_rev"])} em mai/27; o otimista, a {brl(oti_m6)}, acima da média mensal permitida</td><td><span class="b es">Exige adequação</span> no cenário otimista</td>')
    new_rows = ('<tr><td>Vender clone citando o original ' + NOVO + '</td><td>O clone é produto regular da própria marca (Armaf, Lattafa); vender é permitido. Usar o nome do original para vendê-lo ("igual ao Aventus", "dupe de") pode ser aproveitamento parasitário e concorrência desleal (LPI, art. 195, III e IV); comparação objetiva de notas em conteúdo editorial tem mais espaço, nos limites do CONAR</td><td><span class="b va">Juridicamente incerto</span></td><td>Título, anúncio e nome de produto só com o nome do clone; comparação apenas em conteúdo orgânico, com roteiro aprovado pelo advogado (pergunta 11)</td></tr>'
                '<tr><td>Pré-venda e rateio de frasco ' + NOVO + '</td><td>Oferta vincula (CDC, art. 30); recusa de cumprimento dá direito a devolução (art. 35); prazo de entrega precisa estar claro; arrependimento de 7 dias segue valendo (art. 49)</td><td><span class="b es">Exige adequação</span></td><td>Termos escritos: prazo, condição de fechamento, reembolso integral se não fechar (pergunta 12)</td></tr>'
                '<tr><td>Venda do fim de frasco por ml ("até a última gota") ' + NOVO + '</td><td>Mesmo regime do decant (fracionamento)</td><td><span class="b va">Juridicamente incerto</span></td><td>Segue a resposta da pergunta 1</td></tr>'
                '<tr><td>Decant de grife com marca de luxo</td><td>Mesma análise do item "Citar a marca do perfume original"; marcas de luxo costumam notificar revendedores não autorizados</td><td><span class="b va">Juridicamente incerto</span></td><td>Pergunta 5 ao advogado; nada de logotipo da marca em foto de capa ou anúncio</td></tr>')
    o = R(o, '<tr><td>Comparar com perfume de grife em anúncio</td>', new_rows + '<tr><td>Comparar com perfume de grife em anúncio</td>')
    o = R(o, '<li>Preciso de inscrição estadual para vender para outros estados?</li>', '<li>Preciso de inscrição estadual para vender para outros estados?</li><li>No cenário otimista a receita passa de R$ 6.750 por mês a partir do 5º mês: quando migrar para ME no Simples Nacional e quanto custa a transição?</li>')
    o = R(o, '<li>Vender frasco lacrado sob encomenda (fase 2) tem alguma exigência adicional?</li>', '<li>Vender frasco lacrado sob encomenda (fase 2) tem alguma exigência adicional?</li><li>Posso fazer conteúdo orgânico dizendo que um clone "lembra" um perfume de grife ou nicho, comparando notas? Em anúncio pago? Qual roteiro é seguro?</li><li>Como redigir os termos de pré-venda (prazo, fechamento, reembolso) para não gerar obrigação que eu não consiga cumprir?</li>')
    o = R(o, '<h3>Perguntas para o advogado</h3>', '<h3>Perguntas para o advogado</h3><p class="note">As perguntas 11 e 12 são novas nesta versão.</p>')
    return o

def p19():
    o = strip_pn(ORIG['p16'])
    o = R(o, '<td>Baixo; limita a expansão para além do árabe</td><td>Top 3</td>', '<td>Alto agora: o portfólio vai além do árabe</td><td>Reserva</td>')
    o = R(o, 'Para quem quer um perfume árabe marcante sem errar na compra, a Gota Rara é a curadoria de Porto Alegre que entrega decants com origem comprovada por lote.', 'Para quem quer provar perfume de grife, clone ou árabe antes de pagar o frasco, a Gota Rara é a curadoria de Porto Alegre que entrega decants com origem comprovada por lote.')
    o = R(o, 'Explorador (descoberta da perfumaria árabe)', 'Explorador (descoberta de perfumes, da grife ao árabe)')
    o = R(o, '<p><b>Por que Gota Rara:</b> é curto, fácil de falar e de lembrar, traduz o decant (gota) e a curadoria (rara) e não prende a marca a uma origem.', '<p><b>Por que Gota Rara:</b> é curto, fácil de falar e de lembrar, traduz o decant (gota) e a curadoria (rara) e não prende a marca a uma origem, o que ficou mais importante com grife no portfólio.')
    o = R(o, 'presença, acerto, origem, lote, prova, curadoria, elogio, rastro (como palavra comum), assinatura, descoberta', 'presença, acerto, origem, lote, prova, curadoria, elogio, rastro (como palavra comum), assinatura, descoberta, faixa, "lembra" (só em conteúdo orgânico)')
    return o

def p20():
    o = strip_pn(ORIG['p17'])
    o = R(o, '<tr><td>Oferta</td><td>Kits, datas, prazos, lote novo</td><td>Converte a audiência</td><td>1 por semana</td></tr>',
          '<tr><td>Oferta</td><td>Kits, datas, prazos, lote novo</td><td>Converte a audiência</td><td>1 por semana</td></tr><tr><td>Mapa de clones ' + NOVO + '</td><td>Onde o clone se parece com o original e onde não; só em conteúdo orgânico, com roteiro aprovado</td><td>É o que o caçador de clone procura; o líder evita esse formato</td><td>1 a cada 2 semanas</td></tr><tr><td>Frasco aberto ao vivo ' + NOVO + '</td><td>Live de abertura com nota e lote; venda do fim de frasco por ml</td><td>Prova de origem e giro de estoque</td><td>1 por mês</td></tr>')
    o = RR(o, r'<tr><td>5</td><td>05/12 sáb</td>.*?</tr>', '<tr><td>5</td><td>05/12 sáb</td><td>Guia</td><td>Carrossel 7 telas</td><td>Instagram</td><td>Salvamentos</td><td>"6 perfumes para começar: 3 árabes, 2 grifes e 1 unissex"</td><td>Asad, Yara, La Vie Est Belle, 9pm, Liquid Brun e Sauvage EDT: 1 tela cada, com faixa de preço</td><td>"Salve para não esquecer"</td><td>Kit Descoberta</td></tr>')
    o = RR(o, r'<tr><td>9</td><td>09/12 qua</td>.*?</tr>', '<tr><td>9</td><td>09/12 qua</td><td>Abertura de Yara e La Vie Est Belle</td><td>Reels 30 s</td><td>Instagram</td><td>Confiança</td><td>"Um árabe e uma grife, duas notas, dois lotes"</td><td>Mesmo roteiro do dia 8</td><td>"Qual você testaria primeiro?"</td><td>Yara e La Vie Est Belle 5 ml</td></tr>')
    o = RR(o, r'<tr><td>10</td><td>10/12 qui</td>.*?</tr>', '<tr><td>10</td><td>10/12 qui</td><td>Doce árabe ou doce francês</td><td>Reels comparativo</td><td>Instagram e TikTok</td><td>Alcance</td><td>"Yara ou La Vie Est Belle: qual é você?"</td><td>Uma pessoa testa os dois e descreve; os dois estão no catálogo</td><td>"Vote nos comentários"</td><td>Kit Trio</td></tr>')
    o = RR(o, r'<tr><td>13</td><td>13/12 dom</td>.*?</tr>', '<tr><td>13</td><td>13/12 dom</td><td>Mapa de clones</td><td>Reels 45 s</td><td>Instagram e TikTok</td><td>Salvamentos</td><td>"O árabe que muita gente compara a um Dior: onde se parecem e onde não"</td><td>Asad na fita; notas em comum e diferenças; sem logotipo nem nome de marca de terceiro no título; roteiro aprovado pelo advogado</td><td>"Comente MAPA"</td><td>Asad 5 ml</td></tr>')
    o = RR(o, r'<tr><td>19</td><td>19/12 sáb</td>.*?</tr>', '<tr><td>19</td><td>19/12 sáb</td><td>Sauvage no calor</td><td>Reels</td><td>Instagram e TikTok</td><td>Alcance</td><td>"O fresco que aguenta o verão gaúcho"</td><td>Teste em dia quente; decant do frasco próprio com ficha de lote</td><td>"Comente VERÃO"</td><td>Sauvage EDT 5 ml</td></tr>')
    o = R(o, 'Gota Rara · Decants de perfumes árabes com origem comprovada.', 'Gota Rara · Decants de grife, clones e árabes com origem comprovada.')
    o = R(o, 'Kit Descoberta (5 perfumes de 2 ml) por R$ 69,90 e Kit Trio (3 perfumes de 5 ml à sua escolha) por R$ 89,90, com brinde.', f'Kit Descoberta (5 perfumes de 2 ml) a partir de R$ 69,90 e Kit Trio (3 perfumes de 5 ml à sua escolha) a partir de R$ 89,90, com brinde. Com Sauvage no Trio, R$ 102,80; com La Vie Est Belle, R$ 124,80.')
    o = R(o, '<b>Texto:</b> Perfume árabe sem errar na compra.', '<b>Texto:</b> Prove grife e árabe sem errar na compra.')
    o = R(o, 'Kit Trio por R$ 89,90, com brinde.<br>', 'Kit Trio a partir de R$ 89,90, com brinde.<br>')
    o = R(o, 'brinde de 1 ml do próximo perfume que indicarmos para você. R$ 89,90.', 'brinde de 1 ml do próximo perfume que indicarmos para você. A partir de R$ 89,90; perfumes das faixas B e C têm adicional (+R$ 12,90 e +R$ 34,90).')
    o = R(o, '(R$ 59,90, sai mais barato por ml)', '(a partir de R$ 59,90, sai mais barato por ml)')
    o = RR(o, r'<li><b>CAC máximo:</b>.*?</li>', f'<li><b>CAC máximo:</b> {brl(N["cac_max"])}. Conta: valor do cliente de {brl(N["client_value"])} (margem média do 1º pedido de {brl(N["cmo"])} + 30% de chance de recompra × {brl(N["m10A"])} do 10 ml de faixa A) × 50%.</li>')
    o = R(o, '<p class="note">Datas de corte de envio nacional', '<p class="note">Clone e grife no calendário: Asad, Yara, La Vie Est Belle, 9pm, Liquid Brun e Sauvage estão disponíveis em dezembro; Club de Nuit, Sabah, 212 VIP e Fakhar entram com as etapas 2 e 3. Datas de corte de envio nacional')
    return o

def p21():
    o = strip_pn(ORIG['p18'])
    o = R(o, 'o 10 ml deixa R$ 28,72 de margem', f'o 10 ml de faixa A deixa {brl(N["m10A"])} de margem e o de faixa B, {brl(N["sku_econ"]["sauv"][10]["mg"])}')
    o = R(o, 'Custa R$ 20 por cliente novo, abaixo do CAC máximo de R$ 21,22.', f'Custa R$ 20 por cliente novo, abaixo do CAC máximo de {brl(N["cac_max"])}.')
    extra = ('<h3>Mecanismos novos desta versão</h3>'
             + table(['Mecanismo', 'Copiado de', 'Como funciona', 'Quando'], [
                 ['Fim de frasco "até a última gota"', 'Tabs', 'Live mensal; o que sobra abaixo de 30 ml vai por ml com 20% de desconto, prioridade de 24 h para a lista VIP', 'A partir da semana 3'],
                 ['Recompra em faixa superior', 'Perfume Shopping (escada de tamanhos)', 'Quem comprou o clone recebe convite para provar o original em 2 ml (pré-venda) e vice-versa', 'Após a etapa 2'],
                 ['Crédito na avaliação', 'Cashback do líder, simplificado', 'R$ 10 de crédito por avaliação com foto, válido por 60 dias', 'Desde o 1º pedido'],
                 ['Crédito do decant no frasco', 'Ideia deste plano ' + JU, 'O valor do último decant do mesmo perfume abate do frasco lacrado sob encomenda', 'Fase 2'],
                 ['Clube piloto', 'Clube Tabs e Scentbird', '20 assinantes, 1 × 5 ml por mês da fila do cliente, faixas A e B', 'Após 100 clientes'],
             ]))
    o = R(o, '<h3>Programa escolhido: lembrete + indicação</h3>', extra + '<h3>Programa escolhido: lembrete + indicação</h3>')
    return o
