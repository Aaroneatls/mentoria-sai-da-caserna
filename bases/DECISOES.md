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
