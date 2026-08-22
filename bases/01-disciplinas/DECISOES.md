# O que esta base precisa saber

> Extrato de `../DECISOES.md`, so com o que afeta esta base. O arquivo central continua sendo a
> referencia completa; aqui esta o essencial, para a sessao nao gastar contexto com decisao de
> outra base.

## As 21 disciplinas e suas siglas

`AFO` `ADMPUB` `AUDIT` `CONTAB` `CONTPU` `CUSTOS` `CTREXT` `DADM` `DCIVIL` `DCONST` `DEMPRE`
`DPENAL` `DTRIB` `ECOFIN` `ESTAT` `LTRIB` `MATFIN` `PORT` `RACLOG` `REFTRI` `TECINF`

Sigla de 4 a 6 letras, com `AFO` como unica excecao de 3. A lista completa com os nomes esta na
secao A8 do arquivo central.

## O formato do codigo

`SIGLA-NNNN`, quatro digitos.

| Faixa | O que e |
|---|---|
| `0001` a `4999` | vem do Curso Regular |
| `5000` | **nunca existe**, e a fronteira |
| `5001` em diante | nasce em pos-edital |

**A origem e coluna, nunca prefixo.** O codigo identifica **conteudo**; o mesmo topico pode
aparecer em varios concursos.

## Area e LISTA, nao coluna

Nunca criar colunas `Fiscal` e `Controle`. Uma linha por par (disciplina, area), para a area
**Legislativa** entrar depois sem mexer em nada.

## Apelidos: cada fonte guarda o nome dela

O nosso nome **identifica**; o da fonte **localiza**. Uma linha por par (disciplina, fonte, nome
na fonte). E por esse nome que o aluno acha o material dentro daquela fonte.

```
TECINF | Estrategia Regular Controle | "Analise de Informacoes"
TECINF | Estrategia Regular Fiscal   | "Informatica"
TECINF | Bezerra                     | "Tecnologia"
```

## O escopo vem do Curso Regular

O que nao esta no Curso Regular **nao entra** por padrao. Foi assim que Direito Processual Civil
ficou de fora: aparecia no ciclo de estudo, mas nao existe em nenhum dos dois Regulares.

## A familia tributaria sao quatro disciplinas

| | O que e | Quando existe |
|---|---|---|
| `DTRIB` | Direito Tributario | sempre |
| `REFTRI` | Reforma Tributaria | sempre (o conteudo hoje esta dentro de `DTRIB` no material) |
| `LTRIB` | Legislacao Tributaria, **parte geral**, com a **Lei Kandir** | sempre |
| local | legislacao estadual ou municipal | **so no pos-edital** |

## O padrao de nome do Estrategia e INVERTIDO entre os dois cursos

Quem for extrair a materia do nome do curso precisa das duas regras:

```
Fiscal:    "Concursos da Area Fiscal - Curso Basico de <MATERIA>"
Controle:  "Concursos de Tribunais de Contas (Nivel Superior) <MATERIA> - Curso Regular"
```

No Fiscal a materia vem **no fim**; no Controle vem **no meio**, antes do sufixo. Uma regra so
nao pega os dois.

## `tipo_curso_id = 1` NAO garante que e disciplina

Medido em 22/08/2026: **"Sistema de Questoes 1 Ano - Cartao ate 12 x"** (id 143237) vem como
`tipo_curso_id = 1`, igual a uma disciplina, e e **assinatura**.

Filtrar por tipo nao basta. Conferir o nome e excluir explicitamente o que nao for materia.

## A DISCURSIVA nao e disciplina

Decisao do Elvis em 22/08/2026. Ela existe no pacote do Regular Fiscal (cursos 268932 e 268941),
mas **nao entra nas 21**: e treino de producao de texto, e o modelo do projeto
(topico -> ponto -> questao objetiva -> caderno do Tec) nao se aplica a ela.

Registrado para ninguem reabrir daqui a um mes achando que foi esquecimento. **Nao e furo de
levantamento, e decisao.**

Pelo mesmo motivo fica de fora o **"Sistema de Questoes 1 Ano"** (143237), que nem curso e — e
assinatura, e vem com `tipo_curso_id = 1` igual a uma disciplina.

## O NOME da disciplina e congelado, igual a sigla

Decidido pelo Elvis em 22/08/2026. **Nao reabrir.**

Fixamos `Direito Administrativo` e `DADM`, e **nenhum dos dois muda mais**.

