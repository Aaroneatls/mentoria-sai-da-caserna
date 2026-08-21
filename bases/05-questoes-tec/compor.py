# -*- coding: utf-8 -*-
"""Compoe os cadernos N1 a N5 a partir do fichamento, nao do gerador do Tec.

A regra que manda e COBERTURA: antes de repetir qualquer ponto, tocar todos os outros.
Dentro da cota de cada ponto vale a recencia, com desempate por banca prioritaria.
Ver project_cadernos_cobertura_e_composicao_propria e project_recencia_na_selecao_de_questoes.
"""
import sys, os, json, collections

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), 'coleta-tec'))
import dadm_atos as F
import banco

PRIO = {'CEBRASPE': 0, 'FGV': 1, 'FCC': 2}

NIVEIS = [
 (1, 'Fixacao por Topico', 'topico', 15),
 (2, 'Fixacao por Aula', 'aula', 30),
 (3, 'Simulado por Bloco', 'bloco', 40),
 (4, 'Simulado Acumulado', 'acumulado', 40),
 (5, 'Revisao da Materia', 'materia', 30),
]


def meta(c):
    """id -> (banca, ano, dificuldade)"""
    d = {}
    for r in c.execute('SELECT id, banca, ano, dificuldade FROM questao'):
        d[r['id']] = (r['banca'], r['ano'] or 0, r['dificuldade'])
    return d


def ordena(qs, M):
    """dentro da cota do ponto: mais recente primeiro, desempate por banca"""
    return sorted(qs, key=lambda q: (-M.get(q, ('', 0, ''))[1],
                                     PRIO.get(M.get(q, ('', 0, ''))[0], 9), q))


def por_ponto(ids):
    """ponto -> questoes que o cobrem. Uma questao entra em todos os pontos que toca."""
    d = collections.defaultdict(list)
    for q in ids:
        for p in F.FICHA[q]:
            d[p].append(q)
    return d


def compoe(ids, alvo, M, pular=0):
    """Passada 1: uma questao de cada ponto, do mais raro para o mais comum.
    Passada 2+: volta e pega a proxima de cada ponto. So repete quando o acervo acaba.

    `pular` faz o RODIZIO entre niveis: o N3 comeca da 2a questao de cada ponto, o N4 da
    3a, e assim por diante. Sem isso, dois niveis com o mesmo escopo e o mesmo alvo saem
    IDENTICOS — foi o que aconteceu na primeira rodada com N3 e N4. O aluno tem de rever o
    mesmo PONTO em niveis diferentes, com QUESTAO diferente enquanto houver acervo.
    """
    pp = {p: ordena(qs, M) for p, qs in por_ponto(ids).items()}
    if pular:
        pp = {p: (fila[pular:] + fila[:pular]) if len(fila) > pular else fila
              for p, fila in pp.items()}
    # ponto raro primeiro: se sobrar vaga, e ele que corre risco de ficar de fora
    ordem = sorted(pp, key=lambda p: (len(pp[p]), p))
    escolhidas, vistas = [], set()
    rodada = 0
    while len(escolhidas) < alvo and rodada < 12:
        entrou = False
        for p in ordem:
            if len(escolhidas) >= alvo:
                break
            fila = [q for q in pp[p] if q not in vistas]
            if not fila:
                continue
            q = fila[0]
            vistas.add(q)
            escolhidas.append(q)
            entrou = True
        if not entrou:
            break        # acervo esgotado: o caderno sai menor, e esta certo
        rodada += 1
    return escolhidas


def cobertura(qs, ids):
    todos = set(por_ponto(ids))
    tocados = {p for q in qs for p in F.FICHA[q]}
    return len(tocados), len(todos)


def montar():
    c = banco.abre()
    M = meta(c)
    todas = sorted(F.FICHA)
    planos = []
    # N1: um caderno por topico mestre
    for t in sorted(F.NOME_TOPICO):
        ids = [q for q in todas if F.TOPICO[q] == t]
        qs = compoe(ids, 15, M)
        planos.append(dict(nivel=1, escopo=t, nome='%s | %s | N1' % (t, F.NOME_TOPICO[t]),
                           questoes=qs, universo=len(ids), cob=cobertura(qs, ids)))
    # N2 a N5: escopo cada vez maior. Com so uma aula fichada, N3 a N5 partilham o universo.
    for k, (n, nome, escopo, alvo) in enumerate(NIVEIS[1:]):
        qs = compoe(todas, alvo, M, pular=k)
        planos.append(dict(nivel=n, escopo=escopo,
                           nome='DADM Aula 06 | Atos Administrativos | N%d %s' % (n, nome),
                           questoes=qs, universo=len(todas), cob=cobertura(qs, todas)))
    return planos, M


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    planos, M = montar()
    json.dump(planos, open(os.path.join(AQUI, 'plano_cadernos.json'), 'w'), indent=1)
    print('%-52s %5s %6s %9s %s' % ('caderno', 'qtd', 'acervo', 'cobertura', 'bancas'))
    for p in planos:
        b = collections.Counter(M[q][0] for q in p['questoes'])
        print('%-52s %5d %6d %5d/%-3d %s' % (
            p['nome'][:52], len(p['questoes']), p['universo'],
            p['cob'][0], p['cob'][1],
            ' '.join('%s:%d' % (k[:4], v) for k, v in b.most_common())))
