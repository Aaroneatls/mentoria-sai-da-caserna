# TecConcursos — manual completo da plataforma

> Documento de referência autocontido. Pode ser colado inteiro em outra pasta/projeto
> pra que qualquer agente entre já sabendo o que dá e o que não dá pra fazer no TecConcursos.
>
> **Levantado em 18–19/08/2026** por navegação direta na plataforma (conta grátis
> `aaroneatsl.int@gmail.com` **e** conta Plano Avançado `bizu.cadastros@gmail.com`),
> leitura do código da aplicação, do help center oficial e das transcrições dos
> **29 vídeos da playlist "Tec Concursos | Tutoriais"** (prof. Wilson Tavares, 2026).

---

## 1. O que é e como o site se organiza

Banco de questões de concurso + teoria + estatística de desempenho. Números de hoje:
**4.087.546 questões** no universo Global, **185.969 concursos** catalogados,
**146 matérias**, ~1,69 milhão de questões comentadas por professores.
Aplicação AngularJS antiga (jQuery 1.11 + Angular 1.x), alimentada por uma API
interna em `/api/...` que responde com o cookie de sessão do navegador.

**Menu principal:** Início · Guias · Estudo · Estatísticas · Concursos · Mais
(Matérias, Órgãos, Bancas, Blog).

**Dentro de "Estudo":** Minhas pastas · Filtrar questões · Buscar questões ·
Questões favoritas · Discussão de questões.

**URLs que importam:**

| Página | URL |
|---|---|
| Filtro/gerador de caderno | `/questoes/filtrar` |
| Busca por enunciado ou `#numero` | `/questoes/busca` |
| Pastas e cadernos | `/questoes/pastas` |
| Caderno específico | `/questoes/cadernos/{id}` |
| Lixeira de cadernos | `/questoes/cadernos-lixeira` |
| Questões favoritas | `/questoes/favoritas` |
| Questão avulsa | `/questoes/{numeroDaQuestao}` |
| Árvore pública de uma matéria | `/materias/{slug}` |
| Aula/teoria de um assunto | `/aulas/materias/{materiaId}/assuntos/{assuntoId}` (`?videoaulas`, `?mapasmentais`) |
| Guias de estudo por edital | `/guias/` → `/guias/{concurso}/{cargo}/{area}/{especialidade}` |
| Estatísticas | `/estatisticas`, `/estatisticas/configuracao`, `/estatisticas/comparar` |
| Planos | `/assinar` |

---

## 2. O gerador de cadernos (`/questoes/filtrar`)

Três eixos antes dos filtros:

- **Universo:** Global · Concursos · OAB · CFC · ENEM e Vestibular.
  **Global mistura OAB/ENEM com concurso** (o caderno de teste que gerei em Global
  veio com questão do VI Exame da OAB na primeira posição). Pra concurso, usar `CONCURSOS`.
- **Formato:** Objetivas (todas) · Objetivas (inéditas) · Discursivas.
  **Não dá pra misturar objetivas e discursivas no mesmo caderno** — regra do produto.
  Inéditas ficam bloqueadas nos universos OAB, CFC e Vestibular; discursivas ficam
  bloqueadas no CFC.
- **11 abas de filtro:** Matéria e assunto · Banca · Órgão e cargo · Ano ·
  Área (Carreira) · Escolaridade · Formação · Região · Favoritas · Enunciados · Opções.

Todas as abas convivem no mesmo DOM. O contador **"N questões encontradas" atualiza
em tempo real** a cada filtro. Toda aba tem "Pesquisar por nome".

### 2.1 Conteúdo de cada aba

- **Matéria e assunto** — 146 matérias, árvore de até 4 níveis
  (Matéria → Tópico → Subtópico → Sub-subtópico), com "Todo o conteúdo de [X]" em cada nó.
  **A ordem da árvore não é alfabética: é a ordem lógica de aprendizado, como um livro.**
  (Em Direito Administrativo começa por origem e conceito → regime jurídico → atos →
  poderes.) Isso serve de espinha dorsal pronta pra montar plano de estudo.
  Busca por nome devolve dois grupos: *Matérias contendo* e *Assuntos contendo*.
- **Banca** — ordem alfabética, centenas de bancas.
- **Órgão e cargo** — ordem alfabética, árvore órgão → cargo.
- **Ano** — 1989 a 2026, ordem decrescente.
- **Área (Carreira)** — 19 áreas-raiz, várias com subárvore (lista completa na seção 11).
- **Escolaridade** — Fundamental, Médio, Superior, Especialização, Mestrado, Doutorado.
- **Formação** — ~200 cursos de graduação.
- **Região** — Federal, Estadual, Municipal (e busca por município).
- **Favoritas** — filtra pelas pastas de questões favoritas do usuário.
- **Enunciados** — busca livre no texto: "Digite o texto do enunciado procurado".
  Sacada do tutorial: colar um trecho literal do edital aqui pra achar o que a banca
  já cobrou daquele ponto, mesmo sem assunto correspondente na taxonomia.
- **Opções** ("filtros inteligentes") — **bloqueada no plano grátis**. Lista completa
  na seção 2.2.

### 2.2 Aba "Opções" — filtros inteligentes (ids reais da API)

