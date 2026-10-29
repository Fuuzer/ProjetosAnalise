"""Exercícios propostos: enunciados e respostas calculadas em Python.

O HTML usa as respostas para conferir o que o aluno digitar. A planilha
refaz as mesmas contas com fórmulas; verificar.py compara as duas.
"""
from modelo import S, D, I, NOTAS, LCR, FTP, CDI, media

OPCOES_BP = [
    "Disponibilidades (caixa)",
    "Centralização financeira",
    "Aplicações interfinanceiras de liquidez",
    "Títulos e valores mobiliários",
    "Operações de crédito: empréstimos",
    "Operações de crédito: financiamentos rurais",
    "(-) Provisão para perdas esperadas",
    "Bens não de uso próprio (BNDU)",
    "Investimentos",
    "Intangível",
    "Depósitos à vista",
    "Depósitos a prazo (RDC)",
    "Recursos de aceites e emissão de títulos (LCA)",
    "Obrigações por empréstimos e repasses",
    "Provisões (contingências e garantias)",
    "Obrigações sociais e estatutárias",
    "Obrigações fiscais e outras obrigações",
    "Capital social",
    "Fora do balanço (coobrigações e garantias)",
]

CLASSIFICACAO = [
    ("Associado deposita R$ 5 mil em dinheiro na conta corrente. Qual linha do passivo aumenta?",
     "Depósitos à vista",
     "Dinheiro na conta corrente é depósito à vista: o associado saca quando quiser e a cooperativa não paga juros. No ativo, entra em Disponibilidades (caixa) e, no fim do dia, a sobra vai para a centralização."),
    ("A cooperativa libera R$ 200 mil de custeio agrícola para um produtor. Qual linha do ativo aumenta?",
     "Operações de crédito: financiamentos rurais",
     "Custeio, investimento e comercialização agrícola ficam em Financiamentos rurais e agroindustriais. O dinheiro sai da liquidez (centralização) e vira carteira."),
    ("A sobra de caixa do dia é transferida para a Cooperativa Central. Qual linha do ativo aumenta?",
     "Centralização financeira",
     "A sobra de recursos da singular fica aplicada na Central (relações interfinanceiras, centralização financeira), rendendo perto de 100% do CDI. É a principal reserva de liquidez."),
    ("Associado aplica R$ 50 mil em RDC. Qual linha do passivo aumenta?",
     "Depósitos a prazo (RDC)",
     "RDC (Recibo de Depósito Cooperativo) é o depósito a prazo da cooperativa, o equivalente ao CDB do banco. Paga um percentual do CDI e é garantido pelo FGCoop até o limite."),
    ("Associado compra R$ 30 mil em LCA emitida pela cooperativa. Qual linha do passivo aumenta?",
     "Recursos de aceites e emissão de títulos (LCA)",
     "LCA é um título emitido pela instituição com lastro em crédito do agronegócio. Fica em Recursos de aceites e emissão de títulos, não em depósitos."),
    ("A cooperativa recebe um trator em dação em pagamento de uma dívida vencida. Qual linha do ativo aumenta?",
     "Bens não de uso próprio (BNDU)",
     "Bem recebido para quitar dívida não é de uso da cooperativa: vai para BNDU até ser vendido. BNDU crescendo é sinal de recuperação de crédito difícil."),
    ("Um novo associado integraliza R$ 1 mil em quotas-partes. Qual linha aumenta?",
     "Capital social",
     "Quota-parte integralizada é capital social, dentro do patrimônio líquido. Ela pode ser devolvida quando o associado sai, por isso é um capital menos estável que as reservas."),
    ("A AGO destina 5% das sobras ao FATES. Em que linha do balanço o valor fica?",
     "Obrigações sociais e estatutárias",
     "Nas cooperativas de crédito, o FATES é registrado no passivo (obrigações sociais e estatutárias), e não no PL: é um recurso com destino obrigatório (assistência técnica, educacional e social)."),
    ("Financiamento de máquina com recurso do BNDES repassado pelo Banco Sicredi. Qual linha do passivo aumenta?",
     "Obrigações por empréstimos e repasses",
     "O dinheiro veio de um repasse (BNDES, FINAME, BRDE) e a cooperativa deve devolvê-lo: Obrigações por empréstimos e repasses. No ativo, o financiamento entra na carteira de crédito."),
    ("A cooperativa subscreve quotas da Central e da Sicredi Participações. Qual linha do ativo aumenta?",
     "Investimentos",
     "Participação no capital de outras entidades do sistema é Investimento. Ela rende (juros ao capital, dividendos) mas não é liquidez."),
    ("A cooperativa presta fiança de R$ 100 mil a um associado perante um fornecedor. Onde aparece o valor garantido?",
     "Fora do balanço (coobrigações e garantias)",
     "Garantia prestada não sai do caixa: fica em contas de compensação (fora do balanço). Mesmo assim consome capital (entra no RWA) e, pela Res. 4.966, pode exigir provisão no passivo."),
    ("Compra de licença de software de uso por 5 anos. Qual linha do ativo aumenta?",
     "Intangível",
     "Software e licenças de longo prazo são ativos intangíveis, amortizados ao longo do uso. O intangível é deduzido do capital no cálculo do PR."),
    ("A cooperativa constitui provisão para perdas de uma operação em atraso. Qual linha do ativo é afetada?",
     "(-) Provisão para perdas esperadas",
     "A provisão é uma conta redutora da carteira (fica negativa no ativo). A contrapartida é a despesa de provisão na DSP, que reduz o resultado."),
    ("Juros do mês sobre os RDC são apropriados (reconhecidos), mas o associado só recebe no vencimento. Qual linha do passivo aumenta?",
     "Depósitos a prazo (RDC)",
     "Os juros apropriados aumentam o saldo devido ao associado no próprio RDC (regime de competência). Contrapartida: despesa de captação na DSP."),
    ("Salários de dezembro, pagos só em janeiro. Qual linha do passivo aumenta no fechamento?",
     "Obrigações fiscais e outras obrigações",
     "Salários, encargos, tributos e fornecedores a pagar ficam em obrigações fiscais e outras obrigações. A contrapartida é despesa de pessoal."),
]


