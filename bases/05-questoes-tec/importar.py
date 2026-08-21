# -*- coding: utf-8 -*-
"""Importa pro banco o que ja foi colhido pelo navegador.

Os arquivos vem do coletor que roda no tecconcursos.com.br e exporta por download:
  censo_dificuldade.json  {id: FAIXA}
  censo_banca.json        {id: BANCA}
  censo_por_assunto.json  {mapa: {assunto: {j, ids}}, dif: {...}}
  enunciados.json         [{id, enunciado, alternativas, ...}]
"""
import io, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banco

MAP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mapeamento')
le = lambda n: json.load(io.open(os.path.join(MAP, n), encoding='utf-8')) \
               if os.path.exists(os.path.join(MAP, n)) else None
agora = lambda: time.strftime('%Y-%m-%d %H:%M:%S')


def importar():
    c = banco.abre()
    # 1) os alvos: quais questoes existem em cada assunto
    pa = le('censo_por_assunto.json')
    if pa:
        linhas = [(int(a), int(i), v['j']) for a, v in pa['mapa'].items() for i in v['ids']]
        c.executemany('INSERT OR IGNORE INTO alvo VALUES (?,?,?)', linhas)
        print('alvos:', len(linhas))
    # 2) censos: dificuldade e banca de tudo
    dif, bnc = le('censo_dificuldade.json') or {}, le('censo_banca.json') or {}
    for ids, campo, dados in ((dif.keys(), 'dificuldade', dif), (bnc.keys(), 'banca', bnc)):
        c.executemany('INSERT INTO questao (id, %s) VALUES (?,?) '
                      'ON CONFLICT(id) DO UPDATE SET %s = excluded.%s' % (campo, campo, campo),
                      [(int(i), dados[i]) for i in ids])
        print('%s: %d' % (campo, len(dados)))
    # 3) enunciados ja colhidos
    en = le('enunciados_amostra.json') or []
    c.executemany("""INSERT INTO questao (id, enunciado, alternativas, orgao, ano, tipo,
                       id_assunto, assunto_tec, comentada, baixada_em)
                     VALUES (?,?,?,?,?,?,?,?,?,?)
                     ON CONFLICT(id) DO UPDATE SET
                       enunciado=excluded.enunciado, alternativas=excluded.alternativas,
                       orgao=excluded.orgao, ano=excluded.ano, tipo=excluded.tipo,
                       id_assunto=excluded.id_assunto, assunto_tec=excluded.assunto_tec,
                       comentada=excluded.comentada, baixada_em=excluded.baixada_em""",
                  [(x['id'], x['enunciado'], json.dumps(x['alternativas'], ensure_ascii=False),
                    x.get('orgao'), x.get('ano'), x.get('tipo'), x.get('id_assunto'),
                    x.get('assunto_tec'), x.get('comentada', 0), agora()) for x in en])
    print('enunciados:', len(en))
    c.commit()
    return c


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    c = importar()
    print()
    r = banco.resumo(c)
    for k, v in r.items(): print('  %-16s %6d' % (k, v))
    falta = len(banco.falta_enunciado(c))
    print('\n  falta enunciado  %6d' % falta)