| Grupo | Filtro | id |
|---|---|---|
| SOLUÇÃO DA QUESTÃO | Somente comentadas (Professor ou IA) | `REMOVER_NAO_COMENTADAS` |
| | Somente comentadas em TEXTO (Professor) | `REMOVER_NAO_COMENTADAS_EM_TEXTO` |
| | Somente comentadas em VÍDEO (Professor) | `REMOVER_NAO_COMENTADAS_EM_VIDEO` |
| | Somente comentadas em TEXTO (IA) | `SOMENTE_COMENTADAS_POR_IA` |
| DIFICULDADE | muito fácil / fácil / média / difícil / muito difícil | `DIFICULDADE_MUITO_FACIL` … `DIFICULDADE_MUITO_DIFICIL` |
| TIPO DE QUESTÃO | Múltipla escolha | `REMOVER_CERTO_ERRADO` |
| | Certo ou Errado | `REMOVER_MULTIPLA_ESCOLHA` |
| GABARITO | somente CERTO | `SOMENTE_GABARITO_CERTO` |
| | somente ERRADO | `SOMENTE_GABARITO_ERRADO` |
| RESOLUÇÕES E ACERTOS | Remover as que acertei | `REMOVER_AS_QUE_ACERTEI` |
| | Remover as que errei | `REMOVER_ERRADAS` |
| | Remover as que resolvi | `REMOVER_AS_QUE_RESOLVI` |
| | Remover as que não resolvi | `REMOVER_NAO_RESOLVIDAS` |
| OUTRAS CARACTERÍSTICAS | Remover anuladas | `REMOVER_ANULADAS` |
| | Remover desatualizadas | `REMOVER_DESATUALIZADAS` |
| | Remover sem classificação por assunto | `REMOVER_SEM_CLASSIFICACAO_ASSUNTO` |
| | Remover adaptadas/inéditas | `REMOVER_ADAPTADAS_INEDITAS` |
| SUAS ATIVIDADES | Somente anotadas | `SOMENTE_ANOTADAS` |
| | Somente favoritas | `SOMENTE_FAVORITAS` |
| (oculto) | Somente adaptadas/inéditas | `SOMENTE_ADAPTADAS_INEDITAS` |

Definições oficiais: **anulada** = anulada pela banca (não dá nem pra marcar);
**desatualizada** = mudou lei ou jurisprudência (ainda dá pra marcar).

### 2.3 "Editar quantidades" — a tela de mapeamento

Tabela editável do número de questões por assunto que vai entrar no caderno.

- **Organizar por:** `Hierarquia` · `Relevância (com matéria)` · `Relevância (apenas assuntos)`.
  **Padrão a usar: "Relevância (apenas assuntos)"** — lista plana, só assuntos-folha,
  frequência decrescente, colunas *Assuntos | Questões encontradas (n + %) |
  Frequência Acumulada (barra + %) | Questões no caderno*.
- **Popular com questões:** `Mais Recentes` · `Aleatórias`. **Padrão: Mais Recentes.**
  Aleatórias só pra simulado (senão o caderno fica concentrado num concurso só).
- Dá pra digitar quantidade assunto a assunto (**Tab pula pra próxima linha**) ou
  mexer só no total ("Todos os assuntos") e deixar o Tec distribuir proporcionalmente
  **respeitando a relevância** — distribuir por Hierarquia fica desbalanceado.
- `EXPORTAR PARA PLANILHA` gera o arquivo com assunto + contagem + frequência acumulada.

Funciona no plano grátis.

### 2.4 "Calcular dificuldade" (pago)

Mostra uma barra em gradiente com a **dificuldade média do caderno em %** e o rótulo
(ex.: 14% = "Muito fácil"). Escala oficial de 5 níveis, atribuída por professor ou
automaticamente pelo desempenho dos alunos.

### 2.5 "Gerar cadernos em série" (pago)

Marca o checkbox e o botão passa a criar o caderno **sem sair da tela de filtro**,
devolvendo só um popup com o link. Duas consequências importantes:

1. Permite montar vários cadernos em sequência mexendo só num filtro por vez.
2. **As questões já usadas nos cadernos anteriores da série são excluídas dos
   próximos** — é assim que se monta uma bateria de simulados sem repetição.

Não funciona quando o único filtro é o de enunciado.

#### Limitação séria do "em série": a distribuição é proporcional, não pedagógica

**Teste real feito em 19/08/2026** (conta Avançado): Língua Portuguesa + Área Fiscal,
sem anuladas nem desatualizadas = **13.916 questões distribuídas em 73 assuntos**.
Distribuição da base:

| Assunto | Questões | % |
|---|---|---|
| Interpretação de Textos (Compreensão) | 3.044 | **21,87%** |
| Outras Questões de Português / Mescladas | 614 | 4,41% |
| Concordância (Verbal e Nominal) | 611 | 4,39% |
| … | … | … |
| Pronomes de Tratamento | 3 | 0,02% |
| Inicial Maiúscula | 2 | 0,01% |
| Pronomes Interrogativos | 1 | 0,01% |

Pedindo um caderno de **20 questões**, o Tec distribuiu assim:
**5 questões de Interpretação de Textos (25% do caderno) + 1 questão em cada um de
outros 15 assuntos + 57 assuntos com ZERO.**

Gerei três cadernos em série (20 questões cada) e conferi o índice dos três:
**a composição temática é idêntica nos três**. As questões não se repetem — isso o
recurso garante —, mas os mesmos 16 assuntos aparecem sempre, com os mesmos pesos,
e os 57 assuntos da cauda longa não entram em nenhum deles.

Duas consequências práticas:

1. **O caderno vira monotemático.** Um quarto de cada caderno é interpretação de texto.
   Pro aluno, resolver quatro cadernos seguidos assim é maçante e não distribui o esforço.
2. **A cauda longa nunca chega.** Como a distribuição proporcional é recalculada igual a
   cada rodada, assunto com poucas questões só entra quando o total do caderno for grande
   o bastante pra que sua fatia arredonde pra 1. Com 73 assuntos e caderno de 20, isso
   só aconteceria com o total lá em cima. Assunto pequeno **pode ser justamente o que
   o edital cobra** — a relevância histórica do banco não é a relevância do edital.

**Conclusão de uso:** "gerar em série" é ótimo pra **simulado** (onde a proporção
histórica é desejável, porque imita a prova) e péssimo pra **plano de estudo por assunto**.
Pra plano de estudo, a distribuição tem que ser definida por fora — ver 2.5-A.

#### O filtro é SEM MEMÓRIA: fora do "em série", cadernos iguais saem idênticos

**Teste real, 19/08/2026** (conta Avançado). Recorte fixo: `Assunto = Crase` +
remover anuladas + remover desatualizadas = **8.596 questões**. Sempre 10 questões por
caderno, quantidade digitada **linha a linha** no "Editar quantidades".

