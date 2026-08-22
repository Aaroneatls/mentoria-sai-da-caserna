# -*- coding: utf-8 -*-
"""Validacoes da Base 1. NAO ESCREVE NADA. Sai 0 se tudo passou, 1 se falhou.

    python bases/01-disciplinas/conferir.py

E o modo padrao quando houver duvida: rodar isto antes de qualquer `criar` ou
`atualizar`. Nasceu de um caso real de 21/08/2026, em que conferir antes de
executar evitou ~600 chamadas produzindo dado errado.
"""
import io, csv, os, re, sys, unicodedata
from collections import Counter, defaultdict

RAIZ = os.path.dirname(os.path.abspath(__file__))
D, F = os.path.join(RAIZ, "dados"), os.path.join(RAIZ, "fontes")
ler = lambda p: list(csv.DictReader(io.open(p, encoding="utf-8-sig")))
falhas, avisos = [], []
def check(cond, msg):  (falhas if not cond else avisos.__class__()) if False else (None if cond else falhas.append(msg))

disc = ler(os.path.join(D, "disciplinas.csv"))
ap   = ler(os.path.join(D, "apelidos.csv"))
ar   = ler(os.path.join(D, "areas.csv"))
ren  = ler(os.path.join(D, "renomear-pastas.csv"))
siglas = [r["sigla"] for r in disc]
S = set(siglas)

# 1. as 21, unicas, no formato fechado na A8
check(len(disc) == 21, "disciplinas.csv tem %d linhas, deveria ter 21" % len(disc))
check(len(S) == 21, "sigla repetida em disciplinas.csv")
for s in siglas:
    check(re.fullmatch(r"[A-Z]{4,6}", s) or s == "AFO",
          "sigla fora do padrao 4-6 letras (AFO e a unica excecao de 3): %s" % s)
check(len(set(r["nome_canonico"] for r in disc)) == 21, "nome_canonico repetido")

# 2. integridade referencial
for r in ap:
    check(r["sigla"] in S or r["status"] != "ok",
          "apelido com status ok e sigla desconhecida: %r -> %r" % (r["nome_na_fonte"], r["sigla"]))
    check(r["sigla"] == "" or r["status"] == "ok",
          "apelido com sigla preenchida mas status %r: %r" % (r["status"], r["nome_na_fonte"]))
    check(r["status"] in ("ok","fora_escopo","local","lixo_migracao","olho"),
          "status invalido: %r" % r["status"])
for r in ar:
    check(r["sigla"] in S, "areas.csv referencia sigla desconhecida: %s" % r["sigla"])
    check(r["evidencia"].strip() != "", "area sem evidencia: %s/%s" % (r["sigla"], r["area"]))

# 3. nenhuma fonte perdida: toda linha do .txt tem de aparecer em apelidos.csv
def fonte_txt(nome, col=None):
    out = []
    for l in io.open(os.path.join(F, nome), encoding="utf-8"):
        l = l.rstrip("\n")
        if not l.strip() or l.lstrip().startswith("#"): continue
        out.append(l.split("|")[col].strip() if col is not None else l.strip())
    return out
vistos = Counter(r["nome_na_fonte"] for r in ap)
for arq, col, rot in [("tec.txt",1,"Tec"), ("bezerra.txt",None,"Bezerra"), ("tutory.txt",None,"Tutory")]:
    for nome in fonte_txt(arq, col):
        check(vistos[nome] > 0, "%s: entrada do .txt sumiu do apelidos.csv: %r" % (rot, nome))

# 4. area e LISTA, nunca coluna
for r in ar:
    check(r["area"] in ("Fiscal","Controle","Legislativo"), "area desconhecida: %r" % r["area"])
check(not any(c in ("Fiscal","Controle") for c in (ar[0].keys() if ar else [])),
      "areas.csv virou coluna por area; tem de ser uma linha por par (sigla, area)")

# 5. contador DERIVADO, nunca gravado
for r in disc:
    check(not any(k.lower().startswith(("proximo","contador","ultimo")) for k in r),
          "disciplinas.csv guarda contador; ele tem de ser DERIVADO (maior usado + 1)")

# 6. orcamento de caracteres da nomenclatura de pastas
for r in ren:
    if r["status"] != "ok": continue
    check(r["sigla"] in S, "renomear-pastas: sigla desconhecida %r" % r["sigla"])
    check(len(r["pasta_nova_sem_data"]) <= 45,
          "pasta_nova_sem_data estoura 45 (%d): %s" % (len(r["pasta_nova_sem_data"]), r["pasta_nova_sem_data"]))
    check(r["pasta_nova_sem_data"].startswith(r["sigla"] + " - "),
          "pasta fora do padrao <SIGLA> - <Disciplina>: %s" % r["pasta_nova_sem_data"])
    # Regra 9 do NOMENCLATURA.md: a data desce para o nivel da disciplina.
    # O teto do nivel e 64, repartido assim:
    #     45  <SIGLA> - <Disciplina>   (o que ESTA base produz)
    #    +13  ` (DD-MM-AAAA)`          (o download acrescenta ao renomear)
    #    + 6  ` (N-M)`                 (o download acrescenta SO se sobrar pendencia, regra 6)
    #    ---
    #     64
    # Esta base confere ate a data (58), que e o limite do que ela mesma produz. Os 6 da
    # marca de pendencia sao conferidos pelo `conferir` do download, que e quem a escreve.
    # O teto de 64 foi levantado de 58 em 22/08/2026, depois de esta verificacao mostrar que
    # `AFO - Administracao Financeira e Orcamentaria (18-08-2026)` fechava em 58 EXATOS: sem
    # a folga, a marca de pendencia da regra 6 estouraria o caminho no meio da execucao.
    check(int(r["chars_com_data"]) <= 58,
          "com a data da regra 9 estoura 58 (%s): %s" % (r["chars_com_data"], r["pasta_nova_sem_data"]))
    check(int(r["chars_com_data"]) + 6 <= 64,
          "com data + marca de pendencia (regra 6) estoura o teto de 64: %s" % r["pasta_nova_sem_data"])
