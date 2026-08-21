---
name: project-arquitetura-bases-e-link-imutavel
description: "Arquitetura das bases: uma planilha por disciplina + uma global com 4 registros. O link do caderno no Tec é IMUTÁVEL — atualiza-se o conteúdo, nunca o link"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T20:03:09.807Z
---

Decidido com Elvis em 2026-08-19.

## 1. O link do caderno é imutável (regra dura)

O link do caderno no Tec **vai para a plataforma Tutory** e chega ao aluno. A partir daí ele
deixa de ser nosso: é contrato com o mundo externo.

- **Atualizar no lugar, sempre.** Trocar questão, acrescentar, remover — tudo pode.
- **Nunca recriar o caderno.** Recriar gera id novo, logo link novo, e quebra o que já está
  distribuído.
- Elvis foi explícito: mudar a composição do caderno **não é problema nenhum**; mudar o link
  é o único problema real.
- **Versionamento foi descartado** por isso — não se cria "v2" de caderno.

### Onde a regra tem limite (Elvis, 2026-08-19)

O link é imutável enquanto a **identidade** do caderno sobrevive. Se o tópico/ponto de origem
deixar de existir como conceito, o caderno também deixa — e aí criar caderno novo, com link
novo, **não é problema**: Elvis recarrega o link na Tutory.

O ciclo de vida do caderno segue os quatro casos da regra de código
(ver [[feedback_codigo_identifica_conteudo_nao_posicao]]):

| O que aconteceu com o tópico/ponto | O que acontece com o caderno |
|---|---|
| **Renomeação** | mesmo caderno, mesmo link, só muda o nome |
| **Composição muda** (questão entra/sai) | mesmo caderno, mesmo link — caso mais comum |
| **Fusão** de dois tópicos | um caderno sobrevive e absorve; o outro é **aposentado** |
| **Desdobramento** em dois | o original mantém o link; o recorte novo nasce como caderno novo |
| **Extinção** do tópico | caderno **aposentado** |

**Entregável obrigatório:** sempre que a rotina aposentar ou criar caderno, ela tem que
produzir uma **lista de troca de links** — o que sai, o que entra e onde estava — senão Elvis
não tem como saber o que atualizar na Tutory no meio de centenas de cadernos. O status
`aposentado` fica no Registro Mestre, com a coluna de "substituído por".

Consequência técnica: a manutenção usa exclusivamente
`DELETE /cadernos/{id}/questoes/remover-questao-id/{q}` e
`POST /cadernos/{id}/questoes/adicionar-questoes-por-codigo` (ver `_contexto/tecconcursos.md`).
E **nunca** o "atualizar" nativo do Tec, que re-executa o filtro original e desfaz a curadoria.

## 2. Uma planilha por disciplina, mais uma global

**Escala real (Elvis, 2026-08-19):** ~100 a 200 cadernos **por disciplina**; os ~10 mil são o
total acumulado na conta do Tec, somando todas as disciplinas, níveis, áreas e bancas.

**Planilha por disciplina** (ex.: "Base DADM"): Taxonomia · Pontos · Questões Fichadas ·
Questão x Ponto · Composição dos Cadernos. Fica na casa dos poucos milhares de linhas — leve.

**Planilha global** (uma só), com quatro registros:
1. **Registro Mestre de Cadernos** — código nosso, id no Tec, disciplina, nível, escopo,
   acervo, banca, área, janela, data de criação, data da última verificação, status, link.
2. **Registro de Concursos e Editais** — cada edital processado e quais cadernos o atendem.
3. **Fila de Pendências** — ponto único onde aparece tudo que precisa de decisão humana
   (questão desatualizada, ponto sem cobertura, caderno abaixo do mínimo, código descontinuado).
4. **Registro de Execuções** — cada rodada de skill: quando, escopo, o que mudou. É o que
   permite auditar e desfazer.

Mais a aba de **Siglas de Disciplinas** (ver [[project_taxonomia_codigo_mestre_e_atualizacao]]).

## 3. Código do caderno