| # | Caderno | Modo | Popular com | Resultado |
|---|---|---|---|---|
| 1 | MANUAL A | sem série | Mais Recentes | conjunto **X** |
| 2 | MANUAL B | sem série | Mais Recentes | **conjunto X — as MESMAS 10 questões** |
| 3 | SERIE C | em série, 1º da série | Mais Recentes | conjunto X de novo |
| 4 | SERIE D | em série, 2º da série (mesma tela) | Mais Recentes | conjunto **Y**, zero sobreposição |
| 5 | SERIE E | em série, **depois de recarregar a página** | Mais Recentes | **conjunto X de novo** |
| 6 | ALEAT F | sem série | Aleatórias | conjunto Z1 |
| 7 | ALEAT G | sem série | Aleatórias | conjunto Z2, zero sobreposição com Z1 |

**Respondendo direto: não, a seleção manual NÃO desconsidera as questões que já foram
pro caderno anterior.** O filtro é stateless. Com "Mais Recentes" ele é determinístico:
mesmo filtro + mesma quantidade = exatamente as mesmas questões, quantas vezes você
gerar. Montar 10 cadernos de 20 questões um a um, com o mesmo filtro, produz
**10 cadernos idênticos**.

**E o "em série" não salva.** O contador muda de "questões *encontradas*" para
"questões *restantes*" e vai descontando (8.596 → 8.586 → 8.576), mas esse estado vive
**só na aba aberta**. Bastou recarregar a página para o contador voltar a 8.596 e o
caderno seguinte repetir o primeiro. Consequências:

- não dá pra montar a série em dias diferentes;
- não dá pra fechar a aba no meio;
- os cadernos já existentes na conta **não** são levados em conta (as 10 questões de
  MANUAL A e MANUAL B continuavam na base quando a série começou).

**"Aleatórias" não é solução.** Evita a repetição na prática (sorteio em 8.596), mas por
probabilidade, não por regra: nada garante que não repita, e você perde o controle de
pegar as questões mais recentes — que é justamente o que interessa num caderno de estudo.

**Conclusão operacional:** para montar vários cadernos sem repetição **e** com controle
de composição, o controle de "o que já foi usado" tem que ser **nosso**, mantido fora do
Tec (planilha com os `#` já distribuídos), e a injeção feita por
**"Adicionar questões por código"**. É a única rota que sobrevive a fechar o navegador.

### 2.5-A Seleção dirigida x geração em série

| | Gerar em série | Seleção dirigida (quantidade por assunto) | Adicionar por código |
|---|---|---|---|
| Quem decide o peso de cada assunto | o banco (frequência histórica) | você / o edital | você / o edital |
| Cobertura da cauda longa | não entra até o caderno ficar grande | entra por decisão sua | total |
| Risco de caderno monotemático | alto | nenhum | nenhum |
| Não repetir entre cadernos | sim, **mas só na mesma aba aberta** | **não — repete tudo** | sim, controlado por nós |
| Sobrevive a fechar o navegador | não | n/a | sim |
| Escolher questão específica | não | não | sim |
| Esforço | um clique por caderno | preencher assunto a assunto | montar a lista fora |
| Rastreabilidade | nenhuma | parcial | total |

**Como fazer a seleção dirigida na prática, em ordem de controle:**

1. **`Editar quantidades` linha a linha** — organizar por *Relevância (apenas assuntos)*,
   *Mais Recentes*, e digitar a quantidade de cada assunto (Tab pula pra próxima linha).
   Dá pra aplicar um teto (ex.: nenhum assunto passa de 10) e um piso (nenhum assunto
   fica em zero). Resolve os dois problemas de uma vez.
2. **Um caderno por assunto ou por bloco do edital** — filtra o assunto, define a
   quantidade, gera; repete. Mais trabalhoso, mas cada caderno fica com identidade
   própria e o aluno enxerga progresso por tópico.
3. **"Adicionar questões por código"** (Configurações do caderno) — monta a lista de
   ids fora da plataforma e injeta. Controle total sobre quais questões entram,
   em que ordem e em que proporção. É a rota pra automação.

Regra prática: **usar a relevância do Tec como diagnóstico, nunca como distribuidor
automático.** Ela responde "o que a banca cobra mais"; quem responde "quantas questões
o aluno faz de cada assunto" é o plano de estudo.

**Segunda regra, que vem do teste de repetição:** o Tec não guarda o que já foi usado.
Qualquer produção de vários cadernos sobre a mesma base precisa de um **controle de
questões já distribuídas mantido por nós** — planilha com os `#` por caderno. Sem isso,
ou os cadernos saem idênticos (Mais Recentes) ou saem sem critério (Aleatórias).

**Desenho recomendado pra skill de montagem de caderno:**
1. Puxar a taxonomia e os pesos por assunto pela API (`/api/assuntos` + relevância).
2. Cruzar com o edital e definir a quantidade por assunto — decisão nossa, registrada.
3. Puxar os `#` das questões candidatas por assunto, na ordem desejada (mais recentes).
4. Manter na planilha o registro do que já foi para qual caderno.
5. Criar o caderno e injetar os `#` por **"Adicionar questões por código"**.
6. Entregar ao aluno **o link do caderno** — nunca PDF de teoria (ver seção 8, item 5).

### 2.6 Filtro por URL — o atalho de automação

A página aceita os filtros na query string, formato indexado:

```
/questoes/filtrar?universo=CONCURSOS&formato=OBJETIVA&f[0].tipo=ASSUNTO&f[0].id=5886&f[1].tipo=ANO&f[1].id=2024&f[2].tipo=FILTRO_QUESTAO&f[2].id=REMOVER_ANULADAS
```

Testado: carrega com "Filtros ativos: 3" e o contador certo. **Dispensa clicar na
árvore**, que é a parte lenta e frágil da automação.

`tipo`: `MATERIA`, `ASSUNTO`, `SEM_CLASSIFICACAO_ASSUNTO`, `BANCA`, `ORGAO`, `CARGO`,
`ANO`, `AREA_CARGO`, `ESPECIALIDADE`, `ESCOLARIDADE`, `PROFISSAO`, `ESFERA`,
`ENUNCIADO`, `FILTRO_QUESTAO`.
`formato`: `OBJETIVA`, `OBJETIVA_INEDITAS`, `DISCURSIVA`.
`universo`: `GLOBAL`, `CONCURSOS`, `OAB`, `CFC`, `VESTIBULAR`, `PASTAS`.

### 2.7 API interna (`/api/...`)

