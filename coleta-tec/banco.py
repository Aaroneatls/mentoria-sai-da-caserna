# -*- coding: utf-8 -*-
"""Banco local de questoes do TecConcursos.

Por que existe: sem ele, cada ajuste de fichamento, de criterio de Ouro ou de composicao
de caderno obriga a voltar no Tec, e a volta e cara — o limite aperta a cada rodada. Com o
banco, o Tec vira FONTE (usada uma vez) e nao CONSULTA (usada sempre).

Regras que nao se negociam:
  1. O arquivo do banco NUNCA entra no git. Fica no Drive, fora do repositorio.
  2. Nada do conteudo do Tec sai nas entregas ao aluno: nem enunciado, nem resolucao.
     O que vai pro aluno e link de caderno, nome de topico nosso e texto nosso.
  3. O BIZURITO e ESCRITO por nos. A resolucao do Tec e fonte de leitura, nunca texto
     a ser copiado.
"""
import os, sqlite3, json, time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANCO = os.path.join(RAIZ, 'dados', 'banco-tec', 'questoes.db')

ESQUEMA = """
CREATE TABLE IF NOT EXISTS questao (
  id            INTEGER PRIMARY KEY,
  enunciado     TEXT,
  alternativas  TEXT,          -- json: lista de strings
  gabarito      TEXT,
  resolucao     TEXT,          -- comentario do professor; NULL enquanto nao baixado
  resolucao_hash TEXT,         -- pra detectar quando o professor edita
  professor     TEXT,
  banca         TEXT,
  ano           INTEGER,
  orgao         TEXT,
  cargo         TEXT,
  id_assunto    INTEGER,
  assunto_tec   TEXT,
  tipo          TEXT,
  dificuldade   TEXT,          -- rotulo do Tec; e' DIMENSAO, nao criterio de Ouro
  acertos       INTEGER,       -- NULL enquanto so' tivermos o censo por faixa
  erros         INTEGER,
  pct_acerto    REAL,
  anulada       INTEGER DEFAULT 0,
  desatualizada INTEGER DEFAULT 0,
  inedita       INTEGER DEFAULT 0,
  comentada     INTEGER DEFAULT 0,
  baixada_em    TEXT,
  conferida_em  TEXT           -- ultima vez que se checou anulada/desatualizada
);
CREATE INDEX IF NOT EXISTS ix_assunto ON questao(id_assunto);
CREATE INDEX IF NOT EXISTS ix_banca   ON questao(banca);
CREATE INDEX IF NOT EXISTS ix_ano     ON questao(ano);
CREATE INDEX IF NOT EXISTS ix_falta_resolucao ON questao(id) WHERE resolucao IS NULL;

-- o que a gente ainda precisa buscar, por assunto
CREATE TABLE IF NOT EXISTS alvo (
  id_assunto INTEGER,
  id_questao INTEGER,
  janela     TEXT,
  PRIMARY KEY (id_assunto, id_questao)
);

-- historico do limitador do Tec, pra calibrar a coleta
CREATE TABLE IF NOT EXISTS evento (
  quando TEXT, tipo TEXT, detalhe TEXT
);
"""


def abre():
    os.makedirs(os.path.dirname(BANCO), exist_ok=True)
    c = sqlite3.connect(BANCO)
    c.row_factory = sqlite3.Row
    c.executescript(ESQUEMA)
    return c


def falta_enunciado(c, limite=None):
    q = ("SELECT a.id_questao FROM alvo a LEFT JOIN questao q ON q.id = a.id_questao "
         "WHERE q.enunciado IS NULL")
    if limite: q += ' LIMIT %d' % int(limite)
    return [r[0] for r in c.execute(q)]


def falta_resolucao(c, limite=None):
    q = ("SELECT id FROM questao WHERE resolucao IS NULL AND comentada = 1 "
         "AND anulada = 0 AND desatualizada = 0")
    if limite: q += ' LIMIT %d' % int(limite)
    return [r[0] for r in c.execute(q)]


def resumo(c):
    def n(sql): return c.execute(sql).fetchone()[0]
    return dict(
        alvo=n('SELECT COUNT(*) FROM alvo'),
        com_enunciado=n('SELECT COUNT(*) FROM questao WHERE enunciado IS NOT NULL'),
        com_resolucao=n('SELECT COUNT(*) FROM questao WHERE resolucao IS NOT NULL'),
        com_dificuldade=n('SELECT COUNT(*) FROM questao WHERE dificuldade IS NOT NULL'),
        com_pct=n('SELECT COUNT(*) FROM questao WHERE pct_acerto IS NOT NULL'),
        anuladas=n('SELECT COUNT(*) FROM questao WHERE anulada = 1'),
        desatualizadas=n('SELECT COUNT(*) FROM questao WHERE desatualizada = 1'))
