"""Monta o HTML do curso a partir dos modelos em tpl/ e dos números de modelo.py.

Marcadores no template:
  {{fmt:expressão}}   número formatado (m, mi, p0, p1, p2, pp, pp1, n0, n1, n2, x2, rs)
  {{html:função()}}   bloco HTML gerado aqui (tabelas, gráficos, exercícios)
"""
import html
import json
import re
from pathlib import Path

import modelo as M
from exercicios import EXERCICIOS, OPCOES_BP
from parecer import PARECER

S, D, I, NOTAS = M.S, M.D, M.I, M.NOTAS
AQUI = Path(__file__).parent
SAIDA = AQUI / "Analise_BP_Cooperativa.html"
PLANILHA = "Exercicios_BP_Cooperativa_Resolvidos.xlsx"


# ------------------------------------------------------------------ formatação PT-BR
def fnum(x, d=0):
    s = f"{abs(x):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if x < 0 and round(abs(x), d) != 0 else "") + s


FMT = {
    "m": lambda x: fnum(x, 0),
    "mi": lambda x: fnum(x / 1000, 1),
    "p0": lambda x: fnum(x * 100, 0) + "%",
    "p1": lambda x: fnum(x * 100, 1) + "%",
    "p2": lambda x: fnum(x * 100, 2) + "%",
    "pp": lambda x: fnum(x, 2),
    "pp1": lambda x: fnum(x, 1),
    "n0": lambda x: fnum(x, 0),
    "n1": lambda x: fnum(x, 1),
    "n2": lambda x: fnum(x, 2),
    "x2": lambda x: fnum(x, 2) + "x",
    "rs": lambda x: "R$ " + fnum(x, 2),
}


def par(x):
    """Valor de demonstrativo: negativo entre parênteses."""
    if x is None:
        return ""
    if abs(x) < 0.5:
        return "-"
    return f"({fnum(-x)})" if x < 0 else fnum(x)


# ------------------------------------------------------------------ atalhos para o template
def s(k, a):
    return S[k][a]


def d(k, a):
    return D[a][k]


def i(k, a):
    return I[a][k]


def n(k, a):
    return NOTAS[k][a]


def avg(k, a):
    return M.media(S[k], a)


def ftp(k, a):
    return I[a]["ftp"][k]


def rar(seg, k):
    return I[2025]["raroc"][seg][k]


def at(k, a):
    return NOTAS["atraso"][a][k]


def est(k, a, j=0):
    return NOTAS["estagio"][a][k][j]


def lcr(k, a):
    return M.LCR[a][k]


def ex(eid, letra):
    for e in EXERCICIOS:
        if e["id"] == eid:
            for it in e["itens"]:
                if it["letra"] == letra:
                    return it["valor"]
    raise KeyError((eid, letra))


def ah(x1, x0):
    return x1 / x0 - 1


NS = dict(S=S, D=D, I=I, NOTAS=NOTAS, M=M, s=s, d=d, i=i, n=n, avg=avg, ftp=ftp, rar=rar, at=at, est=est, lcr=lcr,
          ex=ex, ah=ah, CDI=M.CDI, IPCA=M.IPCA, abs=abs, min=min, max=max, sum=sum)


# ------------------------------------------------------------------ tabelas
def _av(x, base):
    return fnum(x / base * 100, 1) + "%" if base else ""


def _ah(x1, x0):
    if not x0 or (x1 < 0) != (x0 < 0):
        return "n.a."
    return fnum((x1 / x0 - 1) * 100, 1) + "%"


BP_LINHAS = [
    ("sec", None, "Ativo"),
    ("in", "caixa", "Disponibilidades (caixa)"),
    ("in", "centralizacao", "Centralização financeira"),
    ("in", "aplic_interfin", "Aplicações interfinanceiras de liquidez"),
    ("in", "tvm", "Títulos e valores mobiliários"),
    ("in", "cred_emprestimos", "Operações de crédito: empréstimos e títulos descontados"),
    ("in", "cred_financiamentos", "Operações de crédito: financiamentos"),
    ("in", "cred_rural", "Operações de crédito: financiamentos rurais e agroindustriais"),
    ("sub", "carteira", "Carteira de crédito bruta"),
    ("in", "provisao", "(-) Provisão para perdas esperadas"),
    ("sub", "carteira_liq", "Carteira de crédito líquida"),
    ("in", "outros_ativos_fin", "Outros ativos financeiros"),
    ("in", "ativos_fiscais", "Ativos fiscais"),
    ("in", "bndu", "Bens não de uso próprio (BNDU)"),
    ("in", "outros_ativos", "Outros ativos"),
    ("in", "investimentos", "Investimentos (participações no sistema)"),
    ("in", "imobilizado", "Imobilizado de uso"),
    ("in", "intangivel", "Intangível"),
    ("tot", "ativo", "Total do ativo"),
    ("sec", None, "Passivo"),
    ("in", "dep_vista", "Depósitos à vista"),
    ("in", "poupanca", "Depósitos de poupança"),
    ("in", "rdc", "Depósitos a prazo (RDC)"),
    ("sub", "depositos", "Total de depósitos"),
    ("in", "lca", "Recursos de aceites e emissão de títulos (LCA)"),
    ("in", "repasses_interfin", "Relações interfinanceiras (Central e Banco)"),
    ("in", "emprestimos_repasses", "Obrigações por empréstimos e repasses (BNDES e outros)"),
    ("in", "lfs", "Dívida elegível a capital (LFS)"),
    ("in", "outros_passivos_fin", "Outros passivos financeiros"),
    ("in", "provisoes", "Provisões (contingências e garantias)"),
    ("in", "obrig_sociais", "Obrigações sociais e estatutárias"),
    ("in", "obrig_fiscais_outras", "Obrigações fiscais e outras obrigações"),
    ("tot", "passivo", "Total do passivo"),
    ("sec", None, "Patrimônio líquido"),
    ("in", "capital_social", "Capital social"),
    ("in", "reserva_legal", "Reserva legal"),
    ("in", "sobras_acum", "Sobras acumuladas (à disposição da AGO)"),
    ("in", "aap", "Ajustes de avaliação patrimonial"),
    ("tot", "pl", "Total do patrimônio líquido"),
    ("tot", "passivo_pl", "Total do passivo + PL"),
    ("sec", None, "Fora do balanço"),
    ("in", "coobrigacoes", "Coobrigações e garantias prestadas"),
]
ATIVO_KEYS = {"caixa", "centralizacao", "aplic_interfin", "tvm", "cred_emprestimos", "cred_financiamentos", "cred_rural",
              "carteira", "provisao", "carteira_liq", "outros_ativos_fin", "ativos_fiscais", "bndu", "outros_ativos",
              "investimentos", "imobilizado", "intangivel", "ativo"}


def vbp(k, a):
    if k == "carteira_liq":
        return S["carteira"][a] + S["provisao"][a]
    if k == "passivo_pl":
        return S["passivo"][a] + S["pl"][a]
    if k == "coobrigacoes":
        return NOTAS["coobrigacoes"][a]
    return S[k][a]


def tabela_bp():
    h = ['<div class="tbl-wrap"><table class="fin av-ah" id="tab-bp"><caption>Balanço patrimonial da Coop Vale do Ipê, em R$ mil, '
         'posição em 31/12</caption><thead><tr><th>Linha</th><th>31/12/2024</th><th>31/12/2025</th>'
         '<th class="c-av">AV 2024</th><th class="c-av">AV 2025</th><th class="c-ah">AH 25/24</th><th class="c-ah">Variação</th></tr></thead><tbody>']
    for tipo, k, rot in BP_LINHAS:
        if tipo == "sec":
            h.append(f'<tr class="sec"><td colspan="7">{rot}</td></tr>')
            continue
        v24, v25 = vbp(k, 2024), vbp(k, 2025)
        if k == "coobrigacoes":
            b24 = b25 = None
        elif k in ATIVO_KEYS:
            b24, b25 = S["ativo"][2024], S["ativo"][2025]
        else:
            b24, b25 = vbp("passivo_pl", 2024), vbp("passivo_pl", 2025)
        cls = {"sub": "sub", "tot": "tot"}.get(tipo, "")
        link = f'<a href="#l-{k}">{rot}</a>' if tipo == "in" else rot
        h.append(f'<tr class="{cls}"><td>{link}</td><td>{par(v24)}</td><td>{par(v25)}</td>'
                 f'<td class="c-av">{_av(v24, b24)}</td><td class="c-av">{_av(v25, b25)}</td>'
                 f'<td class="c-ah">{_ah(v25, v24)}</td><td class="c-ah">{par(v25 - v24)}</td></tr>')
    h.append("</tbody></table></div>")
    return "".join(h)