Autenticada por cookie de sessão; base `/api`. Sem contrato público.

| Endpoint | Método | Pra quê |
|---|---|---|
| `/api/enums/universos`, `/api/enums/formatos-questoes`, `/api/enums/grupos-filtro` | GET | enums da tela |
| `/api/enums/areas`, `/api/enums/escolaridades` | GET | árvores com ids |
| `/api/enums/filtros-questao?universo=&formato=` | GET | aba Opções (**exige os 2 params**, senão dá erro de servidor) |
| `/api/materias?universo=&formato=` | GET | 146 matérias com id e data de atualização |
| `/api/assuntos?universo=&formato=&materia={id}&hierarquico=true` | GET | **taxonomia completa** com `id`, `nome`, `hierarquia` ("01.02.03") e `subTree` |
| `/api/bancas`, `/api/orgaos`, `/api/cargos`, `/api/anos`, `/api/profissoes`, `/api/esferas` | GET | listas de filtro |
| `/api/questoes/contagem/filtros` | POST | **contagem** → `{"int": 486}` |
| `/api/assuntos/buscar-questoes-por-asssunto-relevancia` | POST | **lista plana de assuntos com peso** (é o "Relevância (apenas assuntos)") |
| `/api/assuntos/buscar-questoes-por-asssunto-mais-materia` | POST | mesma coisa agrupada por matéria |
| `/api/cadernos/gerar-caderno` | POST | cria o caderno |
| `/api/cadernos/dificuldade-gerador` | POST | calcular dificuldade (pago) |
| `/api/cadernos/configuracao-gerador/download` | GET | exportar para planilha |
| `/api/pastas-cadernos`, `/api/pastas-favoritas`, `/api/usuario/filtros` | GET | pastas e filtros salvos |

(Sim, `asssunto` com três "s" — erro de digitação da própria API.)

Params dos POSTs (form-urlencoded): `universo`, `formato`, `gerarEmSerie`, `ordenacao`,
`filtros[0].tipo`, `filtros[0].id`, `filtros[1].tipo`, …
`ordenacao`: `HIERARQUIA` · `RELEVANCIA` · `RELEVANCIA_ASSUNTOS`. Popular: `RECENTES` · `ALEATORIA`.

Retorno da relevância:
`{"list":[{"id":585,"nome":"Princípios Tributários","tipo":"Assunto","contagem":234,"contagemComentadas":0}, …]}`

### 2.8 Página pública da matéria — plano B sem login

`/materias/{slug}` mostra a árvore inteira de assuntos com, por nó: **nº de questões**,
**nº de comentadas** e teoria separada em **Texto / Vídeo / Mapa Mental**. Cada linha
traz o `id` do assunto e monta os links de filtro prontos. Rota mais barata pra montar
base de mapeamento sem depender de sessão logada.

---

## 3. Cadernos

`/questoes/cadernos/{id}`, abas: **Questões · Índice · Estatísticas · Gabarito ·
Configurações · Imprimir · Compartilhar**, com cronômetro.

### 3.1 Questões
Cada questão traz o número `#` único (é esse o identificador, não o "Questão N de 30"),
banca, ano, cargo/órgão, matéria e assunto, com links diretos pra órgão, banca, matéria,
assunto (aula) e concurso. Botões: comentário do professor, teoria da questão, fórum,
favoritar, anotar, desempenho na questão.

**Navegação:** anterior/próxima, aleatória não resolvida, próxima não resolvida,
voltar/avançar pro assunto anterior/seguinte (**tecla X** = tópico seguinte),
desfazer navegação, próxima favorita, próxima anotada, ir pra questão por número.
**Tecla R remove a questão do caderno** (também dá pelos três pontinhos).
A lista completa de atalhos fica no rodapé de todo caderno.

### 3.2 Índice
Três controles independentes:
- **Organizar por** (agrupamento): Matéria e Assunto · Relevância ▸ · Concurso e Provas ▸ ·
  Banca e Ano · Ano (decrescente) · Área (Carreira) · Formação.
- **Ordenar questões por** (sequência dentro do grupo): Data · **Dificuldade** ·
  ordem de prova (quando agrupado por Concurso e Provas).
- **Exibir questões por**: **Quantidade** (nº de questões por assunto + **percentual**) ou
  **Índice** (posição da questão dentro do caderno, pra pular direto com a tecla P).

Mais: **Expandir/Retrair**, **Remover questões** (seleção em massa — marca tudo e
desmarca o que fica, ou remove um tópico inteiro) e **EXPORTAR PARA PLANILHA**.

Combinações que valem decorar:
- *Matéria e Assunto* + *Dificuldade* → cada assunto começa pela questão mais fácil e
  termina na mais difícil. Boa pra primeira passada (fazer as 10 mais fáceis de cada
  assunto) e deixar as difíceis pra segunda.
- *Concurso e Provas* + *ordem de prova* → a numeração bate com a prova original.
  É o formato pra simulado e pra impressão.
- *Relevância* + *Quantidade* → o "raio X": os assuntos mais cobrados primeiro,
  com o peso de cada um.

### 3.3 Estatísticas / "Resumo do caderno"
Questões, resolvidas, acertos, erros, em branco, anuladas, favoritas, anotadas,
tempo total e médio (com botão de zerar cronômetro); rosca de desempenho com opção
"apenas resolvidas" e comparação com "demais usuários"; pontuação Normal x Líquida;
dificuldade média do caderno; **desempenho por matéria e assunto** (expansível, pago).

Nessa tela cada linha do quadro tem um **botão que gera um caderno novo** com aquele
recorte: todas as questões (réplica do caderno) · resolvidas · **acertadas** ·
**erradas** · em branco · anuladas. É o jeito mais rápido de fazer caderno de erros
de um caderno específico.

No rodapé aparecem **os filtros usados** e o botão **"Copiar Filtros"**, que abre o
gerador já preenchido — serve pra corrigir um caderno que saiu errado sem refazer
filtro por filtro. Depois de regerar, rode "Atualizar resoluções" pra não perder o que
já tinha sido resolvido.

### 3.4 Gabarito (pago)
Folha de respostas: Nº | Alternativa marcada (A–E clicáveis) | Status | Resolvida em |
**Código `#` da questão**. Botão `MARCAR GABARITO` resolve tudo de uma vez.
É a forma mais rápida de **extrair a lista de ids das questões de um caderno**.

