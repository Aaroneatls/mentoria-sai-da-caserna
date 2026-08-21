# -*- coding: utf-8 -*-
"""Publica a base multidisciplina do Curso Regular Controle."""
import sys, os, json, io, collections
sys.stdout.reconfigure(encoding='utf-8')
import gspread
CRED = os.path.join('G:' + os.sep, 'Meu Drive', 'Inteligência Artificial', 'Claude Code',
                    'ccos-ratos', 'credenciais') + os.sep
L = json.load(io.open('blocos_todos.json', encoding='utf-8'))
MIN, MAX = 5, 12

por = collections.defaultdict(list)
for x in L:
    por[x[1]].append(x)
CONF = {}
for d, v in por.items():
    fora = sum(1 for x in v if x[7] < MIN or x[7] > MAX)
    pct = 100.0 * fora / len(v)
    CONF[d] = 'ALTA' if pct <= 5 else ('MÉDIA' if pct <= 20 else 'BAIXA')

gc = gspread.oauth(credentials_filename=CRED + 'google-oauth-client.json',
                   authorized_user_filename=CRED + 'google-oauth-token.json')
TIT = 'Base Curso Regular Controle — Blocos de Estudo (multidisciplina)'
try:
    sh = gc.open(TIT)
except gspread.SpreadsheetNotFound:
    sh = gc.create(TIT)
for w in sh.worksheets():
    if w.title in ('Blocos', 'Disciplinas'):
        try:
            sh.del_worksheet(w)
        except Exception:
            pass

H = ['Cód Mestre', 'Disciplina', 'Aula', 'Tema da aula', 'Versão', 'Nome Mestre do Tópico',
     'Subtópicos tratados', 'Nº de páginas', '% com questão', 'INICIE EM', 'TERMINE EM',
     'Confiança', 'Observação']
# Elvis, 2026-08-21: bloco grande em Auditoria e' do MATERIAL, nao do detector. O professor
# escreve secoes de 12 a 14 paginas sem subdivisao — nao existe onde cortar. Decisao: aceitar.
def obs(x):
    if x[7] > 12 and 'Auditoria' in x[1]:
        return 'Seção longa sem subdivisão no material — não há título onde cortar. Aceito por decisão de 21/08/2026.'
    if x[7] > 12: return 'Acima do alvo de 12 páginas'
    if x[7] < 5: return 'Abaixo do mínimo de 5 páginas'
    return ''
linhas = [x + [CONF[x[1]], obs(x)] for x in L]
ws = sh.add_worksheet(title='Blocos', rows=20 + len(linhas), cols=len(H))
TOPO = [
 ['BASE CURSO REGULAR CONTROLE — %d blocos de estudo em %d disciplinas' % (len(linhas), len(por)), ''],
 ['Método', 'Títulos achados pela tipografia do PDF (o corpo de fonte é medido em cada arquivo, não fixado). Corte em ponto de título, alvo 10 páginas, faixa de 5 a 12. Página sempre a do ARQUIVO PDF.'],
 ['Versão do livro', 'LS = livro simplificado, que é a referência. LC = livro completo, usado quando não existe simplificado para aquela aula.'],
 ['Confiança', 'ALTA = até 5% dos blocos fora da faixa 5-12. MÉDIA = até 20%. BAIXA = acima disso; o corte precisa de revisão antes de ir para o aluno.'],
 ['Administração Pública — resolvido', 'O corpo do texto e os títulos usam o MESMO tamanho de fonte. A saída foi o detector de nível 2 (par de linhas roxas). Saiu de 65 para 199 títulos e de 23 para 46 blocos.'],
 ['Auditoria Governamental — decidido, não é defeito', 'O professor escreve seções de 12 a 14 páginas corridas, sem subdivisão. Não existe título onde cortar, então 12 dos 40 blocos passam de 12 páginas. Decisão do Elvis em 21/08/2026: ACEITAR, porque forçar o corte entregaria uma referência que o aluno não consegue seguir. Esses blocos estão marcados na coluna Observação.'],
 ['Pendente', 'Ligar cada bloco ao item do edital, ao TecConcursos e ao Bezerra.']]
