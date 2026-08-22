# Relatório — ESP-TAXONOMIA · Base 1 (Disciplinas)

> Entregue ao Elvis em 22/08/2026. Sobrescrito a cada entrega.
> Estado de trabalho em `ESP-TAXONOMIA-ESTADO.md`; lições em `bases/01-disciplinas/APRENDIZADO.md`.

**Situação: construída, conferida, e com as três pendências resolvidas pelo Elvis em 22/08/2026.**
Último commit dos dados: ver `ESP-TAXONOMIA-ESTADO.md`.

```
21 disciplinas · 432 apelidos · 31 áreas · 34 pastas (31 prontas, 3 pendentes de execução)
conferir.py: 11 blocos, todos passando
amostragem cega da Tutory: 30/30, semente 20260822
vista: docs.google.com/spreadsheets/d/1a_F3RLdtj5lsLeNaOiD4YyasxfDRD9xnFN2NsUbH3pU
```

---

## 1 · Como eu fiz

Detalhe suficiente para outra pessoa refazer sem falar comigo. Só o passo 2 toca a rede.

**1. `disciplinas.csv`** — transcrição literal da seção **A8** de `bases/DECISOES.md`. Zero
interpretação: as 21 já estavam fechadas.

**2. `fontes/tec.txt`** — `GET /api/materias?universo=&formato=OBJETIVA`, autenticado, **1
chamada**, HTTP 200. **Armadilha:** a resposta é um **objeto**, não uma lista; o array vem dentro
(`Array.isArray(j) ? j : (j.dados || j.materias || Object.values(j).find(Array.isArray))`).
Vale `bases/05-questoes-tec/REGRAS.md`: 429 encerra o dia sem retentativa, CAPTCHA é do Elvis.

**3. Conciliação das 5 camadas** contra as 21, gerando `apelidos.csv`, **uma linha por par
(sigla, fonte, nome literal)**:

| Camada | Origem | Entradas |
|---|---|---|
| Estratégia · drive | `fontes/estrategia.txt` (nome de pasta) | 34 |
| Estratégia · plataforma | `fontes/estrategia-plataforma.txt` (nome de curso + `curso_id`) | 37 tipo 1 |
| Bezerra | `fontes/bezerra.txt` | 29 |
| Tec | `fontes/tec.txt` (nome + `id`) | 146 |
| Tutory | `fontes/tutory.txt` (legado) | 168 |

Estratégia, Bezerra e Tec foram mapeados **à mão**, um a um. A Tutory, por **regex ordenada**
(a 1ª regra que casa vence, então **a ordem importa**: `local` e `lixo` vêm antes das de
disciplina, senão `Economia Regional do Pará` viraria `ECOFIN`).

**4. Validação da regex por amostragem cega.** 30 das 168 sorteadas com `random.seed(20260822)`,
classificadas **à mão antes** de olhar o resultado da regex, e comparadas. **30/30.** A mesma
semente reproduz a mesma amostra. Isso não prova correção absoluta; dá um **teto de erro medido**
no lugar de "não sei".

**5. `areas.csv`** — a área sai de **qual Regular de fato tem o curso**, com o `curso_id` como
evidência escrita em cada linha.

**6. `conferir.py`** antes de publicar qualquer coisa. 11 blocos, sem escrever nada.

**Ambiente:** é `python` (3.12.10), não `python3`. O `/tmp` do Git Bash não é visível para o
Python nativo do Windows.

---

## 2 · Onde escolhi, e a alternativa que descartei

**O casamento é muitos-para-muitos nos DOIS sentidos.** O Tec junta o que separamos e separa o que
juntamos:

| Matéria do Tec | Vira |
|---|---|
| 69 · AFO, Direito Financeiro e Contabilidade Pública | `AFO` **e** `CONTPU` |
| 37 · Auditoria Governamental e Controle | `AUDIT` **e** `CTREXT` |
| 4 · Informática + as 9 `TI - ...` | `TECINF` (10 → 1) |

**Escolhi** duas linhas, uma por sigla. **Descartei** eleger uma "principal": `AUDIT` acharia a
matéria 37 e `CTREXT` não, e a 37 é a única matéria de `CTREXT` no Tec inteiro.