### 3.5 Configurações (pago)
- **Atualização de questões** — `VERIFICAR ATUALIZAÇÕES` reaplica o filtro e traz o que
  entrou desde a criação. Pode **adicionar e também remover** questões (o Tec
  reclassifica assunto às vezes).
- **Atualização de resoluções** — importa sua resposta mais recente daquela questão em
  outros cadernos.
- **Filtros utilizados neste caderno** — um **Grupo** por caderno que foi unido
  (caderno unido de 3 = Grupo 1, 2, 3). Cada grupo tem `Selecionar Grupo`,
  `Editar Filtros`, `Copiar Filtros`; e há `COPIAR GRUPOS SELECIONADOS`.
  É por aqui que se atualiza um guia antigo: edita ano/banca/área grupo a grupo.
- **Adicionar questões por código** — cola os números das questões separados por espaço
  e injeta no caderno. **Permite montar caderno a partir de uma lista arbitrária de ids
  produzida fora da plataforma** — a rota mais direta pra automação de "edital → caderno".

### 3.6 Imprimir (pago)
Quantidade máxima de questões (slider) · Início da impressão (a partir da questão N /
aleatoriamente) · Tamanho da fonte (Normal/Grande/Extra grande) · Imprimir texto
associado · Imprimir QR code em cada questão · Cabeçalho (com matéria e assunto / sem /
não imprimir) · Gabaritos (no fim / junto de cada questão / não imprimir) ·
Remover questões (nenhuma / as que resolvi / as que acertei / não favoritas) ·
Espaço para rascunho (não / lateral / entre questões N / entre alternativas N).
**Limite: saldo de 1.000 questões de impressão por dia.**

### 3.7 Menus de caderno e de pasta
- **Caderno (⋯):** Renomear · Criar atalho · Compartilhar · **Unir** · Imprimir · Mover · Excluir.
- **Pasta (⋯):** Mover itens para outra pasta · Excluir um ou mais itens · **Unir cadernos** ·
  **Exportar para planilha** · Criar Subpasta · **Criar caderno a partir da pasta**.
- **Pasta (links):** Renomear · Excluir · **Visualizar como curso** · Carregar desempenho.
- Ordenação da pasta: por nome · por criação · por último acesso.
- Cadernos excluídos vão pra **lixeira** (`/questoes/cadernos-lixeira`) e dá pra recuperar.

### 3.8 "Criar caderno a partir da pasta" — o `universo=PASTAS`
Cria um caderno novo cujo universo de questões é **apenas o que já está naquele caderno
ou pasta**. Serve pra três coisas do dia a dia:
- **fatiar** um caderno grande em blocos por tópico;
- montar **mini-simulados** a partir de um caderno consolidado;
- montar simulado **só das erradas** (combinado com a aba Estatísticas).

### 3.9 Unir cadernos
Seleciona dois ou mais, dá nome ao caderno único e opcionalmente exclui os originais.
O caderno resultante **preserva os filtros de cada origem como grupos**, o que mantém a
capacidade de atualizar cada pedaço separadamente. É o padrão recomendado nos tutoriais:
gerar em série → unir → atualizar por grupo.

---

## 4. Guias de Estudo — o "edital pronto" do Tec

`/guias/` lista guias por concurso (destaque, recentes, de carreira), filtráveis por
área e banca. **São cadernos que a equipe de professores do Tec montou mapeando o
conteúdo programático do edital ponto a ponto contra a taxonomia da plataforma.**

Cada guia de cargo entrega:
- ficha do concurso: **edital em arquivo**, **conteúdo programático (edital
  verticalizado)**, banca, salário, taxa, vagas, prazo de inscrição, data da prova;
- **cadernos prontos por matéria**, agrupados nos blocos do edital (Conhecimentos
  Básicos / Específicos / Especializados), cada um com nº de questões e nº de capítulos
  teóricos, botão `SALVAR` individual e `SALVAR TUDO`;
- um caderno de **questões inéditas** feitas pelo Tec para os pontos do edital sem
  questão real (legislação específica, lei de servidor etc.);
- `Ver detalhes` → **índice completo assunto a assunto com a quantidade de questões**;
- **Observações** dizendo o que o guia não cobre e o que virou questão inédita;
- provas anteriores do mesmo cargo;
- **Análise geral dos concursos anteriores**: distribuição de questões por matéria, em
  número absoluto e em %, filtrável por ano.

### Edital verticalizado
O Tec tem conteúdo próprio ensinando a montar edital verticalizado (pegar o conteúdo
programático e quebrar em linhas/colunas por disciplina → tópico → subtópico, com
colunas de estudo e revisão). Duas situações:
- **Edital publicado** — verticaliza direto do documento oficial.
- **Edital ainda não publicado** — usa o edital anterior *ou* o raio X do próprio Tec
  (assuntos mais cobrados naquele órgão/banca/área nos últimos anos) como proxy.

Dentro do guia, o campo **"Conteúdo Programático"** já traz o edital verticalizado
pronto quando a equipe conseguiu extrair.

### Fluxo oficial de "reaproveitar guia antigo" (tutorial 26)
1. `Guias` → busca o concurso (mesmo de 2021) → `Acessar` → **SALVAR TUDO**.
2. Renomear a pasta com ano/mês da atualização (ex.: `PRF 2026-01`).
3. Em cada caderno: `Configurações` → ver quantos **grupos** existem → `Editar Filtros`
   grupo a grupo: atualizar anos, ajustar banca/área/escolaridade, remover anuladas e
   desatualizadas.
4. `Editar quantidades` → **Relevância (apenas assuntos)** + **Mais Recentes** → aplicar
   um critério de teto por assunto (o professor usa: >100 questões → 25; 30–100 → 18;
   10–30 → 12; <10 → tudo) ou digitar um total e deixar distribuir por relevância,
   subindo pra 1–4 os assuntos que zeraram.
5. `Salvar alterações`. Dali em diante, manutenção = `Verificar atualizações` no grupo
   que representa o ano corrente.

---

## 5. Aulas / teoria e "Visualizar como curso"

