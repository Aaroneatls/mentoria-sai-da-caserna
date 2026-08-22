# Decisões fechadas

> **Leia isto antes de começar qualquer base.** Cada decisão aqui já foi discutida e fechada com
> o Elvis. Não reabrir sem motivo novo. Este arquivo existe para que a sessão de cada skill
> comece sabendo o que já está resolvido.

---

## Discursiva nao entra como disciplina · fechado em 22/08/2026

O curso **"Concursos da Area Fiscal - Curso Basico de Discursiva (Sem Correcao)"**
(id 268932) esta dentro do pacote Regular Fiscal (220865) e vem com
`tipo_curso_id = 1`. Pela regra "o que nao esta no Curso Regular nao entra", ele
seria candidato a disciplina.

**Decisao do Elvis: NAO entra como disciplina.** E treino de producao de texto, e o
modelo do projeto (topico -> ponto -> questao objetiva -> caderno do Tec) nao se
aplica a ele.

Existe ainda um segundo produto no catalogo, **"Curso Basico de Correcao Analitica
de Discursiva (3 Correcoes por aluno)"** (id 268941), que **nao** esta dentro do
pacote 220865 — e avulso. Sao dois produtos diferentes, um com correcao e outro
sem, e nenhum dos dois vira disciplina.

**Consequencia:** o Regular Fiscal tem 25 cursos de tipo 1, dos quais a Discursiva
sai por esta decisao e o "Sistema de Questoes 1 Ano" sai por nao ser curso. Reforca
a regra de que **`tipo_curso_id = 1` nao garante disciplina**.

---

## Marca d'agua do Estrategia: CPF e nome no texto extraido · fechado em 22/08/2026

> **Trava de vazamento. Roda na EXTRACAO, antes de qualquer consumo do texto.**
> Nao e otimizacao de hash: e impedir que dado pessoal chegue no aluno.

Todo PDF do Estrategia vem **marcado por download**, e a marca **esta na camada de
texto**, nao so na imagem. Em praticamente toda pagina do livro, do resumo e do
mapa mental aparece:

```
02055447114 - Gisilene Tatianne Santos de Lima
```

CPF e nome completo de pessoa real — a conta compartilhada da familia do Elvis.

**O risco:** esse texto e extraido junto com a teoria. Se passar batido para dentro
de ancora de prosa, de citacao no BIZURITO, de resumo gerado ou de qualquer coisa
distribuida, o material publicado em escala carrega o CPF de uma pessoa real.

**A regra:** na extracao de texto de qualquer PDF do Estrategia, **descartar as
linhas que casem com `\d{11}\s*-\s*<Nome>`** (e, em geral, o que variar por conta
ou por download) **antes** de usar o texto para qualquer fim — hash, ancora,
citacao, fichamento, geracao de material.

**Efeito colateral bom — o `hash_teoria` continua valendo.** Medido em 22/08/2026:
4 downloads do mesmo arquivo geraram 4 hashes de ARQUIVO diferentes, mas o texto
extraido foi identico nos quatro (4.598 caracteres, mesmo hash), sem normalizacao.
A marca nao quebrou o hash porque e **constante para a mesma conta**. O problema
aparece **entre contas diferentes** (coleta x producao): mesmo conteudo, hash
diferente, e a falha e **silenciosa** — o sistema deixa de reconhecer que dois
cursos tem a mesma teoria e o aluno estuda duas vezes a mesma coisa.

Com a normalizacao, o `hash_teoria` fica independente de conta e segue sendo a peca
que liga teoria compartilhada ao mesmo Cod Mestre.

**Nao confundir os dois hashes:**

| | |
|---|---|
| hash do ARQUIVO (bytes) | **inutil** — muda a cada download pela marca. Identidade = nome do arquivo no CDN |
| `hash_teoria` (texto extraido, normalizado) | **valido** — e o que detecta repaginacao/reescrita |

## Capa, indice e contracapa do livro de teoria · medido em 22/08/2026

Padrao rigido, valido em 100% dos PDFs abertos no piloto (15 aulas, simplificado e
original):

| Pagina | Conteudo |
|---|---|
| p1 | capa (titulo da aula, curso, autor, data) |
| p2 | indice (secoes numeradas + pagina) |
| p3 | inicio da teoria |
| ultima | em branco (contracapa, so imagem) |

**O alvo de ~10 paginas de bloco desconta 2 paginas na frente e 1 no fim.** Um PDF
de 84 paginas tem 81 de conteudo. Sem o desconto, o bloco de abertura de cada aula
nasce com 2 paginas a menos de teoria do que parece — e e justamente o mais denso.

O mesmo vale para o resumo compilado do apoio: p1 e apresentacao generica
("Queridos alunos!!") e p2 e folha de rosto. Por isso a tabela de apoio tem
`paginas` e `paginas_conteudo` separados: a minutagem do plano usa 5 min/pagina, e
contar bruto cobraria 10 minutos de nada em cada resumo.

---

## Apoio do Estratégia: resumo e mapa mental · fechado em 22/08/2026

### Onde eles ficam

**Não são da aula: são de cada vídeo dentro dela.** No objeto do vídeo
(`/api/aluno/aula/{id}` → `videos[]`) existem `resumo`, `slide` e `mapa_mental`,
preenchidos quando existem e `null` quando não. Rotas:
`/api/video/{videoId}/download/{resumo|mapa_mental|slideshow}`. A tela mostra o
botão **do vídeo aberto** — por isso parece haver um só por aula.

Medido no piloto de Direito Constitucional (Regular Fiscal, curso 220880):
22 aulas, 198 vídeos, **12 resumos e 20 mapas mentais distintos**, em 14 aulas.
7 aulas têm exatamente 1 resumo, 2 têm mais de 1, 13 não têm nenhum. 28 MB.

### Prioridade