DSP_LINHAS = [
    ("sec", None, "Receitas (ingressos) da intermediação financeira"),
    ("in", "rend_credito", "Operações de crédito"),
    ("in", "recuperacao", "Recuperação de créditos baixados como prejuízo"),
    ("in", "rend_centralizacao", "Ingressos da centralização financeira"),
    ("in", "rend_aplic", "Aplicações interfinanceiras de liquidez"),
    ("in", "rend_tvm", "Títulos e valores mobiliários"),
    ("sub", "receitas_intermed", "Total das receitas da intermediação"),
    ("sec", None, "Despesas (dispêndios) da intermediação financeira"),
    ("in", "desp_poupanca", "Depósitos de poupança"),
    ("in", "desp_rdc", "Depósitos a prazo (RDC)"),
    ("in", "desp_lca", "LCA"),
    ("in", "desp_lfs", "LFS"),
    ("in", "fgcoop_neg", "Contribuição ao FGCoop"),
    ("sub", "desp_captacao", "Operações de captação no mercado"),
    ("in", "desp_repasses_interfin", "Repasses interfinanceiros (Central e Banco)"),
    ("in", "desp_emprestimos_repasses", "Empréstimos e repasses (BNDES e outros)"),
    ("sub", "desp_repasses", "Operações de empréstimos e repasses"),
    ("in", "pdd", "Provisão para perdas esperadas (PDD)"),
    ("sub", "despesas_intermed", "Total das despesas da intermediação"),
    ("tot", "resultado_bruto", "Resultado bruto da intermediação financeira"),
    ("sec", None, "Outras receitas e despesas operacionais"),
    ("in", "servicos", "Receitas de prestação de serviços"),
    ("in", "tarifas", "Rendas de tarifas"),
    ("in", "pessoal", "Despesas de pessoal"),
    ("in", "outras_adm", "Outras despesas administrativas"),
    ("in", "tributarias", "Despesas tributárias"),
    ("in", "outras_rec_op", "Outras receitas operacionais"),
    ("in", "outras_desp_op", "Outras despesas operacionais"),
    ("in", "contingencias", "Provisões para contingências e garantias (líquidas)"),
    ("sub", "outras_op", "Total de outras receitas e despesas operacionais"),
    ("tot", "resultado_operacional", "Resultado operacional"),
    ("in", "nao_operacional", "Resultado não operacional"),
    ("tot", "resultado_antes_ir", "Resultado antes da tributação"),
    ("in", "ir_cs", "IR e CS sobre atos não cooperativos"),
    ("tot", "resultado", "Resultado antes dos juros ao capital (sobras brutas)"),
    ("in", "juros_capital", "Juros ao capital"),
    ("tot", "sobras_apos_juros", "Sobras do exercício após juros ao capital"),
    ("sec", None, "Destinações"),
    ("in", "dest_fates_ato", "FATES: resultado de atos não cooperativos"),
    ("in", "dest_reserva", "Reserva legal (45% da base)"),
    ("in", "dest_fates", "FATES estatutário (5% da base)"),
    ("tot", "sobras_ago", "Sobras à disposição da AGO"),
]


def vdsp(k, a):
    if k == "fgcoop_neg":
        return -D[a]["fgcoop"]
    return D[a][k]


def tabela_dsp():
    h = ['<div class="tbl-wrap"><table class="fin av-ah" id="tab-dsp"><caption>Demonstração de sobras ou perdas (DSP), em R$ mil. '
         'AV sobre o total das receitas da intermediação</caption><thead><tr><th>Linha</th><th>2024</th><th>2025</th>'
         '<th class="c-av">AV 2024</th><th class="c-av">AV 2025</th><th class="c-ah">AH 25/24</th><th class="c-ah">Variação</th></tr></thead><tbody>']
    b24, b25 = D[2024]["receitas_intermed"], D[2025]["receitas_intermed"]
    for tipo, k, rot in DSP_LINHAS:
        if tipo == "sec":
            h.append(f'<tr class="sec"><td colspan="7">{rot}</td></tr>')
            continue
        v24, v25 = vdsp(k, 2024), vdsp(k, 2025)
        cls = {"sub": "sub", "tot": "tot"}.get(tipo, "")
        h.append(f'<tr class="{cls}"><td>{rot}</td><td>{par(v24)}</td><td>{par(v25)}</td>'
                 f'<td class="c-av">{_av(v24, b24)}</td><td class="c-av">{_av(v25, b25)}</td>'
                 f'<td class="c-ah">{_ah(v25, v24)}</td><td class="c-ah">{par(v25 - v24)}</td></tr>')
    h.append("</tbody></table></div>")
    return "".join(h)


def ger(k, a):
    dd = D[a]
    return {
        "g_credito": dd["rend_credito"], "g_liquidez": dd["rend_liquidez"], "g_captacao": dd["desp_captacao"],
        "g_repasses": dd["desp_repasses"], "mf": dd["mf"], "g_servicos": dd["servicos"] + dd["tarifas"],
        "g_outras": dd["outras_rec_op"] + dd["outras_desp_op"] + dd["tributarias"] + dd["contingencias"],
        "receita_liquida": dd["receita_liquida"], "desp_adm": dd["desp_adm"], "pdd_liquida": dd["pdd_liquida"],
        "res_op": dd["receita_liquida"] + dd["desp_adm"] + dd["pdd_liquida"], "g_nao_op": dd["nao_operacional"],
        "g_ir": dd["ir_cs"], "resultado": dd["resultado"], "nr": I[a]["nao_recorrente"],
        "resultado_recorrente": I[a]["resultado_recorrente"],
    }[k]


GER_LINHAS = [
    ("in", "g_credito", "Receita de crédito", "Operações de crédito"),
    ("in", "g_liquidez", "(+) Receita da liquidez", "Centralização + aplicações + TVM"),
    ("in", "g_captacao", "(-) Despesa de captação", "Poupança, RDC, LCA, LFS e FGCoop"),
    ("in", "g_repasses", "(-) Despesa de repasses", "Central, Banco e BNDES"),
    ("tot", "mf", "(=) Margem financeira", "Antes da PDD"),
    ("in", "g_servicos", "(+) Serviços e tarifas", ""),
    ("in", "g_outras", "(+/-) Outras receitas e despesas operacionais", "Inclui tributárias e contingências"),
    ("tot", "receita_liquida", "(=) Receita líquida", "Base do índice de eficiência"),
    ("in", "desp_adm", "(-) Despesas administrativas", "Pessoal + outras administrativas"),
    ("in", "pdd_liquida", "(-) PDD líquida de recuperações", "Custo do risco de crédito"),
    ("tot", "res_op", "(=) Resultado operacional", ""),
    ("in", "g_nao_op", "(+/-) Resultado não operacional", ""),
    ("in", "g_ir", "(-) IR e CS", ""),
    ("tot", "resultado", "(=) Resultado antes dos juros ao capital", "Base do ROE"),
    ("in", "nr", "(-) Itens não recorrentes", "Notas"),
    ("tot", "resultado_recorrente", "(=) Resultado recorrente", ""),
]


def tabela_gerencial():
    h = ['<div class="tbl-wrap"><table class="fin"><caption>DRE gerencial em cascata, em R$ mil</caption><thead><tr>'
         '<th>Linha</th><th>2024</th><th>2025</th><th>AH</th><th>Observação</th></tr></thead><tbody>']
    for tipo, k, rot, obs in GER_LINHAS:
        v24, v25 = ger(k, 2024), ger(k, 2025)
        cls = "tot" if tipo == "tot" else ""
        h.append(f'<tr class="{cls}"><td>{rot}</td><td>{par(v24)}</td><td>{par(v25)}</td><td>{_ah(v25, v24)}</td><td class="obs">{obs}</td></tr>')
    h.append("</tbody></table></div>")
    return "".join(h)


def tabela(cab, linhas, caption="", classe="fin", alinhar_esq=1):
    h = [f'<div class="tbl-wrap"><table class="{classe}">']
    if caption:
        h.append(f"<caption>{caption}</caption>")
    h.append("<thead><tr>" + "".join(f"<th>{c}</th>" for c in cab) + "</tr></thead><tbody>")
    for ln in linhas:
        cls = ""
        if isinstance(ln, dict):
            cls = ln.get("cls", "")
            ln = ln["c"]
        h.append(f'<tr class="{cls}">' + "".join(f"<td>{c}</td>" for c in ln) + "</tr>")
    h.append("</tbody></table></div>")
    return "".join(h)


def nota_saldos_2023():
    ks = [("ativo", "Ativo total"), ("caixa", "Disponibilidades"), ("centralizacao", "Centralização financeira"),
          ("aplic_interfin", "Aplicações interfinanceiras"), ("tvm", "TVM"), ("cred_comercial", "Carteira comercial"),
          ("cred_rural", "Carteira rural"), ("carteira", "Carteira bruta"), ("provisao", "Provisão"),
          ("dep_vista", "Depósitos à vista"), ("poupanca", "Poupança"), ("rdc", "RDC"), ("lca", "LCA"),
          ("repasses_interfin", "Repasses interfinanceiros"), ("emprestimos_repasses", "Empréstimos e repasses"),
          ("pl", "Patrimônio líquido"), ("capital_social", "Capital social")]
    return tabela(["Saldo em 31/12/2023", "R$ mil"], [[r, par(S[k][2023])] for k, r in ks],
                  "Usados só para calcular as médias de 2024")