`/aulas/materias/{materiaId}/assuntos/{assuntoId}` — cada assunto da taxonomia é um
capítulo com quatro abas: **Aula em texto · Questões · Videoaula · Mapa mental**,
mais "Exercícios do capítulo" filtráveis por ano e banca, e "informar erro deste capítulo".
Recursos da aula (Avançado): **modo leitura** (tela cheia), **marca-texto** em amarelo /
laranja / azul com borracha, **notas adesivas**, **marcar como lido**,
**imprimir o capítulo**.

**"Visualizar como curso"** (link no cabeçalho da pasta) transforma a pasta numa trilha
sequencial:
- barra de progresso teórico **Básico → Intermediário → Avançado → Expert**;
- cada caderno vira uma etapa mostrando **"X de N assuntos"** (não nº de questões);
- dentro de cada assunto: aula em texto, videoaula, mapa mental **e exatamente as
  questões daquele caderno**;
- `marcar como lido` por assunto, com acertos/erros ao lado;
- engrenagem pra **zerar resoluções** do assunto (todas / só as erradas / só as acertadas);
- "Curso completo!" no fim.

**Funciona bem com um caderno grande por matéria; fica ruim se a matéria estiver fatiada
em muitos cadernos.** É o formato de entrega mais próximo de um "plano de estudo pronto"
dentro do próprio Tec.

---

## 5-A. Receitas prontas (extraídas dos tutoriais oficiais)

### Raio X dos temas mais cobrados por banca
1. Filtrar **matéria** + **banca** + **área (carreira)** (+ anos, se quiser recorte).
2. Gerar o caderno.
3. `Índice` → **Expandir** tudo → **Exibir questões por: Quantidade**.
4. **Antes de ler os números, remover as questões sem classificação de assunto**
   (`Editar caderno` → `Remover sem classificação por assunto`) — elas entram no total
   mas não somam em nenhum assunto, e distorcem os percentuais.
5. Ler o % por tópico/subtópico, ou `Organizar por: Relevância` e exportar pra planilha.
6. Repetir com outro recorte (outra área, outra escolaridade) e comparar as planilhas —
   o próprio tutorial sugere jogar as duas numa IA/NotebookLM pra cruzar.

### Caderno de erros (dois caminhos)
- **De um caderno específico:** dentro do caderno → `Estatísticas` → botão ao lado de
  "Erros" → *criar novo caderno apenas com as questões que errou* → escolher pasta.
- **Global, com filtro:** menu `Estatísticas` → escolher período (7 dias / 30 dias /
  personalizado) + matéria + banca + pasta + **dificuldade** → `Selecionar todos` →
  `Gerar caderno com erradas`.
- Dá pra cruzar com **Somente favoritas** pra montar "as favoritas que eu errei nos
  últimos 15 dias".

### Simulado fiel a uma prova real
1. Gerar um caderno do **último concurso** (órgão + cargo + ano, removendo inéditas).
2. `Índice` → `Relevância (com matéria)` → anotar quantas questões cada matéria teve.
3. Na pasta do guia → ⋯ → **Criar caderno a partir da pasta** → selecionar tudo →
   `Editar quantidades` e replicar exatamente aquela distribuição por matéria.
4. Marcar **Gerar cadernos em série** e repetir 3–4 vezes: os simulados saem sem
   repetir questão entre si.
5. Mover tudo pra uma subpasta "Simulados".
6. Pra imprimir: `Índice` organizado por *Concurso e Provas* + *ordem de prova*,
   cabeçalho sem matéria e assunto, gabarito no fim.

### Fatiar um caderno grande em blocos
Pasta/caderno → ⋯ → **Criar caderno a partir da pasta** → selecionar só aquele caderno →
no `Editar quantidades`, marcar apenas os assuntos do bloco → nomear
"Bloco 001 — Regime Jurídico" → **Gerar em série** → repetir por tópico → mover pra subpasta.

### Resolver várias questões de uma vez
Marcar a alternativa de cada questão **sem clicar em "Resolver"**, avançar, e ao final
o site oferece o botão que marca todas como resolvidas de uma vez. (Também dá pela aba
`Gabarito` → `MARCAR GABARITO`.)

### Manutenção periódica de um caderno
- `Configurações` → **Verificar atualizações** (por grupo de filtro) traz as questões
  novas que entraram naquele filtro.
- `Configurações` → **Atualizar resoluções** importa a resposta mais recente que você
  deu àquela questão em qualquer outro caderno. **É irreversível.**
- Quem salvou um guia **recebe e-mail** quando a equipe do Tec atualiza aquele guia.

---

## 6. Estatísticas

Seções: **Meu desempenho · Minha evolução · Atividades · Configuração**, mais
**Grupos de Comparação**. Filtros: período, matéria(s), banca(s), pasta(s), dificuldade.

Em **Configuração**:
- **Modo de pontuação**: Normal (erro não anula) x **Líquida** (erro anula — modo CESPE);
- **Contabilização**: só a última resolução x todas as resoluções;
- **Pesos das matérias** (1 a 10, de meio em meio) e quais matérias aparecem.

**Criar caderno a partir das estatísticas** (Avançado) — filtra período + banca + pasta +
dificuldade + disciplina, marca "as que errei" e gera o caderno. **É o caderno de erros.**

**Grupos de Comparação** — até 10 grupos, por Concurso ou por Área, com ranking e
desempenho por matéria; estatísticas dos últimos 7 dias. Dá também um termômetro de
mercado: hoje a área **Fiscal tem 13.947 membros** e **Tribunais de Contas 4.950**;
entre concursos, SEDES DF 6.692, TJ SP 4.840, SEFAZ GO 4.283, SEFAZ CE 3.216, SRFB 2.773.

---

## 7. Planos e o que cada um libera

