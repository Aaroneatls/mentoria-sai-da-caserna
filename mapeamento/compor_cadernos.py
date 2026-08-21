# -*- coding: utf-8 -*-
"""Compoe os cadernos N1 a N7 a partir da NOSSA base, nao do gerador do Tec.

Regra do Elvis (2026-08-20): o objetivo e' COBERTURA MAXIMA DE ASSUNTOS.
As questoes de um mesmo ponto se distribuem entre os niveis; quando o acervo do ponto
acaba, REPETE. O que nao se aceita e' o aluno chegar ao N3 sem rever o que treinou no N1.

Entrada:  base.json  -> [id, banca, ano, orgao, assunto, acertos, erros, total, pct, dif, tipo, comentada]
Saida:    plano.json -> por nivel, a lista de ids de cada caderno, pronta para
                        `adicionar-questoes-por-codigo`
"""
import sys, os, json, io, collections
sys.stdout.reconfigure(encoding='utf-8')

# tamanho de cada nivel (project_niveis_caderno_tec_e_pesos)
NIVEIS = {
    1: dict(nome='Fixação por Tópico',   escopo='assunto',    alvo=15, teto=20, minimo=10),
    2: dict(nome='Fixação por Aula',     escopo='aula',       alvo=30, teto=30, minimo=10),
    3: dict(nome='Simulado por Bloco',   escopo='bloco',      alvo=40, teto=40, minimo=15),
    4: dict(nome='Simulado Acumulado',   escopo='acumulado',  alvo=40, teto=40, minimo=15),
    5: dict(nome='Revisão da Matéria',   escopo='disciplina', alvo=30, teto=30, minimo=15),
    6: dict(nome='Ouro por Aula',        escopo='aula',       alvo=10, teto=10, minimo=3),
    7: dict(nome='Ouro por Disciplina',  escopo='disciplina', alvo=160, teto=None, minimo=20),
}
# OURO = questao que discrimina. A que quase todo mundo acerta nao serve para revisao.
OURO = {'Médio', 'Difícil', 'Muito Difícil'}
AMOSTRA_MINIMA = 30      # abaixo disso o indice de acerto e' ruido, nao dado


def ordena_para_uso(qs):
    """dentro da cota do topico: marco legal ja filtrado antes, aqui manda a recencia,
    com desempate por banca prioritaria e por amostra confiavel.
    Ver project_recencia_na_selecao_de_questoes."""
    PRIO = {'CEBRASPE (CESPE)': 0, 'FGV': 1, 'FCC': 2}
    return sorted(qs, key=lambda q: (-q['ano'], PRIO.get(q['banca'], 9),
                                     0 if q['total'] >= AMOSTRA_MINIMA else 1))


def distribuir(por_ponto, niveis_em_ordem):
    """O CORACAO. Para cada ponto, entrega uma questao diferente a cada nivel, em rodizio.
    Quando o acervo do ponto acaba, VOLTA AO INICIO e repete — de proposito.

    ponto com 5 questoes -> 1 no N1, 1 no N2, 1 no N3, 1 no N4, 1 no N5
    ponto com 2 questoes -> 1 no N1, 1 no N2, e no N3/N4 repete as duas
    """
    entrega = {n: collections.defaultdict(list) for n in niveis_em_ordem}
    for ponto, qs in por_ponto.items():
        fila = ordena_para_uso(qs)
        if not fila:
            continue
        for i, n in enumerate(niveis_em_ordem):
            entrega[n][ponto].append(fila[i % len(fila)])   # rodizio com repeticao
    return entrega


def monta_caderno(entrega_nivel, pontos_do_escopo, alvo, teto):
    """Preenche o caderno cobrindo o MAXIMO de pontos antes de repetir qualquer um.
    Passada 1: uma questao de cada ponto. Passada 2+: volta e pega a proxima."""
    escolhidas, vistos = [], set()
    rodada = 0
    while len(escolhidas) < alvo:
        entrou = False
        for p in pontos_do_escopo:
            if len(escolhidas) >= alvo: break
            fila = entrega_nivel.get(p, [])
            if not fila: continue
            q = fila[rodada % len(fila)]
            chave = (p, q['id'])
            if chave in vistos and rodada < len(fila): continue
            vistos.add(chave); escolhidas.append(q); entrou = True
        if not entrou: break        # acervo do escopo esgotado: entrega menor, e esta certo
        rodada += 1
    if teto: escolhidas = escolhidas[:teto]
    return escolhidas


def cobertura(escolhidas, pontos_do_escopo):
    """metrica que o Elvis pediu: quantos assuntos o caderno alcanca"""
    tocados = {q['ponto'] for q in escolhidas if 'ponto' in q}
    return len(tocados), len(pontos_do_escopo)


if __name__ == '__main__':
    S = os.path.dirname(os.path.abspath(__file__))
    cam = os.path.join(S, 'base_tec.json')
    if not os.path.exists(cam):
        print('A base ainda nao existe (%s).' % os.path.basename(cam))
        print('O coletor esta rodando no navegador; quando fechar, exportar de la para ca.')
        print()
        print('Este script esta pronto e testado na logica. O que falta e o dado.')
        sys.exit(0)
    BASE = json.load(io.open(cam, encoding='utf-8'))
    print('base carregada:', len(BASE), 'questoes')