1. **Aba Resumos / Mapa Mental** (arquivo já separado) — o aluno só clica e baixa.
2. **Seção de resumo dentro do livro** — e só vale se **o próprio livro** rotular
   aquilo como resumo. Trecho de teoria escolhido por nós **não** é resumo.
   Simplificado primeiro; original só onde não houver simplificado.

**Resumo e mapa mental não têm hierarquia entre si**: se houver os dois, indicar
os dois. Se o mesmo conteúdo existir nos dois lugares, comparar e ficar com o
**mais completo**.

Na ordem geral do plano, o **resumo do Bruno Bezerra é o preferencial**; o
Estratégia é a alternativa.

### O apoio segue o CURSO que foi indicado ao aluno

A indicação inclui o caminho ("Aula 00 › vídeo 18 › aba Resumo"), e esse caminho
só existe no curso que o aluno tem em mãos. Portanto:

- bloco veio do **curso específico (pós-edital)** → o resumo tem de estar **nele**;
- bloco veio de aula aproveitada do **Curso Regular** → o resumo tem de estar **no Regular**;
- **não estando no curso indicado, não indica** — mesmo que exista no outro.

A tabela de apoio guarda o `curso ID` de origem, e a correlação só usa linhas do
mesmo curso do bloco entregue.

**A trava vale só para o Estratégia.** O resumo do **Bruno Bezerra é outra base, em
outra plataforma, e o aluno já tem o material salvo com ele** — então pode ser
indicado **independentemente do curso** de onde veio o bloco. Indicar outro curso
do Estratégia mandaria o aluno caçar um curso que ele talvez nem tenha; com o
Bezerra esse problema não existe.

### Deduplicação e descarte

- **Deduplicar pelo nome do arquivo no CDN, nunca por hash.** O PDF é marcado por
  download: o mesmo arquivo baixado 4 vezes dá 4 hashes diferentes (tamanho varia
  ~100 bytes). Conferir com páginas + primeira linha do texto.
- **Arquivo repetido em vários vídeos: baixar uma vez, indicar uma vez.** No
  piloto, um resumo servia aos vídeos 1, 2, 8 e 13 da mesma aula.
- **Arquivo sem conteúdo (só capa) é descartado.** Caso real: `apznza-2.pdf`,
  1 página, só "MAPAS MENTAIS – Direito Constitucional / Material compilado".
- **Registrar o que foi conferido**: na atualização do curso, repassar o apoio
  para ver o que mudou.

### Identidade x caminho

Cada arquivo carrega duas informações distintas:

| | |
|---|---|
| **Identidade** | do que trata + **páginas**, igual ao Bezerra (`arquivo + pág. inicial-final`) |
| **Caminho** | onde o aluno clica: `Aula NN › vídeo N › aba Resumo` |

Os arquivos são indexáveis por página: o resumo compilado traz folha de rosto com
o tema na p. 2 (a p. 1 é apresentação genérica), e o mapa mental grande traz o
subtópico **no cabeçalho de cada página**.

**Dois tipos de resumo:** o **compilado** abre com "APRESENTAÇÃO DO MATERIAL —
Queridos alunos!!" e cobre um tema inteiro (4 a 12 páginas); o **pontual** vai
direto ao assunto em ~2 páginas. Mapa mental varia de 1 a 55 páginas.

### Organização em pasta

**Uma pasta por disciplina** (`Apoio - Resumos e Mapas Mentais`), sem subpasta por
aula: o mesmo arquivo serve vários vídeos e às vezes aulas diferentes, e a aula é
circunstância, não identidade. A aula/vídeo é **coluna na planilha**.

### Limitação que define a fase

A API **não diz quais páginas do livro o vídeo cobre**. A ligação apoio → bloco /
Cód Mestre é por **assunto** (título do vídeo), nunca por página — e acontece na
**fase de granularidade**, não na de download. A **coleta** fica na fase de
download, que já percorre as aulas autenticada.

**O apoio nunca é fonte da taxonomia.** Não se lê resumo nem mapa mental para
definir tópico, nome mestre ou divisão de bloco: a base é o livro simplificado
(original só onde não houver simplificado). O apoio só pendura indicação num
tópico que já existe.

### Texto para o aluno

Curto e com ícone servindo de rótulo (a Tutory tem limite de caracteres, ainda a
confirmar — premissa de ~300):

```
📄 Resumo Bezerra: Dir. Constitucional, PDF 03, p. 12-18
🧠 Estratégia: Aula 00 › vídeo 18 › aba Resumo (p. 2-3)
⚠️ Sem resumo para este tópico
```

O número do vídeo é obrigatório: sem ele o aluno abre a aula, não acha botão de
resumo e conclui que não existe.

---

## A14 — Cód Mestre, ordem e o que vai na Tutory · fechado em 21/08/2026

### O código

| | |
|---|---|
| Formato | `SIGLA-NNNN`, quatro dígitos |
| Curso Regular | `0001` a `4999` |
| Fronteira | **`5000` nunca existe** |
| Nasce em pós-edital | `5001` em diante |
| Origem do tópico | **coluna**, nunca prefixo no código |

**Por que sem prefixo de edital:** o código identifica **conteúdo**. O mesmo tópico pode aparecer
em vários concursos; com prefixo (`DADM-TCDF-001`) o mesmo conteúdo ganharia um código por
concurso, que é o oposto do que o eixo existe para fazer.

### A ordem

**A ordem pertence ao PLANO, não ao tópico.** O mesmo tópico é o 18º no Regular, o 22º no TCDF e
o 7º num plano filtrado por Curva A.

| Tabela | Guarda |
|---|---|
| `topico` | Cód Mestre, nome, disciplina — a identidade |
| `plano` | "Regular Controle", "TCDF 2026 Etapa 1", "Curva A Fiscal" |
| `plano_topico` | plano + Cód Mestre + ordem |