def nota_carteira():
    lin = []
    for k, r, prov in (("cred_comercial", "Comercial (empréstimos + financiamentos)", "prov_comercial"),
                       ("cred_rural", "Rural e agroindustrial", "prov_rural")):
        rec = "rend_comercial" if k == "cred_comercial" else "rend_rural"
        lin.append([r, par(S[k][2024]), par(S[k][2025]), par(NOTAS[prov][2024]), par(NOTAS[prov][2025]),
                    par(D[2024][rec]), par(D[2025][rec])])
    lin.append({"cls": "tot", "c": ["Total", par(S["carteira"][2024]), par(S["carteira"][2025]), par(-S["provisao"][2024]),
                                    par(-S["provisao"][2025]), par(D[2024]["rend_credito"]), par(D[2025]["rend_credito"])]})
    return tabela(["Carteira", "Saldo 2024", "Saldo 2025", "Provisão 2024", "Provisão 2025", "Receita 2024", "Receita 2025"], lin,
                  "Carteira, provisão e receita por segmento, em R$ mil")


def nota_atraso():
    rot = {"em_dia": "Em dia", "d1_14": "1 a 14 dias", "d15_30": "15 a 30 dias", "d31_60": "31 a 60 dias",
           "d61_90": "61 a 90 dias", "d90": "Acima de 90 dias"}
    lin = [[r, par(at(k, 2024)), _av(at(k, 2024), S["carteira"][2024]), par(at(k, 2025)), _av(at(k, 2025), S["carteira"][2025])]
           for k, r in rot.items()]
    lin.append({"cls": "tot", "c": ["Total", par(S["carteira"][2024]), "100,0%", par(S["carteira"][2025]), "100,0%"]})
    return tabela(["Faixa de atraso", "2024", "% carteira", "2025", "% carteira"], lin,
                  "Carteira bruta por faixa de atraso, em R$ mil (o saldo inteiro da operação vai para a faixa da parcela mais atrasada)")


def nota_estagio():
    lin = []
    for k, r in (("e1", "Estágio 1: risco normal (perda de 12 meses)"), ("e2", "Estágio 2: aumento significativo do risco (perda da vida toda)"),
                 ("e3", "Estágio 3: ativo com problema de recuperação")):
        lin.append([r, par(est(k, 2024)), par(est(k, 2024, 1)), fnum(est(k, 2024, 1) / est(k, 2024) * 100, 1) + "%",
                    par(est(k, 2025)), par(est(k, 2025, 1)), fnum(est(k, 2025, 1) / est(k, 2025) * 100, 1) + "%"])
    lin.append({"cls": "tot", "c": ["Total", par(S["carteira"][2024]), par(-S["provisao"][2024]), fnum(I[2024]["prov_carteira"] * 100, 1) + "%",
                                    par(S["carteira"][2025]), par(-S["provisao"][2025]), fnum(I[2025]["prov_carteira"] * 100, 1) + "%"]})
    return tabela(["Estágio (Res. CMN 4.966)", "Saldo 2024", "Provisão 2024", "Cobertura", "Saldo 2025", "Provisão 2025", "Cobertura"], lin,
                  "Carteira por estágio, em R$ mil (2024 apresentado em base comparável, para treino)")


def nota_outros():
    lin = [
        ["Associados (quantidade)", fnum(NOTAS["associados"][2023]), fnum(NOTAS["associados"][2024]), fnum(NOTAS["associados"][2025])],
        ["Operações renegociadas no ano (saldo, R$ mil)", "", par(NOTAS["renegociadas"][2024]), par(NOTAS["renegociadas"][2025])],
        ["20 maiores devedores ÷ carteira", "", FMT["p1"](NOTAS["top20_devedores"][2024]), FMT["p1"](NOTAS["top20_devedores"][2025])],
        ["10 maiores depositantes ÷ captação", "", FMT["p1"](NOTAS["top10_depositantes"][2024]), FMT["p1"](NOTAS["top10_depositantes"][2025])],
        ["Coobrigações e garantias prestadas (R$ mil)", "", par(NOTAS["coobrigacoes"][2024]), par(NOTAS["coobrigacoes"][2025])],
        ["Depreciação e amortização, dentro de outras despesas administrativas (R$ mil)", "", par(NOTAS["deprec"][2024]), par(NOTAS["deprec"][2025])],
        ["Rateios da Central e da Confederação, dentro de outras despesas administrativas (R$ mil)", "", par(NOTAS["rateios"][2024]), par(NOTAS["rateios"][2025])],
        ["CDI médio do ano (premissa)", "", FMT["p1"](M.CDI[2024]), FMT["p1"](M.CDI[2025])],
        ["IPCA do ano (premissa)", "", FMT["p1"](M.IPCA[2024]), FMT["p1"](M.IPCA[2025])],
    ]
    return tabela(["Informação", "2023", "2024", "2025"], lin, "Outras informações das notas")


def nota_nao_recorrentes():
    rot = [("nr_pdv", "Programa de desligamento voluntário (despesa de pessoal)"),
           ("nr_venda_imovel", "Venda de imóvel de agência (resultado não operacional)"),
           ("nr_reversao_conting", "Reversão de contingência fiscal ganha (contingências)"),
           ("nr_recuperacao_extra", "Recuperação extraordinária de um grande crédito já baixado")]
    lin = [[r, par(NOTAS[k][2024]), par(NOTAS[k][2025])] for k, r in rot]
    lin.append({"cls": "tot", "c": ["Total (efeito no resultado)", par(I[2024]["nao_recorrente"]), par(I[2025]["nao_recorrente"])]})
    return tabela(["Item não recorrente (+ ganho, - perda)", "2024", "2025"], lin, "Itens que a diretoria classifica como não recorrentes, em R$ mil")


def nota_dmpl():
    cap24, res24, sob24, aap24 = S["capital_social"][2024], S["reserva_legal"][2024], S["sobras_acum"][2024], S["aap"][2024]
    ago_cap = M.r10(sob24 * M.DMPL["pct_ago_capital"])
    jcp = -D[2025]["juros_capital"]
    fates = D[2025]["dest_fates_ato"] + D[2025]["dest_fates"]
    resv = -D[2025]["dest_reserva"]
    lin = [
        {"cls": "tot", "c": ["Saldo em 31/12/2024", par(cap24), par(res24), par(sob24), par(aap24), par(S["pl"][2024])]},
        ["Integralizações de capital", par(M.DMPL["integralizacoes"]), "-", "-", "-", par(M.DMPL["integralizacoes"])],
        ["Devoluções de quotas (associados desligados)", par(M.DMPL["devolucoes"]), "-", "-", "-", par(M.DMPL["devolucoes"])],
        ["AGO: sobras de 2024 capitalizadas", par(ago_cap), "-", par(-ago_cap), "-", "-"],
        ["AGO: sobras de 2024 creditadas em conta corrente", "-", "-", par(-(sob24 - ago_cap)), "-", par(-(sob24 - ago_cap))],
        ["Resultado do exercício", "-", "-", par(D[2025]["resultado"]), "-", par(D[2025]["resultado"])],
        ["Juros ao capital (destinação e incorporação às quotas)", par(jcp), "-", par(-jcp), "-", "-"],
        ["FATES (ato não cooperativo + 5%)", "-", "-", par(fates), "-", par(fates)],
        ["Reserva legal (45%)", "-", par(resv), par(-resv), "-", "-"],
        ["Ajuste de avaliação patrimonial", "-", "-", "-", par(S["aap"][2025] - aap24), par(S["aap"][2025] - aap24)],
        {"cls": "tot", "c": ["Saldo em 31/12/2025", par(S["capital_social"][2025]), par(S["reserva_legal"][2025]), par(S["sobras_acum"][2025]),
                             par(S["aap"][2025]), par(S["pl"][2025])]},
    ]
    return tabela(["Evento", "Capital social", "Reserva legal", "Sobras acumuladas", "Ajustes de avaliação", "Total do PL"], lin,
                  "Mutações do patrimônio líquido em 2025 (DMPL), em R$ mil")


FPR_ROT = {"caixa": "Disponibilidades", "centralizacao": "Centralização financeira", "aplic_interfin": "Aplicações interfinanceiras",
           "tvm": "Títulos públicos federais", "comercial": "Carteira comercial (líquida de provisão)", "rural": "Carteira rural (líquida de provisão)",
           "outros_ativos_fin": "Outros ativos financeiros", "ativos_fiscais": "Ativos fiscais", "bndu_outros": "BNDU e outros ativos",
           "investimentos": "Investimentos", "imobilizado": "Imobilizado", "coobrigacoes": "Coobrigações e garantias (fora do balanço)"}


