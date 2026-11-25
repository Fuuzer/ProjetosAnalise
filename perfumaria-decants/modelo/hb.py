"""Helpers de HTML e dados compartilhados pelas seções."""
import json, os, re
import model as m
from calc import N, brl, num, pct

D = os.path.dirname(os.path.abspath(__file__))
SK = m.SKUS
ORIG = json.load(open(os.path.join(D, 'build/orig_sections.json'), encoding='utf-8'))

FA = '<span class="b fa">Fato</span>'
ES = '<span class="b es">Estimativa</span>'
HI = '<span class="b hi">Hipótese</span>'
JU = '<span class="b ju">Julgamento</span>'
VA = '<span class="b va">A validar</span>'
NOVO = '<span class="tag">novo</span>'

def a(url, text):
    return f'<a href="{url}">{text}</a>'

def table(head, rows, cls='', tot_rows=(), scroll=False, align=None):
    h = '<table' + (f' class="{cls}"' if cls else '') + '><thead><tr>' + ''.join(f'<th>{x}</th>' for x in head) + '</tr></thead><tbody>'
    for i, r in enumerate(rows):
        trc = ' class="tot"' if i in tot_rows else ''
        cells = []
        for j, c in enumerate(r):
            al = align[j] if align and j < len(align) else ''
            cells.append(f'<td class="{al}">{c}</td>' if al else f'<td>{c}</td>')
        h += f'<tr{trc}>' + ''.join(cells) + '</tr>'
    h += '</tbody></table>'
    if scroll:
        h = '<div class="scroll">' + h + '</div>'
    return h

def src(*links):
    return '<div class="src"><b>Fontes:</b> ' + ' &middot; '.join(links) + '</div>'

def bar(v, vmax, label=None, cls=''):
    w = 0 if vmax == 0 else max(0.5, 100 * v / vmax)
    return f'<div class="barw"><div class="bar {cls}" style="width:{w:.1f}%"></div><span>{label if label is not None else num(v)}</span></div>'

# ---------- Trends ----------
TBR = m.TR_BR; TRS = m.TR_RS
SAUV_BR = TBR['Dior Sauvage']['mean12m']; SAUV_RS = TRS['Dior Sauvage']['mean12m']
def t_idx(key, geo='BR'):
    d = TBR if geo == 'BR' else TRS
    base = SAUV_BR if geo == 'BR' else SAUV_RS
    if key == 'Chanel Bleu de Chanel':
        return 100 * d['_anchor']['mean'] / base
    return 100 * d[key]['mean12m'] / base
def t_chg(key, geo='BR'):
    d = TBR if geo == 'BR' else TRS
    if key not in d: return None
    v = d[key]
    if v['first_q'] < 0.5: return None
    return v['last_q'] / v['first_q'] - 1

LINHA_T = {}
for k in TBR:
    if k.startswith('_'): continue
LINHA_ARABE = ['Lattafa Asad', 'Lattafa Yara', 'Lattafa Khamrah', 'Armaf Club de Nuit', 'Afnan 9pm', 'Al Wataniah Sabah Al Ward', 'French Avenue Liquid Brun', 'Lattafa Fakhar', 'Rasasi Hawas', 'Lattafa Badee Al Oud', 'Armaf Odyssey', 'Al Haramain Amber Oud', 'Queen of Arabia', 'French Avenue Vulcan Feu', 'Lattafa Eclaire', 'Lattafa Hayaati', 'Al Wataniah Eqaab', 'Lattafa Qaed Al Fursan', 'Lattafa His Confession', 'Lattafa Ana Abiyedh', 'Afnan Supremacy']
LINHA_NICHO = ['MFK Baccarat Rouge 540', 'PDM Delina', 'Xerjoff Erba Pura', 'Kilian Angels Share', 'PDM Layton', 'PDM Althair', 'Tom Ford Tobacco Vanille', 'Creed Aventus']
def linha_of(k):
    if k in LINHA_ARABE: return 'Árabe'
    if k in LINHA_NICHO: return 'Nicho'
    return 'Grife'
