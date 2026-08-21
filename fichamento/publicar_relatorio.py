# -*- coding: utf-8 -*-
"""Publica o relatorio dos cadernos N1 a N5 do bloco de Atos Administrativos."""
import sys, os, json, collections
sys.stdout.reconfigure(encoding='utf-8')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI); sys.path.insert(0, os.path.join(RAIZ, 'coleta-tec'))
import dadm_atos as F, banco, gspread

CRED = os.path.join(RAIZ, 'credenciais') + os.sep

CADERNOS = [
 [101445052, 'DADM-018 | Atos Administrativos: Atributos | N1', 15],
 [101445071, 'DADM-019 | Atos Administrativos: Elementos e Requisitos | N1', 15],
 [101445079, 'DADM-020 | Atos Administrativos: Merito e Vicios | N1', 9],
 [101445085, 'DADM-023 | Atos Administrativos: Convalidacao e Nulidades | N1', 15],
 [101445099, 'DADM Aula 06 | Atos Administrativos | N2 Fixacao por Aula', 30],
 [101445107, 'DADM Aula 06 | Atos Administrativos | N3 Simulado por Bloco', 40],
 [101445122, 'DADM Aula 06 | Atos Administrativos | N4 Simulado Acumulado', 40],
 [101445130, 'DADM Aula 06 | Atos Administrativos | N5 Revisao da Materia', 30],
]
LINK = 'https://www.tecconcursos.com.br/questoes/cadernos/%d/caderno'

AZUL = {'red': .85, 'green': .89, 'blue': .95}
CINZA = {'red': .96, 'green': .96, 'blue': .96}
OURO = {'red': 1.0, 'green': .93, 'blue': .78}


def fmt(sh, ws, ncols, nlin, hdr):
    g = ws.id
    return [
     {'repeatCell': {'range': {'sheetId': g, 'startRowIndex': hdr - 1, 'endRowIndex': hdr + nlin,
       'startColumnIndex': 0, 'endColumnIndex': ncols},
      'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER',
       'verticalAlignment': 'MIDDLE', 'wrapStrategy': 'WRAP'}},
      'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)'}},
     {'repeatCell': {'range': {'sheetId': g, 'startRowIndex': hdr - 1, 'endRowIndex': hdr,
       'startColumnIndex': 0, 'endColumnIndex': ncols},
      'cell': {'userEnteredFormat': {'textFormat': {'bold': True}, 'backgroundColor': AZUL}},
      'fields': 'userEnteredFormat(textFormat,backgroundColor)'}},
     {'updateSheetProperties': {'properties': {'sheetId': g,
       'gridProperties': {'frozenRowCount': hdr}}, 'fields': 'gridProperties(frozenRowCount)'}}]


