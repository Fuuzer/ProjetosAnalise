import re, sys, os, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hb import *
import sec_a, sec_b, sec_c, sec_d, sec_e

TABS = [
 ('Resumo executivo', sec_a.p1), ('Decisão recomendada', sec_a.p2), ('Respostas às suas perguntas', sec_a.p3), ('Auditoria das versões', sec_a.p4),
 ('Metodologia e fontes', sec_a.p5), ('Mercado e tendências', sec_a.p6), ('Google Trends', sec_a.p7), ('Concorrência', sec_a.p8),
 ('Benchmark de serviços', sec_b.p9), ('Cliente e posicionamento', sec_b.p10), ('Modelo de negócio', sec_b.p11), ('Portfólio', sec_b.p12),
 ('Fornecedores', sec_b.p13), ('Precificação e kits', sec_c.p14), ('Cenários de R$ 1.000 a R$ 3.000', sec_c.p15), ('Canais', sec_d.p16),
 ('Operação e logística', sec_d.p17), ('Jurídico, regulatório e tributário', sec_d.p18), ('Marca e experiência', sec_d.p19), ('Marketing', sec_d.p20),
 ('Retenção', sec_d.p21), ('Projeções financeiras', sec_e.p22), ('Riscos', sec_e.p23), ('Plano de ação', sec_e.p24), ('Indicadores', sec_e.p25),
 ('Decisões que dependem de validação', sec_e.p26), ('Lista final de compras', sec_e.p27), ('Checklist de lançamento', sec_e.p28),
 ('Respostas executivas', sec_e.p29), ('Se eu estivesse começando amanhã', sec_e.p30),
]
NEW = {'Respostas às suas perguntas', 'Google Trends', 'Benchmark de serviços', 'Cenários de R$ 1.000 a R$ 3.000'}
n = len(TABS)
orig = open(os.path.join(D, 'build/original.html'), encoding='utf-8').read()
css = re.search(r'<style>(.*?)</style>', orig, flags=re.S).group(1)
css = css.split('#t1:checked~main #p1')[0]
sel_show = ','.join(f'#t{i}:checked~main #p{i}' for i in range(1, n + 1)) + '{display:block}'
sel_nav = ','.join(f'#t{i}:checked~nav label[for="t{i}"]' for i in range(1, n + 1)) + '{background:#9C4A1A;color:#fff;border-color:#9C4A1A}'
sel_span = ','.join(f'#t{i}:checked~nav label[for="t{i}"] span' for i in range(1, n + 1)) + '{background:#fff;color:#9C4A1A}'
css += ('.barw{position:relative;background:#F4EBDD;border-radius:4px;height:18px;min-width:140px}'
        '.bar{position:absolute;left:0;top:0;bottom:0;background:#C9A45C;border-radius:4px}'
        '.barw span{position:relative;padding-left:6px;font-size:12px;line-height:18px;font-weight:600}'
        'nav label.nv{border-color:#C9A45C}nav label i{font-style:normal;font-size:10px;color:#9C4A1A;font-weight:700}'
        '#t1:checked~nav label[for="t1"] i' + ''.join(f',#t{i}:checked~nav label[for="t{i}"] i' for i in range(2, n + 1)) + '{color:#fff}'
        '.src{word-break:break-word}main td:first-child{min-width:130px}'
        '@media (max-width:700px){.wrap{padding:10px 16px}.kpis{grid-template-columns:repeat(auto-fit,minmax(140px,1fr))}main table{display:block;overflow-x:auto;max-width:100%}.grid2{grid-template-columns:1fr}.barw{min-width:110px}}')
css += sel_show + sel_nav + sel_span
out = ['<!DOCTYPE html>\n<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n',
       '<title>Plano de negócio: perfumaria online com decants</title>\n<style>', css, '</style></head>\n<body>\n',
       '<header><h1>Plano de negócio: perfumaria online com decants de grife, clones e árabes</h1>\n',
       '<p>Versão 2 de 25/11/2026 · valores em R$ · fontes, preços e Google Trends consultados em 25/11/2026 · clique nas abas para navegar</p></header>\n',
       '<div class="wrap">\n']
out.append(''.join(f'<input type="radio" name="tab" id="t{i}"{" checked" if i == 1 else ""}>' for i in range(1, n + 1)) + '\n')
nav = '<nav>'
for i, (t, f) in enumerate(TABS, 1):
    cls = ' class="nv"' if t in NEW else ''
    nav += f'<label for="t{i}"{cls}><span>{i}</span>{t}' + (' <i>novo</i>' if t in NEW else '') + '</label>'
nav += '</nav>\n'
out.append(nav)
out.append('<main>')
for i, (t, f) in enumerate(TABS, 1):
    body = f()
    prev = f'<label for="t{i-1}">&larr; {TABS[i-2][0]}</label>' if i > 1 else '<span></span>'
    nxt = f'<label for="t{i+1}">{TABS[i][0]} &rarr;</label>' if i < n else '<span></span>'
    out.append(f'<section class="panel" id="p{i}">\n{body}\n<div class="pn">{prev}{nxt}</div></section>')
out.append('</main>\n</div>\n<footer>Documento de apoio à decisão. Não substitui parecer jurídico, contábil ou sanitário. Números marcados como estimativa ou hipótese devem ser trocados pelos dados reais assim que existirem. Comparações entre clones e perfumes originais citam guias de terceiros e não são afirmação das marcas.</footer>\n</body></html>\n')
doc = ''.join(out)
# entidades numéricas para todo caractere fora do ASCII
enc = ''.join(c if ord(c) < 128 else f'&#{ord(c)};' for c in doc)
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, 'build/plano-perfumaria-decants-v2.html')
open(path, 'w', encoding='ascii').write(enc)
print('ok', path, len(enc), 'bytes', n, 'abas')