def tabela_rwa():
    lin = []
    for k, r in FPR_ROT.items():
        lin.append([r, fnum(M.FPR[k] * 100) + "%", par(I[2024]["expo"][k]), par(I[2024]["rwa_cred_det"][k]),
                    par(I[2025]["expo"][k]), par(I[2025]["rwa_cred_det"][k])])
    lin.append({"cls": "sub", "c": ["RWA de risco de crédito", "", "", par(I[2024]["rwa_credito"]), "", par(I[2025]["rwa_credito"])]})
    lin.append(["RWA de risco operacional (15% × receita bruta média de 3 anos ÷ 8%)", "", "", par(I[2024]["rwa_operacional"]), "", par(I[2025]["rwa_operacional"])])
    lin.append(["RWA de risco de mercado (informado)", "", "", par(I[2024]["rwa_mercado"]), "", par(I[2025]["rwa_mercado"])])
    lin.append({"cls": "tot", "c": ["RWA total", "", "", par(I[2024]["rwa"]), "", par(I[2025]["rwa"])]})
    lin.append(["Patrimônio líquido", "", "", par(S["pl"][2024]), "", par(S["pl"][2025])])
    lin.append(["(-) Ajustes prudenciais (intangível + outros)", "", "", par(-I[2024]["ajustes_prud"]), "", par(-I[2025]["ajustes_prud"])])
    lin.append({"cls": "sub", "c": ["(=) Capital principal (Nível I)", "", "", par(I[2024]["capital_principal"]), "", par(I[2025]["capital_principal"])]})
    lin.append(["(+) Nível II (LFS)", "", "", par(I[2024]["nivel2"]), "", par(I[2025]["nivel2"])])
    lin.append({"cls": "tot", "c": ["(=) Patrimônio de referência (PR)", "", "", par(I[2024]["pr"]), "", par(I[2025]["pr"])]})
    lin.append({"cls": "tot", "c": ["Índice de Basileia (PR ÷ RWA)", "", "", FMT["p2"](I[2024]["basileia"]), "", FMT["p2"](I[2025]["basileia"])]})
    return tabela(["Exposição", "FPR", "Exposição 2024", "RWA 2024", "Exposição 2025", "RWA 2025"], lin,
                  "Do balanço ao índice de Basileia, em R$ mil (FPR ilustrativos)")


def tabela_ftp():
    rot = [("comercial", "Crédito comercial", "paga"), ("rural", "Crédito rural", "paga"), ("dep_vista", "Depósito à vista", "recebe"),
           ("poupanca", "Poupança", "recebe"), ("rdc", "RDC", "recebe"), ("lca", "LCA", "recebe")]
    lin = []
    for k, r, sentido in rot:
        lin.append([r, sentido, FMT["p1"](M.FTP[k][2024]), FMT["p1"](M.FTP[k][2025]), par(ftp(k, 2024)), par(ftp(k, 2025))])
    lin.append({"cls": "sub", "c": ["Soma dos produtos", "", "", "", par(ftp("soma_produtos", 2024)), par(ftp("soma_produtos", 2025))]})
    lin.append(["Tesouraria / ALM (descasamento + PL sem custo + FGCoop, LFS e repasses)", "", "", "", par(ftp("tesouraria", 2024)), par(ftp("tesouraria", 2025))])
    lin.append({"cls": "tot", "c": ["Margem financeira", "", "", "", par(D[2024]["mf"]), par(D[2025]["mf"])]})
    return tabela(["Produto", "Em relação à tesouraria", "FTP 2024", "FTP 2025", "Margem FTP 2024", "Margem FTP 2025"], lin,
                  "Margem financeira repartida por produto com FTP, em R$ mil")


def tabela_lcr():
    lin = []
    for a in (2024, 2025):
        pass
    L24, L25 = M.LCR[2024], M.LCR[2025]
    lin = [
        ["Caixa + TVM + centralização (ativos líquidos)", "", par(I[2024]["hqla"]), par(I[2025]["hqla"])],
        ["Fuga de depósitos à vista", FMT["p0"](L25["dv_fator"]), par(S["dep_vista"][2024] * L24["dv_fator"]), par(S["dep_vista"][2025] * L25["dv_fator"])],
        ["Fuga de poupança", FMT["p0"](L25["poup_fator"]), par(S["poupanca"][2024] * L24["poup_fator"]), par(S["poupanca"][2025] * L25["poup_fator"])],
        ["Fuga de RDC (média, inclui liquidez diária)", FMT["p0"](L25["rdc_fator"]), par(S["rdc"][2024] * L24["rdc_fator"]), par(S["rdc"][2025] * L25["rdc_fator"])],
        ["LCA vencendo em 30 dias", "100%", par(L24["lca_30d"]), par(L25["lca_30d"])],
        ["Repasses e obrigações vencendo em 30 dias", "100%", par(L24["obrig_30d"]), par(L25["obrig_30d"])],
        ["Uso de limites não utilizados", FMT["p0"](L25["limites_fator"]) + " de " + "limites", par(L24["limites"] * L24["limites_fator"]), par(L25["limites"] * L25["limites_fator"])],
        ["Outras saídas contratuais", "100%", par(L24["outras_saidas"]), par(L25["outras_saidas"])],
        {"cls": "sub", "c": ["Saídas totais", "", par(I[2024]["lcr_saidas"]), par(I[2025]["lcr_saidas"])]},
        ["Entradas: 50% das parcelas a receber + aplicações que vencem (teto de 75% das saídas)", "", par(I[2024]["lcr_entradas"]), par(I[2025]["lcr_entradas"])],
        {"cls": "sub", "c": ["Saídas líquidas", "", par(I[2024]["lcr_saidas"] - I[2024]["lcr_entradas"]), par(I[2025]["lcr_saidas"] - I[2025]["lcr_entradas"])]},
        {"cls": "tot", "c": ["LCR didático", "", FMT["p0"](I[2024]["lcr"]), FMT["p0"](I[2025]["lcr"])]},
    ]
    return tabela(["Componente (estresse de 30 dias)", "Fator", "2024", "2025"], lin, "LCR didático da Coop Vale do Ipê, em R$ mil")


def tabela_taxas():
    rot = [
        ("Carteira comercial", D[2024]["rend_comercial"] / M.media(S["cred_comercial"], 2024), D[2025]["rend_comercial"] / M.media(S["cred_comercial"], 2025)),
        ("Carteira rural", D[2024]["rend_rural"] / M.media(S["cred_rural"], 2024), D[2025]["rend_rural"] / M.media(S["cred_rural"], 2025)),
        ("Liquidez (centralização + aplicações + TVM)", I[2024]["taxa_liquidez"], I[2025]["taxa_liquidez"]),
        ("Poupança", -D[2024]["desp_poupanca"] / M.media(S["poupanca"], 2024), -D[2025]["desp_poupanca"] / M.media(S["poupanca"], 2025)),
        ("RDC", -D[2024]["desp_rdc"] / M.media(S["rdc"], 2024), -D[2025]["desp_rdc"] / M.media(S["rdc"], 2025)),
        ("LCA", -D[2024]["desp_lca"] / M.media(S["lca"], 2024), -D[2025]["desp_lca"] / M.media(S["lca"], 2025)),
        ("Repasses interfinanceiros", -D[2024]["desp_repasses_interfin"] / M.media(S["repasses_interfin"], 2024), -D[2025]["desp_repasses_interfin"] / M.media(S["repasses_interfin"], 2025)),
        ("Empréstimos e repasses (BNDES)", -D[2024]["desp_emprestimos_repasses"] / M.media(S["emprestimos_repasses"], 2024), -D[2025]["desp_emprestimos_repasses"] / M.media(S["emprestimos_repasses"], 2025)),
    ]
    lin = [[r, FMT["p1"](t24), FMT["p0"](t24 / M.CDI[2024]), FMT["p1"](t25), FMT["p0"](t25 / M.CDI[2025])] for r, t24, t25 in rot]
    lin.append({"cls": "sub", "c": ["CDI médio (referência)", FMT["p1"](M.CDI[2024]), "100%", FMT["p1"](M.CDI[2025]), "100%"]})
    return tabela(["Linha", "Taxa 2024", "% do CDI", "Taxa 2025", "% do CDI"], lin,
                  "Taxas implícitas: receita ou despesa ÷ saldo médio")