**Por que:** a Tutory reconhece que o aluno ja estudou um assunto comparando
**nome do assunto + NOME DA DISCIPLINA** entre planos. Mudar o nome da disciplina, ainda que
por **um unico espaco**, faz a plataforma tratar como disciplina nova, e o historico do aluno
se perde. Nao ha desfazer depois de publicado.

| | Estatuto |
|---|---|
| `sigla` | irreversivel |
| `nome_canonico` | **irreversivel tambem** |
| apelido de qualquer fonte | muda a vontade, e literal |

**Ao carregar plano novo na Tutory, vai o NOSSO nome**, nao o legado. Os 168 nomes legados
(`Direito Administrativo (Fiscal/ Controle)`, `Direito Tribubario`, ...) servem so como
conhecimento para a **migracao** (item A28), nunca como alvo a imitar. Depois se faz a passada
de troca.

**Uma disciplina nossa pode cobrir varias materias da fonte, e continua com um nome so.**
`Tecnologia da Informacao` e um nome unico, mesmo o Tec fatiando em 10 materias e o Estrategia
em 2. O fatiamento da fonte vira **apelido**, nunca nome novo.

**Onde esta travado:** `dados/nomes-congelados.csv` guarda o par (sigla, nome) com data e motivo,
e o **bloco 11** do `conferir.py` falha se o nome divergir ou ganhar espaco sobrando ou duplicado.
Testado: espaco duplicado em `Direito Administrativo` derruba a conferencia.

## Legislacao Tributaria sobre o Consumo: o CONTEUDO decide, nao o curso

Corrigido pelo Elvis em 22/08/2026, revendo o que ele mesmo tinha dito antes.

O curso **336350** ("Legislacao Tributaria sobre o Consumo (LTC) - Reforma Tributaria") **nao e
inteiro `LTRIB`**:

| Conteudo | Codigo |
|---|---|
| **Lei Kandir** | `LTRIB` — e a parte geral |
| **LC 214/2025, LC 227/2026, EC 132/2023** | `REFTRI` — e reforma |

Por isso o 336350 aparece **duas vezes** no `apelidos.csv`, como `REFTRI` e como `LTRIB`. A
separacao real sai na **base 2**, lendo os PDFs. E o mesmo principio que ja valia para a Reforma
que mora dentro de `DTRIB`: **o conteudo decide o codigo, nao onde o professor guardou.**

## Fonte sem dona nao vira disciplina, e nao ganha Cod Mestre

Resolvido pelo Elvis em 22/08/2026, sobre as 8 entradas do balde 1 do `SEM-DONA.md`.

**Nao ha problema a resolver.** Elas ficam **mapeadas na fonte** (o resumo do Bezerra continua
achavel, o nome da Tutory continua registrado) e simplesmente **nao recebem Cod Mestre**.

**O motivo:** o Cod Mestre pressupoe que exista **conteudo teorico nosso** por tras dele. Sem
material no Curso Regular, nao ha o que o aluno estude, e um codigo apontaria para o vazio.

Se um dia a materia entrar no Regular, ela ganha sigla e codigo pelo modo `atualizar`. Ate la,
`status = olho` no `apelidos.csv` e o registro no `SEM-DONA.md` bastam.

## A familia da LEGISLACAO TRIBUTARIA · fechado em 22/08/2026

**A `LTRIB` generica morreu.** Detalhe completo em `../DECISOES.md`. O que esta base guarda:

| Sigla | Disciplina | Material |
|---|---|---|
| `LTEST` | Legislacao Tributaria Estadual (parte geral) | curso 220891 |
| `LTMUN` | Legislacao Tributaria Municipal (parte geral) | curso 220896 |
| `LTFED` | Legislacao Tributaria Federal | **nao ha no Regular**: nasce nomeada e SEM Cod Mestre |

A **Lei Kandir** (LC 87/96) mora em `LTEST`: e norma nacional do ICMS, e ICMS e competencia
estadual. Por ente (`LTCE`, `LTMAO`, ...) nasce em pos-edital.

### Sigla APOSENTADA nunca se reaproveita

`LTRIB` continua em `dados/nomes-congelados.csv` com `status = APOSENTADA`, **nao foi apagada**.
Apagar deixaria a sigla parecendo livre, e alguem a reatribuiria a outra disciplina; se ela tiver
sido publicada em qualquer lugar, o aluno seria mandado para conteudo errado. O bloco 11 do
`conferir.py` **falha** se uma sigla aposentada reaparecer em `disciplinas.csv`.

