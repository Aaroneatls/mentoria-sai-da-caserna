# -*- coding: utf-8 -*-
"""Gera blocos de estudo a partir de um mapa de disciplina, e escreve a planilha."""
import sys, os, re, json, glob, collections, io
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caixa import titulo

MIN, ALVO, MAX = 5, 10, 12
_NUM = re.compile(r'^\s*\d+\s*[-–—.)]?\s*')
_NAO = re.compile(r'^(resumo|para revisar|mapas? (mental|e esquema)|revis[ãa]o|bibliografia|'
                  r'respostas d[ao]s quest)', re.I)
class NAO_TEORIA:
    @staticmethod
    def match(t):
        return _NAO.match(_NUM.sub('', t or ''))

SIGLA = {
 'mapa18':                'DADM',   # Direito Administrativo
 'mapa_direito_consti':   'DCON',
 'mapa_afo__or_ament':    'AFO',
 'mapa_administra__':     'ADMP',
 'mapa_controle_exter':   'CEXT',
 'mapa_auditoria_gove':   'AUDG',
 'mapa_contabilidade':    'CPUB',
 'mapa_portugu_s':        'PORT',
}
NOME = {
 'DADM': 'Direito Administrativo', 'DCON': 'Direito Constitucional',
 'AFO': 'AFO, Orcamento Publico e LRF', 'ADMP': 'Administracao Publica',
 'CEXT': 'Controle Externo', 'AUDG': 'Auditoria Governamental',
 'CPUB': 'Contabilidade Publica', 'PORT': 'Portugues',
}

POR_PALAVRA = [('administra', 'ADMP'), ('afo', 'AFO'), ('auditoria', 'AUDG'),
               ('contabilidade', 'CPUB'), ('controle', 'CEXT'), ('consti', 'DCON'),
               ('portugu', 'PORT'), ('mapa18', 'DADM')]
def sigla_de(arq):
    b = os.path.basename(arq)[:-5].lower()
    for chave, sg in POR_PALAVRA:
        if chave in b: return sg
    return b[:4].upper()

def blocos_da_aula(pontos, zonas, fim):
    """corta em ponto de titulo, 5 a 12 paginas, sem misturar zona de revisao"""
    P = [tuple(x) for x in pontos]
    n = len(P)
    if n == 0: return []
    fora = []
    for k, (p, y, nv, t, r) in enumerate(P):
        if nv == 1 and NAO_TEORIA.match(t):
            prox = next((j for j in range(k + 1, n) if P[j][2] == 1), n)
            fora.append((k, prox))
    regs, cur = [], 0
    for a, b in fora:
        if a > cur: regs.append((cur, a))
        cur = b
    if cur < n: regs.append((cur, n))
    saida = []
    for (r0, r1) in regs:
        fim_reg = fim if r1 == n else P[r1][0]
        INF = float('inf'); custo = {r0: 0}; volta = {}
        for j in range(r0 + 1, r1 + 1):
            melhor, de = INF, None
            for i in range(r0, j):
                if custo.get(i, INF) == INF: continue
                pa, pb = P[i][0], (P[j][0] if j < r1 else fim_reg)
                npg = pb - pa + 1
                if npg < MIN and j < r1: continue
                if npg > MAX + 8: continue
                pen = abs(npg - ALVO) ** 1.6
                if npg > MAX: pen += (npg - MAX) * 9
                if j < r1: pen += {1: 0, 2: 2, 3: 7, 4: 14}.get(P[j][2], 18)
                c = custo[i] + pen
                if c < melhor: melhor, de = c, i
            custo[j], volta[j] = melhor, de
        if custo.get(r1, INF) == INF: continue
        seq, cur2 = [], r1
        while cur2 != r0:
            seq.append((volta[cur2], cur2)); cur2 = volta[cur2]
        for i, j in reversed(seq):
            saida.append({'ini': P[i], 'fim': (P[j] if j < r1 else None), 'ult': fim_reg})
    return saida

def gerar(arqjson):
    M = json.load(io.open(arqjson, encoding='utf-8'))
    sg = sigla_de(arqjson)
    linhas, n = [], 0
    for aula in sorted(M):
        d = M[aula]
        tema = titulo(d['tema'])
        guarda = re.sub(r'\s*\(Parte \d\)$', '', tema)
        P = d['pontos']
        zt = d.get('zonas_teoria') or [[d['ini'], d['fim']]]
        blocos_aula = []
        for (za, zb) in [(int(z[0]), int(z[1])) for z in zt]:
            Pz = [t for t in P if za <= t[0] <= zb]
            if not Pz: continue
            blocos_aula += blocos_da_aula(Pz, None, zb)
        for b in blocos_aula:
            n += 1
            pi, yi, nvi, ti, _ = b['ini']
            pf = b['fim'][0] if b['fim'] else b['ult']
            yf = b['fim'][1] if b['fim'] else 10 ** 6
            dentro = [t for t in P if (pi, yi) <= (t[0], t[1]) < (pf, yf)]
            subs = [titulo(t[3]) for t in dentro[1:]]
            rot = titulo(ti)
            itens = []
            if rot.lower() != guarda.lower(): itens.append(rot)
            menor = min([t[2] for t in dentro[1:]], default=9)
            for t in dentro[1:]:
                if len(itens) >= 3: break
                if t[2] > menor + 1: continue
                n2 = titulo(t[3])
                if n2.lower() == guarda.lower() or n2 in itens: continue
                if len(', '.join(itens + [n2])) > 105: break
                itens.append(n2)
            nome = '%s: %s' % (guarda, ', '.join(itens)) if itens else guarda
            ult = dentro[-1] if len(dentro) > 1 else b['ini']
            inicie = 'Pagina %d, em "%s"' % (pi, rot)
            if b['fim']:
                termine = 'Pagina %d, ao concluir "%s"' % (pf, titulo(ult[3]))
            else:
                termine = 'Pagina %d, ao concluir "%s" - e o fim da teoria desta aula' % (pf, titulo(ult[3]))
            npg = pf - pi + 1
            if npg < 1:      # trava: multi-zona nao pode gerar bloco invertido
                continue
            pq = sum(1 for x in d['paginas_questao'] if pi <= x <= pf)
            linhas.append(['%s-%03d' % (sg, n), NOME.get(sg, sg), aula, tema, d['versao'],
                           nome, chr(10).join('%d. %s' % (i+1, x) for i, x in enumerate(subs)) or '-',
                           npg, '%d%%' % round(100 * pq / npg), inicie, termine])
    return linhas

if __name__ == '__main__':
    todas = []
    for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapa*.json'))):
        try:
            l = gerar(f)
        except Exception as e:
            print('ERRO em %s: %s' % (os.path.basename(f), e)); continue
        todas += l
        if l:
            t = [x[7] for x in l]
            print('%-30s %3d blocos | %2d a %2d pag | media %.1f | fora da faixa: %d' %
                  (l[0][1][:30], len(l), min(t), max(t), sum(t)/len(t),
                   sum(1 for x in t if x < MIN or x > MAX)))
    json.dump(todas, io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blocos_todos.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print()
    print('TOTAL: %d blocos em %d disciplinas' % (len(todas), len({x[1] for x in todas})))
