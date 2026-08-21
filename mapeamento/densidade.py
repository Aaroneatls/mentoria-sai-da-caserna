# -*- coding: utf-8 -*-
"""Mede quanto de cada bloco e' questao POR AREA, nao por 'a pagina tem questao'.
A caixa "ESTA CAI NA PROVA!" e' delimitada por linhas pontilhadas."""
import sys, os, re, glob, json
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf
S = r"C:\Users\saida\AppData\Local\Temp\claude\G--Meu-Drive-Intelig-ncia-Artificial-Claude-Code-ccos-ratos\d1ec1cd8-e665-4dfb-a047-a7395dc82975\scratchpad"
D = r"G:\Meu Drive\Inteligência Artificial\Estrategia\Regular Controle (18-08-2026)\Curso Regular\Direito Administrativo (Regular Controle) (18-08-2026)"
MAPA = json.load(open(os.path.join(S, 'mapa18.json'), encoding='utf-8'))
TOPO_TEXTO, BASE_TEXTO = 70.0, 780.0          # area util da pagina, fora cabecalho e rodape
ALTURA_UTIL = BASE_TEXTO - TOPO_TEXTO

def altura_questao(pg):
    """soma a altura das caixas de questao da pagina, em pontos"""
    ys = sorted({round(d['rect'].y0, 1) for d in pg.get_drawings()
                 if d.get('dashes') and d['dashes'] != '[] 0' and d['rect'].width > 300})
    if len(ys) < 2:
        return 0.0
    # as linhas pontilhadas vem aos pares (borda de cima e de baixo da caixa);
    # o par externo e' a moldura, o interno e' o quadro da questao
    total, i = 0.0, 0
    while i < len(ys) - 1:
        alto = ys[i + 1] - ys[i]
        if 25 < alto < 620:
            total += alto
            i += 2
        else:
            i += 1
    return min(total, ALTURA_UTIL)

res = {}
for aula in sorted(MAPA):
    d = MAPA[aula]
    f = glob.glob(os.path.join(D, aula + '*.pdf'))[0]
    doc = pymupdf.open(f)
    por_pag = {}
    for p in range(d['ini'], d['fim'] + 1):
        por_pag[p] = altura_questao(doc[p - 1]) / ALTURA_UTIL
    res[aula] = por_pag
    n = d['fim'] - d['ini'] + 1
    print('%-8s %3d pág de teoria | questão ocupa %2d%% da área | páginas com alguma questão: %d' %
          (aula, n, round(100 * sum(por_pag.values()) / n), sum(1 for v in por_pag.values() if v > 0)))

json.dump({a: {str(p): v for p, v in res[a].items()} for a in res},
          open(os.path.join(S, 'densidade.json'), 'w', encoding='utf-8'))
tot = sum(sum(v.values()) for v in res.values())
npg = sum(len(v) for v in res.values())
print()
print('MÉDIA GERAL: questão ocupa %d%% da área de teoria (antes eu dizia 32%%, medindo por página)'
      % round(100 * tot / npg))