### O total de disciplinas deixou de ser fixo

Eram 21; sao 23, e a familia por ente **cresce a cada pos-edital**. O `conferir.py` parou de
checar "sao 21" e passou a checar o que vale sempre: **unicidade de sigla e de nome**, e que a
lista nunca **encolha** (sigla nao se apaga, se aposenta).

### Disciplina sem material no Regular fica sem area, e DECLARA isso

`LTFED` nao tem curso no Curso Regular, entao nao ha de onde tirar area. E estado valido, mas o
bloco 8 exige que a observacao diga `SEM material no Curso Regular` — sem a declaracao, area
vazia parece esquecimento.

### Teoria duplicada em dois cursos: esperado, nao e defeito

Os cursos **336350** ("Consumo") e **220891** (Estadual) cobrem **a mesma Lei Kandir**. Quem
resolve e a regra de que **mesmo `hash_teoria` = mesmo Cod Mestre**. A base 2 precisa **esperar**
isso; se ela tratar como anomalia, vai duplicar topico.

### A sigla de cada ente: deterministica, sem "quem chegou primeiro"

Fechado em 22/08/2026, refinando o esquema aprovado no mesmo dia.

| Ente | Regra | Exemplos |
|---|---|---|
| Estado | `LT` + UF | `LTCE` Ceara · `LTSP` Sao Paulo · `LTPA` Para · `LTGO` Goias |
| Municipio **CAPITAL** | `LTM` + UF | `LTMSP` Sao Paulo · `LTMAM` Manaus · `LTMCE` Fortaleza |
| Municipio nao-capital | `LTM` + UF + inicial | `LTMSPC` Campinas/SP |
| **Distrito Federal** | **`LTDF`, e so** | acumula estadual E municipal |
| Empate | o `nomes-congelados.csv` decide, **nunca a formula** | |

**Por que a capital leva o nome curto, e nao o primeiro que aparecer.** A primeira versao dizia
`LT` + tres letras para municipio, e os exemplos usavam **duas convencoes diferentes**: `LTMAO`
(Manaus) vinha do codigo IATA do aeroporto, e `LTMSP` vinha de "M de municipio + SP". Diante de
"Legislacao Tributaria de Fortaleza", uma sessao geraria `LTFOR` e outra `LTMCE`, **e a que
gravasse primeiro ganharia para sempre**, porque a sigla congela no nascimento.

A segunda versao (minha) trocou isso por `LTM` + UF, mas deixou o nome curto para **o primeiro
municipio daquele estado que aparecesse** — um arbitrio menor, da mesma familia. **Capital e fato;
ordem de chegada e acidente.** Duas sessoes diante do mesmo municipio agora geram a mesma sigla.

**Nao ha colisao entre estado e municipio:** `LT`+UF tem 4 caracteres e `LTM`+UF tem 5. Conferidos
os casos capciosos: `LTMA` (Maranhao) x `LTMAM` (Manaus), `LTMS` (Mato Grosso do Sul) x `LTMSP`
(municipio de Sao Paulo). Todos cabem nos 6 caracteres do orcamento de nome de pasta.

**A formula PROPOE; o `nomes-congelados.csv` DECIDE.** Nenhuma formula garante unicidade: dois
municipios de SP comecando com C colidem em `LTMSPC` de qualquer jeito. A formula existe para ser
previsivel e legivel; o registro existe para ser verdadeiro. Conferir colisao **antes** de congelar.

#### `LTMDF` NUNCA EXISTE

O Distrito Federal **nao e dividido em municipios** (CF art. 32) e **concentra as competencias
tributarias de estado e de municipio** (CF art. 147). Logo ISS, IPTU e ITBI no DF sao **lei
distrital**, e `LTDF` carrega os dois blocos de conteudo.

**Por que isso e trava e nao nota de rodape:** o TCDF e o pos-edital mais provavel, entao o DF e o
primeiro ente que vai nascer. Quem aplicar a formula no automatico cria `LTDF` **e** `LTMDF`. Na
melhor hipotese o `LTMDF` nasce vazio para sempre; na pior ele leva metade do conteudo do `LTDF`, e
**os dois ficam pela metade sem ninguem perceber** — que e a falha cara, porque nao da erro.

O **bloco 11** do `conferir.py` falha se `LTMDF` aparecer.

---

**Duvida sobre algo que nao esta aqui?** Consulte `../DECISOES.md`.
**Licao aprendida nesta base?** Escreva em `APRENDIZADO.md`, nao aqui.
