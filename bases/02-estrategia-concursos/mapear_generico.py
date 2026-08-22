# -*- coding: utf-8 -*-
"""Mapeia as 18 aulas de Direito Administrativo (Regular Controle) em blocos de estudo."""
import sys, os, re, glob, json, collections, hashlib
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf
S = r"C:\Users\saida\AppData\Local\Temp\claude\G--Meu-Drive-Intelig-ncia-Artificial-Claude-Code-ccos-ratos\d1ec1cd8-e665-4dfb-a047-a7395dc82975\scratchpad"
sys.path.insert(0, S)
RASTERIZADAS, SEGUNDA_FAIXA = {}, {}
try:
    from faixas_lidas import RASTERIZADAS, SEGUNDA_FAIXA
except Exception:
    pass
# transcricoes por disciplina (slug vem do nome do arquivo de saida)
try:
    from faixas_lidas_disc import FAIXAS_LIDAS, SEGUNDA
except Exception:
    FAIXAS_LIDAS, SEGUNDA = {}, {}
D = sys.argv[1] if len(sys.argv) > 1 else r"G:\Meu Drive\Inteligência Artificial\Estrategia\Regular Controle (18-08-2026)\Curso Regular\Direito Administrativo (Regular Controle) (18-08-2026)"
SAIDA = sys.argv[2] if len(sys.argv) > 2 else "mapa18.json"
SLUG = SAIDA[5:-5] if SAIDA.startswith('mapa_') else ''
for (_d, _a, _p), _t in list(FAIXAS_LIDAS.items()):
    if _d == SLUG: RASTERIZADAS[(_a, _p)] = _t
for (_d, _a, _p), _t in list(SEGUNDA.items()):
    if _d == SLUG: SEGUNDA_FAIXA[(_a, _p)] = _t

ROXO = (0.259, 0.192, 0.643)
def roxo(c): return c and all(abs(a - b) < .05 for a, b in zip(c, ROXO))
# a faixa pode vir NUMERADA ("6. LISTA DE QUESTOES", "5 - GABARITO"): tira o prefixo antes
NUMERO = re.compile(r'^\s*\d+\s*[-–—.)]?\s*')
_FIM = re.compile(r'^(quest[õo]es|lista d[ae]s? quest|gabarito|refer[êe]ncias|bibliografia|'
                  r'respostas d[ao]s quest|simulado|considera[çc][õo]es finais)', re.I)
_APRES = re.compile(r'^(apresenta[çc][ãa]o|motiva[çc][ãa]o da aula|quem (sou|é)|'
                    r'sobre (o|a) professor|seja bem[- ]vindo|palavras iniciais)', re.I)
class FIM_TEORIA:
    @staticmethod
    def match(t):
        return _FIM.match(NUMERO.sub('', t or ''))
class APRES:
    @staticmethod
    def match(t):
        return _APRES.match(NUMERO.sub('', t or ''))
LIXO = re.compile(r'herbert almeida|equipe direito|www\.|gisilene|^aula \d+$|^\d+$|^índice', re.I)
QUESTAO = re.compile(r'\(\s*[A-ZÀ-Ú][^()]{2,70}?[-–/]\s*(19|20)\d\d\s*[^()]{0,30}\)')
COMENT = re.compile(r'^\s*coment[áa]rios?\s*:', re.I | re.M)

def tem_questao(pg):
    t = pg.get_text('text')
    return bool(COMENT.search(t)) or bool(QUESTAO.search(re.sub(r'\s+', ' ', t)))
MIN, ALVO, MAX = 5, 10, 12

# LIMIARES: faixa de tolerancia, nunca constante cravada. O layout varia por professor
# e por aula. Quando da' pra medir no proprio documento, medir (ver corpo_do_doc).
LARG_MIN_FAIXA = 400          # medido: faixas reais tem 452-528pt
ALT_FAIXA = (24, 60)          # medido: 27/30/31/34pt. Abaixo de 24 e' cabecalho de tabela
                              # ou caixa de mnemonico (o (JoVeM...) da Aula 07 tem 21pt)
X0_MAX_FAIXA = 60             # medido: 30/34/36/41pt. A varredura dos 1096 PDFs sugeriu
                              # 28-36, o que descartaria 57 faixas boas das Aulas 06 e 07

def faixa_valida(dr):
    """faixa de titulo: roxa, larga, alta e na margem esquerda"""
    r = dr['rect']
    return (roxo(dr.get('fill')) and r.width > LARG_MIN_FAIXA
            and ALT_FAIXA[0] <= r.height < ALT_FAIXA[1] and r.x0 <= X0_MAX_FAIXA)


LIMPEZA = [
    (re.compile(r'=+[0-9A-Fa-f]{4,}=+'), ''),                 # marca d'agua antipirataria no titulo
    (re.compile(r'[​‌‍⁠﻿‪-‮]'), ''),  # zero-width e marcas de direcao
]