`<SIGLA>.<NÍVEL>.<NNN>` — ex.: `DADM.N1.001`. Sufixo `-I` quando o acervo é de inéditas
(`DADM.N1.001-I`). **O id do Tec é coluna, não identidade** — mesma lógica do Cód Mestre
(ver [[feedback_codigo_identifica_conteudo_nao_posicao]]).

## 4. Questões inéditas: trilha separada

Verificado em 2026-08-19: Direito Administrativo tem **3.547 questões inéditas** (1.056 na área
de Controle). Elas **não têm banca de concurso real**, então qualquer filtro com `BANCA` as
exclui — foi o que manteve os cadernos do teste limpos, por acidente e não por desenho.

- Identificação: campo `questaoAdaptadaOuInedita` na questão; filtros
  `SOMENTE_ADAPTADAS_INEDITAS` / `REMOVER_ADAPTADAS_INEDITAS`.
- **Cuidado:** o campo `assinanteAvancado` **não** é flag da questão — reflete o plano de quem
  está logado (veio `true` em todas). Não serve pra inferir exigência de plano.
- **Nunca misturar** real e inédita no mesmo caderno: um item inédito inutiliza o caderno
  inteiro para o aluno de plano padrão (premissa do Elvis, não verificada por API).
- Incluir `REMOVER_ADAPTADAS_INEDITAS` nos filtros fixos do caderno de concurso real, pra a
  proteção ser deliberada.

## 5. Portabilidade entre contas do Tec e ritmo de requisição

Levantado por Elvis em 2026-08-19: risco de a conta ser restringida por volume de requisições,
e necessidade de continuar o trabalho em outra conta.

**A base já é portátil por construção.** Tudo que custa caro é global do Tec e igual em
qualquer login: número da questão, id de assunto, matéria, banca e código de área. O
fichamento inteiro não tem nenhuma referência dependente de conta.

**O que é da conta:** id e link de cada caderno, id da pasta de destino, histórico de
desempenho. Só isso se perde.

**Consequência:** trocar de conta **não exige refichar nada**. É replay — pega a composição da
planilha e reinjeta pelos códigos.

**Custo medido (2026-08-19):**
- Criar + injetar + conferir um caderno: **~3 requisições** (a injeção aceita a lista inteira
  de uma vez). 200 cadernos ≈ 600 requisições, questão de minutos.
- Fichar: **2 requisições por questão** (detalhe + comentário). ~2.200 para as 1.111 do DADM.
  **Pago uma vez só**, não se repete na troca de conta.

**Ajustes obrigatórios no desenho dos registros:**
- **Coluna "Conta"** no Registro Mestre de Cadernos — com duas contas, é o que diz onde cada
  link vive.
- **Pasta de destino vira parâmetro, não constante.** O `pastaDestino=7460777` é da conta atual.
- **Ponto de retomada** gravado na base: rodada interrompida retoma de onde parou, em vez de
  recomeçar. Vale para bloqueio e para queda de conexão.

**Ritmo (pra não chegar no bloqueio):**
- **Sequencial, nunca em paralelo**, com intervalo e alguma variação. ~350-600 ms em lote
  pequeno; **~1 s** em lote grande.
- **Usar o que aceita lote** — `adicionar-questoes-por-codigo` recebe a lista toda.
- **Nunca reler o que já está fichado.** A planilha é o cache.
- **Quebrar lote grande em sessões ao longo de dias**, em vez de 40 minutos de rajada.
- **Parar no primeiro sinal** (429, 403, ou HTML no lugar de JSON) e avisar. Nunca insistir em
  laço — mesma regra das skills de download.

**Ressalva registrada:** base portátil serve pra **não perder meses de fichamento**, não pra
contornar bloqueio. Se um bloqueio ocorrer, o primeiro passo é falar com o suporte do Tec.

## 6. A atualização tem que ser incremental

Com milhares de cadernos, varrer todos a cada rodada não termina. A rotina parte **do que
mudou**: questões que viraram desatualizadas → pontos que elas tocam → cadernos que usam esses
pontos. Só esses são abertos. Ver [[project_banco_fichamento_questoes]].
