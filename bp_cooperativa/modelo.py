"""Modelo da cooperativa fictícia usada em todo o material (Coop Vale do Ipê).

Fonte única dos números: o HTML e a planilha leem daqui. Valores em R$ mil.
A centralização financeira é a conta que fecha o balanço (o que não vira
crédito fica aplicado na Central), por isso é calculada, não digitada.
"""

ANOS = (2024, 2025)

# ---------------------------------------------------------------- premissas
CDI = {2024: 0.109, 2025: 0.143}
IPCA = {2024: 0.048, 2025: 0.045}

# Taxas médias usadas para gerar as receitas e despesas (o analista não as vê:
# ele recalcula as taxas implícitas a partir do BP e da DSP).
TAXA = {
    "comercial": {2024: 0.220, 2025: 0.230},
    "rural": {2024: 0.120, 2025: 0.125},
    "centralizacao": {2024: 0.109, 2025: 0.143},
    "aplic_interfin": {2024: 0.112, 2025: 0.147},
    "tvm": {2024: 0.109, 2025: 0.143},
    "poupanca": {2024: 0.076, 2025: 0.083},
    "rdc": {2024: 0.111, 2025: 0.1445},
    "lca": {2024: 0.101, 2025: 0.132},
    "lfs": {2024: 0.0, 2025: 0.207},
    "repasses_interfin": {2024: 0.095, 2025: 0.110},
    "emprestimos_repasses": {2024: 0.090, 2025: 0.098},
}

# ---------------------------------------------------------------- saldos (R$ mil)
# 2023 só para as médias de 2024.
SALDO = {
    # ativo
    "caixa": {2023: 25_000, 2024: 28_000, 2025: 31_000},
    "centralizacao": {2023: 640_000},  # 2024 e 2025 = conta de fechamento
    "aplic_interfin": {2023: 50_000, 2024: 60_000, 2025: 85_000},
    "tvm": {2023: 120_000, 2024: 140_000, 2025: 150_000},
    "cred_emprestimos": {2023: 735_000, 2024: 830_000, 2025: 940_000},
    "cred_financiamentos": {2023: 255_000, 2024: 290_000, 2025: 340_000},
    "cred_rural": {2023: 460_000, 2024: 520_000, 2025: 590_000},
    "provisao": {2023: -68_000, 2024: -82_000, 2025: -108_000},
    "outros_ativos_fin": {2024: 45_000, 2025: 52_000},
    "ativos_fiscais": {2024: 9_000, 2025: 12_000},
    "bndu": {2024: 8_000, 2025: 11_000},
    "outros_ativos": {2024: 13_000, 2025: 15_000},
    "investimentos": {2024: 95_000, 2025: 104_000},
    "imobilizado": {2024: 62_000, 2025: 70_000},
    "intangivel": {2024: 4_000, 2025: 5_000},
    # passivo
    "dep_vista": {2023: 360_000, 2024: 390_000, 2025: 410_000},
    "poupanca": {2023: 190_000, 2024: 210_000, 2025: 235_000},
    "rdc": {2023: 1_150_000, 2024: 1_330_000, 2025: 1_520_000},
    "lca": {2023: 95_000, 2024: 120_000, 2025: 150_000},
    "repasses_interfin": {2023: 140_000, 2024: 160_000, 2025: 175_000},
    "emprestimos_repasses": {2023: 105_000, 2024: 120_000, 2025: 140_000},
    "lfs": {2023: 0, 2024: 0, 2025: 15_000},
    "outros_passivos_fin": {2024: 25_000, 2025: 28_000},
    "provisoes": {2024: 11_000, 2025: 12_000},
    "obrig_sociais": {2024: 18_000, 2025: 21_000},
    "obrig_fiscais_outras": {2024: 28_000, 2025: 31_000},
    # PL (2024: capital e reserva digitados; sobras derivadas da DSP)
    "capital_social": {2023: 120_000, 2024: 130_000},
    "reserva_legal": {2024: 150_000},
    "aap": {2024: 1_000, 2025: 1_500},
}
ATIVO_2023 = 2_390_000
PL_2023 = 280_000

