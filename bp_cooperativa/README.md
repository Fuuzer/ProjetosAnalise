# Análise de BP de cooperativa de crédito

Material de estudo para analisar o balanço patrimonial de uma cooperativa de crédito no contexto Sicredi, com uma cooperativa fictícia (Coop Vale do Ipê) usada em todos os exemplos.

## Entregáveis

- `Analise_BP_Cooperativa.html`: curso completo (abre offline no navegador). Fundamentos, BP e DSP de exemplo, ativo, passivo e PL linha a linha, análise vertical e horizontal, os 15 indicadores, painel, simulador, roteiro de análise, 13 exercícios resolvidos, 15 exercícios propostos com conferência automática, estudo de caso, autoavaliação e glossário.
- `Exercicios_BP_Cooperativa_Resolvidos.xlsx`: BP, DSP, DRE gerencial, notas, DMPL, RWA, indicadores com fórmulas vivas e uma aba por exercício (Ex01 a Ex15) com passo a passo, fórmula em Excel PT-BR e explicação.

## Como regenerar

```bash
python3 gerar_planilha.py                      # cria a planilha (fórmulas sem valores em cache)
python3 <skill xlsx>/scripts/recalc.py Exercicios_BP_Cooperativa_Resolvidos.xlsx 90
python3 verificar.py                           # confere a planilha contra o modelo em Python
python3 gerar_html.py                          # monta o HTML a partir de tpl/*.html
```

- `modelo.py`: fonte única dos números (saldos, DSP, notas e indicadores). A centralização financeira fecha o balanço.
- `exercicios.py`: enunciados e respostas dos exercícios propostos.
- `parecer.py`: parecer modelo, usado no HTML e na aba Ex15.
- `tpl/`: texto do HTML com marcadores `{{formato:expressão}}` preenchidos pelo modelo.

Os números são fictícios; FPR, risco operacional e premissas de estresse de liquidez são simplificações didáticas.