def main():
    c = banco.abre()
    M = {r['id']: r for r in c.execute(
        'SELECT id, banca, ano, dificuldade, orgao FROM questao')}
    plano = {p['nome']: p for p in json.load(open(os.path.join(AQUI, 'plano_cadernos.json')))}
    gc = gspread.oauth(credentials_filename=CRED + 'google-oauth-client.json',
                       authorized_user_filename=CRED + 'google-oauth-token.json')
    TIT = 'Cadernos N1-N5 — Atos Administrativos (teste de 21/08/2026)'
    try:
        sh = gc.open(TIT)
        for w in sh.worksheets()[1:]:
            sh.del_worksheet(w)
    except gspread.SpreadsheetNotFound:
        sh = gc.create(TIT)

    # ---------- aba 1: os cadernos ----------
    H = ['Nível', 'Caderno', 'Questões', 'Pontos cobertos', 'Cobertura',
         'Cebraspe', 'FGV', 'FCC', 'Ano mais antigo', 'Ano mais novo', 'Link']
    linhas = []
    for cad, nome, n in CADERNOS:
        p = plano[nome]
        qs = p['questoes']
        b = collections.Counter(M[q]['banca'] for q in qs)
        anos = [M[q]['ano'] for q in qs if M[q]['ano']]
        linhas.append([nome.split('| N')[-1][0] if '| N' in nome else '1', nome, len(qs),
                       '%d de %d' % (p['cob'][0], p['cob'][1]),
                       '%d%%' % round(100 * p['cob'][0] / p['cob'][1]),
                       b.get('CEBRASPE', 0), b.get('FGV', 0), b.get('FCC', 0),
                       min(anos), max(anos), LINK % cad])
    TOPO = [
     ['CADERNOS N1 A N5 — ATOS ADMINISTRATIVOS', ''],
     ['O que é isto', 'Primeiro teste de ponta a ponta: 199 questões lidas uma a uma, '
      'ligadas a 38 pontos e a 4 tópicos mestres, e daí compostos 8 cadernos. '
      'Nenhum caderno saiu do gerador do Tec: a composição é nossa.'],
     ['Regra da composição', 'Cobertura primeiro. Antes de repetir qualquer ponto, todos os '
      'outros são tocados. Dentro da cota de cada ponto vale a recência, com desempate por banca.'],
     ['Por que os níveis se repetem em parte', 'De propósito. O aluno revê o mesmo PONTO em '
      'níveis diferentes, mas com QUESTÃO diferente enquanto houver acervo. A sobreposição '
      'medida entre N2 e N5 ficou entre 37% e 50%.'],
     ['Limite conhecido', 'Só a Aula 06 está fichada. Por isso N3, N4 e N5 partilham o mesmo '
      'universo de 199 questões; quando a disciplina inteira estiver fichada, cada um terá '
      'escopo próprio.'],
     ['Ainda não entra aqui', 'Níveis 6 e 7 (Ouro) dependem de ler a resolução das candidatas, '
      'que a impressão do Tec não traz.']]
    ws = sh.get_worksheet(0)
    ws.clear()
    ws.update_title('Cadernos')
    ws.update(values=TOPO, range_name='A1:B%d' % len(TOPO))
    hdr = len(TOPO) + 2
    ws.update(values=[H], range_name='A%d:K%d' % (hdr, hdr))
    ws.update(values=linhas, range_name='A%d:K%d' % (hdr + 1, hdr + len(linhas)))
    rq = fmt(sh, ws, len(H), len(linhas), hdr)
    rq.append({'repeatCell': {'range': {'sheetId': ws.id, 'startRowIndex': 0,
      'endRowIndex': len(TOPO), 'startColumnIndex': 0, 'endColumnIndex': 2},
      'cell': {'userEnteredFormat': {'horizontalAlignment': 'LEFT', 'wrapStrategy': 'WRAP',
       'backgroundColor': CINZA}},
      'fields': 'userEnteredFormat(horizontalAlignment,wrapStrategy,backgroundColor)'}})
    for r in range(1, len(TOPO)):
        rq.append({'mergeCells': {'range': {'sheetId': ws.id, 'startRowIndex': r,
          'endRowIndex': r + 1, 'startColumnIndex': 1, 'endColumnIndex': 11},
          'mergeType': 'MERGE_ALL'}})
    for k, w in enumerate([55, 330, 75, 110, 85, 80, 60, 60, 110, 110, 330]):
        rq.append({'updateDimensionProperties': {'range': {'sheetId': ws.id,
          'dimension': 'COLUMNS', 'startIndex': k, 'endIndex': k + 1},
          'properties': {'pixelSize': w}, 'fields': 'pixelSize'}})
    sh.batch_update({'requests': rq})

    # ---------- aba 2: os pontos ----------
    H2 = ['Tópico mestre', 'Ponto', 'O que a banca cobra', 'Questões', 'Como principal', '% do tópico']
    l2 = []
    for t in sorted(F.NOME_TOPICO):
        ids = [q for q in F.FICHA if F.TOPICO[q] == t]
        cnt = collections.Counter(p for q in ids for p in F.FICHA[q])
        prin = collections.Counter(F.FICHA[q][0] for q in ids)
        for p, n in cnt.most_common():
            l2.append([t, p, F.PONTOS[p], n, prin.get(p, 0),
                       '%d%%' % round(100 * n / len(ids))])
    w2 = sh.add_worksheet(title='Pontos', rows=10 + len(l2), cols=len(H2))
    w2.update(values=[['O QUE CADA TÓPICO REALMENTE COBRA', '']], range_name='A1:B1')
    w2.update(values=[['Como foi feito', 'Cada questão foi lida e ligada aos pontos que ela cobra. '
      'Uma questão pode cobrar vários. "Como principal" conta só quando o ponto é o eixo da questão.']],
      range_name='A2:B2')
    w2.update(values=[H2], range_name='A4:F4')
    w2.update(values=l2, range_name='A5:F%d' % (4 + len(l2)))
    rq2 = fmt(sh, w2, len(H2), len(l2), 4)
    rq2.append({'repeatCell': {'range': {'sheetId': w2.id, 'startRowIndex': 4,
      'endRowIndex': 4 + len(l2), 'startColumnIndex': 2, 'endColumnIndex': 3},
      'cell': {'userEnteredFormat': {'horizontalAlignment': 'LEFT'}},
      'fields': 'userEnteredFormat(horizontalAlignment)'}})
    for k, w in enumerate([110, 60, 430, 80, 110, 90]):
        rq2.append({'updateDimensionProperties': {'range': {'sheetId': w2.id,
          'dimension': 'COLUMNS', 'startIndex': k, 'endIndex': k + 1},
          'properties': {'pixelSize': w}, 'fields': 'pixelSize'}})
    sh.batch_update({'requests': rq2})

    # ---------- aba 3: questao por questao ----------
    H3 = ['Caderno', 'Nº', 'Questão', 'Banca', 'Ano', 'Órgão', 'Dificuldade (Tec)',
          'Tópico', 'Pontos que cobra', 'Link da questão']
    l3 = []
    for cad, nome, _ in CADERNOS:
        for i, q in enumerate(plano[nome]['questoes'], 1):
            m = M[q]
            l3.append([nome, i, q, m['banca'], m['ano'], m['orgao'], m['dificuldade'],
                       F.TOPICO[q], ' + '.join(F.FICHA[q]),
                       'https://www.tecconcursos.com.br/questoes/%d' % q])
    w3 = sh.add_worksheet(title='Questões', rows=10 + len(l3), cols=len(H3))
    w3.update(values=[['QUAL QUESTÃO ENTROU EM QUAL CADERNO', '']], range_name='A1:B1')
    w3.update(values=[['Para que serve', 'Registro de composição. É por aqui que se confere se '
      'uma questão pertence mesmo ao tópico, e é aqui que se vê a repetição entre níveis.']],
      range_name='A2:B2')
    w3.update(values=[H3], range_name='A4:J4')
    w3.update(values=l3, range_name='A5:J%d' % (4 + len(l3)))
    rq3 = fmt(sh, w3, len(H3), len(l3), 4)
    for k, w in enumerate([300, 45, 90, 100, 60, 90, 120, 100, 170, 260]):
        rq3.append({'updateDimensionProperties': {'range': {'sheetId': w3.id,
          'dimension': 'COLUMNS', 'startIndex': k, 'endIndex': k + 1},
          'properties': {'pixelSize': w}, 'fields': 'pixelSize'}})
    sh.batch_update({'requests': rq3})

    print(sh.url)
    print('cadernos: %d | pontos: %d | linhas de questao: %d' % (len(linhas), len(l2), len(l3)))


if __name__ == '__main__':
    main()