# ---------------------------------------------------------------- DSP digitada (R$ mil)
DSP_FIXA = {
    "recuperacao": {2024: 7_000, 2025: 9_000},
    "fgcoop": {2024: 2_800, 2025: 3_300},
    "pdd": {2024: -46_000, 2025: -64_000},
    "servicos": {2024: 41_000, 2025: 48_000},
    "tarifas": {2024: 12_500, 2025: 14_000},
    "pessoal": {2024: -78_000, 2025: -86_000},
    "outras_adm": {2024: -60_000, 2025: -66_000},
    "tributarias": {2024: -4_700, 2025: -5_400},
    "outras_rec_op": {2024: 6_500, 2025: 7_500},
    "outras_desp_op": {2024: -11_500, 2025: -13_500},
    "contingencias": {2024: -1_200, 2025: 1_800},
    "nao_operacional": {2024: 300, 2025: 4_200},
    "ir_cs": {2024: -600, 2025: -700},
    "juros_capital": {2024: -8_200, 2025: -12_600},
    "ato_nao_coop": {2024: 1_200, 2025: 1_400},
}
PCT_RESERVA_LEGAL = 0.45  # estatuto (lei pede ao menos 10%)
PCT_FATES = 0.05          # estatuto (lei pede ao menos 5%)

# Fluxos do PL em 2025 (DMPL)
DMPL = {
    "integralizacoes": 14_000,
    "devolucoes": -9_000,
    "pct_ago_capital": 0.50,  # AGO 2025: metade das sobras de 2024 vira capital
}

# ---------------------------------------------------------------- notas complementares
NOTAS = {
    "associados": {2023: 91_000, 2024: 98_000, 2025: 106_000},
    "coobrigacoes": {2024: 180_000, 2025: 210_000},
    "atraso": {  # carteira bruta por faixa de atraso
        2024: {"em_dia": 1_548_000, "d1_14": 25_000, "d15_30": 16_000, "d31_60": 12_000, "d61_90": 8_000, "d90": 31_000},
        2025: {"em_dia": 1_735_000, "d1_14": 30_000, "d15_30": 20_000, "d31_60": 18_000, "d61_90": 12_000, "d90": 55_000},
    },
    "estagio": {  # (saldo, provisão)
        2024: {"e1": (1_462_000, 21_930), "e2": (120_000, 13_200), "e3": (58_000, 46_870)},
        2025: {"e1": (1_640_000, 26_240), "e2": (150_000, 18_000), "e3": (80_000, 63_760)},
    },
    "prov_comercial": {2024: 70_000, 2025: 92_000},
    "prov_rural": {2024: 12_000, 2025: 16_000},
    "renegociadas": {2024: 41_000, 2025: 62_000},
    "top10_depositantes": {2024: 0.080, 2025: 0.095},
    "top20_devedores": {2024: 0.060, 2025: 0.065},
    # não recorrentes (sinal = efeito no resultado)
    "nr_pdv": {2024: -2_500, 2025: 0},
    "nr_venda_imovel": {2024: 300, 2025: 4_200},
    "nr_reversao_conting": {2024: 0, 2025: 3_000},
    "nr_recuperacao_extra": {2024: 0, 2025: 2_000},
    "deprec": {2024: 6_800, 2025: 7_500},
    "rateios": {2024: 15_500, 2025: 18_000},
    "receita_bruta_2022": 160_000,
    "receita_bruta_2023": 180_000,
    "ajuste_prudencial_outros": {2024: 3_000, 2025: 3_000},
    "rwa_mercado": {2024: 3_000, 2025: 4_000},
    "nml": 0.30,
}

# FPR ilustrativos (ver ressalva no material)
FPR = {
    "caixa": 0.0, "centralizacao": 0.20, "aplic_interfin": 0.20, "tvm": 0.0,
    "comercial": 0.85, "rural": 0.75, "outros_ativos_fin": 1.0, "ativos_fiscais": 1.0,
    "bndu_outros": 1.0, "investimentos": 1.0, "imobilizado": 1.0, "coobrigacoes": 0.75,
}

