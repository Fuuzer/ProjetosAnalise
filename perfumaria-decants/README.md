# Plano de negócio: perfumaria online com decants

- `plano-perfumaria-decants-v2.html`: versão 2 do plano (30 abas), revisada em 25/11/2026.
- `plano-perfumaria-decants-v1.html`: versão anterior, mantida para referência.
- `modelo/`: modelo financeiro e gerador do HTML.
  - `model.py`: premissas, faixas de preço, SKUs, cenários de orçamento e simulação mensal.
  - `calc.py`: números derivados usados nas tabelas.
  - `sec_*.py` e `hb.py`: conteúdo das abas; `build.py` monta o HTML (`python3 build.py saida.html`).
  - `trends/`, `ps/`, `epoca/`: dados coletados em 25/11/2026 (Google Trends, ranking e preços da Perfume Shopping, preços da Época Cosméticos).
  - `trends_*.py`, `ps_*.py`, `epoca.py`: scripts de coleta.