ws.update(values=TOPO, range_name='A1:B%d' % len(TOPO))
HDR = len(TOPO) + 2
ws.update(values=[H], range_name='A%d:M%d' % (HDR, HDR))
ws.update(values=linhas, range_name='A%d:M%d' % (HDR + 1, HDR + len(linhas)))
g = ws.id
AZUL = {"red": .85, "green": .89, "blue": .95}
VERDE = {"red": .87, "green": .95, "blue": .87}
CINZA = {"red": .96, "green": .96, "blue": .96}
rq = [
 {"repeatCell": {"range": {"sheetId": g, "startRowIndex": HDR - 1, "endRowIndex": HDR + len(linhas), "startColumnIndex": 0, "endColumnIndex": 13},
  "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP"}},
  "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"}},
 {"repeatCell": {"range": {"sheetId": g, "startRowIndex": HDR - 1, "endRowIndex": HDR, "startColumnIndex": 0, "endColumnIndex": 13},
  "cell": {"userEnteredFormat": {"textFormat": {"bold": True}, "backgroundColor": AZUL}},
  "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
 {"repeatCell": {"range": {"sheetId": g, "startRowIndex": HDR, "endRowIndex": HDR + len(linhas), "startColumnIndex": 9, "endColumnIndex": 11},
  "cell": {"userEnteredFormat": {"backgroundColor": VERDE, "horizontalAlignment": "LEFT"}},
  "fields": "userEnteredFormat(backgroundColor,horizontalAlignment)"}},
 {"repeatCell": {"range": {"sheetId": g, "startRowIndex": HDR, "endRowIndex": HDR + len(linhas), "startColumnIndex": 6, "endColumnIndex": 7},
  "cell": {"userEnteredFormat": {"horizontalAlignment": "LEFT"}}, "fields": "userEnteredFormat(horizontalAlignment)"}},
 {"repeatCell": {"range": {"sheetId": g, "startRowIndex": 0, "endRowIndex": len(TOPO), "startColumnIndex": 0, "endColumnIndex": 2},
  "cell": {"userEnteredFormat": {"horizontalAlignment": "LEFT", "wrapStrategy": "WRAP", "backgroundColor": CINZA}},
  "fields": "userEnteredFormat(horizontalAlignment,wrapStrategy,backgroundColor)"}},
 {"updateSheetProperties": {"properties": {"sheetId": g, "gridProperties": {"frozenRowCount": HDR}}, "fields": "gridProperties(frozenRowCount)"}},
 {"mergeCells": {"range": {"sheetId": g, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 13}, "mergeType": "MERGE_ALL"}}]
for r in range(1, len(TOPO)):
    rq.append({"mergeCells": {"range": {"sheetId": g, "startRowIndex": r, "endRowIndex": r + 1,
                                        "startColumnIndex": 1, "endColumnIndex": 13}, "mergeType": "MERGE_ALL"}})
for k, w in enumerate([95, 175, 65, 215, 65, 300, 430, 80, 85, 340, 340, 85, 300]):
    rq.append({"updateDimensionProperties": {"range": {"sheetId": g, "dimension": "COLUMNS", "startIndex": k, "endIndex": k + 1},
                                             "properties": {"pixelSize": w}, "fields": "pixelSize"}})
sh.batch_update({"requests": rq})

HD = ['Disciplina', 'Blocos', 'Menor', 'Maior', 'Média', 'Fora da faixa', '% fora', 'Confiança']
ld = []
for d in sorted(por):
    v = por[d]
    t = [x[7] for x in v]
    fora = sum(1 for x in t if x < MIN or x > MAX)
    ld.append([d, len(v), min(t), max(t), round(sum(t) / len(t), 1), fora,
               '%d%%' % round(100 * fora / len(v)), CONF[d]])
wd = sh.add_worksheet(title='Disciplinas', rows=10 + len(ld), cols=len(HD))
wd.update(values=[['QUALIDADE DO CORTE POR DISCIPLINA', '']], range_name='A1:B1')
wd.update(values=[HD], range_name='A3:H3')
wd.update(values=ld, range_name='A4:H%d' % (3 + len(ld)))
gd = wd.id
sh.batch_update({"requests": [
 {"repeatCell": {"range": {"sheetId": gd, "startRowIndex": 2, "endRowIndex": 4 + len(ld), "startColumnIndex": 0, "endColumnIndex": 8},
  "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP"}},
  "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,wrapStrategy)"}},
 {"repeatCell": {"range": {"sheetId": gd, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": 8},
  "cell": {"userEnteredFormat": {"textFormat": {"bold": True}, "backgroundColor": AZUL}},
  "fields": "userEnteredFormat(textFormat,backgroundColor)"}}]
 + [{"updateDimensionProperties": {"range": {"sheetId": gd, "dimension": "COLUMNS", "startIndex": k, "endIndex": k + 1},
     "properties": {"pixelSize": w}, "fields": "pixelSize"}} for k, w in enumerate([230, 80, 70, 70, 80, 110, 80, 95])]})
print(sh.url)
for d in sorted(por):
    print('   %-30s %3d blocos  %s' % (d[:30], len(por[d]), CONF[d]))