# FTP (taxas de transferência anuais de 2025 e 2024)
FTP = {
    "comercial": {2024: 0.116, 2025: 0.150},
    "rural": {2024: 0.090, 2025: 0.108},
    "dep_vista": {2024: 0.098, 2025: 0.129},
    "poupanca": {2024: 0.094, 2025: 0.120},
    "rdc": {2024: 0.109, 2025: 0.143},
    "lca": {2024: 0.104, 2025: 0.136},
}
# Para o RAROC por carteira (2025)
RAROC = {
    "custo_op": {"comercial": 0.035, "rural": 0.015},
    "pe": {"comercial": 0.038, "rural": 0.010},
    "capital": 0.125,  # 10,5% regulatório + 2 p.p. de piso gerencial
    "hurdle": 0.15,
}

# LCR (premissas didáticas)
LCR = {
    2024: {"dv_fator": 0.15, "poup_fator": 0.10, "rdc_fator": 0.12, "lca_30d": 18_000,
           "obrig_30d": 14_000, "limites": 280_000, "limites_fator": 0.05, "outras_saidas": 11_000,
           "parcelas_30d": 135_000, "parcelas_fator": 0.50, "aplic_30d": 25_000},
    2025: {"dv_fator": 0.15, "poup_fator": 0.10, "rdc_fator": 0.12, "lca_30d": 20_000,
           "obrig_30d": 15_000, "limites": 320_000, "limites_fator": 0.05, "outras_saidas": 12_000,
           "parcelas_30d": 150_000, "parcelas_fator": 0.50, "aplic_30d": 30_000},
}


def _arred(x, passo):
    # arredonda "para longe do zero" no meio, como o ARRED do Excel
    q = abs(x) / passo
    n = int(q + 0.5 + 1e-9)
    return (n if x >= 0 else -n) * passo


def r100(x):
    return _arred(x, 100)


def r10(x):
    return _arred(x, 10)


def media(d, ano):
    return (d[ano - 1] + d[ano]) / 2


def construir():
    S = {k: dict(v) for k, v in SALDO.items()}
    # carteira
    S["cred_comercial"] = {a: S["cred_emprestimos"][a] + S["cred_financiamentos"][a] for a in (2023, 2024, 2025)}
    S["carteira"] = {a: S["cred_comercial"][a] + S["cred_rural"][a] for a in (2023, 2024, 2025)}

    outros_ativos_keys = ["caixa", "aplic_interfin", "tvm", "carteira", "provisao", "outros_ativos_fin",
                          "ativos_fiscais", "bndu", "outros_ativos", "investimentos", "imobilizado", "intangivel"]
    passivo_keys = ["dep_vista", "poupanca", "rdc", "lca", "repasses_interfin", "emprestimos_repasses", "lfs",
                    "outros_passivos_fin", "provisoes", "obrig_sociais", "obrig_fiscais_outras"]

    D = {}
    cent = {2023: S["centralizacao"][2023], 2024: 700_000.0, 2025: 800_000.0}
    for _ in range(60):
        for ano in ANOS:
            S["centralizacao"][ano] = cent[ano]
            d = {}
            d["rend_comercial"] = media(S["cred_comercial"], ano) * TAXA["comercial"][ano]
            d["rend_rural"] = media(S["cred_rural"], ano) * TAXA["rural"][ano]
            d["rend_centralizacao"] = media(S["centralizacao"], ano) * TAXA["centralizacao"][ano]
            d["rend_aplic"] = media(S["aplic_interfin"], ano) * TAXA["aplic_interfin"][ano]
            d["rend_tvm"] = media(S["tvm"], ano) * TAXA["tvm"][ano]
            d["desp_poupanca"] = -media(S["poupanca"], ano) * TAXA["poupanca"][ano]
            d["desp_rdc"] = -media(S["rdc"], ano) * TAXA["rdc"][ano]
            d["desp_lca"] = -media(S["lca"], ano) * TAXA["lca"][ano]
            d["desp_lfs"] = -media(S["lfs"], ano) * TAXA["lfs"][ano]
            d["desp_repasses_interfin"] = -media(S["repasses_interfin"], ano) * TAXA["repasses_interfin"][ano]
            d["desp_emprestimos_repasses"] = -media(S["emprestimos_repasses"], ano) * TAXA["emprestimos_repasses"][ano]
            d = {k: r100(v) for k, v in d.items()}
            for k, v in DSP_FIXA.items():
                d[k] = v[ano]
            D[ano] = completar_dsp(d)
            # PL
            res = D[ano]
            s_base = res["sobras_apos_juros"] - res["ato_nao_coop"]
            if ano == 2024:
                S["sobras_acum"] = {2024: res["sobras_ago"]}
                S["capital_social"][2024] = SALDO["capital_social"][2024]
            else:
                ago_cap = r10(S["sobras_acum"][2024] * DMPL["pct_ago_capital"])
                S["capital_social"][2025] = (S["capital_social"][2024] + DMPL["integralizacoes"] + ago_cap
                                             - res["juros_capital"] + DMPL["devolucoes"])
                S["reserva_legal"][2025] = S["reserva_legal"][2024] - res["dest_reserva"]
                S["sobras_acum"][2025] = res["sobras_ago"]
            pl = S["capital_social"][ano] + S["reserva_legal"][ano] + S["sobras_acum"][ano] + S["aap"][ano]
            S.setdefault("pl", {2023: PL_2023})[ano] = pl
            passivo = sum(S[k][ano] for k in passivo_keys)
            outros = sum(S[k][ano] for k in outros_ativos_keys)
            cent[ano] = passivo + pl - outros
    for ano in ANOS:
        S["centralizacao"][ano] = int(round(cent[ano]))
        S["passivo"] = S.get("passivo", {})
        S["passivo"][ano] = sum(S[k][ano] for k in passivo_keys)
        S["ativo"] = S.get("ativo", {2023: ATIVO_2023})
        S["ativo"][ano] = sum(S[k][ano] for k in outros_ativos_keys) + S["centralizacao"][ano]
        assert S["ativo"][ano] == S["passivo"][ano] + S["pl"][ano], ano
    S["depositos"] = {a: S["dep_vista"][a] + S["poupanca"][a] + S["rdc"][a] for a in (2023, 2024, 2025)}
    S["liquidez"] = {a: S["caixa"][a] + S["centralizacao"][a] + S["aplic_interfin"][a] + S["tvm"][a]
                     for a in (2023, 2024, 2025)}
    S["reserva_legal"][2025] = int(S["reserva_legal"][2025])
    S["sobras_acum"][2025] = int(S["sobras_acum"][2025])
    return S, D


