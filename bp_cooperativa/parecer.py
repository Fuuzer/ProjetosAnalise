"""Parecer modelo da Coop Vale do Ipê (usado no HTML e na aba Ex15)."""
import modelo as M

S, D, I = M.S, M.D, M.I


def pct(x, d=1):
    return f"{x * 100:.{d}f}".replace(".", ",") + "%"


def mil(x):
    return f"{x:,.0f}".replace(",", ".")


def num(x, d=1):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar():
    i24, i25 = I[2024], I[2025]
    return [
        ("1. Conclusão", f"A Coop Vale do Ipê é saudável, líquida e capitalizada acima do mínimo, mas a rentabilidade recorrente caiu forte em 2025 (ROE recorrente de {pct(i24['roe_recorrente'])} para {pct(i25['roe_recorrente'])}) e ficou abaixo do custo de capital de ~15%. A piora vem de três lugares: margem comprimida pelo CDI, risco de crédito subindo e captação mais cara."),
        ("2. Tamanho e crescimento", f"Ativo de R$ {mil(S['ativo'][2025])} mil (+{pct(i25['cresc_ativo'])}). Carteira de R$ {mil(S['carteira'][2025])} mil (+{pct(i25['cresc_carteira'])}, {pct(i25['cresc_real'])} real). Crescimento equilibrado entre comercial (+{pct(i25['cresc_comercial'])}) e rural (+{pct(i25['cresc_rural'])})."),
        ("3. Captação", f"Captação de R$ {mil(i25['captacao_total'])} mil (+{pct(i25['cresc_captacao'])}). O mix piorou: depósito à vista caiu para {pct(i25['mix_dv'])} e RDC subiu para {pct(i25['mix_rdc'])}. O RDC custa {pct(-D[2025]['desp_rdc'] / M.media(S['rdc'], 2025) / M.CDI[2025])} do CDI e tem margem FTP negativa."),
        ("4. Margem e spread", f"Margem financeira de R$ {mil(D[2025]['mf'])} mil (+{pct(D[2025]['mf'] / D[2024]['mf'] - 1)}), mas o NIM caiu de {pct(i24['nim'], 2)} para {pct(i25['nim'], 2)} e o spread de crédito de {num(i24['spread_credito'] * 100)} para {num(i25['spread_credito'] * 100)} p.p. Motivo: captação reprecifica com o CDI na hora; a carteira pré, só no vencimento."),
        ("5. Eficiência", f"IE contábil estável ({pct(i24['ie'])} para {pct(i25['ie'])}), mas o recorrente piorou ({pct(i24['ie_recorrente'])} para {pct(i25['ie_recorrente'])}). O IEAR subiu de {pct(i24['iear'])} para {pct(i25['iear'])}: o risco pesa mais que o custo."),
        ("6. Crédito", f"NPL 90 subiu de {pct(i24['npl90'], 2)} para {pct(i25['npl90'], 2)}, a inadimplência de 15 a 90 dias também subiu e as renegociações cresceram 51%. Cobertura caiu de {pct(i24['cobertura_npl'], 0)} para {pct(i25['cobertura_npl'], 0)}. Custo do risco de {pct(i24['custo_risco'], 2)} para {pct(i25['custo_risco'], 2)} da carteira."),
        ("7. Capital", f"Basileia de {pct(i24['basileia'], 2)} para {pct(i25['basileia'], 2)} (MM/RWA de {num(i25['mm_rwa'], 2)} p.p.), mas sem a LFS seria {pct(i25['basileia_sem_lfs'], 2)}. O PL cresceu {pct(i25['cresc_pl'])} e o RWA {pct(i25['rwa'] / i24['rwa'] - 1)}. Potencial de crédito até o piso de 2 p.p.: cerca de R$ {mil(i25['potencial_credito'])} mil."),
        ("8. Liquidez", f"Folgada: índice interno de {num(i25['indice_liquidez'], 2)}x, LCR didático de {pct(i25['lcr'], 0)}, crédito/captação de {pct(i25['credito_captacao'])}. Não é restrição; o excesso tem custo de carregamento."),
        ("9. Resultado recorrente", f"Resultado de R$ {mil(D[2025]['resultado'])} mil inclui R$ {mil(i25['nao_recorrente'])} mil não recorrentes (venda de imóvel, reversão de contingência, recuperação extraordinária). Recorrente: R$ {mil(i25['resultado_recorrente'])} mil, queda de {pct(1 - i25['resultado_recorrente'] / i24['resultado_recorrente'])} contra 2024."),
        ("10. Três riscos", "(1) Risco de crédito em alta (NPL, estágio 3 e renegociações subindo juntos). (2) Margem: dependência crescente de RDC caro com carteira pré. (3) Capital: se o resultado recorrente continuar caindo, o PL deixa de acompanhar o RWA e a folga some."),
        ("11. Três recomendações", "(1) Rever a política de concessão e a cobrança das safras de 2024 e 2025, e acompanhar o estágio 2 todo mês. (2) Precificar o crédito novo pelo RAROC (taxa mínima por produto) e evitar pagar acima de 100% do CDI em RDC sem destino em crédito. (3) Priorizar retenção de sobras em reserva na AGO e planejar a substituição da LFS por capital próprio."),
    ]


PARECER = gerar()
