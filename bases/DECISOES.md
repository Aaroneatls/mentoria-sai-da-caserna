# Decisões fechadas

> **Leia isto antes de começar qualquer base.** Cada decisão aqui já foi discutida e fechada com
> o Elvis. Não reabrir sem motivo novo. Este arquivo existe para que a sessão de cada skill
> comece sabendo o que já está resolvido.

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

Casos concretos: `CONTAB`, `ESTAT` e `ECOFIN` não aparecem no ciclo do Controle, mas o Curso
Regular de Controle tem o material.

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