def completar_dsp(d):
    d = dict(d)
    d["rend_credito"] = d["rend_comercial"] + d["rend_rural"]
    d["rend_liquidez"] = d["rend_centralizacao"] + d["rend_aplic"] + d["rend_tvm"]
    d["receitas_intermed"] = d["rend_credito"] + d["recuperacao"] + d["rend_liquidez"]
    d["desp_captacao"] = d["desp_poupanca"] + d["desp_rdc"] + d["desp_lca"] + d["desp_lfs"] - d["fgcoop"]
    d["desp_repasses"] = d["desp_repasses_interfin"] + d["desp_emprestimos_repasses"]
    d["despesas_intermed"] = d["desp_captacao"] + d["desp_repasses"] + d["pdd"]
    d["resultado_bruto"] = d["receitas_intermed"] + d["despesas_intermed"]
    d["outras_op"] = (d["servicos"] + d["tarifas"] + d["pessoal"] + d["outras_adm"] + d["tributarias"]
                      + d["outras_rec_op"] + d["outras_desp_op"] + d["contingencias"])
    d["resultado_operacional"] = d["resultado_bruto"] + d["outras_op"]
    d["resultado_antes_ir"] = d["resultado_operacional"] + d["nao_operacional"]
    d["resultado"] = d["resultado_antes_ir"] + d["ir_cs"]  # antes dos juros ao capital
    d["sobras_apos_juros"] = d["resultado"] + d["juros_capital"]
    s_base = d["sobras_apos_juros"] - d["ato_nao_coop"]
    d["dest_fates_ato"] = -d["ato_nao_coop"]
    d["dest_reserva"] = -r10(s_base * PCT_RESERVA_LEGAL)
    d["dest_fates"] = -r10(s_base * PCT_FATES)
    d["sobras_ago"] = d["sobras_apos_juros"] + d["dest_fates_ato"] + d["dest_reserva"] + d["dest_fates"]
    # visão gerencial
    d["mf"] = d["rend_credito"] + d["rend_liquidez"] + d["desp_captacao"] + d["desp_repasses"]
    d["receita_liquida"] = (d["mf"] + d["servicos"] + d["tarifas"] + d["outras_rec_op"] + d["outras_desp_op"]
                            + d["tributarias"] + d["contingencias"])
    d["desp_adm"] = d["pessoal"] + d["outras_adm"]
    d["pdd_liquida"] = d["pdd"] + d["recuperacao"]
    return d