def tabela_fontes_usos():
    linhas_a = [("Carteira de crédito líquida", S["carteira"][2025] + S["provisao"][2025] - S["carteira"][2024] - S["provisao"][2024]),
                ("Centralização financeira", S["centralizacao"][2025] - S["centralizacao"][2024]),
                ("Aplicações interfinanceiras", S["aplic_interfin"][2025] - S["aplic_interfin"][2024]),
                ("TVM", S["tvm"][2025] - S["tvm"][2024]),
                ("Investimentos", S["investimentos"][2025] - S["investimentos"][2024]),
                ("Imobilizado e intangível", S["imobilizado"][2025] + S["intangivel"][2025] - S["imobilizado"][2024] - S["intangivel"][2024]),
                ("Caixa, outros ativos financeiros, fiscais, BNDU e outros",
                 sum(S[k][2025] - S[k][2024] for k in ("caixa", "outros_ativos_fin", "ativos_fiscais", "bndu", "outros_ativos")))]
    linhas_p = [("Depósitos a prazo (RDC)", S["rdc"][2025] - S["rdc"][2024]),
                ("Depósitos à vista e poupança", S["dep_vista"][2025] + S["poupanca"][2025] - S["dep_vista"][2024] - S["poupanca"][2024]),
                ("LCA", S["lca"][2025] - S["lca"][2024]),
                ("Repasses (Central, Banco e BNDES)", S["repasses_interfin"][2025] + S["emprestimos_repasses"][2025] - S["repasses_interfin"][2024] - S["emprestimos_repasses"][2024]),
                ("LFS", S["lfs"][2025] - S["lfs"][2024]),
                ("Outros passivos", sum(S[k][2025] - S[k][2024] for k in ("outros_passivos_fin", "provisoes", "obrig_sociais", "obrig_fiscais_outras"))),
                ("Patrimônio líquido", S["pl"][2025] - S["pl"][2024])]
    tu, tf = sum(v for _, v in linhas_a), sum(v for _, v in linhas_p)
    lin = []
    for j in range(max(len(linhas_a), len(linhas_p))):
        a = linhas_a[j] if j < len(linhas_a) else ("", None)
        p = linhas_p[j] if j < len(linhas_p) else ("", None)
        lin.append([a[0], par(a[1]) if a[1] is not None else "", _av(a[1], tu) if a[1] is not None else "",
                    p[0], par(p[1]) if p[1] is not None else "", _av(p[1], tf) if p[1] is not None else ""])
    lin.append({"cls": "tot", "c": ["Total de usos", par(tu), "100,0%", "Total de fontes", par(tf), "100,0%"]})
    return tabela(["Usos (para onde foi)", "R$ mil", "%", "Fontes (de onde veio)", "R$ mil", "%"], lin,
                  "Fontes e usos de 2025: variação de cada linha do balanço")


# ------------------------------------------------------------------ painel (indicadores)
def semaforo(nivel):
    rot = {"bom": ("ok", "✓", "Bom"), "atencao": ("warn", "!", "Atenção"), "ruim": ("bad", "✕", "Ruim")}[nivel]
    return f'<span class="st st-{rot[0]}" title="{rot[2]}"><span aria-hidden="true">{rot[1]}</span> {rot[2]}</span>'


def regua(valor, verde, vermelho, maior_melhor=True):
    if maior_melhor:
        return "bom" if valor >= verde else ("ruim" if valor < vermelho else "atencao")
    return "bom" if valor <= verde else ("ruim" if valor > vermelho else "atencao")


PAINEL = [
    # rótulo, chave, formato, régua(verde, vermelho, maior_melhor) ou função, texto da régua, âncora
    ("ROE contábil", "roe", "p1", (0.15, 0.1434, True), "verde ≥ 15% (custo de capital); vermelho < CDI", "ind-roe"),
    ("ROE recorrente", "roe_recorrente", "p1", (0.15, 0.1434, True), "mesma régua do ROE", "ind-recorrente"),
    ("Margem financeira ÷ ativo (NIM)", "nim", "p2", (0.065, 0.05, True), "verde ≥ 6,5%; vermelho < 5%", "ind-mf"),
    ("Spread de crédito (p.p.)", "spread_pp", "pp1", (9, 6, True), "verde ≥ 9 p.p.; vermelho < 6 p.p.", "ind-spread"),
    ("Índice de eficiência", "ie", "p1", (0.55, 0.65, False), "verde ≤ 55%; vermelho > 65%", "ind-ie"),
    ("IEAR (eficiência + risco)", "iear", "p1", (0.75, 0.90, False), "verde ≤ 75%; vermelho > 90%", "ind-ie"),
    ("Inadimplência > 90 dias", "npl90", "p2", (0.025, 0.04, False), "verde ≤ 2,5%; vermelho > 4%", "ind-inad"),
    ("Cobertura do NPL 90", "cobertura_npl", "p0", (2.0, 1.2, True), "verde ≥ 200%; vermelho < 120%", "ind-pdd"),
    ("Custo do risco", "custo_risco", "p2", (0.03, 0.045, False), "verde ≤ 3%; vermelho > 4,5%", "ind-pdd"),
    ("Crescimento da carteira", "cresc_carteira", "p1", None, "verde se ≤ crescimento do PL + 2 p.p.", "ind-cresc"),
    ("Custo da captação ÷ CDI", "custo_capt_cdi", "p0", (0.80, 0.90, False), "verde ≤ 80% do CDI; vermelho > 90%", "ind-capt"),
    ("Índice de Basileia", "basileia", "p2", (0.145, 0.125, True), "verde ≥ 14,5%; vermelho < 12,5% (10,5% + 2 p.p.)", "ind-basileia"),
    ("RWA ÷ ativo (densidade)", "densidade", "p1", (0.80, 0.90, False), "verde ≤ 80%; vermelho > 90%", "ind-rwa"),
    ("Índice de liquidez interno", "indice_liquidez", "x2", None, "verde entre 1,2 e 2,0; vermelho < 1", "ind-liq"),
    ("PL ÷ ativo", "pl_ativo", "p1", (0.11, 0.08, True), "verde ≥ 11%; vermelho < 8%", "ind-pl"),
]


def _valor_painel(k, a):
    if k == "spread_pp":
        return I[a]["spread_credito"] * 100
    if k == "custo_capt_cdi":
        return I[a]["custo_captacao"] / M.CDI[a]
    if k == "densidade":
        return I[a]["rwa"] / S["ativo"][a]
    return I[a][k]


def painel():
    h = ['<div class="kpis">']
    for rot, k, fmt, rg, txt, anc in PAINEL:
        v24, v25 = _valor_painel(k, 2024), _valor_painel(k, 2025)
        if k == "cresc_carteira":
            nivel = "bom" if v25 <= I[2025]["cresc_pl"] + 0.02 else "atencao"
        elif k == "indice_liquidez":
            nivel = "bom" if 1.2 <= v25 <= 2.0 else ("ruim" if v25 < 1 else "atencao")
        else:
            nivel = regua(v25, *rg)
        delta = v25 - v24
        if fmt in ("p0", "p1", "p2"):
            dtxt = fnum(delta * 100, 1) + " p.p."
        elif fmt == "x2":
            dtxt = fnum(delta, 2) + "x"
        else:
            dtxt = fnum(delta, 1) + " p.p."
        seta = "▲" if delta > 0 else ("▼" if delta < 0 else "■")
        h.append(f'<a class="kpi" href="#{anc}"><div class="kpi-lbl">{rot}</div><div class="kpi-val">{FMT[fmt](v25)}</div>'
                 f'<div class="kpi-delta"><span aria-hidden="true">{seta}</span> {("+" if delta > 0 else "")}{dtxt} vs 2024 ({FMT[fmt](v24)})</div>'
                 f'<div class="kpi-st">{semaforo(nivel)}</div><div class="kpi-regua">{txt}</div></a>')
    h.append("</div>")
    return "".join(h)


def tabela_resumo():
    rows = [
        ("Patrimônio líquido (R$ mil)", par(S["pl"][2024]), par(S["pl"][2025]), "ind-pl"),
        ("Crescimento do PL", FMT["p1"](I[2024]["cresc_pl"]), FMT["p1"](I[2025]["cresc_pl"]), "ind-pl"),
        ("Crescimento da carteira", FMT["p1"](I[2024]["cresc_carteira"]), FMT["p1"](I[2025]["cresc_carteira"]), "ind-cresc"),
        ("Captação com associados (R$ mil)", par(I[2024]["captacao_total"]), par(I[2025]["captacao_total"]), "ind-capt"),
        ("Custo médio da captação", FMT["p2"](I[2024]["custo_captacao"]), FMT["p2"](I[2025]["custo_captacao"]), "ind-capt"),
        ("Margem financeira (R$ mil)", par(D[2024]["mf"]), par(D[2025]["mf"]), "ind-mf"),
        ("NIM (margem ÷ ativo médio)", FMT["p2"](I[2024]["nim"]), FMT["p2"](I[2025]["nim"]), "ind-mf"),
        ("Spread de crédito", fnum(I[2024]["spread_credito"] * 100, 2) + " p.p.", fnum(I[2025]["spread_credito"] * 100, 2) + " p.p.", "ind-spread"),
        ("Índice de eficiência", FMT["p1"](I[2024]["ie"]), FMT["p1"](I[2025]["ie"]), "ind-ie"),
        ("IEAR", FMT["p1"](I[2024]["iear"]), FMT["p1"](I[2025]["iear"]), "ind-ie"),
        ("NPL 90", FMT["p2"](I[2024]["npl90"]), FMT["p2"](I[2025]["npl90"]), "ind-inad"),
        ("Provisão ÷ carteira", FMT["p2"](I[2024]["prov_carteira"]), FMT["p2"](I[2025]["prov_carteira"]), "ind-pdd"),
        ("Cobertura do NPL 90", FMT["p0"](I[2024]["cobertura_npl"]), FMT["p0"](I[2025]["cobertura_npl"]), "ind-pdd"),
        ("Resultado (R$ mil)", par(D[2024]["resultado"]), par(D[2025]["resultado"]), "ind-roe"),
        ("Resultado recorrente (R$ mil)", par(I[2024]["resultado_recorrente"]), par(I[2025]["resultado_recorrente"]), "ind-recorrente"),
        ("ROE", FMT["p2"](I[2024]["roe"]), FMT["p2"](I[2025]["roe"]), "ind-roe"),
        ("ROE recorrente", FMT["p2"](I[2024]["roe_recorrente"]), FMT["p2"](I[2025]["roe_recorrente"]), "ind-recorrente"),
        ("RWA (R$ mil)", par(I[2024]["rwa"]), par(I[2025]["rwa"]), "ind-rwa"),
        ("Índice de Basileia", FMT["p2"](I[2024]["basileia"]), FMT["p2"](I[2025]["basileia"]), "ind-basileia"),
        ("MM/RWA", fnum(I[2024]["mm_rwa"], 2) + " p.p.", fnum(I[2025]["mm_rwa"], 2) + " p.p.", "ind-basileia"),
        ("Índice de liquidez interno", FMT["x2"](I[2024]["indice_liquidez"]), FMT["x2"](I[2025]["indice_liquidez"]), "ind-liq"),
        ("LCR didático", FMT["p0"](I[2024]["lcr"]), FMT["p0"](I[2025]["lcr"]), "ind-liq"),
        ("Margem FTP do RDC (R$ mil)", par(ftp("rdc", 2024)), par(ftp("rdc", 2025)), "ind-ftp"),
        ("RAROC da carteira comercial", "", FMT["p1"](rar("comercial", "raroc")), "ind-raroc"),
        ("RAROC da carteira rural", "", FMT["p1"](rar("rural", "raroc")), "ind-raroc"),
    ]
    return tabela(["Indicador", "2024", "2025"], [[f'<a href="#{a}">{r}</a>', x, y] for r, x, y, a in rows],
                  "Os 15 indicadores da Coop Vale do Ipê lado a lado")