| | GRÁTIS R$ 0 | PADRÃO R$ 39,90/30d | AVANÇADO R$ 79,80/30d |
|---|---|---|---|
| Resolver objetivas | 15/dia | ilimitado | ilimitado |
| Filtrar objetivas | sim | sim | sim |
| Favoritar | não | sim | sim |
| Comentário do professor (texto) | 5/dia | sim | sim |
| Comentário do professor (vídeo) | não | **não** | sim |
| Comentário de IA | 5/dia | sim | sim |
| Discursivas (filtrar/resolver/favoritar/fórum/resolução da banca) | não | sim | sim |
| Inéditas: filtrar | sim | sim | sim |
| Inéditas: resolver / fórum / comentário | não | **não** | sim |
| Caderno: criar e excluir | sim | sim | sim |
| Caderno: atualizar, editar, imprimir, unir/manipular, zerar resoluções, organização e distribuição | não | sim | sim |
| Caderno de Favoritas / Caderno de Erros e Acertos | não | sim | sim |
| Modo Leitura | sim | sim | sim |
| Comparar desempenho de caderno | não | **não** | sim |
| Aulas em texto | 1/dia | 3/dia | ilimitado |
| Grifar e anotar aula | não | **não** | sim |
| Vídeos | 1/dia | 3/dia | ilimitado |
| Mapas mentais | não | **não** | sim |
| Guias de estudo | sim | sim | sim |
| Estatísticas: visualizar desempenho | parcial | sim | sim |
| Estatísticas: filtrar / ordenar por assunto | não | sim | sim |
| Estatísticas: criar cadernos, exportar CSV, ordenar por desempenho | não | **não** | sim |
| Grupos de comparação: participar | não | sim | sim |
| Grupos: ranking e desempenho por matéria | não | **não** | sim |
| Modo CESPE e matérias com peso | não | **não** | sim |
| Criação e edição de pastas | não | sim | sim |
| Carregar cadernos na pasta por clique | 10 | 30 | 60 |
| Modo noturno | não | sim | sim |
| Pesquisa de concursos / aplicativo | sim | sim | sim |

Cartão recorrente a cada 30 dias; PIX só por solicitação no WhatsApp. Garantia de 7 dias.

### Testado na prática

**Grátis** — funciona: filtrar por qualquer aba menos "Opções"; contador em tempo real;
`Editar quantidades` com as três ordenações e exportação; gerar caderno; Índice;
Estatísticas do caderno (menos "por matéria e assunto"); Guias completos; páginas
públicas; API interna. Bloqueado: aba "Opções", `Calcular dificuldade`,
`Gerar cadernos em série`, `Configurações`, `Gabarito`, `Imprimir`, criação de pastas.
Curiosidade: os links `Remover anuladas`/`Remover desatualizadas` do painel lateral
"Filtros ativos" funcionam mesmo no grátis, embora a aba esteja bloqueada.

**Avançado** — confirmei funcionando: aba Opções completa; `Calcular dificuldade`
(14% = "Muito fácil" no caderno de teste); Configurações com grupos de filtro,
verificar atualizações, atualizar resoluções e adicionar questões por código;
Gabarito com marcação em lote; Imprimir com todas as opções e saldo diário de 1.000
questões; Índice com 7 formas de organizar; Visualizar como curso; Grupos de comparação.

---

## 8. Limitações que continuam existindo mesmo no plano Avançado

Estas **não** se resolvem pagando:

1. **A taxonomia do Tec não é a do edital.** O próprio Tec avisa: editais não têm
   nomenclatura padronizada, então a plataforma usa classificação própria. Um assunto do
   edital pode estar com outro nome ou dentro de outra matéria. Não existe mapeamento
   automático oficial — o mais perto disso são os Guias, curados manualmente e só
   existentes pros concursos que a equipe cobriu.
2. **Nem toda questão é comentada.** O cadastro corre mais rápido que os professores.
   Filtrar só comentadas encolhe a base.
3. **Nem toda questão tem classificação de assunto.** Existe o nó
   "Sem Classificação (Matéria X)". Matéria, ano, órgão e cargo sempre existem; assunto, não.
4. **Não dá pra baixar comentário de professor nem material teórico.** Só provas,
   gabaritos, editais e cadernos via impressão em PDF. Exportação de dados se limita ao
   "Exportar para planilha" (quantidades / índice / pasta) e ao CSV de estatísticas.
5. **O material teórico é protegido: "proibida a comercialização sem autorização".**
   Dá pra imprimir capítulo pro próprio estudo, não pra redistribuir como produto.
6. **Conta é pessoal e intransferível, com sessão única.** Dois acessos simultâneos
   derrubam um. Trava real pra automação: rodar script enquanto o usuário navega na
   mesma conta desloga alguém.
7. **Impressão tem teto diário de 1.000 questões.**
8. **Não dá pra misturar objetivas e discursivas no mesmo caderno.**
9. **"Gerar cadernos em série" não funciona só com filtro de enunciado.**
10. **Não existe contato direto com professor.** Dúvida vai pro suporte, que intermedeia.
11. **Não existe API pública nem documentada.** O `/api` é interno, sem contrato estável —
    a versão dos assets subiu de `15.2.71` para `15.2.72` no meio deste levantamento.
    Tratar como conveniência, sempre com plano B pela interface.
12. **Dificuldade é estimada, não absoluta** (5 níveis, por professor ou pelo desempenho
    dos alunos).
13. **"Visualizar como curso" só rende com caderno consolidado** — se a matéria estiver
    picada em muitos cadernos, a visão de curso perde a serventia.
14. **Site legado (AngularJS 1.x).** A plataforma recomenda Chrome/Firefox/Edge
    atualizados e trata "erro no site" como problema de navegador.

---

## 9. Bizus de automação

1. **Prefira URL e API a clicar na árvore.** Montar `/questoes/filtrar?f[0]...` ou bater
   em `/api/questoes/contagem/filtros` é ordens de grandeza mais rápido e estável.
2. **Pra montar caderno com seleção arbitrária, use "Adicionar questões por código"**
   (Configurações do caderno): decide os ids fora e injeta de uma vez.
3. **Pra extrair a lista de ids de um caderno, use a aba Gabarito** — a coluna "Código"
   traz o `#` de todas as questões.
4. **Se a árvore bagunçar, recarregue a página** e refaça a sequência.
5. **Clique por `ref` do `read_page`, não por pixel.**
6. **`get_page_text` não é confiável em `/questoes/filtrar`** — com questão de amostra
   na tela ele devolve o `<article>` da questão. Ler por `read_page` ("Filtros ativos:",
   "questões encontradas") ou pelo `innerText` do body.