S, D = construir()


def indicadores():
    I = {}
    for a in ANOS:
        d = D[a]
        i = {}
        i["ativo_medio"] = media(S["ativo"], a)
        i["pl_medio"] = media(S["pl"], a)
        i["carteira_media"] = media(S["carteira"], a)
        i["liq_rentavel_media"] = (media(S["centralizacao"], a) + media(S["aplic_interfin"], a) + media(S["tvm"], a))
        # rentabilidade
        i["roe"] = d["resultado"] / i["pl_medio"]
        i["roa"] = d["resultado"] / i["ativo_medio"]
        nr = sum(NOTAS[k][a] for k in ("nr_pdv", "nr_venda_imovel", "nr_reversao_conting", "nr_recuperacao_extra"))
        i["nao_recorrente"] = nr
        i["resultado_recorrente"] = d["resultado"] - nr
        i["roe_recorrente"] = i["resultado_recorrente"] / i["pl_medio"]
        i["nim"] = d["mf"] / i["ativo_medio"]
        # spread
        i["taxa_credito"] = d["rend_credito"] / i["carteira_media"]
        i["taxa_liquidez"] = d["rend_liquidez"] / i["liq_rentavel_media"]
        capt_media = (media(S["dep_vista"], a) + media(S["poupanca"], a) + media(S["rdc"], a) + media(S["lca"], a))
        custo_capt = -(d["desp_poupanca"] + d["desp_rdc"] + d["desp_lca"])
        i["captacao_media"] = capt_media
        i["custo_captacao"] = custo_capt / capt_media
        i["custo_oneroso"] = custo_capt / (capt_media - media(S["dep_vista"], a))
        i["spread_credito"] = i["taxa_credito"] - i["custo_captacao"]
        # eficiência
        i["ie"] = -d["desp_adm"] / d["receita_liquida"]
        i["iear"] = -(d["desp_adm"] + d["pdd_liquida"]) / d["receita_liquida"]
        nr_rl = NOTAS["nr_reversao_conting"][a]
        nr_adm = NOTAS["nr_pdv"][a]
        i["ie_recorrente"] = -(d["desp_adm"] - nr_adm) / (d["receita_liquida"] - nr_rl)
        # crédito
        at = NOTAS["atraso"][a]
        i["npl90"] = at["d90"] / S["carteira"][a]
        i["inad15_90"] = (at["d15_30"] + at["d31_60"] + at["d61_90"]) / S["carteira"][a]
        i["cobertura_npl"] = -S["provisao"][a] / at["d90"]
        i["prov_carteira"] = -S["provisao"][a] / S["carteira"][a]
        i["custo_risco"] = -d["pdd"] / i["carteira_media"]
        i["custo_risco_liq"] = -d["pdd_liquida"] / i["carteira_media"]
        i["baixas"] = S["provisao"][a - 1] + d["pdd"] - S["provisao"][a]
        i["baixas"] = -i["baixas"]
        est = NOTAS["estagio"][a]
        i["e3_pct"] = est["e3"][0] / S["carteira"][a]
        i["cob_e3"] = est["e3"][1] / est["e3"][0]
        # crescimento
        i["cresc_carteira"] = S["carteira"][a] / S["carteira"][a - 1] - 1
        i["cresc_comercial"] = S["cred_comercial"][a] / S["cred_comercial"][a - 1] - 1
        i["cresc_rural"] = S["cred_rural"][a] / S["cred_rural"][a - 1] - 1
        i["cresc_real"] = (1 + i["cresc_carteira"]) / (1 + IPCA[a]) - 1
        i["cresc_depositos"] = S["depositos"][a] / S["depositos"][a - 1] - 1
        i["cresc_pl"] = S["pl"][a] / S["pl"][a - 1] - 1
        i["cresc_ativo"] = S["ativo"][a] / S["ativo"][a - 1] - 1
        # captação
        capt = S["depositos"][a] + S["lca"][a]
        i["captacao_total"] = capt
        i["mix_dv"] = S["dep_vista"][a] / capt
        i["mix_poup"] = S["poupanca"][a] / capt
        i["mix_rdc"] = S["rdc"][a] / capt
        i["mix_lca"] = S["lca"][a] / capt
        i["cresc_captacao"] = capt / (S["depositos"][a - 1] + S["lca"][a - 1]) - 1
        i["credito_captacao"] = S["carteira"][a] / capt
        i["captacao_associado"] = capt / NOTAS["associados"][a]
        # liquidez
        i["liquidez_ativo"] = S["liquidez"][a] / S["ativo"][a]
        i["liq_imediata"] = (S["caixa"][a] + S["centralizacao"][a]) / S["dep_vista"][a]
        i["liq_minima"] = NOTAS["nml"] * S["depositos"][a]
        i["indice_liquidez"] = S["liquidez"][a] / i["liq_minima"]
        L = LCR[a]
        hqla = S["caixa"][a] + S["tvm"][a] + S["centralizacao"][a]
        saidas = (S["dep_vista"][a] * L["dv_fator"] + S["poupanca"][a] * L["poup_fator"] + S["rdc"][a] * L["rdc_fator"]
                  + L["lca_30d"] + L["obrig_30d"] + L["limites"] * L["limites_fator"] + L["outras_saidas"])
        entradas = L["parcelas_30d"] * L["parcelas_fator"] + L["aplic_30d"]
        entradas_lim = min(entradas, 0.75 * saidas)
        i["hqla"] = hqla
        i["lcr_saidas"] = saidas
        i["lcr_entradas"] = entradas_lim
        i["lcr"] = hqla / (saidas - entradas_lim)
        # PL
        i["pl_ativo"] = S["pl"][a] / S["ativo"][a]
        i["alavancagem"] = S["ativo"][a] / S["pl"][a]
        i["capital_associado"] = S["capital_social"][a] / NOTAS["associados"][a]
        I[a] = i
    # capital (RWA, Basileia)
    for a in ANOS:
        i = I[a]
        prov_c = NOTAS["prov_comercial"][a]
        prov_r = NOTAS["prov_rural"][a]
        expo = {
            "caixa": S["caixa"][a],
            "centralizacao": S["centralizacao"][a],
            "aplic_interfin": S["aplic_interfin"][a],
            "tvm": S["tvm"][a],
            "comercial": S["cred_comercial"][a] - prov_c,
            "rural": S["cred_rural"][a] - prov_r,
            "outros_ativos_fin": S["outros_ativos_fin"][a],
            "ativos_fiscais": S["ativos_fiscais"][a],
            "bndu_outros": S["bndu"][a] + S["outros_ativos"][a],
            "investimentos": S["investimentos"][a],
            "imobilizado": S["imobilizado"][a],
            "coobrigacoes": NOTAS["coobrigacoes"][a],
        }
        i["expo"] = expo
        i["rwa_cred_det"] = {k: v * FPR[k] for k, v in expo.items()}
        i["rwa_credito"] = sum(i["rwa_cred_det"].values())
        rb = {2022: NOTAS["receita_bruta_2022"], 2023: NOTAS["receita_bruta_2023"]}
        for aa in ANOS:
            rb[aa] = D[aa]["mf"] + D[aa]["servicos"] + D[aa]["tarifas"]
        i["receita_bruta"] = rb
        i["rwa_operacional"] = 0.15 * (rb[a - 2] + rb[a - 1] + rb[a]) / 3 / 0.08
        i["rwa_mercado"] = NOTAS["rwa_mercado"][a]
        i["rwa"] = i["rwa_credito"] + i["rwa_operacional"] + i["rwa_mercado"]
        i["ajustes_prud"] = S["intangivel"][a] + NOTAS["ajuste_prudencial_outros"][a]
        i["capital_principal"] = S["pl"][a] - i["ajustes_prud"]
        i["nivel2"] = S["lfs"][a]
        i["pr"] = i["capital_principal"] + i["nivel2"]
        i["basileia"] = i["pr"] / i["rwa"]
        i["indice_cp"] = i["capital_principal"] / i["rwa"]
        i["mm_rwa"] = (i["basileia"] - 0.105) * 100
        i["margem_capital"] = i["pr"] - 0.105 * i["rwa"]
        i["potencial_credito"] = (i["pr"] / 0.125 - i["rwa"]) / 1.1
        i["basileia_sem_lfs"] = i["capital_principal"] / i["rwa"]
    # FTP e RAROC (2025 e 2024)
    for a in ANOS:
        i = I[a]
        d = D[a]
        cm = media(S["cred_comercial"], a)
        rm = media(S["cred_rural"], a)
        f = {}
        f["comercial"] = d["rend_comercial"] - cm * FTP["comercial"][a]
        f["rural"] = d["rend_rural"] - rm * FTP["rural"][a]
        f["dep_vista"] = media(S["dep_vista"], a) * FTP["dep_vista"][a]
        f["poupanca"] = media(S["poupanca"], a) * FTP["poupanca"][a] + d["desp_poupanca"]
        f["rdc"] = media(S["rdc"], a) * FTP["rdc"][a] + d["desp_rdc"]
        f["lca"] = media(S["lca"], a) * FTP["lca"][a] + d["desp_lca"]
        f["soma_produtos"] = sum(f[k] for k in ("comercial", "rural", "dep_vista", "poupanca", "rdc", "lca"))
        f["tesouraria"] = d["mf"] - f["soma_produtos"]
        i["ftp"] = f
    # RAROC por carteira só em 2025
    a = 2025
    i = I[a]
    d = D[a]
    out = {}
    for seg in ("comercial", "rural"):
        saldo_m = media(S["cred_comercial"] if seg == "comercial" else S["cred_rural"], a)
        prov_m = media(NOTAS["prov_comercial"] if seg == "comercial" else NOTAS["prov_rural"], a)
        margem_ftp = i["ftp"][seg]
        custo_op = saldo_m * RAROC["custo_op"][seg]
        pe = saldo_m * RAROC["pe"][seg]
        rwa = (saldo_m - prov_m) * FPR[seg]
        capital = rwa * RAROC["capital"]
        credito_capital = capital * FTP[seg][a]
        resultado = margem_ftp - custo_op - pe + credito_capital
        out[seg] = dict(saldo_m=saldo_m, prov_m=prov_m, margem_ftp=margem_ftp, custo_op=custo_op, pe=pe, rwa=rwa,
                        capital=capital, credito_capital=credito_capital, resultado=resultado,
                        raroc=resultado / capital)
    i["raroc"] = out
    return I