# ------------------------------------------------------------------ gráficos SVG
def _esc(t):
    return html.escape(str(t), quote=True)


def _barras_100(titulo, linhas, legenda, idt):
    W, x0, bw = 760, 120, 620
    h = 24
    n_l = len(linhas)
    out = [f'<svg class="chart" viewBox="0 0 {W} {n_l * 40 + 70}" role="img" aria-labelledby="{idt}"><title id="{idt}">{_esc(titulo)}</title>']
    for n_, (rot, segs) in enumerate(linhas):
        yy = 8 + n_ * 40
        out.append(f'<text class="ax" x="{x0 - 8}" y="{yy + 16}" text-anchor="end">{rot}</text>')
        tot = sum(v for _, v in segs)
        x = x0
        for j, (nome, v) in enumerate(segs):
            w = v / tot * bw
            out.append(f'<rect class="s{j + 1}" x="{x + 1:.1f}" y="{yy}" width="{max(w - 2, 0.5):.1f}" height="{h}" rx="3" '
                       f'data-tip="{_esc(rot)}: {_esc(nome)} = R$ {fnum(v / 1000, 1)} mi ({fnum(v / tot * 100, 1)}%)"></rect>')
            if w > 40:
                out.append(f'<text class="in-lbl" x="{x + w / 2:.1f}" y="{yy + 16}" text-anchor="middle">{fnum(v / tot * 100, 0)}%</text>')
            x += w
    ly, lx = n_l * 40 + 30, x0
    for j, nome in enumerate(legenda):
        larg = 14 + len(nome) * 6.4 + 16
        if lx + larg > W:
            ly += 20
            lx = x0
        out.append(f'<rect class="s{j + 1}" x="{lx}" y="{ly - 10}" width="10" height="10" rx="2"></rect><text class="ax" x="{lx + 14}" y="{ly}">{nome}</text>')
        lx += larg
    out.append("</svg>")
    return "".join(out)


def svg_composicao():
    def segs_ativo(a):
        return [("Liquidez", S["liquidez"][a]), ("Crédito líquido", S["carteira"][a] + S["provisao"][a]),
                ("Investimentos, imobilizado e intangível", S["investimentos"][a] + S["imobilizado"][a] + S["intangivel"][a]),
                ("Outros ativos", S["outros_ativos_fin"][a] + S["ativos_fiscais"][a] + S["bndu"][a] + S["outros_ativos"][a])]

    def segs_passivo(a):
        return [("Depósitos à vista", S["dep_vista"][a]), ("Poupança", S["poupanca"][a]), ("RDC", S["rdc"][a]), ("LCA", S["lca"][a]),
                ("Repasses", S["repasses_interfin"][a] + S["emprestimos_repasses"][a]),
                ("Outros passivos e LFS", S["lfs"][a] + S["outros_passivos_fin"][a] + S["provisoes"][a] + S["obrig_sociais"][a] + S["obrig_fiscais_outras"][a]),
                ("Patrimônio líquido", S["pl"][a])]
    a1 = _barras_100("Composição do ativo, 2024 e 2025", [("Ativo 2024", segs_ativo(2024)), ("Ativo 2025", segs_ativo(2025))],
                     [n_ for n_, _ in segs_ativo(2025)], "t-comp-a")
    a2 = _barras_100("Composição do passivo + PL, 2024 e 2025", [("Passivo + PL 2024", segs_passivo(2024)), ("Passivo + PL 2025", segs_passivo(2025))],
                     [n_ for n_, _ in segs_passivo(2025)], "t-comp-p")
    return '<h4>Para onde vai o dinheiro (ativo)</h4>' + a1 + '<h4>De onde vem o dinheiro (passivo + PL)</h4>' + a2


def svg_cascata(a=2025):
    passos = [("Receita de crédito", D[a]["rend_credito"], "abs"), ("Receita da liquidez", D[a]["rend_liquidez"], "rel"),
              ("Captação", D[a]["desp_captacao"], "rel"), ("Repasses", D[a]["desp_repasses"], "rel"), ("Margem financeira", D[a]["mf"], "tot"),
              ("Serviços e tarifas", D[a]["servicos"] + D[a]["tarifas"], "rel"),
              ("Outras", D[a]["outras_rec_op"] + D[a]["outras_desp_op"] + D[a]["tributarias"] + D[a]["contingencias"], "rel"),
              ("Receita líquida", D[a]["receita_liquida"], "tot"), ("Despesas adm.", D[a]["desp_adm"], "rel"),
              ("PDD líquida", D[a]["pdd_liquida"], "rel"), ("Não oper. e IR", D[a]["nao_operacional"] + D[a]["ir_cs"], "rel"),
              ("Resultado", D[a]["resultado"], "tot")]
    W, H, top, base = 760, 345, 20, 260
    vmax = 500_000
    esc = (base - top) / vmax
    bw = 42
    gap = (W - 60) / len(passos)
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t-casc"><title id="t-casc">Cascata do resultado de {a}, em R$ mi</title>']
    for t in range(0, vmax + 1, 100_000):
        yy = base - t * esc
        out.append(f'<line class="grid" x1="50" x2="{W - 10}" y1="{yy:.1f}" y2="{yy:.1f}"></line><text class="ax" x="44" y="{yy + 4:.1f}" text-anchor="end">{t // 1000}</text>')
    acum = 0
    for j, (rot, v, tipo) in enumerate(passos):
        x = 60 + j * gap + (gap - bw) / 2
        if tipo in ("abs", "tot"):
            y0, y1 = 0, v
            acum = v
            cls = "s1" if tipo == "abs" else "tot-bar"
        else:
            y0, y1 = acum, acum + v
            acum += v
            cls = "pos" if v >= 0 else "neg"
        lo, hi = min(y0, y1), max(y0, y1)
        yy, hh = base - hi * esc, max((hi - lo) * esc, 1)
        out.append(f'<rect class="{cls}" x="{x:.1f}" y="{yy:.1f}" width="{bw}" height="{hh:.1f}" rx="3" data-tip="{_esc(rot)}: R$ {fnum(v / 1000, 1)} mi"></rect>')
        out.append(f'<text class="val" x="{x + bw / 2:.1f}" y="{yy - 5:.1f}" text-anchor="middle">{fnum(v / 1000, 0)}</text>')
        for k_, pal in enumerate(_quebra(rot, 8)):
            out.append(f'<text class="ax" x="{x + bw / 2:.1f}" y="{base + 16 + k_ * 13}" text-anchor="middle">{pal}</text>')
    out.append(f'<line class="axis" x1="50" x2="{W - 10}" y1="{base}" y2="{base}"></line>')
    out.append("</svg>")
    return "".join(out)


def _quebra(texto, maximo):
    linhas, atual = [], ""
    for p in texto.split(" "):
        if atual and len(atual) + 1 + len(p) > maximo:
            linhas.append(atual)
            atual = p
        else:
            atual = (atual + " " + p).strip()
    linhas.append(atual)
    return linhas


