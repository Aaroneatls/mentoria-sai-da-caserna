---
name: project_nome_disciplina_congelado_tutory
description: "O nome da disciplina é congelado como a sigla; a Tutory quebra o histórico do aluno se ele mudar, ainda que por um espaço"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9ea9a90c-b4ff-422b-950a-e3fdebe622ed
  modified: 2026-08-22T18:53:23.790Z
---

Decidido pelo Elvis em 22/08/2026, ao fechar a base 1.

**O nome da disciplina tem o mesmo estatuto da sigla: irreversível depois de publicado.**
Fixamos `Direito Administrativo` e `DADM`, e nenhum dos dois muda mais.

**Por quê:** a Tutory reconhece que o aluno já estudou um assunto comparando
**nome do assunto + NOME DA DISCIPLINA** entre planos. Se o nome da disciplina mudar,
ainda que por **um único espaço**, a plataforma trata como disciplina nova e o histórico
do aluno se perde. Não há desfazer.

**Consequência prática:** ao carregar plano novo na Tutory, a disciplina vai com **o nosso
nome**, não com o nome legado. Os 168 nomes legados da Tutory (`Direito Administrativo
(Fiscal/ Controle)`, `Direito Tribubário`, etc) servem só como **conhecimento para a
migração**, nunca como alvo a imitar. Depois se faz a passada de troca.

Vale também para o caso de uma disciplina nossa cobrir várias matérias da fonte:
`Tecnologia da Informação` é **um nome só**, mesmo que o Estratégia e o Tec fatiem em
muitas matérias. O fatiamento da fonte vira apelido, nunca nome novo.

**Onde está travado:** `bases/01-disciplinas/dados/nomes-congelados.csv` guarda o par
(sigla, nome) com a data e o motivo, e o bloco 11 do `bases/01-disciplinas/conferir.py`
falha se o nome divergir ou se ganhar espaço sobrando/duplicado.

Ver [[project_taxonomia_codigo_mestre_e_atualizacao]] e
[[feedback_codigo_identifica_conteudo_nao_posicao]].