I = indicadores()

if __name__ == "__main__":
    for a in ANOS:
        print("=" * 30, a)
        for k in ("ativo", "centralizacao", "liquidez", "carteira", "depositos", "pl", "capital_social", "reserva_legal", "sobras_acum"):
            print(f"{k:20s} {S[k][a]:>14,.0f}")
        d = D[a]
        for k in ("rend_credito", "rend_liquidez", "desp_captacao", "desp_repasses", "mf", "receita_liquida", "desp_adm",
                  "pdd_liquida", "resultado", "juros_capital", "sobras_apos_juros", "dest_reserva", "dest_fates", "sobras_ago"):
            print(f"{k:20s} {d[k]:>14,.0f}")
        i = I[a]
        for k in ("roe", "roe_recorrente", "nim", "taxa_credito", "custo_captacao", "spread_credito", "ie", "ie_recorrente", "iear",
                  "npl90", "cobertura_npl", "custo_risco", "baixas", "cresc_carteira", "credito_captacao", "indice_liquidez", "lcr",
                  "rwa", "rwa_credito", "rwa_operacional", "pr", "basileia", "mm_rwa", "potencial_credito", "pl_ativo"):
            v = i[k]
            print(f"{k:20s} {v:>14,.4f}")
        print("FTP", {k: round(v) for k, v in i["ftp"].items()})
    print("RAROC", {k: round(v["raroc"], 4) for k, v in I[2025]["raroc"].items()})