def svg_barras(titulo, categorias, s24, s25, fmt, vmax=None, sufixo=""):
    W, H, top, base = 760, 250, 24, 190
    vmax = vmax or max(max(s24), max(s25)) * 1.18
    esc = (base - top) / vmax
    gap = (W - 70) / len(categorias)
    bw = min(24, gap / 3)
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img"><title>{_esc(titulo)}</title>']
    passo = _passo(vmax)
    t = 0.0
    while t <= vmax + 1e-9:
        yy = base - t * esc
        out.append(f'<line class="grid" x1="60" x2="{W - 10}" y1="{yy:.1f}" y2="{yy:.1f}"></line><text class="ax" x="54" y="{yy + 4:.1f}" text-anchor="end">{fmt(t)}</text>')
        t += passo
    for j, cat in enumerate(categorias):
        cx = 70 + j * gap + gap / 2
        for k_, (serie, cls, ano) in enumerate(((s24, "y24", 2024), (s25, "s1", 2025))):
            v = serie[j]
            x = cx - bw - 1 + k_ * (bw + 2)
            hh = max(v * esc, 1)
            out.append(f'<path class="{cls}" d="{_barra(x, base, bw, hh)}" data-tip="{_esc(cat)} {ano}: {fmt(v)}{sufixo}"></path>')
            if k_ == 1:
                out.append(f'<text class="val" x="{x + bw / 2:.1f}" y="{base - hh - 5:.1f}" text-anchor="middle">{fmt(v)}</text>')
        out.append(f'<text class="ax" x="{cx:.1f}" y="{base + 16}" text-anchor="middle">{_esc(cat)}</text>')
    out.append(f'<line class="axis" x1="60" x2="{W - 10}" y1="{base}" y2="{base}"></line>')
    out.append(f'<rect class="y24" x="{W - 190}" y="6" width="10" height="10" rx="2"></rect><text class="ax" x="{W - 175}" y="15">2024</text>'
               f'<rect class="s1" x="{W - 130}" y="6" width="10" height="10" rx="2"></rect><text class="ax" x="{W - 115}" y="15">2025</text>')
    out.append("</svg>")
    return "".join(out)


def _passo(vmax):
    import math
    bruto = vmax / 5
    e = 10 ** math.floor(math.log10(bruto))
    for m in (1, 2, 2.5, 5, 10):
        if m * e >= bruto:
            return m * e
    return 10 * e


def _barra(x, base, w, h):
    r = min(4, h, w / 2)
    y = base - h
    return (f"M{x:.1f},{base:.1f} L{x:.1f},{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} L{x + w - r:.1f},{y:.1f} "
            f"Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f} L{x + w:.1f},{base:.1f} Z")


def svg_rentabilidade():
    cats = ["ROE contábil", "ROE recorrente", "NIM", "Custo do risco"]
    s24 = [I[2024]["roe"] * 100, I[2024]["roe_recorrente"] * 100, I[2024]["nim"] * 100, I[2024]["custo_risco"] * 100]
    s25 = [I[2025]["roe"] * 100, I[2025]["roe_recorrente"] * 100, I[2025]["nim"] * 100, I[2025]["custo_risco"] * 100]
    return svg_barras("Rentabilidade e risco, em %", cats, s24, s25, lambda v: fnum(v, 1), 24, "%")


def svg_atraso():
    ks = [("d1_14", "1-14 dias"), ("d15_30", "15-30"), ("d31_60", "31-60"), ("d61_90", "61-90"), ("d90", "> 90 dias")]
    s24 = [at(k, 2024) / S["carteira"][2024] * 100 for k, _ in ks]
    s25 = [at(k, 2025) / S["carteira"][2025] * 100 for k, _ in ks]
    return svg_barras("Carteira em atraso por faixa, % da carteira", [r for _, r in ks], s24, s25, lambda v: fnum(v, 1), 3.5, "%")


def svg_basileia():
    W, H = 760, 180
    x0, x1 = 40, 720
    vmax = 16.0
    esc = (x1 - x0) / vmax
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img"><title>Índice de Basileia contra as réguas</title>']
    marcos = [(7.0, "CP mín. 7%"), (8.5, "Nível I 8,5%"), (10.5, "PR mín. 10,5%"), (12.5, "Piso 12,5%")]
    for j, (a, y) in enumerate(((2024, 40), (2025, 90))):
        v = I[a]["basileia"] * 100
        cp = I[a]["indice_cp"] * 100
        out.append(f'<text class="ax" x="{x0}" y="{y - 6}">{a}</text>')
        out.append(f'<rect class="track" x="{x0}" y="{y}" width="{x1 - x0}" height="18" rx="4"></rect>')
        out.append(f'<rect class="s1" x="{x0}" y="{y}" width="{cp * esc:.1f}" height="18" rx="4" data-tip="Capital principal ÷ RWA {a}: {fnum(cp, 2)}%"></rect>')
        if v - cp > 0.01:
            out.append(f'<rect class="s3" x="{x0 + cp * esc + 2:.1f}" y="{y}" width="{(v - cp) * esc - 2:.1f}" height="18" rx="2" data-tip="Nível II (LFS) {a}: {fnum(v - cp, 2)} p.p."></rect>')
        out.append(f'<text class="val" x="{x0 + v * esc + 6:.1f}" y="{y + 14}">{fnum(v, 2)}%</text>')
    for m_, rot in marcos:
        x = x0 + m_ * esc
        out.append(f'<line class="mark" x1="{x:.1f}" x2="{x:.1f}" y1="30" y2="116"></line>')
        out.append(f'<text class="ax" x="{x:.1f}" y="{130 + (13 if m_ in (8.5, 12.5) else 0)}" text-anchor="middle">{rot}</text>')
    out.append(f'<rect class="s1" x="{x0}" y="162" width="10" height="10" rx="2"></rect><text class="ax" x="{x0 + 14}" y="171">Capital principal</text>'
               f'<rect class="s3" x="{x0 + 130}" y="162" width="10" height="10" rx="2"></rect><text class="ax" x="{x0 + 144}" y="171">Nível II (LFS)</text>')
    out.append("</svg>")
    return "".join(out)


def svg_maquina():
    return """<svg class="chart diagram" viewBox="0 0 760 360" role="img" aria-labelledby="t-maq"><title id="t-maq">Como o dinheiro circula numa cooperativa de crédito</title>
<defs><marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="arrowhead"></path></marker></defs>
<rect class="box" x="20" y="130" width="170" height="100" rx="10"></rect>
<text class="bt" x="105" y="160" text-anchor="middle">Associados</text>
<text class="ax" x="105" y="180" text-anchor="middle">donos e usuários</text>
<text class="ax" x="105" y="196" text-anchor="middle">poupadores e tomadores</text>
<rect class="box accent" x="295" y="110" width="190" height="140" rx="10"></rect>
<text class="bt" x="390" y="140" text-anchor="middle">Cooperativa singular</text>
<text class="ax" x="390" y="162" text-anchor="middle">Passivo + PL: de onde vem</text>
<text class="ax" x="390" y="180" text-anchor="middle">Ativo: para onde vai</text>
<text class="ax" x="390" y="198" text-anchor="middle">DSP: quanto sobra</text>
<text class="ax" x="390" y="222" text-anchor="middle">Balanço = foto; DSP = filme</text>
<rect class="box" x="580" y="40" width="160" height="80" rx="10"></rect>
<text class="bt" x="660" y="70" text-anchor="middle">Central</text>
<text class="ax" x="660" y="90" text-anchor="middle">centralização financeira</text>
<text class="ax" x="660" y="106" text-anchor="middle">~100% do CDI</text>
<rect class="box" x="580" y="240" width="160" height="80" rx="10"></rect>
<text class="bt" x="660" y="270" text-anchor="middle">Banco e fundos</text>
<text class="ax" x="660" y="290" text-anchor="middle">repasses (BNDES, rural)</text>
<text class="ax" x="660" y="306" text-anchor="middle">e recursos do sistema</text>
<path class="flow" d="M190,150 C240,140 250,135 295,140" marker-end="url(#seta)"></path>
<text class="lbl" x="242" y="128" text-anchor="middle">depósitos, LCA,</text><text class="lbl" x="242" y="141" text-anchor="middle">quotas</text>
<path class="flow" d="M295,215 C250,225 240,225 190,212" marker-end="url(#seta)"></path>
<text class="lbl" x="242" y="240" text-anchor="middle">crédito, juros,</text><text class="lbl" x="242" y="253" text-anchor="middle">sobras</text>
<path class="flow" d="M485,140 C530,110 545,90 580,82" marker-end="url(#seta)"></path>
<text class="lbl" x="520" y="98" text-anchor="middle">sobra de caixa</text>
<path class="flow" d="M580,282 C540,275 520,250 485,225" marker-end="url(#seta)"></path>
<text class="lbl" x="522" y="285" text-anchor="middle">funding direcionado</text>
<path class="flow thin" d="M390,250 C390,300 360,330 300,338" marker-end="url(#seta)"></path>
<text class="lbl" x="250" y="342" text-anchor="end">resultado: reservas, FATES, juros ao capital, AGO</text>
</svg>"""