def _rl(a):
    return D[a]["receita_liquida"]


def gerar():
    E = []

    def add(eid, titulo, tema, enunciado, itens, dica=""):
        E.append(dict(id=eid, titulo=titulo, tema=tema, enunciado=enunciado, itens=itens, dica=dica))

    def it(letra, pergunta, valor, unidade, tol=None):
        if tol is None:
            tol = {"%": 0.0015, "R$ mil": max(abs(valor) * 0.003, 6), "p.p.": 0.06, "x": 0.02, "R$": max(abs(valor) * 0.003, 1)}[unidade]
        return dict(letra=letra, pergunta=pergunta, valor=valor, unidade=unidade, tol=tol)

    # P01 classificação
    add("P01", "Onde entra cada lançamento?", "Linhas do BP",
        "Para cada evento, escolha a linha do balanço que ele afeta. A ideia é treinar o olhar: antes de analisar um número, saiba o que mora dentro dele.",
        [dict(letra=str(n + 1), pergunta=q, valor=r, unidade="opcao", explicacao=e) for n, (q, r, e) in enumerate(CLASSIFICACAO)])

    # P02 AV do passivo + PL
    tot = {a: S["passivo"][a] + S["pl"][a] for a in (2024, 2025)}
    add("P02", "Análise vertical do passivo e do PL", "AV",
        "Use o BP da Coop Vale do Ipê. Calcule a participação de cada grupo no total do passivo + PL em 2024 e em 2025 e explique o que mudou na forma como a cooperativa se financia.",
        [it("a", "Depósitos a prazo (RDC) ÷ passivo + PL, em 2024", S["rdc"][2024] / tot[2024], "%"),
         it("b", "Depósitos a prazo (RDC) ÷ passivo + PL, em 2025", S["rdc"][2025] / tot[2025], "%"),
         it("c", "Depósitos à vista ÷ passivo + PL, em 2024", S["dep_vista"][2024] / tot[2024], "%"),
         it("d", "Depósitos à vista ÷ passivo + PL, em 2025", S["dep_vista"][2025] / tot[2025], "%"),
         it("e", "PL ÷ passivo + PL, em 2025", S["pl"][2025] / tot[2025], "%"),
         it("f", "Captação com associados (depósitos + LCA) ÷ passivo + PL, em 2025", (S["depositos"][2025] + S["lca"][2025]) / tot[2025], "%")],
        "AV = linha ÷ total do passivo + PL do mesmo ano. O total do passivo + PL é igual ao total do ativo.")

    # P03 AH da DSP
    def ah(k):
        return D[2025][k] / D[2024][k] - 1
    add("P03", "Análise horizontal da DSP", "AH",
        "Calcule a variação de 2025 contra 2024 das linhas abaixo. Depois responda: por que a despesa de captação cresceu muito mais que a receita de crédito?",
        [it("a", "AH da receita de operações de crédito", ah("rend_credito"), "%"),
         it("b", "AH da despesa de captação (operações de captação no mercado)", ah("desp_captacao"), "%"),
         it("c", "AH da margem financeira (visão gerencial)", ah("mf"), "%"),
         it("d", "AH da despesa de provisão para perdas (PDD)", ah("pdd"), "%"),
         it("e", "AH do resultado antes dos juros ao capital", ah("resultado"), "%")],
        "AH = valor de 2025 ÷ valor de 2024 - 1. Despesas negativas dividem por negativas: o sinal some e a conta funciona.")

    # P04 margem financeira e NIM
    add("P04", "Margem financeira e NIM de 2024", "Margem financeira",
        "Monte a margem financeira de 2024 pela visão gerencial (receita de crédito + receita da liquidez - despesa de captação - despesa de repasses) e calcule o NIM sobre o ativo médio. Compare com 2025.",
        [it("a", "Margem financeira de 2024 (R$ mil)", D[2024]["mf"], "R$ mil"),
         it("b", "NIM de 2024 (margem ÷ ativo médio de 2023 e 2024)", I[2024]["nim"], "%"),
         it("c", "NIM de 2025", I[2025]["nim"], "%"),
         it("d", "Variação do NIM de 2024 para 2025, em pontos percentuais", (I[2025]["nim"] - I[2024]["nim"]) * 100, "p.p.")],
        "Ativo médio de 2024 = (ativo de 31/12/2023 + ativo de 31/12/2024) ÷ 2. O ativo de 2023 está nas notas.")

    # P05 spread 2024
    add("P05", "Spread de 2024", "Spread",
        "Calcule as taxas médias implícitas de 2024 a partir da DSP e dos saldos médios. Use como captação os depósitos (à vista, poupança e RDC) e a LCA.",
        [it("a", "Taxa média da carteira de crédito (receita de crédito ÷ carteira média)", I[2024]["taxa_credito"], "%"),
         it("b", "Custo médio da captação, incluindo o depósito à vista a custo zero", I[2024]["custo_captacao"], "%"),
         it("c", "Spread de crédito (a - b), em pontos percentuais", I[2024]["spread_credito"] * 100, "p.p."),
         it("d", "Custo médio só dos passivos onerosos (sem o depósito à vista)", I[2024]["custo_oneroso"], "%")],
        "Custo da captação = despesas de poupança + RDC + LCA (sem FGCoop e sem LFS) ÷ saldo médio de depósitos + LCA.")

    # P06 ROE e DuPont 2024
    i24 = I[2024]
    margem = D[2024]["resultado"] / D[2024]["receita_liquida"]
    giro = D[2024]["receita_liquida"] / i24["ativo_medio"]
    alav = i24["ativo_medio"] / i24["pl_medio"]
    add("P06", "ROE contábil, ROE recorrente e DuPont de 2024", "ROE e resultado recorrente",
        "Calcule o ROE de 2024 (resultado antes dos juros ao capital ÷ PL médio), tire os itens não recorrentes listados nas notas e decomponha o ROE em margem × giro × alavancagem.",
        [it("a", "ROE contábil de 2024", i24["roe"], "%"),
         it("b", "Resultado recorrente de 2024 (R$ mil)", i24["resultado_recorrente"], "R$ mil"),
         it("c", "ROE recorrente de 2024", i24["roe_recorrente"], "%"),
         it("d", "Margem: resultado ÷ receita líquida", margem, "%"),
         it("e", "Giro: receita líquida ÷ ativo médio", giro, "%"),
         it("f", "Alavancagem: ativo médio ÷ PL médio", alav, "x")],
        "Item não recorrente com sinal negativo (despesa) é somado de volta; com sinal positivo (ganho) é retirado.")

    # P07 eficiência
    alvo = I[2024]["ie_recorrente"]
    adm_rec25 = -D[2025]["desp_adm"] + NOTAS["nr_pdv"][2025]
    rl_rec25 = D[2025]["receita_liquida"] - NOTAS["nr_reversao_conting"][2025]
    corte = adm_rec25 - alvo * rl_rec25
    add("P07", "Eficiência operacional (cost-to-income)", "Eficiência",
        "Calcule o índice de eficiência (despesas administrativas ÷ receita líquida) e o IEAR (somando a PDD líquida de recuperações). Depois descubra quanto de despesa a cooperativa teria de cortar em 2025 para o IE recorrente voltar ao IE recorrente de 2024.",
        [it("a", "IE de 2024", I[2024]["ie"], "%"),
         it("b", "IEAR de 2024", I[2024]["iear"], "%"),
         it("c", "IE recorrente de 2025 (sem a reversão de contingência na receita)", I[2025]["ie_recorrente"], "%"),
         it("d", "Corte de despesas administrativas em 2025 para o IE recorrente voltar ao IE recorrente de 2024 (R$ mil)", corte, "R$ mil")],
        "Receita líquida = margem financeira + serviços e tarifas + outras receitas - outras despesas - tributárias +/- contingências.")

    # P08 crédito 2024
    add("P08", "Inadimplência e provisão de 2024", "Inadimplência e PDD",
        "Use as notas de carteira por atraso e por estágio. Depois explique por que a cobertura caiu em 2025.",
        [it("a", "Inadimplência acima de 90 dias (NPL 90) em 2024", I[2024]["npl90"], "%"),
         it("b", "Inadimplência de 15 a 90 dias em 2024 (sinal antecedente)", I[2024]["inad15_90"], "%"),
         it("c", "Cobertura: provisão ÷ carteira vencida há mais de 90 dias, 2024", I[2024]["cobertura_npl"], "%"),
         it("d", "Custo do risco: despesa de PDD ÷ carteira média, 2024", I[2024]["custo_risco"], "%"),
         it("e", "Baixas para prejuízo em 2024 (R$ mil), pela movimentação da provisão", I[2024]["baixas"], "R$ mil"),
         it("f", "Participação do estágio 3 na carteira em 2025", I[2025]["e3_pct"], "%")],
        "Provisão final = provisão inicial + despesa de PDD - baixas. Isole as baixas.")

    # P09 capital
    i25 = I[2025]
    rwa_novo = i25["rwa"] + 200_000 * 0.85 - 200_000 * 0.20
    add("P09", "RWA e Índice de Basileia", "RWA e Basileia",
        "Use a aba RWA e as premissas de FPR (ilustrativas). Calcule o RWA e o índice de 2024, o índice de 2025 sem a LFS e o efeito de crescer R$ 200 mi de crédito comercial, pagos com a centralização.",
        [it("a", "RWA de risco de crédito de 2024 (R$ mil)", I[2024]["rwa_credito"], "R$ mil"),
         it("b", "RWA de risco operacional de 2024 (R$ mil)", I[2024]["rwa_operacional"], "R$ mil"),
         it("c", "Índice de Basileia de 2024", I[2024]["basileia"], "%"),
         it("d", "MM/RWA de 2024 (folga sobre 10,5%, em p.p.)", I[2024]["mm_rwa"], "p.p."),
         it("e", "Índice de Basileia de 2025 sem a LFS", i25["basileia_sem_lfs"], "%"),
         it("f", "Capital mínimo (10,5%) consumido por R$ 200 mi de crédito comercial com FPR 85% (R$ mil)", 200_000 * 0.85 * 0.105, "R$ mil"),
         it("g", "Novo índice de Basileia de 2025 com esse crédito (sai da centralização, FPR 20%)", i25["pr"] / rwa_novo, "%")],
        "RWA de crédito = soma de exposição × FPR. RWA operacional (simplificado) = 15% × média da receita bruta de 3 anos ÷ 8%.")

    # P10 liquidez 2024
    L = LCR[2024]
    add("P10", "Liquidez de 2024: LCR e indicadores internos", "Liquidez",
        "Com as premissas de estresse de 30 dias das notas, calcule o LCR didático de 2024 e os indicadores internos.",
        [it("a", "Ativos líquidos de alta qualidade (caixa + TVM + centralização), 2024 (R$ mil)", I[2024]["hqla"], "R$ mil"),
         it("b", "Saídas de caixa no estresse de 30 dias (R$ mil)", I[2024]["lcr_saidas"], "R$ mil"),
         it("c", "LCR de 2024 (ativos líquidos ÷ saídas líquidas)", I[2024]["lcr"], "%"),
         it("d", "Índice de liquidez interno: liquidez ÷ (30% dos depósitos)", I[2024]["indice_liquidez"], "x"),
         it("e", "Crédito ÷ captação (depósitos + LCA)", I[2024]["credito_captacao"], "%"),
         it("f", "Liquidez imediata: (caixa + centralização) ÷ depósitos à vista", I[2024]["liq_imediata"], "x")],
        "Saídas líquidas = saídas - mínimo(entradas; 75% das saídas).")

    # P11 FTP
    f = I[2025]["ftp"]
    rdc_m = media(S["rdc"], 2025)
    pct_cdi = -D[2025]["desp_rdc"] / rdc_m / CDI[2025]
    extra = rdc_m * CDI[2025] * 1.05 + D[2025]["desp_rdc"]
    add("P11", "FTP: quem gera a margem?", "FTP",
        "Use as taxas de transferência (FTP) de 2025 das notas. Calcule a margem de cada captação e responda: vale a pena pagar 105% do CDI no RDC para crescer captação?",
        [it("a", "Margem FTP da poupança em 2025 (R$ mil)", f["poupanca"], "R$ mil"),
         it("b", "Margem FTP do RDC em 2025 (R$ mil)", f["rdc"], "R$ mil"),
         it("c", "Custo implícito do RDC em % do CDI de 2025", pct_cdi, "%"),
         it("d", "Custo anual a mais se todo o RDC médio pagasse 105% do CDI (R$ mil)", extra, "R$ mil"),
         it("e", "Impacto desse custo no ROE de 2025, em p.p.", -extra / I[2025]["pl_medio"] * 100, "p.p."),
         it("f", "Resultado da tesouraria (ALM) que fecha a margem financeira de 2025 (R$ mil)", f["tesouraria"], "R$ mil")],
        "Margem da captação = saldo médio × FTP - despesa. Margem do crédito = receita - saldo médio × FTP.")

    # P12 RAROC operação
    valor = 500.0
    pe = valor * 0.03 * 0.45
    cap = valor * 1.0 * 0.125
    res = valor * 0.21 - valor * 0.15 - valor * 0.025 - pe + cap * 0.15
    taxa_min = (0.15 * cap + valor * 0.15 + valor * 0.025 + pe - cap * 0.15) / valor
    add("P12", "RAROC e taxa mínima de uma operação", "RAROC",
        "Operação PJ de R$ 500 mil por 1 ano: taxa de 21% a.a., FTP de 15%, custo operacional de 2,5% a.a., PD de 3%, LGD de 45%, FPR de 100%, capital alocado de 12,5% do RWA. O capital alocado é remunerado pela FTP. A meta (hurdle) é RAROC de 15%.",
        [it("a", "Perda esperada (R$ mil)", pe, "R$ mil", 0.05),
         it("b", "Capital alocado (R$ mil)", cap, "R$ mil", 0.05),
         it("c", "Resultado ajustado ao risco (R$ mil)", res, "R$ mil", 0.05),
         it("d", "RAROC da operação", res / cap, "%"),
         it("e", "Taxa mínima para o RAROC chegar a 15%", taxa_min, "%")],
        "Perda esperada = valor × PD × LGD. RAROC = (receita - FTP - custo operacional - perda esperada + crédito do capital) ÷ capital alocado.")

    # P13 captação
    mixes = I[2025]
    c_poup = -D[2025]["desp_poupanca"] / media(S["poupanca"], 2025)
    c_rdc = -D[2025]["desp_rdc"] / media(S["rdc"], 2025)
    c_lca = -D[2025]["desp_lca"] / media(S["lca"], 2025)
    add("P13", "Captação: mix e custo por produto", "Captação",
        "Calcule o mix de captação de 2025 e o custo implícito de cada produto. Depois calcule quanto custa por ano a migração de R$ 50 mi de depósito à vista para RDC a 101% do CDI.",
        [it("a", "Depósito à vista no total da captação de 2025", mixes["mix_dv"], "%"),
         it("b", "RDC no total da captação de 2025", mixes["mix_rdc"], "%"),
         it("c", "Custo implícito da poupança em 2025", c_poup, "%"),
         it("d", "Custo implícito da LCA em % do CDI", c_lca / CDI[2025], "%"),
         it("e", "Custo anual da migração de R$ 50 mi de DV para RDC a 101% do CDI (R$ mil)", 50_000 * CDI[2025] * 1.01, "R$ mil")],
        "Custo implícito = despesa do produto ÷ saldo médio do produto.")

    # P14 PL
    cap_m = media(S["capital_social"], 2025)
    add("P14", "Patrimônio líquido e destinação das sobras", "PL",
        "Use a DMPL de 2025 nas notas. Refaça o capital social e o PL de 31/12/2025 e analise a qualidade do capital.",
        [it("a", "Capital social em 31/12/2025 (R$ mil)", S["capital_social"][2025], "R$ mil", 1),
         it("b", "PL em 31/12/2025 (R$ mil)", S["pl"][2025], "R$ mil", 1),
         it("c", "Juros ao capital de 2025 em % do CDI (sobre o capital médio)", -D[2025]["juros_capital"] / (cap_m * CDI[2025]), "%"),
         it("d", "Capital social por associado em 2025 (R$)", S["capital_social"][2025] * 1000 / NOTAS["associados"][2025], "R$"),
         it("e", "Capital social ÷ PL em 2025", S["capital_social"][2025] / S["pl"][2025], "%"),
         it("f", "Crescimento do PL menos crescimento do RWA em 2025, em p.p.", (I[2025]["cresc_pl"] - (I[2025]["rwa"] / I[2024]["rwa"] - 1)) * 100, "p.p.")],
        "PL final = PL inicial + integralizações - devoluções + resultado - FATES - sobras distribuídas +/- ajustes. Juros ao capital incorporados entram no capital e saem do resultado: efeito zero no PL.")

    # P15 caso
    add("P15", "Estudo de caso: o parecer da Coop Vale do Ipê", "Análise completa",
        "Escreva um parecer de uma página sobre a Coop Vale do Ipê, seguindo o roteiro de 10 passos. Responda: a cooperativa está saudável? O que melhorou, o que piorou, quais são os três riscos principais e quais as três recomendações para a diretoria? Compare depois com o parecer modelo (no HTML e na aba Ex15).",
        [])
    return E


EXERCICIOS = gerar()

if __name__ == "__main__":
    for e in EXERCICIOS:
        print(e["id"], e["titulo"])
        for i in e["itens"]:
            v = i["valor"]
            print("   ", i["letra"], i["unidade"], v if isinstance(v, str) else round(v, 5))
