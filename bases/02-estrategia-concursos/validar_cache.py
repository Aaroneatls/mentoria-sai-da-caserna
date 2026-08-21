# -*- coding: utf-8 -*-
"""Valida o cache por amostragem: reprocessa algumas aulas do zero e compara com o guardado.
Pega tanto arquivo alterado quanto detector alterado ou detector que sempre esteve errado."""
import sys, os, re, json, glob, random, hashlib, collections
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf
S = r"C:\Users\saida\AppData\Local\Temp\claude\G--Meu-Drive-Intelig-ncia-Artificial-Claude-Code-ccos-ratos\d1ec1cd8-e665-4dfb-a047-a7395dc82975\scratchpad"
D = r"G:\Meu Drive\Inteligência Artificial\Estrategia\Regular Controle (18-08-2026)\Curso Regular\Direito Administrativo (Regular Controle) (18-08-2026)"

VERSAO_DETECTOR = 'v8-2026-08-20'      # muda sempre que a regra de deteccao muda
FRACAO_AMOSTRA = 0.20                  # 20% das aulas, no minimo 2
COMPLETA = '--completa' in sys.argv    # verificacao total, nao amostra

MAPA = json.load(open(os.path.join(S, 'mapa18.json'), encoding='utf-8'))
ROXO = (0.259, 0.192, 0.643)
def roxo(c): return c and all(abs(a - b) < .05 for a, b in zip(c, ROXO))
FIM_TEORIA = re.compile(r'^(quest[õo]es|lista de quest|gabarito|refer[êe]ncias)', re.I)
COMENT = re.compile(r'^\s*coment[áa]rios?\s*:', re.I | re.M)
BANCA = re.compile(r'\(\s*[A-ZÀ-Ú][^()]{2,70}?[-–/]\s*(19|20)\d\d\s*[^()]{0,30}\)')

def limpa(t):
    t = re.sub(r'=+[0-9A-Fa-f]{4,}=+', '', t)
    t = re.sub(r'\s+', ' ', t.replace('\n', ' ')).strip()
    return t

def remede(f, aula):
    """reprocessa a aula DO ZERO, sem olhar nada do que está guardado"""
    doc = pymupdf.open(f)
    fim = None
    for p in range(1, doc.page_count + 1):
        for dr in doc[p - 1].get_drawings():
            r = dr['rect']
            if not (roxo(dr.get('fill')) and r.width > 400 and 24 <= r.height < 60 and r.x0 <= 60):
                continue
            t = limpa(doc[p - 1].get_text('text', clip=r))
            if t and FIM_TEORIA.match(t) and fim is None:
                fim = p - 1
        if fim: break
    ini = 3
    for p in range(2, 6):
        if 'Índice' in doc[p - 1].get_text('text')[:400]: ini = p + 1
    if fim is None:                      # faixa rasterizada: usa a transcricao visual
        sys.path.insert(0, S)
        from faixas_lidas import RASTERIZADAS
        cand = [p for (a, p), t in RASTERIZADAS.items() if a == aula and FIM_TEORIA.match(t)]
        fim = (min(cand) - 1) if cand else doc.page_count
    nq = sum(1 for p in range(ini, fim + 1)
             if COMENT.search(doc[p - 1].get_text('text'))
             or BANCA.search(re.sub(r'\s+', ' ', doc[p - 1].get_text('text'))))
    h = hashlib.sha256(open(f, 'rb').read()).hexdigest()[:16]
    return {'ini': ini, 'fim': fim, 'pag_questao': nq, 'hash': h}

aulas = sorted(MAPA)
if COMPLETA:
    amostra, k = aulas, len(aulas)
    print('cache: %d aulas | VERIFICAÇÃO COMPLETA (todas)' % len(aulas))
else:
    k = max(2, round(len(aulas) * FRACAO_AMOSTRA))
    random.seed()                        # amostra diferente a cada execucao, de proposito
    amostra = random.sample(aulas, k)
    print('cache: %d aulas | amostra desta rodada: %d (%s)' % (len(aulas), k, ', '.join(amostra)))
print('versão do detector:', VERSAO_DETECTOR)
print()
falhas = []
for aula in amostra:
    f = glob.glob(os.path.join(D, aula + '*.pdf'))[0]
    novo, velho = remede(f, aula), MAPA[aula]
    dif = [c for c in ('ini', 'fim', 'pag_questao', 'hash')
           if str(novo[c]) != str(velho.get(c))]
    ok = not dif
    print('%-8s teoria p%d-%d | %2d pág com questão | %s  %s' %
          (aula, novo['ini'], novo['fim'], novo['pag_questao'], novo['hash'],
           'OK' if ok else 'DIVERGE em ' + ', '.join(dif)))
    if not ok:
        for c in dif:
            print('           %-12s guardado=%s  recalculado=%s' % (c, velho.get(c), novo[c]))
        falhas.append(aula)
print()
if falhas:
    print('>>> CACHE INVÁLIDO. Reprocessar a disciplina inteira e avisar o Elvis.')
else:
    print('>>> cache confere na amostra. Pode reaproveitar o resto.')