TNAME = {
 'Paco Rabanne Invictus': 'Paco Rabanne Invictus', 'Dior Sauvage': 'Dior Sauvage', 'Armaf Club de Nuit': 'Armaf Club de Nuit', 'Paco Rabanne 1 Million': 'Paco Rabanne 1 Million',
 'Carolina Herrera 212 VIP': 'Carolina Herrera 212 VIP', 'Lancome La Vie Est Belle': 'Lancôme La Vie Est Belle', 'PDM Delina': 'Parfums de Marly Delina', 'Lattafa Asad': 'Lattafa Asad',
 'Lattafa Yara': 'Lattafa Yara', 'JPG Le Male / Ultra Male': 'Jean Paul Gaultier Le Male e Ultra Male', 'Al Wataniah Sabah Al Ward': 'Al Wataniah Sabah Al Ward', 'Lattafa Fakhar': 'Lattafa Fakhar',
 'Miss Dior': 'Dior Miss Dior', 'YSL Libre': 'YSL Libre', 'CH Good Girl': 'Carolina Herrera Good Girl', 'Rasasi Hawas': 'Rasasi Hawas', 'Creed Aventus': 'Creed Aventus', 'JPG Scandal': 'Jean Paul Gaultier Scandal',
 'Armani Acqua di Gio': 'Armani Acqua di Giò', 'Dior J adore': "Dior J'adore", 'Armani Stronger With You': 'Armani Stronger With You', 'Xerjoff Erba Pura': 'Xerjoff Erba Pura', 'Paco Rabanne Olympea': 'Paco Rabanne Olympéa',
 'Azzaro Wanted': 'Azzaro Wanted', 'French Avenue Liquid Brun': 'French Avenue Liquid Brun', 'MFK Baccarat Rouge 540': 'MFK Baccarat Rouge 540', 'Chanel Coco Mademoiselle': 'Chanel Coco Mademoiselle', 'Versace Eros': 'Versace Eros',
 'Lattafa Khamrah': 'Lattafa Khamrah', 'French Avenue Vulcan Feu': 'French Avenue Vulcan Feu', 'Valentino Born in Roma': 'Valentino Born in Roma', 'PDM Layton': 'Parfums de Marly Layton', 'JPG Le Beau': 'Jean Paul Gaultier Le Beau',
 'Lattafa Eclaire': 'Lattafa Eclaire', 'Burberry Goddess': 'Burberry Goddess', 'PDM Althair': 'Parfums de Marly Althair', 'Al Haramain Amber Oud': 'Al Haramain Amber Oud', 'Queen of Arabia': 'Queen of Arabia',
 'Afnan Supremacy': 'Afnan Supremacy', 'Afnan 9pm': 'Afnan 9pm', 'Lattafa Qaed Al Fursan': 'Lattafa Qaed Al Fursan', 'Tom Ford Tobacco Vanille': 'Tom Ford Tobacco Vanille', 'Armaf Odyssey': 'Armaf Odyssey',
 'Lattafa His Confession': 'Lattafa His Confession', 'Lattafa Badee Al Oud': "Lattafa Bade'e Al Oud", 'Lattafa Hayaati': 'Lattafa Hayaati', 'Kilian Angels Share': "Kilian Angels' Share", 'Lattafa Ana Abiyedh': 'Lattafa Ana Abiyedh',
 'Al Wataniah Eqaab': 'Al Wataniah Eqaab', 'Carolina Herrera 212 VIP': 'Carolina Herrera 212 VIP',
}
AMBIG = {'Paco Rabanne Invictus': 'termo "invictus" também pega o filme', 'Paco Rabanne 1 Million': 'termo "1 million" é genérico', 'JPG Le Male / Ultra Male': 'soma dois perfumes', 'Carolina Herrera 212 VIP': 'soma as versões Men, Black e Rosé', 'Armaf Club de Nuit': 'soma toda a linha Club de Nuit', 'Lattafa Fakhar': 'soma Fakhar Black e Rose', 'Rasasi Hawas': 'soma a linha Hawas', 'PDM Delina': '"delina" também é nome próprio', 'Dior Sauvage': 'soma EDT, EDP, Parfum e Elixir'}

def trends_rank(geo='BR'):
    d = TBR if geo == 'BR' else TRS
    rows = [(k, t_idx(k, geo)) for k in d if not k.startswith('_')]
    rows.append(('Chanel Bleu de Chanel', t_idx('Chanel Bleu de Chanel', geo)))
    rows.sort(key=lambda x: -x[1])
    return rows