for r in ren:
    if r["status"] == "pendente":
        check(r["sigla"] == "" and r["pasta_nova_sem_data"] == "",
              "linha pendente nao pode ter sigla nem nome novo: %s" % r["pasta_atual_no_disco"])

# 7. trava de vazamento: nenhum CPF em lugar nenhum
CPF = re.compile(r"\b\d{11}\b")
for arq, linhas in [("disciplinas.csv",disc),("apelidos.csv",ap),("areas.csv",ar),("renomear-pastas.csv",ren)]:
    for r in linhas:
        for v in r.values():
            check(not CPF.search(v or ""), "possivel CPF em %s: %r" % (arq, v))

# 8. toda sigla tem pelo menos um apelido e pelo menos uma area
comap = set(r["sigla"] for r in ap if r["status"] == "ok")
for s in siglas:
    check(s in comap, "sigla sem nenhum apelido: %s (ninguem acha o material dela)" % s)
    check(any(r["sigla"] == s for r in ar), "sigla sem area: %s" % s)

# 9. entrada de fonte SEM REGRA falha, nao avisa.
#    Furo apontado em 22/08/2026: cobertura foi provada uma vez, na mao. Quando a area
#    Legislativa entrar, virao nomes que as regras nunca viram, e "sem regra" tem de
#    quebrar ruidosamente em vez de virar linha sem sigla que ninguem le.
for r in ap:
    check(not (r["status"] == "" or r["status"] is None),
          "apelido sem classificacao nenhuma: %r (%s)" % (r["nome_na_fonte"], r["fonte"]))

# 10. cobertura por PAR (sigla, area), nao por sigla.
#     Sem isto, MATFIN passava: tinha material no Controle, nenhum no Fiscal, e a tabela
#     parecia completa. Falha silenciosa com aparencia de sucesso.
FONTE_DA_AREA = {"Fiscal": "Estrategia Regular Fiscal", "Controle": "Estrategia Regular Controle"}
pares_area = set((r["sigla"], r["area"]) for r in ar)
for sig, area in sorted(pares_area):
    fonte = FONTE_DA_AREA.get(area)
    if not fonte: continue
    check(any(r["sigla"] == sig and r["fonte"] == fonte and r["status"] == "ok" for r in ap),
          "%s consta na area %s mas nao tem apelido no %s: o aluno dessa area "
          "nao acha o material" % (sig, area, fonte))

# 11. O NOME DA DISCIPLINA E CONGELADO, igual a sigla.
#     Decisao do Elvis em 22/08/2026: a Tutory reconhece que o aluno ja estudou um assunto
#     comparando "nome do assunto + NOME DA DISCIPLINA" entre planos. Mudar o nome da
#     disciplina, AINDA QUE POR UM UNICO ESPACO, faz a plataforma tratar como disciplina
#     nova e o historico do aluno se perde. Nao ha desfazer depois de publicado.
#     Por isso `nome_canonico` tem o mesmo estatuto da sigla: irreversivel, nivel 3.
cong = {r["sigla"]: r["nome_canonico"] for r in ler(os.path.join(D, "nomes-congelados.csv"))}
for r in disc:
    esperado = cong.get(r["sigla"])
    check(esperado is not None,
          "sigla %s nao esta em nomes-congelados.csv: nome novo tem de ser congelado ao nascer" % r["sigla"])
    if esperado is not None:
        check(r["nome_canonico"] == esperado,
              "NOME CONGELADO ALTERADO em %s: %r -> %r. Isso quebra o historico do aluno na "
              "Tutory. Reverter, ou subir ao Elvis (nivel 3)." % (r["sigla"], esperado, r["nome_canonico"]))
    n = r["nome_canonico"]
    check(n == n.strip() and "  " not in n,
          "nome com espaco sobrando ou duplicado em %s: %r. A Tutory le como disciplina "
          "diferente." % (r["sigla"], n))

print("Base 1 — conferencia")
print("  disciplinas %d | apelidos %d | areas %d | pastas %d" % (len(disc), len(ap), len(ar), len(ren)))
c = Counter(r["status"] for r in ap)
print("  apelidos por status:", ", ".join("%s=%d" % kv for kv in sorted(c.items())))
if falhas:
    print("\n%d FALHA(S):" % len(falhas))
    for f_ in falhas: print("  x", f_)
    sys.exit(1)
print("\n  tudo passou, 11 blocos de verificacao.")