def limpa(t):
    t = re.sub(r'\s+', ' ', t.replace('\n', ' ')).strip()
    t = re.sub(r'\s+([,;:?!])', r'\1', t)
    t = re.sub(r'\b([B-DF-HJ-NP-TV-Z])\s+([A-ZÀ-Ú]{2,})', r'\1\2', t)
    return t.strip(' ,;:·-–—')

def faixas_da_pagina(pg, aula, p):
    """faixas roxas, com o texto lido do PDF ou da transcricao visual"""
    rs = sorted([dr['rect'] for dr in pg.get_drawings()
                 if faixa_valida(dr)],
                key=lambda r: r.y0)
    # junta faixa que quebrou em duas linhas (retangulos colados na vertical)
    merged = []
    for r in rs:
        if merged and r.y0 - merged[-1].y1 < 6:
            merged[-1] = pymupdf.Rect(merged[-1].x0, merged[-1].y0, max(merged[-1].x1, r.x1), r.y1)
        else:
            merged.append(pymupdf.Rect(r))
    out = []
    for i, r in enumerate(merged):
        t = limpa(pg.get_text('text', clip=r))
        raster = False
        if not t:
            t = (SEGUNDA_FAIXA.get((aula, p), '') if i > 0 else '') or RASTERIZADAS.get((aula, p), '')
            raster = True
        out.append({'y': r.y0, 'nivel': 1, 'texto': t, 'raster': raster, 'ordem': i})
    return out

def titulo_valido(t):
    """descarta prosa do corpo que caiu no filtro de tamanho de fonte"""
    if len(t) < 3 or len(t) > 110: return False
    if LIXO.search(t) or APRES.match(t): return False
    if not t[0].isupper(): return False              # titulo nao comeca em minuscula
    if t[-1] in '.,;:': return False                 # titulo nao termina em pontuacao de frase
    if re.search(r'\.\s+[A-ZÀ-Ú]', t): return False   # duas frases = prosa, nao titulo
    if len(t.split()) > 14: return False
    if re.match(r'^(art|inc|par|§)', t, re.I): return False
    if QUESTAO.search(t): return False               # enunciado de questao
    if t[0] in '▪•●→-': return False       # marcador de lista
    d = sum(1 for c in t if c.isdigit())
    if d and d / len(t) > .30: return False          # valor de tabela, nao titulo
    if 'R$' in t: return False
    if t.count(')') > t.count('('): return False     # fragmento de item ("IV, “c”)")
    return True


def corpo_do_doc(doc, a, b):
    h = collections.Counter()
    for p in range(a, b + 1):
        for bl in doc[p - 1].get_text('dict')['blocks']:
            if bl['type'] != 0: continue
            for ln in bl['lines']:
                for sp in ln['spans']:
                    if sp['text'].strip(): h[round(sp['size'], 1)] += len(sp['text'].strip())
    if not h: return 12.0, h
    return max(h.items(), key=lambda kv: kv[1])[0], h

