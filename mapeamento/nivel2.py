# -*- coding: utf-8 -*-
"""Detector de NIVEL 2: subtitulo entre um par de linhas roxas finas.
Serve para as disciplinas em que o corpo do texto e o titulo tem o MESMO tamanho de fonte,
onde a tipografia sozinha nao separa (Administracao Publica e Auditoria Governamental).

Regra dura: o par de linhas SOZINHO nao identifica subtitulo. Testado em Direito
Administrativo, 245 candidatos, 43 falso positivo (caixa de destaque com marcadores e ate a
marca d'agua). Tem que exigir os dois sinais juntos.
"""
import sys, os, re, glob, json, collections
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf

ROXO = (0.259, 0.192, 0.643)
def roxo(c): return c and all(abs(a - b) < .05 for a, b in zip(c, ROXO))

LIXO = re.compile(r'www\.|^aula \d+$|^\d+$|^índice|equipe |^prof\b|=+[0-9A-Fa-f]{4,}=+', re.I)

def limpa(t):
    t = re.sub(r'=+[0-9A-Fa-f]{4,}=+', '', t)
    t = re.sub(r'\s+', ' ', t.replace('\n', ' ')).strip()
    t = re.sub(r'\s+([,;:?!])', r'\1', t)
    return t.strip(' ,;:·-–—')

def valido(t):
    """mesmo crivo do detector tipografico, mais o que o par de linhas deixa passar"""
    if len(t) < 4 or len(t) > 95: return False
    if LIXO.search(t): return False
    # titulo numerado e' legitimo: "1 - Conceitos Introdutorios"
    corpo_t = re.sub(r'^\s*\d+\s*[-–—.)]\s*', '', t)
    if not corpo_t or not corpo_t[0].isupper(): return False
    if t[-1] in '.,;:': return False
    if re.search(r'\.\s+[A-ZÀ-Ú]', t): return False
    if len(t.split()) > 12: return False
    if t[0] in '▪•●→-': return False
    d = sum(1 for c in corpo_t if c.isdigit())
    if d and d / len(corpo_t) > .30: return False
    if 'R$' in t: return False
    if t.count(')') > t.count('('): return False
    return True

def subtitulos_por_linhas(pg, corpo):
    """par de linhas roxas finas + o texto entre elas tem fonte >= a do corpo e e' negrito.
    Os DOIS sinais, nunca um so'."""
    linhas = sorted([d['rect'] for d in pg.get_drawings()
                     if roxo(d.get('fill')) and d['rect'].width > 400 and d['rect'].height <= 2],
                    key=lambda r: r.y0)
    out = []
    i = 0
    while i < len(linhas) - 1:
        r1, r2 = linhas[i], linhas[i + 1]
        gap = r2.y0 - r1.y0
        if not (18 < gap < 46):
            i += 1; continue
        caixa = pymupdf.Rect(r1.x0, r1.y0, r1.x1, r2.y1)
        # 2o sinal: fonte MAIOR que o corpo, ou familia tipografica diferente.
        # NUNCA testar negrito: aqui o titulo e' "Montserrat Medium", que nao tem "Bold"
        # no nome e seria descartado (mesma armadilha ja registrada na memoria).
        sinal = False
        for bl in pg.get_text('dict', clip=caixa)['blocks']:
            if bl['type'] != 0: continue
            for ln in bl['lines']:
                for sp in ln['spans']:
                    if not sp['text'].strip(): continue
                    if round(sp['size'], 1) > corpo + 0.4: sinal = True
                    elif 'Bold' in sp['font'] or 'Medium' in sp['font'] or 'Semib' in sp['font']:
                        sinal = True
        t = limpa(pg.get_text('text', clip=caixa))
        if sinal and valido(t):
            out.append((r1.y0, t))
        i += 2
    return out

def corpo_do_doc(doc, a, b):
    h = collections.Counter()
    for p in range(a, min(b, doc.page_count) + 1):
        for bl in doc[p - 1].get_text('dict')['blocks']:
            if bl['type'] != 0: continue
            for ln in bl['lines']:
                for sp in ln['spans']:
                    if sp['text'].strip(): h[round(sp['size'], 1)] += len(sp['text'].strip())
    return max(h.items(), key=lambda kv: kv[1])[0] if h else 12.0

if __name__ == '__main__':
    S = os.path.dirname(os.path.abspath(__file__))
    RC = r"G:\Meu Drive\Inteligência Artificial\Estrategia\Regular Controle (18-08-2026)\Curso Regular"
    ALVOS = [('Administração Pública', 'mapa_administra_§_£.json'),
             ('Auditoria Governamental', 'mapa_auditoria_gove.json')]
    for disc, arq in ALVOS:
        cam = os.path.join(S, arq)
        if not os.path.exists(cam):
            print('sem mapa:', arq); continue
        M = json.load(open(cam, encoding='utf-8'))
        pasta = glob.glob(os.path.join(RC, disc + '*'))[0]
        print('=== %s' % disc)
        total_antes = total_depois = 0
        for aula in sorted(M):
            d = M[aula]
            f = glob.glob(os.path.join(pasta, aula + '*.pdf'))
            if not f: continue
            doc = pymupdf.open(f[0])
            corpo = corpo_do_doc(doc, d['ini'], d['fim'])
            cobre = {(p, round(y)) for p, y, nv, t, r in d['pontos']}
            novos = []
            for (a, b) in (d.get('zonas_teoria') or [[d['ini'], d['fim']]]):
                for p in range(int(a), int(b) + 1):
                    if p > doc.page_count: break
                    for (y, t) in subtitulos_por_linhas(doc[p - 1], corpo):
                        if any(pp == p and abs(yy - y) < 16 for pp, yy in cobre): continue
                        novos.append((p, y, 2, t, False))
            total_antes += len(d['pontos']); total_depois += len(d['pontos']) + len(novos)
            d['pontos'] = sorted(d['pontos'] + novos, key=lambda x: (x[0], x[1]))
            if novos:
                print('   %-8s %3d titulos -> %3d  (+%d pelo par de linhas)' %
                      (aula, len(d['pontos']) - len(novos), len(d['pontos']), len(novos)))
        json.dump(M, open(cam, 'w', encoding='utf-8'), ensure_ascii=False)
        tp = sum(x['fim'] - x['ini'] + 1 for x in M.values())
        print('   TOTAL: %d -> %d titulos | 1 titulo a cada %.1f paginas (antes %.1f)' %
              (total_antes, total_depois, tp / max(total_depois, 1), tp / max(total_antes, 1)))
        print()