**`TECINF` ficou com as 10 matérias do Tec.** Descartei filtrar só a Informática (a mais rasa):
filtro na base 1 é invisível depois; o corte de profundidade é **coluna auditável na base 2**.

**A Tutory foi por regra, não a mão.** Aceitei o risco de a regra casar errado em silêncio, e o
mitiguei com a amostragem cega do item 1.4. Reprodutível é melhor que artesanal em 168 linhas.

**`areas.csv` deixou de nascer vazio.** O combinado literal era deixar em branco para não chutar.
Preenchi com evidência por linha, porque a lista de matrícula dos dois pacotes é evidência dura, e
**vazio não distingue "não medido" de "não existe"**. O Elvis confirmou o critério em 22/08.

---

## 3 · O que está frágil

**A classificação da Tutory por regex.** Continua o ponto mais fraco, agora com teto medido.
Quando a **área Legislativa** entrar, virão nomes que as regras nunca viram. Mitigado pelo **bloco
9** do `conferir.py`: entrada sem classificação **falha**, não avisa.

**Área como evidência de matrícula não sobrevive à Legislativa** sem um Regular Legislativo. A
estrutura aguenta (é linha, não coluna); o **método** é que não. Sem pacote, não há evidência, e a
tentação será preencher no olho.

**432 linhas ainda cabem na cabeça.** Com o edital como sexta fonte, e um edital por concurso, o
`apelidos.csv` num arquivo só fica ruim de revisar. Não otimizei: doer antes, otimizar depois.

**O orçamento de caracteres fecha exato.** `AFO - Administracao Financeira e Orcamentaria
(18-08-2026)` bate **58 de 58**, e com a marca de pendência da regra 6 bate **64 de 64**. Cabe, mas
com folga zero declarada. Conferido pelo bloco 6.

---

## 4 · Onde o combinado divergiu do que eu medi

**A seção A8 estava errada.** Dizia que o Regular Controle tem `CONTAB`, `ESTAT` e `ECOFIN`.
Conferido nos **dois** pacotes do Controle (365538 e 224364, listas de disciplina idênticas): só o
`CONTAB` existe. **Corrigido, com autorização expressa do Elvis.**

**A A8 diz que legislação local só nasce em pós-edital**, mas os cursos 220891 e 220896 estão no
Regular Fiscal. **Não corrigi**, e depois a contradição **caiu sozinha**: os dois são **genéricos**
(o 220891 diz "(Todos Estados)"), logo não são o `LTRIB-<ente>` de que a A8 fala.

**Nome de pasta é dado derivado, e esconde disciplina.** O Regular Fiscal tem **22 pastas para 25
cursos**: alguém consolidou três Reformas numa e não baixou a Discursiva. O Regular Controle casou
**12 para 12**. Não dá para confiar nem desconfiar da pasta em bloco: confere-se área por área.
Foi o que motivou a coluna `camada` (`drive` / `plataforma`).

**404 no Estratégia significa "não matriculado"**, não "não existe" (curso devolve 500 no mesmo
caso). Tratar 404 como "acabou" faria uma skill descartar material que está lá.

---

## 5 · O que ficou pendente do Elvis — e como ele resolveu

Os três subiram por serem **nível 3**: irreversíveis depois de o Cód Mestre ser publicado.

**a) Legislação Tributária sobre o Consumo (curso 336350).** Ele havia dito que era `LTRIB`;
**revisou em 22/08 e corrigiu**: quem manda é o **conteúdo**. Lei Kandir → `LTRIB` (parte geral);
LC 214/2025, LC 227/2026 e EC 132/2023 → `REFTRI`. O curso aparece **duas vezes** no
`apelidos.csv`, e a separação real sai na **base 2**, lendo os PDFs.

**b) As 8 do balde 1 do `SEM-DONA.md`.** Resolvido: **não há problema**. Elas ficam mapeadas na
fonte e **não recebem Cód Mestre**, porque o código pressupõe conteúdo teórico nosso, e sem
material no Regular ele apontaria para o vazio. Se entrarem no Regular um dia, ganham código pelo
modo `atualizar`.