**Guardar como ÂNCORA, não como número:** o tópico de pós-edital registra "vem depois de
`DADM-0017`". A sequência final é calculada ao gerar o plano. Assim sobrevive a reordenação do
curso e resolve a Curva ABC sozinha, entregando sequência contígua mesmo quando o filtro pula
tópicos.

**Na Tutory:** número **inteiro**, **por disciplina**, de 1 a 999, e **buraco é permitido** (ela
já usa: 1 a 11 e depois 101). Renumerar não dá problema — confirmado pelo Elvis. Usar **passo
10** para inserir no meio sem mexer no resto.

**Ordem por relevância** (reta final) é outro critério do mesmo plano, e **precisa respeitar
pré-requisito**: peso alto não pode colocar um tópico antes da base dele.

### Pré-requisito

Coluna `depende de`, preenchida **durante o mapeamento**, por duas fontes baratas:

1. a ordem do próprio curso
2. as **referências cruzadas no texto** do PDF ("conforme estudamos na aula anterior")

**O padrão é `livre`.** Só marcar dependência com evidência: marcar sem evidência acorrenta a
disciplina numa fila e mata a ordenação por peso.

### Bloco × Tópico: muitos para muitos

`Tópico` é conteúdo; `bloco` é um trecho de páginas **de um curso específico**. A ligação é uma
tabela de pares, porque um curso pode juntar o que o outro separa (caso clássico: TI, com "Banco
de Dados e NoSQL" numa aula só em um curso e em duas noutro).

**Montar a tabela desde já**, mesmo com 95% das linhas 1 para 1. Refinar o grão só onde a
comparação entre cursos mostrar divergência. Com o alvo de ~10 páginas por bloco, a divergência
fica rara.

**O que torna a quebra segura:** as questões estão penduradas no **ponto**, que é mais fino que o
tópico. Quebrar um tópico em dois é redistribuir pontos, não reclassificar questões.

### O que vai na Tutory — opção C

| Campo | Conteúdo | Muda? |
|---|---|---|
| Disciplina | `Direito Administrativo` | **nunca** |
| Assunto | `DADM-0018` | **nunca** |
| Referência | nome do tópico + `INICIE EM` / `TERMINE EM` | sim |
| Dica | orientação e links | sim |
| Caderno | link do caderno no TecConcursos | sim |

**Motivo:** a Tutory identifica que o aluno já estudou comparando **nome do assunto + matéria**
entre planos. Hoje o nome carrega o concurso (`AFO - TCU (PRÉ-EDITAL) 2026 (AUDCEX)_1`), então
nenhum nome se repete e **esse recurso está desligado na prática**. Com o código, passa a
funcionar.

**Plano reserva:** se o campo Referência não for alimentável pela planilha que abastece a Tutory,
cai para a opção B (`DADM-0018 - Nome do Tópico` no assunto), assumindo que o nome congela.

---

## Pendências que nasceram destas decisões

| | O que fazer | Quando |
|---|---|---|
| Migração de nomes | Hoje a disciplina é `Direito Administrativo (Fiscal/ Controle)`. Vai virar `Direito Administrativo`. Precisa de plano de migração para não quebrar o histórico dos alunos. | antes do primeiro plano novo |
| Planilha da Tutory | Ela é alimentada por planilha. Mapear as colunas, e descobrir se `Referência` é alimentável. | na skill da Tutory |
| Página de orientação | Hoje é uma planilha publicada, feia e compartilhada entre cursos. Proposta: **uma página por disciplina com âncora por tópico** (`.../direito-administrativo#DADM-0018`), o que dá 25 páginas em vez de 2.300. Falta decidir hospedagem. | depois |
| Técnica de Estudos | Aparece na página do aluno ("Metodologia Completa") e não está no modelo. É atributo do plano ou do tópico? | depois |

---

## A8 — Disciplinas e siglas · fechado em 21/08/2026

**21 disciplinas**, consolidadas dos Cursos Regulares Fiscal e Controle. Sigla de **4 a 6
letras**, com `AFO` como única exceção de 3, por ser o nome consagrado.

| # | Disciplina | Sigla |
|---|---|---|
| 1 | Administração Financeira e Orçamentária | `AFO` |
| 2 | Administração Pública | `ADMPUB` |
| 3 | Auditoria | `AUDIT` |
| 4 | Contabilidade de Custos | `CUSTOS` |
| 5 | Contabilidade Geral e Avançada | `CONTAB` |
| 6 | Contabilidade Pública | `CONTPU` |
| 7 | Controle Externo | `CTREXT` |
| 8 | Direito Administrativo | `DADM` |
| 9 | Direito Civil | `DCIVIL` |
| 10 | Direito Constitucional | `DCONST` |
| 11 | Direito Empresarial | `DEMPRE` |
| 12 | Direito Penal | `DPENAL` |
| 13 | Direito Tributário | `DTRIB` |
| 14 | Economia e Finanças Públicas | `ECOFIN` |
| 15 | Estatística | `ESTAT` |
| 16 | Legislação Tributária (parte geral) | `LTRIB` |
| 17 | Matemática Financeira | `MATFIN` |
| 18 | Português | `PORT` |
| 19 | Raciocínio Lógico | `RACLOG` |
| 20 | Reforma Tributária | `REFTRI` |
| 21 | Tecnologia da Informação | `TECINF` |

**A coluna de área fica em aberto de propósito.** As pastas dos cursos e os ciclos de estudo
divergem em alguns pontos (Matemática Financeira, por exemplo, aparece junto do Raciocínio Lógico
na pasta do Fiscal e separada no ciclo). Isso se resolve ao abrir os PDFs; chutar agora criaria
dado errado que ninguém iria conferir depois.

### Regra de escopo: o que não está no Curso Regular não entra

Decidido em 21/08/2026, no caso do **Direito Processual Civil**: ele aparecia no ciclo de estudo
mas não existe em nenhum dos dois Cursos Regulares, então **fica de fora**. Veio de outro curso.

Se uma disciplina aparecer numa lista e não no Curso Regular, é caso a caso, não entrada
automática.

### As fusões, e por quê

| Virou | O que absorveu | Motivo |
|---|---|---|
| `AUDIT` | Auditoria Governamental + Auditoria | metade do conteúdo é comum às duas áreas |
| `TECINF` | Informática + Análise de Informações + Tecnologia da Informação | os editais usam nomes diferentes para a mesma coisa |
| `CONTAB` | as duas versões de Contabilidade Geral e Avançada | mesma matéria, professores diferentes |

**A regra por trás:** a lista de disciplinas é **a nossa taxonomia**, não a dos editais. Criar uma
disciplina por nome que edital usa reproduz a bagunça das 170 entradas da Tutory que este
projeto existe para consertar.

**O que é específico de uma área aparece no NOME DO TÓPICO**, não no da disciplina:

```
AUDIT-0034   Auditoria Governamental: Achados e Evidências
AUDIT-0051   Auditoria Fiscal: Malha Fina e Cruzamento
```

### As três exatas ficam separadas

`RACLOG`, `MATFIN` e `ESTAT` são disciplinas distintas, **mesmo que cursos, bancas e o próprio
Tec as misturem**. A banca anuncia "Raciocínio Lógico" e cobra Estatística.

**O tópico manda, o rótulo não.** Questão de distribuição normal é `ESTAT`, esteja ela onde
estiver. Como o fichamento é ponto a ponto, dá para **medir** quantas questões rotuladas como RL
são de fato de Estatística, em vez de achar.

### Coluna de profundidade

Em `TECINF` (e onde mais fizer sentido), cada tópico carrega `Noções` ou `Aprofundado`. Edital
que pede "Noções de Informática" puxa só os primeiros; o que pede "Tecnologia da Informação"
puxa tudo. **Sem duplicar tópico.**

### Reforma Tributária sai de dentro de Direito Tributário

`REFTRI` passa a ser **disciplina própria**, embora hoje o conteúdo esteja **dentro** de
`DTRIB` no material. Duas consequências, decididas em 21/08/2026:

1. **Quem manda é o conteúdo, não onde o professor guardou.** Bloco da aula de Direito
   Tributário que trata da reforma recebe código `REFTRI`, com a origem registrada
   ("veio da aula X de Direito Tributário"). Sem isso, o mesmo conteúdo ganharia um código em
   cada disciplina, que é o oposto do que o eixo existe para fazer.
2. **Entra no plano de migração da Tutory** (ver pendência A28): aluno que já estudou a reforma
   dentro de Direito Tributário tem o histórico lá, e a mudança de disciplina faria a plataforma
   tratar como assunto novo.

### A família tributária: quatro disciplinas, não uma

Corrigido em 21/08/2026 depois de o Elvis explicar. A primeira versão deste registro colocava a
Lei Kandir dentro de `DTRIB`, e estava **errada**.

| Disciplina | O que é | Quando existe |
|---|---|---|
| `DTRIB` | Direito Tributário | sempre |
| `REFTRI` | Reforma Tributária | sempre (hoje o conteúdo mora dentro de `DTRIB` no material) |
| `LTRIB` | **Legislação Tributária — parte geral**, comum a todos os fiscos, com a **Lei Kandir** | sempre |
| `LTRIB-<ente>` | legislação do estado ou do município | **só no pós-edital** |

**A parte geral é permanente e entra no escopo.** A parte local nasce quando o edital sai, e é
por isso que a skill precisa do modo `atualizar`: essas disciplinas aparecem no meio do caminho.

**Ao mapear, procurar mais conteúdo comum.** A Lei Kandir é o caso conhecido; pode haver outros
pedaços de legislação que são gerais e estão arquivados junto do que é local.

Vale aqui o mesmo princípio da Reforma: **o conteúdo decide o código, não onde o professor
guardou**. Norma geral que cai em prova nacional não pode ficar de fora por estar numa pasta
estadual.

### Mapear tudo que o Curso Regular tem, mesmo fora do ciclo atual

O ciclo de estudo em uso não cobre todas as matérias do Curso Regular, e há matérias que o Elvis
ainda não lançou na plataforma. **Mapeia mesmo assim**: o ciclo muda, o mapeamento é reaproveitado,
e refazer depois custa mais do que fazer junto.

**CORRIGIDO em 22/08/2026.** A versão anterior desta linha afirmava que `CONTAB`, `ESTAT` e
`ECOFIN` estavam no Curso Regular de Controle. **Só `CONTAB` está.**

O Regular Controle tem **12 disciplinas**, conferidas nas pastas e confirmadas nos dois pacotes
pela sessão das skills de download:

```
AFO · Administração Pública · Análise de Informações · Auditoria Governamental
Contabilidade Geral Avançada (224361) · Contabilidade Pública · Controle Externo
Direito Administrativo · Direito Constitucional · Matemática Financeira
Português · Raciocínio Lógico e Analítico
```

**`ESTAT` e `ECOFIN` são só do Fiscal.** Continuam entre as 21, porque existem no Regular Fiscal.

**Como o erro entrou:** perguntei ao Elvis sobre as três, ele respondeu a regra geral ("mapear
tudo que o Curso Regular tem"), e eu registrei a regra **como se fosse a confirmação do fato**.
Pergunta virou afirmação sem ninguém ter verificado a pasta. Vale como alerta: resposta a uma
regra não confirma o caso concreto que a motivou.

### Ignorar o "(Fiscal/ Controle)" dos nomes

O sufixo entre parênteses que aparece na Tutory (`Direito Administrativo (Fiscal/ Controle)`) foi
uma forma antiga de mapear e **muda muito**. Não é sinal de nada. **Vale o nome da matéria**, e a
área é coluna.

**Nem toda matéria está nas duas áreas**, e isso é normal: `CTREXT` é só do Controle, `DTRIB` é só
do Fiscal.

### Professor de referência

| Disciplina | Referência |
|---|---|
| Contabilidade Geral e Avançada | **Gilmar Possati** |
| Direito Civil | **Paulo Sousa** |

---

## Alerta de nomenclatura no plano · decidido em 21/08/2026

Quando o nome da **nossa** disciplina divergir do que o **edital** usa, o plano avisa o aluno:

```
Estudo de Estatística
ESTAT-0012

Referência: Distribuição Normal
            ⚠ No edital do TCDF isso aparece dentro de "Raciocínio Lógico"
```

Sai de graça: a base já guarda o nosso nome e o do edital lado a lado, então é só comparar e
avisar quando divergir. Sem isso, o aluno procura o assunto na parte errada do edital.

### Vale para TODA fonte, não só para o edital

Cada fonte guarda **o rótulo dela**, e a referência mostra onde o aluno encontra a coisa **naquela
fonte**. O caso que motivou: o aluno está em `TECINF` no plano, mas o resumo do Bezerra está
arquivado na matéria **Informática** dele. Sem o rótulo de origem, o aluno procura e não acha, e
conclui que o material está errado.

```
Estudo de Tecnologia da Informação
TECINF-0203

Referência: Banco de Dados: Normalização
            Estratégia — Aula 07, páginas 12 a 24
            Bezerra   — resumo "Modelagem de Dados", na matéria INFORMÁTICA
            ⚠ No edital do TCDF isso aparece como "Análise de Dados"
```

**Portanto, toda base de fonte carrega uma coluna com o nome que AQUELA fonte usa**: a matéria do
Bezerra, o assunto do Tec, o nome do curso do Estratégia, o item do edital. Nunca substituir pelo
nosso nome na hora de guardar — o nosso nome é para identificar, o da fonte é para **localizar**.
É a mesma regra do `INICIE EM` / `TERMINE EM`.

---

## A24 — Contas · fechado em 21/08/2026

| Conta | Papel | Regra |
|---|---|---|
| **Coleta** | imprime as 1.000/dia | uma só; nunca gera caderno de aluno |
| **Produção** | gera os cadernos do aluno | é a conta atual do Elvis, nível avançado; **nunca** usada para coleta em massa |

Uma conta para imprimir, e não duas: duplicar aceleraria o download, que **não é o gargalo**
(o fichamento é), e aumentaria a exposição de uma conta que já foi sinalizada pela plataforma.

---

## Qual curso serve de referência · fechado em 21/08/2026

**Corrige uma proposta minha que estava errada.** Eu havia sugerido escolher o curso **mais
atualizado**, por data e hash. Não é assim:

```
1º  O Curso REGULAR manda sempre    (Regular Fiscal, Regular Controle, e no futuro Regular Legislativo)
2º  Não existe no Regular           → vai para o curso específico, como suplemento
3º  Em pós-edital, com a aula já
    liberada no específico          → usa a do específico
```

Não é "o mais novo ganha", é **"o Regular é a espinha, o específico completa"**. O aluno de
pós-edital já viu no Regular o que estudou antes.

### O link se escolhe pela ÁREA do aluno

Refinamento de 21/08/2026. Um tópico compartilhado tem **um código e dois endereços**, e cada
aluno recebe o do curso **dele**:

```
Tópico DADM-0018, compartilhado pelas duas áreas
  Aluno de Controle  ->  Regular Controle, aula 06, p. 17-29
  Aluno de Fiscal    ->  Regular Fiscal,   aula 07, p. 22-35
```

Mesmo código, mesmo caderno de questões, PDFs diferentes. Mandar o aluno de Controle para o PDF
do Fiscal seria pedir que ele abrisse um arquivo que talvez nem tenha.

| Situação | Qual link vai |
|---|---|
| Existe nos dois cursos | **o da área do aluno** |
| Existe só num, e é pertinente | o que existe, mesmo sendo da outra área |
| Pós-edital, aula do específico já liberada | a do específico |
| Pós-edital, aula ainda não liberada | **continua no Regular** |

**A data vem da CAPA do PDF**, não da plataforma — o Estratégia não publica data de atualização.

**O `hash_teoria` continua útil, mas para outra coisa:** saber se o conteúdo mudou de verdade, e
com isso decidir se vale avisar o aluno.

---

## Aulas ainda não liberadas no pós-edital · desenho de 21/08/2026

No pós-edital o Estratégia **lista o nome da aula antes de liberar o arquivo**. Para não travar o
plano, o mapeamento chuta pelo nome — mas o chute fica **marcado como chute**:

| Elemento | Para quê |
|---|---|
| `provisorio = true` | o vínculo entrou por palpite, não por leitura |
| `confianca` | quão certo o palpite parece |
| `nome_na_plataforma` | o texto literal que apareceu, para conferir depois |
| fila de conferência | toda aula provisória espera o arquivo sair |

**Registrar o erro, não só a correção.** Quando o arquivo sair e o palpite estiver errado, gravar
o que se chutou, o que era, e quando se corrigiu. Serve para o Elvis avisar quem pegou a versão
errada, e para **medir a taxa de acerto do palpite pelo nome**: se acertar 90%, vale continuar;
se acertar 50%, melhor esperar o material.

**O texto para o aluno afirma, não duvida.** Nada de "pode mudar", que só planta insegurança:

```
Referência: Improbidade: Prescrição
            Aula 12 do Pacotaço TCDF, ainda não liberada pelo Estratégia.
            Estude por enquanto no Regular Controle, aula 16, p. 90-101.
```

E isso tende a ser **raro**: o material costuma sair em cerca de 15 dias.

---

## Quando um plano precisa ser recarregado na Tutory

| Mudou | Recarrega? |
|---|---|
| Incluiu ou excluiu **aula** | **sim** |
| Mudou o conteúdo do caderno de questões | **não** — o link é o mesmo |
| Mudou a Referência ou a Dica | **não** |

Por isso os planos fixos (Regular Fiscal, Regular Controle) mudam pouco. **O mapeamento precisa
indicar qual curso mexeu**, para o Elvis saber o que recarregar em vez de reprocessar tudo.

---

## A estrutura tem de aceitar área e fonte novas · 21/08/2026

O Elvis vai incluir **outras áreas** (a **Legislativa** é a próxima) e **outras fontes de
material** (parceiros, como o **Professor Rabelo** em Legislação Tributária).

**Área é LISTA, não coluna.** Se `Fiscal` e `Controle` forem colunas, entrar `Legislativo` obriga a
mexer em todas as tabelas. Como lista, é linha nova:

```
topico_area:  DADM-0018 -> Fiscal
              DADM-0018 -> Controle
              DADM-0018 -> Legislativo     <- entra sem mexer em nada
```

**Fonte também é lista.** A base 4 deixa de ser "Resumos do Bezerra" e passa a ser **materiais de
parceiros**, com o Bezerra como a primeira fonte. Rabelo entra como fonte nova, não como base
nova. A referência do aluno mostra todas:

```
Referência: ICMS: Substituição Tributária
            Estratégia — Regular Fiscal, aula 09, p. 14-26
            Bezerra    — não cobre
            Rabelo     — Legislação Tributária, módulo 3
```

**Cada fonte guarda o rótulo dela** (ver a regra do rótulo de origem), porque é por ele que o
aluno acha o material dentro daquela fonte.

---

## A32 — Janela de anos por matéria · fechado em 21/08/2026

**Não é fixa. Define-se matéria a matéria**, e Claude propõe antes de coletar.

| | |
|---|---|
| Alvo de acervo | **~2.500 questões** por matéria dentro de uma área |
| Confortável | 3.000 já é um banco muito bom |
| **Teto de janela** | **10 anos**, nunca mais |
| Como medir | consulta de **contagem** por filtro — não precisa imprimir nem exportar planilha |

O método: ir somando ano a ano na contagem até chegar perto de 2.500, e parar. Matéria muito
cobrada fecha com poucos anos; matéria pouco cobrada precisa abrir mais, até o teto de 10.

**Claude sugere, o Elvis confirma**, a cada matéria.

Pode haver assunto sem questão mesmo assim — ver a regra de tópico sem acervo, que manda
registrar e ignorar.

---

## A16 — PPPs e Convênios · fechado em 21/08/2026

**Permanecem no escopo**, principalmente na área de Controle, mesmo não tendo item explícito no
edital do TCDF.

---

## A11 — Questão inédita · fechado em 21/08/2026

**Exige plano avançado do aluno.** Logo:

- **cadernos separados** para inédita, nunca misturada com questão de prova real
- provavelmente numa **conta própria**
- uso principal em **pós-edital**

Misturar quebraria o caderno para o aluno de plano padrão, e o problema apareceria na mão dele.

---

## Filtrar por ÁREA do concurso · levantado em 22/08/2026

**Furo no critério de coleta.** O filtro combinado era `assunto + banca + ano`, e ele **não olha o
cargo**. Entra questão de Contabilidade cobrada em prova de **Contador**, muito mais profunda do
que o que se cobra de Auditor Fiscal, e questão de TI cobrada em prova de Analista de TI.

O Tec tem o filtro: `/api/enums/areas` devolve valores como `FISCAL` e `GESTAO_CONTROLE_TRIBUNAIS`,
e há filtros de cargo e profissão.

**O critério passa a ser `assunto + banca + ano + área`.**

**Mas medir antes de aplicar.** Filtro de área restritivo demais troca contaminação por escassez:
uma disciplina pode ter 5.463 questões sem ele e 1.200 com. Ao definir a janela de anos de cada
matéria, medir **as duas contagens, com e sem área**, e mostrar lado a lado. Custa 1 chamada a
mais por matéria.

### A área do Tec é larga demais para o Controle

O valor `GESTAO_CONTROLE_TRIBUNAIS` junta três coisas, e o **Curso Regular Controle cobre só
duas**:

```
GESTAO_CONTROLE_TRIBUNAIS
  Gestão        <- NAO entra
  Controle      <- entra (controladorias)
  Tribunais     <- entra (tribunais de contas)
```

Então é preciso **um corte adicional por cima da área**. Duas formas, a testar:

| Corte | A favor | Contra |
|---|---|---|
| **Por órgão** | nome padronizado (TCU, TCE, TCM, TCDF, CGU, CGE, CGM), critério explícito e auditável | lista comprida, precisa ser mantida |
| Por cargo | lista menor | nome de cargo é livre e varia por banca, escapa coisa |

**Aposta:** órgão filtra melhor, porque o nome é padronizado. Mas **medir**: comparar as contagens
das duas formas e ver qual traz o acervo mais limpo.

### Verificar se existe filtro de "área especializada"

Ao puxar `/api/enums/filtros-questao?universo=&formato=OBJETIVA` em 21/08, a resposta **veio
cortada** e não deu para ver a lista inteira. Pode haver ali um filtro que remova questão de área
técnica especializada, que resolveria parte do problema sozinho. **Repuxar inteira** — custa 1
chamada.

---

## Medir o tempo de estudo · desenho de 22/08/2026

A Tutory pede minutagem por meta ("estude 120 min"). Três componentes, três fontes:

| Componente | De onde vem | Qualidade |
|---|---|---|
| **Teoria** | páginas do bloco x minutos por página | precisa calibrar |
| **Questões** | **`tempoMedio` do Tec**, por questão, em segundos | **dado real**, média de milhares de alunos |
| **Releitura do resumo** | páginas do resumo x ritmo mais leve | precisa calibrar |

O componente de questões é o mais sólido: `GET /api/questoes/{id}/desempenho` traz `tempoMedio`
(na amostra de 21/08, 71 segundos). Um caderno de 30 questões soma o tempo real das 30, em vez de
um "2 minutos por questão" inventado.

**Calibrar a teoria com dado do próprio público.** O painel do aluno tem "Tempos de Estudos" e
"Horas Líquidas (cronômetro)". Se esses dados forem acessíveis, o minutos-por-página sai do
comportamento real dos alunos do Elvis, e não de estimativa.

---

## Para a skill do plano na Tutory · anotado em 22/08/2026

### A revisão de 15 minutos

Tarefa curta de **revisão teórica** que precisa entrar na grade sem inchar o dia. Perguntas a
resolver quando a skill for feita:

- é tarefa própria na Tutory, ou pedaço de outra?
- revisa qual tópico: o da véspera, o de uma semana atrás, ou o que o desempenho apontar?
- entra todo dia, ou em cadência?

### Caderno de erros com questão que não está no nosso banco

O aluno pode resolver questões por conta própria, fora dos nossos cadernos. Quando ele mandar o
caderno de erros, parte das questões não vai existir na nossa base.

**Não é perda total.** O caderno impresso traz **matéria e assunto** no cabeçalho de cada questão:

| O que dá para saber | Como |
|---|---|
| A que **tópico** pertence | pelo assunto impresso, cruzando com a base 3 |
| A que **ponto** pertence | **não dá** — isso só lendo a questão |

Então o alerta de tópico continua funcionando ("errou três de Atos Administrativos"), e só se
perde a precisão do ponto.

**Se valer descer ao ponto**, buscar no Tec **só essas questões**, que são poucas: as que ele
errou e que a gente não tem. Custo pontual, não passada nova.

---

## Parâmetros de tempo do plano · fechado em 22/08/2026

| Componente | Pré-edital | Pós-edital / reta final |
|---|---|---|
| **Teoria** | 5 min por página | 5 min por página |
| **Resumo** | 5 min por página | 5 min por página |
| **BIZURITO** | 5 min por página | 5 min por página |
| **Questão certo/errado** | **2 min** | **1,5 min** |
| **Questão múltipla escolha** | **3 min** | **2,5 min** |

A leitura **não acelera** na reta final; só as questões apertam, 30 segundos em cada formato.

**Por que 2,5 min na múltipla escolha da reta final:** dá **20 questões por hora**, sobrando 10
minutos para marcar o gabarito. É ritmo de prova.

**A página de resumo tem o mesmo ritmo da teoria** porque ela é densa: condensa o que na teoria
ocupa várias páginas.

### O `tempoMedio` do Tec NÃO vai ser usado

Ele vem em `/api/questoes/{id}/desempenho`, ou seja, **1 requisição por questão**, e **não vem na
impressão**. Usá-lo significaria voltar ao caminho que foi aposentado. O parâmetro fixo entrega
quase o mesmo a custo zero.

### A minutagem atual da Tutory não serve de referência

O Elvis confirmou que os tempos que estão lá hoje não têm parâmetro por trás. **Não calibrar por
eles.**

---

## Área especializada: imprimir tudo e MARCAR · fechado em 22/08/2026

### O filtro por Formação não resolve

Um concurso que **aceita** formação em TI não é um concurso **de** TI. A maioria aceita qualquer
formação, então filtrar por ali pegaria os dois casos.

### A Área (Carreira) resolve o corte do Controle

O filtro tem subníveis. Marcar **Controladorias** e **Tribunais de Contas**, deixando **Gestão
Governamental** de fora. Resolve sem precisar de lista de órgão.

### Para a área especializada: base de concursos

**Imprimir tudo e separar internamente**, em vez de filtrar na origem. Três motivos:

1. **A cota é gasta do mesmo jeito.** Filtro que erra descarta questão boa sem ninguém ver.
2. **Vira ativo.** Se um dia houver material para concurso de Contador, a base já está pronta.
3. **É auditável.** O Elvis pode discordar caso a caso.

**O julgamento é por CONCURSO, não por questão.** Contabilidade num concurso de Contador é pesada;
a mesma matéria num concurso de Analista Administrativo é normal. São centenas de concursos, não
milhares de questões: trabalho finito.

Isso vira uma **base nova, de concursos**, com a marca "área especializada: sim/não" e a fonte do
julgamento (busca, nome do cargo, edital).

**O critério final é por matéria.** TI e Contabilidade sofrem mais; Direito Administrativo quase
não sofre. Definir ao coletar cada matéria.

---

## Bloco de teoria em múltiplos de 30 minutos · 22/08/2026

**A Tutory só aceita múltiplos de 30 minutos**, de 30 a 180. Não existe tarefa de 45.

Consequências:

1. **Precisão fina não vale nada.** 82 e 89 minutos viram os mesmos 90. Isso confirma o descarte
   do `tempoMedio` do Tec: gastar 1 requisição por questão para ganhar precisão que é arredondada
   fora é desperdício puro.

2. **O bloco de teoria mira múltiplos de 30**, e a 5 min/página isso dá:

   | Bloco | Páginas |
   |---|---|
   | 30 min | 6 |
   | **60 min** | **12** |
   | 90 min | 18 |

3. **Teto de 90 minutos por tarefa.** A composição que fecha certo:

   ```
   12 páginas de teoria  ->  60 min
   + questões            ->  30 min
                             90 min  <- o teto
   ```

**O alvo fica em 10 páginas** — confirmado em 22/08, depois de entrar o Pomodoro na conta.

O que decide não é o arredondamento da Tutory, é o **Pomodoro**: o bloco de 30 minutos dela são
**25 de estudo e 5 de intervalo**. Logo, uma tarefa de 90 minutos tem **75 minutos efetivos**, não
90.

| Páginas | Teoria | Pomodoros de teoria | Sobra para questões (de 75 min) |
|---|---|---|---|
| 5 | 25 min | **1 exato** | 50 min |
| **10** | **50 min** | **2 exatos** | **25 min = 1 Pomodoro** |
| 12 | 60 min | 2,4 (quebra) | 15 min, ~5 questões |
| 13 | 65 min | 2,6 (quebra) | 10 min, ~3 questões |
| 15 | 75 min | **3 exatos** | **zero** |

**Por que 12 é o teto:** em 13 páginas sobram 10 minutos, que dão três questões — enfeite, não
caderno. Em 15, a teoria come os três Pomodoros e a tarefa vira só leitura.

**Por que o piso é 5 e não 6:** cinco páginas dão um Pomodoro exato; seis dão 1,2 e quebram.

**Acima de 12** a tarefa vai para 120 min (4 Pomodoros, 100 min efetivos), e aí o número que fecha
é **15 páginas**: 3 Pomodoros de teoria + 1 de questões. Funciona, mas passa do teto de 90 que o
Elvis prefere.

| | |
|---|---|
| **Alvo** | **10 páginas** |
| Faixa que fecha bem | **5 a 12** |
| Números redondos | 5, 10 e 15 |
| Tarefa típica | 2 Pomodoros de teoria + 1 de questões |

**É alvo, não regra.** Quem manda no corte é o título: se o tópico acaba na página 13, corta na 13.
A escada serve para escolher entre dois títulos possíveis, não para forçar.

### Guardar o tempo exato, arredondar só ao publicar

O banco guarda o tempo calculado com precisão; o arredondamento para múltiplo de 30 acontece **na
hora de publicar na Tutory**. Assim dá para somar tempos e planejar com o número real, e se a
plataforma mudar a granularidade nada se perde.

**O corte continua sendo sempre em título.** O alvo orienta, o título manda: nunca cortar no meio
de um tópico.

**Tipos de tarefa** (todas entre 30 e 120 min, mirando 90):

- teoria + questões, com leitura dos comentários
- leitura do resumo (revisão) + algumas questões
- só leitura do resumo
- só caderno de questões

**A carga diária não é problema:** o aluno declara o tempo disponível e a Tutory distribui sozinha.

---

## A base de concursos se monta sozinha · 22/08/2026

**Não precisa buscar lista.** Cada questão impressa já traz o concurso dela no cabeçalho:

```
CEBRASPE (CESPE) - AG (TCE-PE) /TCE PE/Administração/2017
                    cargo        órgão   área          ano
```

Enquanto a coleta roda, a lista de concursos se forma sozinha, **sem chamada extra**, e cobre
exatamente os concursos que apareceram no acervo — nem um a mais. Puxar a lista completa do Tec
traria centenas que nunca serão vistos.

**Fica junto da base 5**, em aba separada, porque está vinculada às próprias questões.

**O julgamento "é de área especializada?" é do Elvis**, com Claude fazendo a busca externa sobre
os concursos duvidosos e trazendo a lista para marcar. Em Direito Administrativo espera-se
pouquíssimos casos; em Contabilidade e TI, mais.

**Serve a três usos**, não só à montagem de caderno:

1. excluir do caderno do aluno o que é de outro nível
2. **excluir do caderno de erros**: se ele errou uma questão especializada, reforçar naquele nível
   piora, porque ele errou pelo nível da questão e não por base fraca
3. guardar como ativo, para o dia em que houver material para concurso especializado

---

## Filtrar por escolaridade · 22/08/2026

**Só nível superior.** Questão de nível médio cobra o mesmo assunto de forma bem mais rasa e
contamina a percepção de dificuldade do tópico.

O filtro existe no menu do Tec, logo abaixo de "Área (Carreira)".

---

## Download do Estrategia: pasta, produto e unidade de mapeamento · fechado em 22/08/2026

> **O padrao completo de nomes esta em `NOMENCLATURA.md`**, com o orcamento de caracteres por
> nivel. O que segue e o principio; os limites estao la.

### A pasta leva o nome do ESTRATEGIA, nao o nosso

Sintetizado se for comprido, mas **nunca traduzido** para a nossa taxonomia. Se a pasta se chamar
`TECINF`, quem abrir a plataforma procurando `TECINF` nao acha nada; se chamar `Informatica`,
bate.

E a regra do rotulo da fonte aplicada aqui: **cada fonte guarda o nome dela, porque e por ele que
se acha o material**. O vinculo com a nossa taxonomia mora na tabela de apelidos da base 1.

**Consequencia boa:** o download **nao depende** da base 1. Ela nao decide nome de pasta nenhum,
e a traducao se aplica na hora de MAPEAR, nao na de baixar. As duas coisas podem correr em
paralelo.

### So o CURSO REGULAR, nunca o pacotaco

O Estrategia oferece, para o mesmo concurso, ate quatro produtos: o **Curso Regular** sozinho, o
**Passo Estrategico** sozinho, o **pacotaco** com os dois, e as vezes o **sistema de questoes**.

**Baixar so o Curso Regular.** O Passo esta fora do escopo, e o pacotaco traria peso morto. A vaga
de matricula e a mesma (1 produto), entao o pacotaco nao compensa.

Se um dia o Passo entrar no escopo, ai sim vale o pacotaco.

Vale tambem para o TCDF: **o Curso Regular dele**, nao o Pacotaco.

### O mapeamento e por CURSO, nao por disciplina

A unidade de organizacao e o **curso**, do jeito que o Estrategia monta. Uma aula que la se chama
"Analise de Dados" pode virar `TECINF` aqui, e um curso pode alimentar mais de uma disciplina
nossa.

**Baixar e organizar por curso**, sem tentar reagrupar pela nossa taxonomia. A reagrupacao
acontece no mapeamento, pela tabela de pares bloco x topico.

### A marca do CPF e da titular da conta

Confirmado pelo Elvis: e a esposa dele, e a conta e legitima. Entao **todo** material do
Estrategia carrega a mesma marca enquanto for a mesma conta.

Alem do problema tecnico do hash, e **CPF de uma pessoa real**: nao pode sair em nada que va para
o aluno.