7. **O seletor de abas do filtro é um `<select>`** (`MATERIAS_ASSUNTOS`, `BANCAS`,
   `ANOS`, `AREAS`, …) — trocar de aba por `form_input` nesse select é mais confiável
   que clicar nos `<li>`.
8. **Painéis de aba só renderizam depois de selecionados.**
9. **Depois de digitar no "Editar quantidades", dar Tab/blur** pro Angular recalcular
   antes de gerar o caderno.
10. **Rodar automação e o usuário navegando na mesma conta = alguém cai.**

---

## 10. Padrões de trabalho combinados com o Elvis

- Roteiro fixo antes de mapear: **disciplina → ano (padrão: últimos 10 anos) →
  banca (padrão: todas; alternativa Cebraspe + FCC + FGV) → área (Fiscal ou
  Gestão e Controle, lembrando que essa se subdivide)**.
- **Sempre** remover anuladas e desatualizadas, sem perguntar.
- Exportação sempre em **"Relevância (apenas assuntos)"** + **"Mais Recentes"**.
- Registrar o **número `#` da questão** em qualquer tabela/relatório.
- Planilha de saída em **Google Sheets** (gspread), não .xlsx.
- Navegador embutido é o padrão; Chrome real só com autorização na hora.

---

## 11. Tabelas de referência

### Áreas (Carreira) — ids da API
```
AGENCIAS_REGULADORAS  Agências Reguladoras
BANCARIA              Bancária e Financeira
CONSELHOS_FISCALIZACAO Conselhos de Fiscalização
DIPLOMACIA            Diplomacia e Comércio Exterior
EDUCACAO              Educação → EDUCACAO_PROFESSORES | EDUCACAO_SERVIDORES
VESTIBULAR            ENEM e Vestibular
EP_SEM                EP e SEM
ESTAGIO               Estágio
EXAMES_PROFICIENCIA_CERTIFICACOES → OAB | CFC e Certificações Contábeis | Demais
EXECUTIVO_GERAL       Executivo (geral)
FISCAL                Fiscal
FORCAS_ARMADAS        Forças Armadas → FORCAS_OFICIAIS | FORCAS_PRACAS
GESTAO_CONTROLE       Gestão e Controle → _CONTROLADORIAS | _TRIBUNAIS | _GOVERNAMENTAL
JURIDICO              Judiciária (Servidores) → TRF | TRT | TRE | TJ | TJM | MP | Defensoria | Procuradoria | Conselho
JURIDICA_AUTORIDADES  Jurídica (Autoridades) → Magistratura (Federal/Trabalho/Estadual/Militar) | Promotoria | Defensoria | Procuradoria | Cartório
LEGISLATIVO           Legislativo
POLICIAL              Policial → Delegados | Peritos | Agentes/Escrivães/Investigadores | Guardas Civis | Penitenciária | Suporte Administrativo
PREVIDENCIARIA        Previdenciária
SAUDE_PAI             Saúde → SAUDE (Servidores) | RESIDENCIA
```

### Matérias de interesse do negócio (com id da API quando conhecido)
Direito Tributário (18) · AFO, Direito Financeiro e Contabilidade Pública (69) ·
Auditoria Governamental e Controle · Contabilidade Geral · Análise das Demonstrações
Contábeis (58) · Contabilidade de Custos · Direito Administrativo (Doutrina e Leis
Federais) · Direito Constitucional (CF/1988 e Doutrina) · Economia e Finanças Públicas ·
Legislação Tributária Federal / dos Estados e DF / dos Municípios · Legislação Aduaneira ·
Administração Geral e Pública (14) · Estatística · Raciocínio Lógico ·
Língua Portuguesa (Português) · Ética no Serviço Público.
(A lista completa das 146 sai de `/api/materias` ou de `/estatisticas/configuracao`.)

---

## 12. Contas

- `aaroneatsl.int@gmail.com` — **Plano Grátis**. Conta de exploração.
  **Não migrar de plano sem autorização.** Ficou lá um caderno de teste
  "TESTE CLAUDE - Dir Tributario 10q".
- `bizu.cadastros@gmail.com` — **Plano Avançado**, conta zerada usada pra validar os
  recursos pagos em 19/08/2026. Ficou lá um caderno de teste "TESTE CLAUDE - exploracao".
- `saidacasernacadastros@gmail.com` — Plano Avançado usado na seção "Mapear Aulas", com
  pastas por concurso (TCDF, TCU, SEFAZ CE, SEFAZ DF, SEFAZ RN, Manaus, Campina Grande,
  Caxias do Sul).
- `aaroncelular@gmail.com` — grátis, testes anteriores.

---

## 13. Fontes

- Navegação direta na plataforma em 18–19/08/2026 (contas grátis e Avançado).
- Canal oficial: <https://www.youtube.com/@Tec.Concursos>
- Playlist oficial **"Tec Concursos | Tutoriais"** — 29 vídeos, prof. Wilson Tavares:
  <https://www.youtube.com/playlist?list=PLX-4skTGVrWVyjFBm2rWrHWoDt3cK8xIK>
- Mais 22 tutoriais avulsos do canal, fora da playlist (Resumo do caderno, Índice,
  atualizar questões/resoluções, filtros por órgão/esfera, caderno de erradas,
  simulado pelos guias, edital verticalizado, #TecResponde).
- **Transcrições de todos os 51 vídeos** salvas em `_contexto/tecconcursos-transcricoes/`.
- Playlist **"Comece por aqui (atualizado para a nova versão do site)"**:
  <https://www.youtube.com/playlist?list=PLX-4skTGVrWXQ_dCFcesuqZyHvoUzQnvg>
- Página de planos: <https://www.tecconcursos.com.br/assinar>
- Central de ajuda: <https://tecconcursos.zendesk.com/hc/pt-br/categories/48370657066651-Como-usar-o-Tec-Concursos>
- "Comece por aqui": <https://tecconcursos.zendesk.com/hc/pt-br/articles/48231812184475-Comece-por-aqui>
- "Principais ferramentas": <https://tecconcursos.zendesk.com/hc/pt-br/articles/48231250314523-Principais-ferramentas-do-Tec-Concursos>