**c) A pasta `Reforma Tributaria` (B69) e a ementa dos cursos 220891/220896 (B70).** Seguem em
execução: B69 é trabalho manual de separação (não se resolve sozinha no modo `atualizar`), e B70
depende de o `ESP-ACERVO` voltar à plataforma.

### A decisão nova, e é a mais pesada da rodada

**O NOME da disciplina é congelado, igual à sigla.** A Tutory reconhece que o aluno já estudou um
assunto comparando **nome do assunto + nome da disciplina**. Mudar o nome, **ainda que por um
espaço**, faz a plataforma tratar como disciplina nova e o histórico do aluno se perde.

Travado em `dados/nomes-congelados.csv` e no **bloco 11** do `conferir.py`, que falha se o nome
divergir ou ganhar espaço sobrando ou duplicado. **Testado:** espaço duplicado em `Direito
Administrativo` derruba a conferência.

Consequência: ao carregar plano novo, vai o **nosso** nome, não o legado. Os 168 nomes da Tutory
servem só para a **migração** (A28).

---

## 6 · O que eu faria diferente do que foi pedido

**Rodar a base 3 antes da base 2, mas só a puxada da árvore.** Não é adiantamento oportunista: é
**medição**. As matérias 69 e 37 juntam duas disciplinas nossas cada, e é preciso saber **quantos
outros casos existem antes de alguém dimensionar acervo por matéria**. Amarrar assunto ao Cód
Mestre continua depois da base 2, porque o tópico nasce da teoria que o aluno lê.

**Custo real: ~29 chamadas, não as ~21 do `ROTEIRO.md`.** Das 146 matérias do Tec, **29** têm
sigla nossa; `TECINF` espalha em 10 e `AUDIT` em 2, e é daí que vem a diferença.

**O impacto do Tec não é "revisar antes de coletar", é mais estreito:** o **corte** da coleta está
salvo (já é por assunto), quem contamina é o **dimensionamento** da decisão A32 e da tarefa B53.
"2.500 questões de AFO" medido na matéria 69 está inflado por questão de outra disciplina, e a
janela de anos sairia **curta demais**. **O tamanho se mede pela soma dos assuntos, nunca pela
matéria.**

**Endereçar agente pela obra, não pelo apelido.** Duas mensagens foram para a sessão errada em
22/08. "Para quem tem `<arquivo>` no disco" é verificável com um `ls`. Adotado no
`agentes/README.md`.


---
---

# Base 3 · A árvore de assuntos do Tec

> Entregue em 22/08/2026. Commit **`0d65be5`**.

```
4.805 assuntos · 30 matérias · profundidade até 6 níveis · 62 chamadas · nenhum 429
dados/assuntos.csv: materia_id, materia_nome, sigla, assunto_id, hierarquia, nivel, nome
```

## 1 · Como eu fiz

**1. Quais matérias.** Saíram do `apelidos.csv` da base 1: as que têm `fonte = Tec` e
`status = ok`. Deram **30**, não as 29 que o coordenador contou — a `LTFED` entrou na conta
quando a família da `LTRIB` nasceu, poucas horas antes.

**2. A chamada certa é `GET /api/assuntos?materia={id}`, SEM `hierarquico=true`.**

**3. Ritmo.** 500 a 800 ms entre chamadas, em lotes de 10. O lote de 30 estourou o limite de 30
segundos da ferramenta, **mas o laço continuou rodando na página** e 28 já estavam baixadas quando
eu voltei a olhar. Vale saber: o timeout é do meu lado, não do laço.

**4. Como os dados saíram da página.** O volume não cabe no contexto. O caminho que funcionou: o
navegador devolve tudo num TSV único, a ferramenta salva sozinha num arquivo quando o resultado é
grande demais, e o Python lê **esse arquivo**. O conteúdo nunca passa pelo meu contexto.