RES = {}
for f in sorted(glob.glob(os.path.join(D, '*.pdf'))):
    base = os.path.basename(f)
    mm = re.match(r'^(Aula \d+)', base)
    if not mm: continue
    aula = mm.group(1)
    tema = re.sub(r'\s*\(\d\d-\d\d-\d{4}\)\.pdf$', '', base)
    tema = re.sub(r'^Aula \d+ - ', '', tema)
    # o sufixo LS/LC entra entre o assunto e a data (renomeacao de 2026-08-20). E' rotulo
    # de versao do livro, nao faz parte do tema. NUNCA deduzir a versao pelo nome do
    # arquivo — so' e' seguro REMOVER o sufixo aqui; a versao vem da API/planilha.
    versao = 'LS' if ' LS (' in base else ('LC' if ' LC (' in base else '—')
    tema = re.sub(r'\s+L[SC]$', '', tema)
    doc = pymupdf.open(f)
    # 1) varre TODAS as faixas do arquivo e monta as zonas. A teoria pode VOLTAR depois de
    # um bloco de questoes (Elvis, 2026-08-20) — parar na primeira faixa de questoes perde
    # a teoria que vem depois. Nunca confiar no indice: o que vale e' varrer o arquivo.
    faixas = []
    for p in range(1, doc.page_count + 1):
        for fx in faixas_da_pagina(doc[p - 1], aula, p):
            fx['pag'] = p
            faixas.append(fx)
    # ESTRUTURA FIXA DO PDF DO ESTRATEGIA (medido em 22/08/2026, vale em 100% dos arquivos):
    #   p1 = capa | p2 = indice | p3 = a teoria comeca | ULTIMA = contracapa em branco
    # O inicio em 3 ja estava certo. O fim NAO estava: ia ate page_count e engolia a contracapa,
    # errando uma pagina no ultimo bloco de cada aula. Conferido em 6 PDFs: 0 caracteres uteis.
    ULTIMA_UTIL = doc.page_count - 1
    zonas, atual, desde = [], 'T', 3
    for fx in faixas:
        t = 'Q' if FIM_TEORIA.match(fx['texto'] or '') else 'T'
        if t != atual:
            if fx['pag'] - 1 >= desde: zonas.append((atual, desde, fx['pag'] - 1))
            atual, desde = t, fx['pag']
    zonas.append((atual, desde, ULTIMA_UTIL))
    zonas_teoria = [(a, b) for (t, a, b) in zonas if t == 'T' and b >= a]
    if not zonas_teoria: zonas_teoria = [(3, ULTIMA_UTIL)]
    fim_teoria = zonas_teoria[0][1]
    zonas_extra = [(a, 'teoria retomada') for (a, b) in zonas_teoria[1:]]
    # 2) inicio da teoria: primeira pagina depois do indice
    ini = 3
    for p in range(2, 6):
        if 'Índice' in doc[p - 1].get_text('text')[:400]: ini = p + 1
    # 3) titulos tipograficos dentro da zona de teoria
    zonas_teoria = [(max(a, ini) if i == 0 else a, b) for i, (a, b) in enumerate(zonas_teoria)]
    corpo, hist = corpo_do_doc(doc, ini, fim_teoria)
    tams = sorted([s for s, n in hist.items() if s > corpo + .4 and n >= 60], reverse=True)
    nivel_de = {s: i + 2 for i, s in enumerate(tams)}
    pontos, pag_questao, paginas_questao, pend_faixa = [], 0, [], []
    paginas_teoria = [p for (a, b) in zonas_teoria for p in range(a, b + 1) if p >= ini]
    for p in paginas_teoria:
        pg = doc[p - 1]
        fxs = [dr['rect'] for dr in pg.get_drawings()
               if faixa_valida(dr)]
        try:
            tabs = [pymupdf.Rect(*t.bbox) for t in pg.find_tables().tables]
        except Exception:
            tabs = []
        caixas = [dr['rect'] for dr in pg.get_drawings()
                  if dr.get('fill') and not roxo(dr.get('fill')) and dr['rect'].width < 420 and dr['rect'].height > 10]
        for fx in faixas_da_pagina(pg, aula, p):
            if fx['texto']: pontos.append((p, fx['y'], 1, fx['texto'], fx['raster']))
            else: pend_faixa.append((p, round(fx['y']), fx['ordem']))
        for bl in pg.get_text('dict')['blocks']:
            if bl['type'] != 0: continue
            for ln in bl['lines']:
                sz = round(ln['spans'][0]['size'], 1)
                if sz not in nivel_de or ln['spans'][0]['color'] == 0xFFFFFF: continue
                pt = pymupdf.Point(ln['bbox'][0] + 2, ln['bbox'][1] + 4)
                if any(pt in r for r in fxs + caixas + tabs): continue
                t = limpa(''.join(s['text'] for s in ln['spans']))
                if not titulo_valido(t): continue
                pontos.append((p, ln['bbox'][1], nivel_de[sz], t, False))
        if tem_questao(pg):
            pag_questao += 1
            paginas_questao.append(p)
    pontos.sort(key=lambda x: (x[0], x[1]))
    # junta titulo quebrado em duas linhas
    m = []
    for a in pontos:
        if m and m[-1][2] == a[2] and a[0] == m[-1][0] and a[1] - m[-1][1] < 26:
            m[-1] = (m[-1][0], m[-1][1], m[-1][2], limpa(m[-1][3] + ' ' + a[3]), m[-1][4])
        else:
            m.append(a)
    RES[aula] = {'arq': base, 'versao': versao, 'tema': tema, 'ini': ini, 'fim': fim_teoria, 'pontos': m,
                 'corpo': corpo, 'tams': tams, 'paginas': doc.page_count,
                 'zonas_extra': zonas_extra, 'zonas_teoria': zonas_teoria,
                 'pag_questao': pag_questao,
                 'paginas_questao': paginas_questao, 'pend_faixa': pend_faixa,
                 'hash': hashlib.sha256(open(f, 'rb').read()).hexdigest()[:16]}
    print('%-8s %-44s teoria %-22s (%3d pág de %3d) | %3d títulos%s' %
          (aula, tema[:42], ' + '.join('p%d-%d' % z for z in zonas_teoria), len(paginas_teoria),
           doc.page_count, len(m), '  << TEORIA VOLTA' if len(zonas_teoria) > 1 else ''))

json.dump({a: {k: v for k, v in d.items()} for a, d in RES.items()},
          open(os.path.join(S, SAIDA), 'w', encoding='utf-8'), ensure_ascii=False)
print()
tot_t = sum(d['fim'] - d['ini'] + 1 for d in RES.values())
tot_q = sum(d['pag_questao'] for d in RES.values())
print('TOTAL: %d páginas de teoria nas 18 aulas | %d dessas têm questão embutida (%.0f%%)' %
      (tot_t, tot_q, 100 * tot_q / tot_t))