# ---------- Perfume Shopping ----------
PS = json.load(open(os.path.join(D, 'ps/top_vars.json')))
PS_RANK = {
 'sauv_edp': 1, 'aventus': 2, 'adg': 3, '212vipblack': 4, 'cdnim': 7, 'sauv_edt': 9, 'lmlp': 11, 'goodgirl': 16, 'asad': 17, 'y': 18,
 'eros': 21, 'libre': 24, 'lveb': 25, '1m': 30, 'brun': 34, 'invictus': 42, 'fakhar': 45, 'missdior': 47, '212men': 49, 'sabah': 65, 'yara': 67,
 'delina': 69, 'br540': 95, 'khamrah': 103, 'erba': 40,
}
PS5 = {  # preço do 5 ml na Perfume Shopping (cartão), 25/11/2026
 'sauv_edp': 79.50, 'sauv_edt': 68.00, 'aventus': 256.00, 'adg': 49.00, '212vipblack': 49.40, 'cdnim': 51.70, 'asad': 56.70, 'yara': 64.40,
 'sabah': 47.40, 'brun': 59.70, 'fakhar': 60.50, 'khamrah': 56.00, 'lveb': 86.00, 'goodgirl': 66.40, '212men': 44.00, '1m': 51.20,
 'invictus': 55.60, 'erba': 188.40, 'delina': 283.00, 'br540': 288.50, 'eros': 54.00, 'lmlp': 58.80, 'missdior': 94.00, 'libre': 79.00, 'y': 79.40,
}
TABS2 = {  # preço do 2 ml na Tabs (a partir de), 25/11/2026
 'sauv_edp': 34.90, 'sauv_edt': 39.90, 'bdc_edp': 44.90, 'bdc_parfum': 49.90, 'aventus': 94.90, 'asad': 24.90, 'cdnim': 22.90, 'khamrah': 19.90,
 'sabah': 19.90, 'brun': 24.90, 'p9pm': 24.90, 'invictus': 22.90, '212vipblack': 24.90, '212men': 24.90, '1m': 24.90, 'lveb': 29.90,
 'goodgirl': 29.90, 'br540': 109.90, 'erba': 74.90, 'fakhar': 19.90, 'hawas': 24.90, 'lemale': 24.90,
}
URL = dict(
 ps='https://www.perfumeshopping.com.br/',
 ps_api='https://www.perfumeshopping.com.br/wp-json/wc/store/v1/products?orderby=popularity&order=desc',
 ps_sauv='https://www.perfumeshopping.com.br/produto/sauvage-elixir-dior-masculino-decant/',
 tabs='https://www.tabsperfumes.com.br/',
 tabs_busca='https://tabsperfumes.com.br/buscar/?q=sauvage',
 epoca='https://www.epocacosmeticos.com.br/',
 epoca_api='https://www.epocacosmeticos.com.br/api/catalog_system/pub/products/search?ft=sauvage%20eau%20de%20toilette',
 trends='https://trends.google.com/trends/explore?geo=BR&q=decant,perfume%20arabe,perfume%20de%20nicho,contratipo,perfume%20importado&date=today%205-y',
 trends_rank='https://trends.google.com/trends/explore?geo=BR&q=bleu%20de%20chanel,sauvage,aventus,invictus,212%20vip',
 trends_rel='https://trends.google.com/trends/explore?geo=BR&q=perfume%20arabe&date=today%2012-m',
 trends_dec='https://trends.google.com/trends/explore?geo=BR&q=decant&date=today%2012-m',
 ra_ps='https://www.reclameaqui.com.br/empresa/perfume-shopping_188290/',
 ra_guido='https://www.reclameaqui.com.br/empresa/guido-decants/',
 ra_tabs='https://www.reclameaqui.com.br/empresa/tabs-perfumes1/',
 ra_casa='https://www.reclameaqui.com.br/empresa/casa-dos-decants/lista-reclamacoes/',
 scentbird='https://www.scentbird.com/blog/perfume-subscription-box-guide/',
 scentsplit='https://www.scentsplit.com/pages/about-us',
 scentsplit_aff='https://www.scentsplit.com/pages/affiliate-program',
 drogaraia_bdc='https://www.drogaraia.com.br/perfume-bleu-de-chanel-eua-de-parfum-edp-100-ml-1452502.html',
 drogaraia_aventus='https://www.drogaraia.com.br/decant-creed-aventus-eau-de-parfum-masculino-creed-8ml-1490265.html',
 scento_khamrah='https://www.scento.com/gr/blog/lattafa-khamrah-dupe-guide',
 scento_sauvage='https://www.scento.com/blog/best-sauvage-elixir-dupes-cheaper-clones.md',
 dupe_cdnim='https://perfumania.com/blogs/articles/top-6-luxury-fragrance-dupes-in-2026',
 ohoje='https://ohoje.com/2026/09/18/decant-a-tendencia-que-esta-mudando-a-forma-como-o-brasileiro-compra-perfume/',
)