> **Armadilha:** aquele arquivo é **duplo-encodado**. É um JSON com blocos `{type, text}`, e o
> `text` é ele mesmo uma string JSON, **seguida de texto solto** (a nota de origem). `json.loads`
> quebra com `Extra data`. O que funciona é `JSONDecoder().raw_decode()` em cada bloco. Perdi duas
> tentativas nisso.

**5. Conferência.** Contei as linhas do arquivo (4.805) contra o total que o próprio JS reportou
(4.805) e contra os ids únicos (4.805). Três contagens de origens diferentes batendo.

## 2 · Onde escolhi, e o que descartei

**Puxei só as 30 nossas, não as 146 do catálogo.** As 116 restantes são de outras carreiras. Custaria
116 chamadas para guardar o que nunca vai ser consultado.

**Não amarrei assunto ao Cód Mestre**, embora fosse a coisa mais óbvia a fazer com a árvore na mão.
O tópico nasce da teoria que o aluno lê; o assunto do Tec é apelido que se pendura nele. Amarrar
antes da base 2 inverteria o desenho, e o vínculo teria de ser refeito.

**Guardei a hierarquia como está (`"10.05.02"`), sem montar árvore aninhada.** A string ordena, agrupa
por prefixo e sobrevive a CSV. Aninhar exigiria JSON, que o git não mostra linha a linha.

## 3 · O que ficou frágil

**A varredura de ramos cruzados é por palavra-chave**, com uma lista de termos que eu escrevi. Ela
achou 4 casos. **Ela não prova que não há um quinto** — prova que não há nenhum cujo nome de ramo
contenha os termos que eu lembrei de listar. É o mesmo tipo de furo da regex da Tutory, e desta vez
**eu não fiz amostragem cega**, porque não há um "gabarito à mão" para comparar: eu teria de julgar
os 499 ramos, que é o trabalho inteiro. Fica declarado.

**O `assuntos.csv` tem 4.805 linhas e nenhum `conferir.py` próprio.** A base 1 tem 11 blocos; a base
3 tem zero. Enquanto o arquivo é só matéria-prima, o risco é baixo; quando ele receber o vínculo com
o Cód Mestre, precisa de conferência antes.

## 4 · Onde o combinado divergiu do medido

**O `ROTEIRO.md` da base 3 estava errado em dois números**, e os dois foram corrigidos:

| | Dizia | É |
|---|---|---|
| assuntos de Direito Administrativo | 2.755 | **276** |
| chamadas | ~21 | **30** |

**E `hierarquico=true` devolve MENOS, não mais:** 121 contra 276 em Direito Administrativo. Ele
filtra. O nome do parâmetro promete o contrário.

**A hierarquia não vem aninhada.** É lista plana com o caminho no campo `hierarquia`. Quem procurar
`filhos`, `children` ou `assuntos` conta só o nível 1 e conclui que a árvore é rasa.

## 5 · Pendente do Elvis

**Nada.** A árvore é matéria-prima; o que falta depende da base 2, não dele.

## 6 · O que eu faria diferente

**As 30 chamadas com o parâmetro errado eu não teria evitado, e é o ponto principal.** Eu usei
`hierarquico=true` porque **era o que o `ROTEIRO.md` mandava**, e o nome do parâmetro é convincente.
O que salvou não foi desconfiança: foi o **número do documento não bater com o meu**. Ele dizia 2.755
para DADM, eu contei 121, e a distância era grande demais para arredondamento.

Então a lição não é "leia a doc da API antes". É: **um número errado no documento pagou as 30
chamadas que ele mesmo causou.** Se o roteiro não tivesse número nenhum, eu teria gravado 121
assuntos por matéria, com profundidade 1, e seguido em frente — e a base 3 nasceria com **um quarto**
da taxonomia, sem ninguém perceber, porque nada mais teria com o que comparar.

**A regra que eu tiro daí:** todo roteiro deve carregar **uma contagem esperada**, mesmo aproximada,
mesmo errada. Número errado se corrige na primeira medição; número ausente não avisa nunca. É a
mesma família de "teste que afirma um invariante de cada linha", só que aplicada a documento.

**E eu deveria ter reportado ao coordenador ao terminar**, não só ao Elvis. Ver a nota abaixo.
