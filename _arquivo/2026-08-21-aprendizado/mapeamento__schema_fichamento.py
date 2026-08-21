# -*- coding: utf-8 -*-
"""Cria o esquema das abas de fichamento COM as colunas que o BIZURITO exige.
Tem que existir ANTES da passada de fichamento — senao e' reabrir ~1.100 questoes depois."""
import sys, os, json, io
sys.stdout.reconfigure(encoding='utf-8')
import gspread
CRED = os.path.join('G:' + os.sep, 'Meu Drive', 'Inteligência Artificial', 'Claude Code',
                    'ccos-ratos', 'credenciais') + os.sep
AZUL = {"red": .85, "green": .89, "blue": .95}
CINZA = {"red": .96, "green": .96, "blue": .96}
OURO = {"red": 1.0, "green": .93, "blue": .78}

# ---------------------------------------------------------------- ABA PONTOS
# Colunas 1-8: a camada de "ponto" que ja estava desenhada.
# Colunas 9-14 (em OURO): exigidas pelo BIZURITO, secao 7 item 1 do briefing.
PONTOS = [
 ('Cód do Ponto',      'Chave plana do ponto: DADM-P001. Não embute o tópico pai — o ponto pode migrar.'),
 ('Cód Mestre',        'Bloco de estudo a que o ponto pertence (DADM-014). Liga o ponto à teoria.'),
 ('Disciplina',        'Nome canônico. É chave no Tutori junto com o Cód Mestre.'),
 ('Enunciado do ponto','A afirmação indivisível que a banca cobra. Uma linha por ponto.'),
 ('Questões',          'Quantas questões do acervo cobram este ponto. Não somar entre blocos.'),
 ('Índice de acerto',  'Percentual de acerto no Tec. NUNCA é impresso no material — vira rótulo de risco.'),
 ('Risco',             'MAIORIA ACERTA (>=70%) · MUITOS ESCORREGAM (50-69%) · ESSA DERRUBA (<50%). Cortes provisórios.'),
 ('Resolvível pela aula', 'sim / não. O "não" alimenta caderno de camada separada, não some.'),
 ('Bizu',              'BIZURITO — a frase que vai na coluna O QUE A BANCA COBRA. Deriva da resolução do professor, nunca de conhecimento próprio.'),
 ('Pergunta',          'BIZURITO — a pergunta da faixa ANTES DE LER, TENTE RESPONDER.'),
 ('Bizu Forte',        'BIZURITO — calculado. Marca o ponto de maior valor dentro do tópico.'),
 ('Letra da Lei',      'BIZURITO — dispositivo verbatim quando a cobrança é literal. Lei e súmula podem ser copiadas.'),
 ('Normas citadas',    'BIZURITO — índice para atualização legislativa. Ex.: Lei 14.133/2021 art. 75. Permite achar o que revisar quando a norma muda.'),
 ('Verificado em',     'BIZURITO — data da última conferência do conteúdo contra a fonte oficial.'),
 ('Data-marco',        'Questão anterior a esta data cobra texto revogado e é DESCARTADA, não despriorizada.'),
]
# ---------------------------------------------------------------- ABA QUESTOES
QUESTOES = [
 ('# da questão',   'O número com # ao lado da banca no Tec. Não é o "Questão N de 30".'),
 ('Banca',          'Cebraspe, FGV, FCC…'),
 ('Órgão',          ''),
 ('Ano',            'Necessário para ordenar por recência dentro da cota do tópico.'),
 ('Data',           'Quando disponível, mais precisa que o ano.'),
 ('Assunto no Tec', 'A classificação do próprio Tec. Referência independente da minha.'),
 ('Índice de acerto', 'Do Tec. Se não vier na API, raspar da tela no momento do fichamento.'),
 ('Anulada',        'sim/não — anulada conta na estatística mas não entra em caderno.'),
 ('Desatualizada',  'sim/não'),
 ('Resolvível pela aula', 'sim/não — a checagem cruzada das três referências.'),
 ('Observação',     ''),
]
# ---------------------------------------------------------------- ABA QUESTAO x PONTO
QXP = [
 ('# da questão', ''),
 ('Cód do Ponto', ''),
 ('Cód Mestre',   'Redundante de propósito: permite contar por bloco sem cruzar duas abas.'),
 ('Principal ou Secundário',
  'PRINCIPAL = é neste ponto que o gabarito se decide. SECUNDÁRIO = a questão toca o ponto, mas não é ele que define o acerto. '
  'Decidir na MESMA passada do fichamento: depois exige reler questão a questão. '
  'Múltipla escolha cobra um ponto por alternativa — sem esta coluna, o reforço dispara sobre assunto que o aluno já domina. '
  'Em Certo/Errado do Cebraspe quase não há problema; concentra-se em FGV e FCC.'),
 ('Origem',       'leitura / classificação do Tec / correlação com questões do PDF — as três referências.'),
 ('Confiança',    'alta / conferir'),
]