def svg_dupont():
    def caixa(x, y, w, titulo, v24, v25):
        return (f'<rect class="box" x="{x}" y="{y}" width="{w}" height="62" rx="8"></rect>'
                f'<text class="bt" x="{x + w / 2}" y="{y + 20}" text-anchor="middle">{titulo}</text>'
                f'<text class="ax" x="{x + w / 2}" y="{y + 38}" text-anchor="middle">2024: {v24}</text>'
                f'<text class="ax b" x="{x + w / 2}" y="{y + 54}" text-anchor="middle">2025: {v25}</text>')
    i24, i25 = I[2024], I[2025]
    mg = lambda a: D[a]["resultado"] / D[a]["receita_liquida"]
    gi = lambda a: D[a]["receita_liquida"] / I[a]["ativo_medio"]
    al = lambda a: I[a]["ativo_medio"] / I[a]["pl_medio"]
    out = ['<svg class="chart diagram" viewBox="0 0 760 330" role="img"><title>Árvore do ROE (DuPont)</title>']
    out.append(caixa(290, 10, 180, "ROE", FMT["p1"](i24["roe"]), FMT["p1"](i25["roe"])))
    out.append(caixa(40, 120, 200, "Margem: resultado ÷ RL", FMT["p1"](mg(2024)), FMT["p1"](mg(2025))))
    out.append(caixa(280, 120, 200, "Giro: RL ÷ ativo médio", FMT["p2"](gi(2024)), FMT["p2"](gi(2025))))
    out.append(caixa(520, 120, 200, "Alavancagem: ativo ÷ PL", FMT["x2"](al(2024)), FMT["x2"](al(2025))))
    out.append(caixa(10, 240, 140, "1 - IEAR", FMT["p1"](1 - i24["iear"]), FMT["p1"](1 - i25["iear"])))
    out.append(caixa(160, 240, 120, "IE", FMT["p1"](i24["ie"]), FMT["p1"](i25["ie"])))
    out.append(caixa(290, 240, 140, "NIM", FMT["p2"](i24["nim"]), FMT["p2"](i25["nim"])))
    out.append(caixa(440, 240, 130, "Serviços ÷ ativo", FMT["p2"]((D[2024]["servicos"] + D[2024]["tarifas"]) / i24["ativo_medio"]),
                     FMT["p2"]((D[2025]["servicos"] + D[2025]["tarifas"]) / i25["ativo_medio"])))
    out.append(caixa(580, 240, 170, "PL ÷ ativo", FMT["p1"](S["pl"][2024] / S["ativo"][2024]), FMT["p1"](S["pl"][2025] / S["ativo"][2025])))
    for x in (140, 380, 620):
        out.append(f'<path class="flow thin" d="M380,72 L{x},120"></path>')
    for x1, x2 in ((140, 80), (140, 220)):
        out.append(f'<path class="flow thin" d="M{x1},182 L{x2},240"></path>')
    for x1, x2 in ((380, 360), (380, 505)):
        out.append(f'<path class="flow thin" d="M{x1},182 L{x2},240"></path>')
    out.append('<path class="flow thin" d="M620,182 L665,240"></path>')
    out.append('<text class="ax" x="482" y="30">ROE = margem × giro × alavancagem</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ exercícios propostos
UNID_TXT = {"%": "%", "R$ mil": "R$ mil", "p.p.": "p.p.", "x": "vezes", "R$": "R$"}


def _disp(it):
    v = it["valor"]
    if it["unidade"] == "%":
        return v * 100, it["tol"] * 100
    return v, it["tol"]


def _fmt_resp(it):
    v = it["valor"]
    u = it["unidade"]
    if u == "%":
        return fnum(v * 100, 2) + "%"
    if u == "R$ mil":
        return "R$ " + fnum(v, 2 if abs(v) < 100 else 0) + " mil"
    if u == "p.p.":
        return fnum(v, 2) + " p.p."
    if u == "x":
        return fnum(v, 2) + "x"
    if u == "R$":
        return "R$ " + fnum(v, 2)
    return str(v)


def exercicios_propostos():
    h = []
    for e in EXERCICIOS:
        if e["id"] == "P15":
            continue
        num = e["id"][1:]
        h.append(f'<article class="ex" id="ex-{e["id"]}" data-ex="{e["id"]}"><header><span class="ex-tag">Exercício {num}</span>'
                 f'<h3>{_esc(e["titulo"])}</h3><span class="ex-tema">{_esc(e["tema"])}</span></header>')
        h.append(f'<p>{_esc(e["enunciado"])}</p>')
        if e.get("dica"):
            h.append(f'<details class="dica"><summary>Dica</summary><p>{_esc(e["dica"])}</p></details>')
        h.append('<ol class="itens">')
        for it in e["itens"]:
            if it["unidade"] == "opcao":
                opts = "".join(f'<option value="{_esc(o)}">{_esc(o)}</option>' for o in OPCOES_BP)
                h.append(f'<li data-tipo="opcao" data-ans="{_esc(it["valor"])}"><span class="q">{_esc(it["pergunta"])}</span>'
                         f'<span class="campo"><select aria-label="Resposta {it["letra"]}"><option value="">Escolha a linha</option>{opts}</select>'
                         f'<span class="fb" aria-live="polite"></span></span><span class="sol" hidden><b>{_esc(it["valor"])}.</b> {_esc(it["explicacao"])}</span></li>')
            else:
                v, tol = _disp(it)
                h.append(f'<li data-tipo="num" data-ans="{v:.6f}" data-tol="{tol:.6f}"><span class="q"><b>{it["letra"]})</b> {_esc(it["pergunta"])}</span>'
                         f'<span class="campo"><input type="text" inputmode="decimal" placeholder="0,00" aria-label="Resposta {it["letra"]}">'
                         f'<span class="un">{UNID_TXT[it["unidade"]]}</span><span class="fb" aria-live="polite"></span></span>'
                         f'<span class="sol" hidden>Resposta: <b>{_fmt_resp(it)}</b></span></li>')
        h.append("</ol>")
        aba = "Ex" + num
        h.append(f'<div class="ex-acoes"><button type="button" class="btn conferir">Conferir</button>'
                 f'<button type="button" class="btn sec ver">Ver respostas</button><span class="placar" aria-live="polite"></span>'
                 f'<span class="ex-planilha">Resolução passo a passo: aba <b>{aba}</b> da planilha</span></div></article>')
    return "".join(h)


def parecer_modelo():
    return "".join(f'<div class="parecer-item"><h4>{_esc(t)}</h4><p>{_esc(x)}</p></div>' for t, x in PARECER)


def simulador_dados():
    a = 2025
    dd, ii = D[a], I[a]
    base = dict(
        resultado=dd["resultado"], pl_medio=ii["pl_medio"], receita_liquida=dd["receita_liquida"], desp_adm=-dd["desp_adm"],
        pdd=-dd["pdd"], pdd_liquida=-dd["pdd_liquida"], servicos=dd["servicos"] + dd["tarifas"], rdc_medio=M.media(S["rdc"], a),
        cdi=M.CDI[a], rdc_pct_cdi=-dd["desp_rdc"] / M.media(S["rdc"], a) / M.CDI[a], pr=ii["pr"], rwa=ii["rwa"],
        liquidez=S["liquidez"][a], depositos=S["depositos"][a], nml=NOTAS["nml"], fpr_credito=M.FPR["comercial"],
        fpr_cent=M.FPR["centralizacao"], custo_risco=ii["custo_risco"], mf=dd["mf"],
    )
    return json.dumps(base)


def dados_js():
    return json.dumps({"planilha": PLANILHA})


FUNCS = {
    "tabela_bp": tabela_bp, "tabela_dsp": tabela_dsp, "tabela_gerencial": tabela_gerencial, "nota_saldos_2023": nota_saldos_2023,
    "nota_carteira": nota_carteira, "nota_atraso": nota_atraso, "nota_estagio": nota_estagio, "nota_outros": nota_outros,
    "nota_nao_recorrentes": nota_nao_recorrentes, "nota_dmpl": nota_dmpl, "tabela_rwa": tabela_rwa, "tabela_ftp": tabela_ftp,
    "tabela_lcr": tabela_lcr, "tabela_taxas": tabela_taxas, "tabela_fontes_usos": tabela_fontes_usos, "painel": painel,
    "tabela_resumo": tabela_resumo, "svg_composicao": svg_composicao, "svg_cascata": svg_cascata, "svg_rentabilidade": svg_rentabilidade,
    "svg_atraso": svg_atraso, "svg_basileia": svg_basileia, "svg_maquina": svg_maquina, "svg_dupont": svg_dupont,
    "exercicios_propostos": exercicios_propostos, "parecer_modelo": parecer_modelo, "simulador_dados": simulador_dados,
}
NS.update(FUNCS)


def render(texto):
    def troca(mt):
        fmt, expr = mt.group(1), mt.group(2)
        val = eval(expr, NS)
        if fmt == "html":
            return val
        if fmt == "raw":
            return str(val)
        return FMT[fmt](val)
    out = re.sub(r"\{\{(\w+):(.+?)\}\}", troca, texto, flags=re.S)
    sobra = re.findall(r"\{\{.*?\}\}", out)
    assert not sobra, sobra[:5]
    return out


def main():
    partes = sorted((AQUI / "tpl").glob("*.html"))
    texto = "".join(p.read_text(encoding="utf-8") for p in partes)
    out = render(texto)
    proibidos = [c for c in ("—", "–") if c in out]
    assert not proibidos, f"travessão encontrado: {proibidos}"
    SAIDA.write_text(out, encoding="utf-8")
    print("ok", SAIDA, len(out) // 1024, "KB")


if __name__ == "__main__":
    main()
