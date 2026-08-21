---
name: project_censo_por_filtro_x_percentual
description: censo por filtro e' atalho aceito so' para a amostra de agora; a skill final tem de pegar o percentual real de acerto questao a questao
metadata:
  type: project
---

O Tec deixa filtrar por **dificuldade** na mesma rota que devolve lista de ids
(`POST /api/questoes/filtros` com `filtros[n].tipo=FILTRO_QUESTAO` e
`id=DIFICULDADE_MEDIA`, etc). Uma chamada devolve todas as questoes daquela faixa, em vez de
perguntar questao a questao. Vale igual para `BANCA` e `ANO`. **A lista vem paginada de 100 em
100**, entao assunto grande precisa de varias chamadas; conferir sempre com
`POST /api/questoes/contagem/filtros`, que devolve o total.

**Decisao (Elvis, 21/08/2026): usar o censo AGORA, para ter a amostra e destravar a analise.
Mas registrar que o objetivo final e o percentual de verdade.** A skill que for criada tem de
pegar o indice de acerto questao a questao, porque o rotulo de dificuldade e uma faixa e a
gente vai precisar do numero fino para calibrar risco. O censo e atalho de amostra, nao o
desenho definitivo.

**O que o censo NAO da:** o percentual exato de acerto (`desempenhoGeral.acertos/erros`), o
orgao e o cargo. O que ele da: assunto, banca, ano, ordem de recencia (`ordenacao=RECENTES`),
tipo e as marcas de anulada, desatualizada e inedita.

**Ponto que muda a conta:** o `/deslogado` **ja traz o enunciado e as alternativas**. Como o
fichamento precisa ler o enunciado de todas as 5.463 de qualquer jeito, essa chamada acontece
com ou sem censo. O censo economiza a segunda chamada (`/desempenho`), nao a primeira. Coletar
sem guardar o texto obrigaria a visitar as 5.463 outra vez. Ver [[project_fichamento_duas_passadas]].

**Onde o texto fica:** IndexedDB `tec_fichamento`, store `q`, porque localStorage estoura em
~5 MB e os enunciados passam disso. A quota medida no navegador foi de 18 GB. O `base` continua
em localStorage, que e pequeno. A linha do `base` foi para 16 campos, e o 16o marca que o texto
daquela questao ja esta no IndexedDB.