def montar(sh, nome, cols, nota):
    try:
        sh.del_worksheet(sh.worksheet(nome))
    except gspread.WorksheetNotFound:
        pass
    ws = sh.add_worksheet(title=nome, rows=200, cols=len(cols))
    ws.update(values=[[nota, '']], range_name='A1:B1')
    ws.update(values=[[c for c, _ in cols]], range_name='A3:%s3' % chr(64 + len(cols)))
    ws.update(values=[[d for _, d in cols]], range_name='A4:%s4' % chr(64 + len(cols)))
    g = ws.id
    novas = {'Bizu', 'Pergunta', 'Bizu Forte', 'Letra da Lei', 'Normas citadas', 'Verificado em',
             'Principal ou Secundário'}
    rq = [
     {"repeatCell": {"range": {"sheetId": g, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": len(cols)},
      "cell": {"userEnteredFormat": {"textFormat": {"bold": True}, "backgroundColor": AZUL,
                                     "horizontalAlignment": "CENTER", "wrapStrategy": "WRAP"}},
      "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment,wrapStrategy)"}},
     {"repeatCell": {"range": {"sheetId": g, "startRowIndex": 3, "endRowIndex": 4, "startColumnIndex": 0, "endColumnIndex": len(cols)},
      "cell": {"userEnteredFormat": {"textFormat": {"italic": True, "fontSize": 9}, "backgroundColor": CINZA,
                                     "wrapStrategy": "WRAP", "verticalAlignment": "TOP"}},
      "fields": "userEnteredFormat(textFormat,backgroundColor,wrapStrategy,verticalAlignment)"}},
     {"mergeCells": {"range": {"sheetId": g, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": len(cols)}, "mergeType": "MERGE_ALL"}},
     {"repeatCell": {"range": {"sheetId": g, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": len(cols)},
      "cell": {"userEnteredFormat": {"horizontalAlignment": "LEFT", "wrapStrategy": "WRAP", "backgroundColor": CINZA}},
      "fields": "userEnteredFormat(horizontalAlignment,wrapStrategy,backgroundColor)"}},
     {"updateSheetProperties": {"properties": {"sheetId": g, "gridProperties": {"frozenRowCount": 4}}, "fields": "gridProperties(frozenRowCount)"}}]
    for k, (c, _) in enumerate(cols):
        if c in novas:
            rq.append({"repeatCell": {"range": {"sheetId": g, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": k, "endColumnIndex": k + 1},
                                      "cell": {"userEnteredFormat": {"backgroundColor": OURO}}, "fields": "userEnteredFormat(backgroundColor)"}})
        rq.append({"updateDimensionProperties": {"range": {"sheetId": g, "dimension": "COLUMNS", "startIndex": k, "endIndex": k + 1},
                                                 "properties": {"pixelSize": 230 if c in ('Enunciado do ponto', 'Bizu', 'Pergunta', 'Letra da Lei') else 130},
                                                 "fields": "pixelSize"}})
    sh.batch_update({"requests": rq})
    return ws

gc = gspread.oauth(credentials_filename=CRED + 'google-oauth-client.json',
                   authorized_user_filename=CRED + 'google-oauth-token.json')
TIT = 'Banco de Fichamento de Questões — esquema'
try:
    sh = gc.open(TIT)
except gspread.SpreadsheetNotFound:
    sh = gc.create(TIT)
montar(sh, 'Pontos', PONTOS,
       'ABA PONTOS — a camada indivisível abaixo do bloco de estudo. As colunas em DOURADO são as que o '
       'BIZURITO exige e precisam existir ANTES da passada de fichamento: se forem criadas depois, é reabrir '
       'cerca de 1.100 questões para preenchê-las.')
montar(sh, 'Questões', QUESTOES,
       'ABA QUESTÕES — uma linha por questão do acervo. Ano e data são obrigatórios: sem eles não há como '
       'ordenar por recência dentro da cota do tópico.')
montar(sh, 'Questão x Ponto', QXP,
       'ABA QUESTÃO x PONTO — a mesma questão pode cobrar mais de um ponto, por isso as contagens não se somam. '
       'A coluna PRINCIPAL/SECUNDÁRIO é a que sustenta o caderno de reforço: a irmandade de questões de um ponto '
       'se define pelo ponto PRINCIPAL, senão volta o ruído que a camada de ponto existe para eliminar.')
for w in sh.worksheets():
    if w.title.lower().startswith(('página1', 'pagina1', 'sheet1')) and len(sh.worksheets()) > 1:
        sh.del_worksheet(w)
print(sh.url)
print('abas:', [w.title for w in sh.worksheets()])
print('colunas novas do BIZURITO na aba Pontos: Bizu, Pergunta, Bizu Forte, Letra da Lei, Normas citadas, Verificado em')
