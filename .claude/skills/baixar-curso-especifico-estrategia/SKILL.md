---
name: baixar-curso-especifico-estrategia
description: >
  Baixa em lote os livros eletrônicos (PDF) de um curso específico do Estratégia
  Concursos, aula por aula, renomeando e organizando os arquivos numa pasta local.
  Prioriza a versão simplificada do livro; se não houver, usa a versão original.
  Use quando o usuário disser "baixa esse curso do Estratégia", "baixa os livros
  da matéria X", "sincroniza esse curso pra pasta", "atualiza o curso que já
  baixei", ou mandar um link de um curso do estrategiaconcursos.com.br pedindo
  pra organizar os PDFs.
---

# /baixar-curso-especifico-estrategia — Download em lote de livros do Estratégia Concursos

## O que essa skill faz

Usa o Chrome real do usuário (via extensão Claude in Chrome, já logado no Estratégia
Concursos) pra navegar pelas aulas de um curso, e baixa direto no disco — sem passar
pela pasta de Downloads — o livro eletrônico de cada aula, renomeado e organizado
numa pasta local.

## Passo 0: Perguntas obrigatórias no início

**Pasta padrão:** `G:\Meu Drive\Inteligência Artificial\Estrategia`
— é aqui que as pastas novas são criadas por padrão, salvo o usuário indicar
outro local. **Essa pasta vive dentro do Google Drive sincronizado**, então
antes de usar ela (seja pra criar algo novo, seja pra checar uma atualização),
**verificar que ela existe de fato no disco** (`Test-Path` / `ls`). Por ser uma
pasta sincronizada, pode não estar montada/sincronizada no momento — se não
existir, avisar o usuário em vez de simplesmente criar uma pasta nova do zero
sem querer em outro lugar.

Sempre perguntar as coisas abaixo antes de fazer qualquer coisa (não assumir, não pular):

1. **Link do curso** — a URL da página do curso no Estratégia Concursos (a página
   que lista "Aula 00, Aula 01..." — normalmente
   `https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{id}/aulas`).
2. **Pasta:** perguntar se quer usar a **pasta padrão** (acima) ou indicar um
   **novo local**. Se confirmar a pasta padrão, usar ela direto. Se pedir outro
   local, usar o caminho informado.

**Não perguntar aqui se é "novo ou atualização"** — isso é descoberto sozinho no
Passo 3, depois de identificar a matéria (Passo 1-2) e procurar automaticamente
por uma pasta já existente dentro do local informado. Ver Passo 3.

3. **Base de siglas de disciplinas (pergunta temporária, perguntar sempre que
   a skill for carregada):** perguntar se já existe alguma planilha/tabela de
   referência com nome de disciplina → sigla. **Hoje essa base ainda não
   existe** — enquanto não existir, seguir usando o nome completo da matéria
   no nome da pasta (padrão atual do Passo 2). Quando o usuário criar essa
   base no futuro, ele vai indicar — a partir daí, usar a sigla da disciplina
   no lugar do nome completo ao montar o nome da pasta. Até lá, essa pergunta
   serve só de lembrete pro usuário, não bloqueia o fluxo. **Por que isso
   importa:** confirmado pelo Elvis em 2026-08-18, depois de um caso real em
   que somar o sufixo de data (Passo 2) ao nome já grande da matéria estourou
   o limite de 260 caracteres do Windows num arquivo — usar sigla no lugar do
   nome completo da matéria é a forma mais eficaz de ganhar margem de caminho
   de forma permanente, em vez de só sintetizar nome de arquivo caso a caso.

**PERGUNTA 0 — QUAL MODO?** Antes de qualquer outra, e sem exceção:

> `baixar` (não existe no disco) · `atualizar` (existe, atualiza o que mudou) ·
> `conferir` (só lê e relata, não escreve nada)

Se o usuário não disser, **a existência da pasta decide** entre `baixar` e
`atualizar` — mas confirmar com ele antes de escrever qualquer coisa. Se ele
disser "confere", "dá uma olhada", "o que mudou?", é `conferir`.

**O modo escolhido muda o que cada passo faz daqui pra frente**, e cada passo diz
o que muda. Ver a seção "Modos de execução" logo abaixo.

**Se o modo for `conferir`, NÃO seguir a numeração dos passos** — ir direto para
o "Caminho curto do `conferir`", ao fim da seção de modos, e encerrar ali.

Não seguir em frente sem as respostas 1 e 2 acima.

**Reduzir o tamanho do caminho é uma preocupação constante, não só nos casos
óbvios** — confirmado pelo Elvis em 2026-08-18. Sempre que for nomear pasta ou
arquivo, já pensar no caminho completo resultante (ver orçamento de
caracteres nos "Detalhes técnicos" mais abaixo) e preferir a versão mais curta
que ainda deixe a aula identificável — não esperar bater no limite pra só
então cortar.

## Modos de execução: `baixar`, `atualizar`, `conferir`

**Confirmado pelo Elvis em 22-08-2026.** As duas skills de download continuam
**separadas por escopo** (uma disciplina x pacote inteiro), e o **modo é
perpendicular ao escopo**: cada skill aceita os três modos. Não fundir as skills.

| Modo | O que faz | Escreve no Drive? |
|---|---|---|
| `baixar` | material não existe no disco. É o fluxo clássico da skill. | sim |
| `atualizar` | material existe. Baixa para temporário, **compara conteúdo** e só escreve o que mudou. | só o que mudou |
| `conferir` | **não baixa e não escreve nada.** Lê o disco contra a plataforma e relata divergência. | não |

**Perguntar o modo no Passo 0** quando o usuário não disser. Na dúvida entre
`baixar` e `atualizar`, a existência da pasta decide.

### O que `atualizar` NÃO faz

**Não rebaixa PDF de aula que já está no disco e íntegro.** Refazer o download de
material já validado é gastar exatamente o volume de requisição que dispara
bloqueio na plataforma, para chegar no mesmo byte. Só baixa:

- aula que existe na plataforma e **não** existe no disco;
- aula cujo `hash_conteudo` divergiu (ver abaixo);
- **apoio** (resumo e mapa mental), que nunca foi baixado.

**Nunca apaga e recria pasta** (regra 4 do `bases/NOMENCLATURA.md`). Renomeia em
cima, e grava log `de -> para` num CSV na pasta de logs.

### `hash_conteudo` — a assinatura que diz se o material mudou

A plataforma **não expõe data de atualização** do PDF (só `data_publicacao`, que é
quando a aula entrou no ar). E **hash de arquivo não serve**: o PDF é marcado por
download, então o mesmo arquivo baixado 4 vezes dá 4 hashes de bytes diferentes,
com tamanho variando ~100 bytes.

O que funciona:

```
hash_conteudo = sha256( texto extraído com a linha da marca d'água removida )
```

Medido em 22-08-2026: 4 downloads do mesmo arquivo deram **texto idêntico**
(4.598 caracteres, mesmo sha) — a marca é constante **para a mesma conta**. A
remoção continua obrigatória por dois motivos: comparar entre **contas
diferentes** (coleta x produção), e não deixar dado pessoal circular.

**Filtros baratos antes do hash:** número de páginas e data da capa. Se qualquer
um mudou, mudou de verdade. Se os dois estão iguais, o hash decide.

> ### REGRA 8 — filtrar a marca d'água ANTES de gerar qualquer nome
>
> O padrão `^\s*\d{11}\s*-\s*.+$` (CPF e nome do titular) está na camada de texto
> de quase toda página, **capa inclusive**. O slug do apoio sai do título da capa.
> Se a extração vier antes do filtro, **o CPF entra no nome do arquivo**, vai para
> o Drive e aparece em qualquer print de tela.
>
> Filtrar na **extração**, antes do hash, antes do slug, antes de qualquer uso.
> Ver `bases/DECISOES.md`, seção "Marca d'agua do Estrategia".

### Caminho curto do `conferir` (não passa pelos passos de download)

**`conferir` tem caminho próprio e termina aqui.** Não entra nos Passos 4 em
diante. O motivo é prático: "faça tudo mas não escreva" erra fácil, e o erro
grava no Drive.

1. **Levantar a plataforma:** lista de aulas pela API (Passo 5A), com `id`,
   rótulo, `is_disponivel`, `data_publicacao`, e quais vídeos têm `resumo` /
   `mapa_mental`.
2. **Levantar o disco:** PDFs, placeholders `.txt`, apoio na subpasta, e o
   `_manifesto.csv` se existir.
3. **Comparar e relatar**, sem escrever nada:
   - aula na plataforma e não no disco;
   - aula no disco e não na plataforma (renomeada ou removida na origem);
   - `hash_conteudo` divergente do manifesto (teoria mudou);
   - apoio novo que ainda não foi baixado;
   - nome de pasta ou arquivo fora do padrão do `bases/NOMENCLATURA.md`;
   - caminho passando de 240 caracteres.
4. **Encerrar com o relatório.** Nenhuma gravação: nem PDF, nem planilha, nem
   `_manifesto.csv`, nem renomeação, nem troca de matrícula.

**Divergência que não der para explicar: parar e reportar ao Elvis.** Não tentar
corrigir dentro do `conferir` — ele é o modo em que nada se escreve.

## Nome de pasta e de arquivo: seguir `bases/NOMENCLATURA.md`

**Este documento não redefine nomenclatura.** O padrão é transversal e vive em
`bases/NOMENCLATURA.md` — ler antes de gravar qualquer arquivo. Resumo do que mais
pega nesta skill:

```
Estrategia\<Concurso> (<Sigla>) <Ano> (<DD-MM-AAAA>)\<Tipo de Curso>\<SIGLA> - <Disciplina>```

- **Regra 1 — não repetir o que o pai já diz.** A pasta da disciplina não repete o
  concurso nem a data; o arquivo não repete a disciplina. Medido em 22-08-2026:
  aplicar só essa regra leva **157 arquivos acima de 240 caracteres para zero**, e
  o pior caminho de 263 para ~230. **É ela que resolve o limite de 260 do Windows**
  — o prefixo de sigla até consome 8 caracteres, é organização, não espaço.
- **Regra 2 — a sigla é nossa, o nome é da fonte.** Sintetizar pode, traduzir não.
- **Regra 3** — primeira letra maiúscula. **Regra 4** — nunca apagar e recriar.
- **Regra 5** — o nome do arquivo vem da capa do PDF. **Regra 6** — pendência vira
  `(N-M)` no nome da pasta.
- **Regra 8** — filtrar a marca d'água antes de gerar qualquer nome (ver acima).

**Encurtar é o padrão, não a exceção:** cortar o nome já na gravação e, se depois
houver critério de classificação, renomear em cima. Para renomear caminho longo no
Windows, usar o prefixo estendido (`\?\` + caminho absoluto) — sem ele o próprio
rename falha com "caminho não encontrado".

**A sigla vem de `bases/01-disciplinas/dados/renomear-pastas.csv`.** Linha marcada
`pendente` fica **com o nome atual, sem prefixo** — nunca chutar sigla.

## Apoio: resumo e mapa mental (obrigatório em `baixar` e `atualizar`)

**Resumo e mapa mental não são da aula: são de cada VÍDEO dentro dela.** No objeto
do vídeo (`/api/aluno/aula/{id}` -> `videos[]`) existem os campos `resumo`,
`slide` e `mapa_mental`, preenchidos quando existem e `null` quando não. Rota:

```
/api/video/{videoId}/download/{resumo|mapa_mental|slideshow}
```

**`slideshow` não interessa** — só resumo e mapa mental.

### Deduplicação: o mesmo arquivo serve vários vídeos

O link é por vídeo, mas o arquivo é compartilhado. No piloto de Direito
Constitucional, 42 links deram **32 arquivos distintos**. Deduplicar **pelo nome
do arquivo no CDN**, que é estável — nunca por hash (marca por download). Conferir
com páginas + primeira linha do texto.

**Baixar uma vez, indicar uma vez.** A aula vira **coluna com lista de valores**,
nunca parte do nome do arquivo.

### Onde salvar e como nomear

Subpasta única por disciplina, **sem subpasta por aula** (regra 7 do
`bases/NOMENCLATURA.md`):

```
<SIGLA> - <Disciplina>/
└── Apoio - Resumos e Mapas Mentais/
    ├── R - <assunto>.pdf
    └── MM - <assunto>.pdf
```

O slug vem **do título da capa do PDF** (regra 5), até 40 caracteres, com a marca
d'água filtrada antes (regra 8). Sem título utilizável na capa, cai para o título
do vídeo — e a planilha registra qual fonte foi usada.

### O que descartar

- **Arquivo sem conteúdo (só capa).** Caso real: `apznza-2.pdf`, 1 página, apenas
  "MAPAS MENTAIS – Direito Constitucional / Material compilado pelo Estratégia".
- **`slideshow`**, sempre.

### Dois tipos de resumo, e por que isso importa na minutagem

| Tipo | Como reconhecer | Escopo |
|---|---|---|
| compilado | abre com "APRESENTAÇÃO DO MATERIAL — Queridos alunos!!" (p1) e folha de rosto com o tema (p2) | tema inteiro, 4 a 12 páginas |
| pontual | vai direto ao assunto | 1 tópico, ~2 páginas |

Registrar `paginas` **e** `paginas_conteudo` (descontando apresentação e folha de
rosto). O plano cobra **5 min por página**; contar bruto cobraria 10 minutos de
nada em cada resumo compilado.

## Saída de dados: `_manifesto.csv` + planilha (a partir da MESMA estrutura)

**Planilha publicada é vista, nunca fonte.** A base 2 precisa ler o levantamento
sem OAuth, sem rede e com diff no git. Então cada disciplina recebe **os dois**:

| Arquivo | Quem lê |
|---|---|
| `_manifesto.csv`, na pasta da disciplina | as skills das bases (e o `git diff`) |
| planilha `<SIGLA> - Metadados` no Sheets | o Elvis |

**Os dois saem da mesma estrutura em memória, na mesma passada — nunca um a partir
do outro**, senão divergem. E o CSV é gravado **antes** de qualquer chamada de
rede: assim um `429` do Sheets não derruba a execução, porque o dado já está em
disco.

### Colunas novas na aba `Aulas`

Acrescentar, **não reescrever** as que já existem:

- `Cód Mestre` — preencher quando `bases/01-disciplinas/dados/renomear-pastas.csv`
  já tiver a sigla daquela disciplina; deixar **vazia** nas marcadas `pendente`.
  **Nunca chutar sigla:** sigla errada contamina o Cód Mestre, que é o número que
  não pode mudar depois de publicado.
- `Hash Conteúdo`
- `Alterado em` — data em que o hash mudou pela última vez.

### Aba nova `Apoio`

`Tipo` (R / MM) · `Assunto` (o slug) · `Arquivo` · `Aulas` (lista, aceita mais de
um valor) · `Fonte do nome` (capa / vídeo) · `Páginas` · `Páginas conteúdo` ·
`Cód Mestre`.

## Gatilho de impacto no fim do `atualizar`

Skill não é ilha: download alimenta a base 2, que alimenta o mapeamento, que
alimenta os cadernos. **Material atualizado sem reprocessar a base deixa a base
mentindo**, apontando para páginas e blocos que mudaram de lugar — e o erro só
aparece lá na frente, num caderno com tópico errado, quando já não dá para saber
de onde veio.

Então o modo `atualizar` **termina escrevendo em `bases/IMPACTOS.md`** o que mudou
e perguntando ao Elvis se é para rodar também a skill da base que consome aquele
material. A máquina já existe: é o `IMPACTOS.md` que toda base lê ao começar e
escreve ao terminar.

## Passo 1: Escolher o navegador, abrir o curso e identificar matéria / concurso / cargo

1. **Escolher qual navegador controlar, antes de carregar qualquer tool:**
   - **Navegador embutido (Browser pane, `mcp__Claude_Browser__*`) é o padrão**
     — confirmado pelo Elvis em 2026-08-18. Usar esse por padrão sempre que o
     usuário não pedir explicitamente o Chrome. Essas tools já vêm carregadas
     por padrão, **não precisa de `ToolSearch`** — só confirmar o estado atual
     com `tabs_context` antes de navegar. Se a sessão estiver deslogada
     (redirecionar pra tela de login), avisar o usuário e esperar ele logar —
     nunca tentar digitar credenciais.
   - **Claude in Chrome (`mcp__claude-in-chrome__*`)** — **só usar com
     autorização prévia do usuário na própria conversa**, pedida a cada vez que
     for considerar essa alternativa (não vale autorização de uma sessão
     anterior). Se em algum momento parecer que vale a pena trocar pro Chrome
     (ex: navegador embutido indisponível ou deslogado), **perguntar antes de
     tentar** — nunca trocar de navegador sozinho no meio do processo sem
     avisar. Quando autorizado, carregar via `ToolSearch` com
     `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__browser_batch,mcp__claude-in-chrome__javascript_tool`
   - Se ficar ambíguo qual dos dois usar (nenhum sinal claro na mensagem do
     usuário), perguntar antes de prosseguir — evita carregar/tentar navegar
     no navegador errado.
   - **Tabela de equivalência** (os passos daqui pra frente na skill usam os
     nomes genéricos da esquerda — trocar pela tool real do navegador
     escolhido):

     | Ação genérica | Claude in Chrome | Navegador embutido |
     |---|---|---|
     | Navegar pra URL | `navigate` | `navigate` |
     | Rodar JS na página | `javascript_tool` | `javascript_tool` |
     | Ler texto da página | `get_page_text` | `get_page_text` |
     | Screenshot / clique | `computer` | `computer` |
     | Contexto de abas | `tabs_context_mcp` | `tabs_context` |
     | Buscar elemento | `find` | `find` |

   - **Mecânica de download é a mesma nos dois navegadores** (ver Passo 5) —
     a diferença é só qual conjunto de tools chamar. Não depende de clicar em
     card nem abrir aba, então a instabilidade de clique em coordenadas
     observada no navegador embutido não afeta esse fluxo.
2. Navegar até o link do curso. Se o navegador pedir aprovação de domínio (ou
   login, no caso do navegador embutido), é normal na primeira vez.
3. Ler o título da página / cabeçalho do curso pra extrair:
   - **Matéria** (ex: Direito Constitucional)
   - **Sigla do concurso** (ex: TCDF) — geralmente já vem entre parênteses no título
   - **Cargo** (ex: Analista Administrativo de Controle Externo)
4. **Sigla do cargo:** se não tiver uma sigla óbvia already no título (tipo "ANACE"),
   pesquisar (na própria página do curso ou na internet) pela sigla oficial do cargo
   pro concurso em questão, e decidir sozinho — não precisa confirmar com o usuário.
5. **Sigla do concurso quando não vem óbvia entre parênteses:** pesquisar no Google
   (cruzando com o próprio site do Estratégia Concursos como referência) pelo nome
   do concurso/edital pra achar a sigla oficial ou a forma abreviada mais usada.
   Manter a sigla como ela realmente é usada — não forçar juntar palavras num
   bloco só se o uso comum mantém espaço (ex: o concurso "ISS Manaus" usa a sigla
   com espaço mesmo, `ISS Manaus`, não `ISSMANAUS`).
6. **Curso "Regular" sem concurso específico:** alguns cursos não pertencem a
   um concurso/edital específico — fazem parte de um pacote genérico por área.
   **O sinal pra reconhecer esse caso é a própria palavra "Regular" no nome do
   pacote/curso** (ex: pacote "Curso Regular para Área Fiscal" → é o pacote
   "Regular Fiscal"; existe também "Regular Controle"), não a ausência de
   sigla de edital. **Atualizado em 22-08-2026:** esse identificador NÃO vai
   mais no nome da pasta da disciplina (REGRA 1) — ele vira o **nome da pasta do
   concurso**, um nível acima: `Regular Fiscal\Curso Regular\DADM - Direito
   Administrativo (18-08-2026)`. Não precisa perguntar ao usuário quando
   reconhecer esse padrão.
7. **"Reforma Tributária" conta como disciplina própria** — confirmado pelo
   Elvis em 2026-08-17. Se o curso pedido for de Reforma Tributária, tratar
   normalmente como qualquer outra matéria (não descartar, não tratar como
   "extra"). **Atenção:** dentro de um pacote pode existir mais de um curso de
   Reforma Tributária ao mesmo tempo (cobrindo frentes diferentes da reforma —
   não são duplicados) — se o usuário pedir "o curso de Reforma Tributária" de
   forma genérica nessa situação, confirmar qual dos cursos ele quer, ou
   sugerir rodar a skill `baixar-curso-completo-estrategia` no pacote inteiro,
   que já sabe agrupar todos eles numa pasta-mãe `Reforma Tributária` com uma
   subpasta por curso.

### Pacote não matriculado? Rodar o rodízio de matrículas antes de tudo

**Confirmado pelo Elvis em 19/20-08-2026.** A assinatura vitalícia do Estratégia
permite **no máximo 3 produtos matriculados ao mesmo tempo**. Produto que não
está em "Produtos matriculados" não abre: a página do pacote vem vazia e a API
devolve **HTTP 500**. Atenção: **500 significa "sem matrícula", não "curso
removido"** — não concluir que o material sumiu com base nisso.

Em `/app/dashboard/assinaturas`:

1. Ler o bloco **"Produtos matriculados"**. Se o produto alvo já estiver lá,
   seguir normalmente.
2. Se não estiver e os 3 slots estiverem cheios, **liberar um slot**: clicar
   `DESMATRICULAR` no produto que vai sair, digitar `CORUJA` e confirmar.
3. Buscar o produto alvo na aba **PACOTES** do bloco "Matricular em novos
   produtos", clicar `MATRICULAR` e digitar `CORUJA`.
4. Recarregar e confirmar que ele apareceu em "Produtos matriculados", com o
   `href` `/app/dashboard/pacote/{id}`.

Regras desse rodízio:

- **A palavra `CORUJA` vale nos dois sentidos** — matrícula e desmatrícula.
- **Qualquer pacote pode entrar ou sair do rodízio, inclusive o da PRF.** Fazer
  a troca quando a tarefa pedida exigir, sem perguntar de novo.
- **Antes de desmatricular, checar a pasta daquele pacote no Drive por
  placeholders `.txt`** (aulas ainda não publicadas) e avisar o Elvis quantas
  são: enquanto o pacote estiver fora, essas aulas não podem ser baixadas.
- Ao terminar, atualizar a coluna `Matriculado hoje` da aba `Produto` no índice
  do pacote (Passo 11B) dos pacotes afetados — o que entrou e o que saiu.

### Buscar no catálogo é sempre por PACOTE, nunca por curso

**Confirmado pelo Elvis em 20-08-2026, depois de um falso negativo real.** O que
o usuário chama de "curso" (ex: "Regular Fiscal") é um **pacote** no Estratégia.
As disciplinas dentro dele têm nomenclatura diferente e não repetem o nome do
pacote: o pacote `Curso Regular para Área Fiscal - Pacote Completo` (id 220865)
contém `Concursos da Área Fiscal - Curso Básico de Direito Administrativo`
(id 220883). Procurar por "Curso Regular ... Direito Administrativo" não acha
nada, e dá a impressão errada de que o produto saiu do catálogo.

Usar a busca interna do catálogo, com o mesmo Bearer dos outros passos:

```
GET /api/assinatura/curso/search?q=<nome>&type=pacote&size=51&page=N
```

Ela devolve `id` + `nome` de cada pacote — é a fonte pra preencher a aba
`Produto` do índice (Passo 11B) e pra achar o `Pacote ID` de qualquer produto,
matriculado ou não. Só descer pra `type=curso` quando o alvo for reconhecidamente
uma disciplina avulsa.

## Passo 2: Nomear a pasta da disciplina (padrão `bases/NOMENCLATURA.md`)

> **Reescrito em 22-08-2026, autorizado pelo Elvis** (`agentes/AUTORIZACOES.md`).
> O padrão antigo `Matéria (SIGLA_CONCURSO-SIGLA_CARGO) (DD-MM-AAAA)` **está
> extinto** — não conviver com ele, não usar como alternativa. Ele repetia no
> nome da pasta o concurso que o nível de cima já dizia, e foi a causa medida do
> caminho de 263 caracteres contra o limite de 260 do Windows.

### O formato

```
<SIGLA> - <Nome que a fonte usa> (<DD-MM-AAAA>)
```

Exemplo: `DCONST - Direito Constitucional (18-08-2026)`

| Parte | De onde vem | Teto |
|---|---|---|
| `<SIGLA>` | `bases/01-disciplinas/dados/renomear-pastas.csv`, coluna `sigla` | — |
| `<Nome que a fonte usa>` | o nome do curso **no Estratégia**, sintetizado se preciso, **nunca traduzido** | 45 com a sigla |
| `(<DD-MM-AAAA>)` | data desta atualização **desta disciplina** (REGRA 9) | 13 |
| `(N-M)` | marca de pendência, quando houver (REGRA 6) | 6 |

Teto do nível disciplina: **64** (45 + 13 + 6). Teto do arquivo: **92**. Mas
**os tetos são guarda-corpo, não orçamento**: eles não somam o limite, porque os
níveis não estouram juntos. **A regra que manda é uma só — nenhum caminho real
pode chegar a 240.**

**A pasta do concurso (nível 1) NÃO leva data** — ela desceu para cá em
22-08-2026. Motivo: com o modo `atualizar`, a atualização é **por disciplina**;
uma data no nível do concurso passa a mentir assim que uma única matéria for
atualizada. **Não pode ficar nos dois lugares:** são duas versões da mesma
verdade, e elas divergem.

**Nunca repetir aqui o concurso, o cargo nem o tipo de curso.** Eles já estão nos
níveis de cima (REGRA 1).

### A sigla

Sai do `renomear-pastas.csv`, coluna **`pasta_nova_sem_data`**, que já vem com a
regra 1 aplicada e conferida contra o teto. **A data é acrescentada por esta
skill**, não vem do CSV — por isso o nome da coluna. Casar pela coluna
`pasta_atual_no_disco`, **por igualdade**, nunca por prefixo. As colunas `chars` e
`chars_com_data` trazem o comprimento já calculado, para conferência.

**Estado em 22-08-2026:** 34 linhas, 33 `ok` e 1 `pendente`. A antiga `LTRIB` foi
desdobrada em **`LTEST`** (Legislação Tributária Estadual), **`LTMUN`**
(Municipal) e `LTFED` — não usar `LTRIB`, que não existe mais.

**Linha marcada `pendente` fica com o nome atual, sem prefixo.** Nunca chutar
sigla: sigla errada contamina o Cód Mestre, que é o número que não pode mudar
depois de publicado. Pasta sem sigla qualquer um vê que falta; pasta com sigla
errada ninguém percebe.

**Se a disciplina não estiver no CSV** (curso novo), gravar sem prefixo e
registrar a falta no relatório final, para a base 1 atribuir a sigla depois.

### Depois de renomear, devolver o estado

Toda renomeação **atualiza a coluna `pasta_atual_no_disco`** do
`renomear-pastas.csv` com o nome novo. Sem isso o CSV vira histórico em vez de
estado, e o `conferir` da base 1 deixa de casar. Gravar também o log
`de -> para` num CSV na pasta de logs — renomeação é reversível, mas só com log.

### Duas matérias com o mesmo nome no mesmo curso

Caso real: duas "Contabilidade Geral e Avançada", uma por professor. Diferenciar
pelo nome do professor, que aparece no título do curso no site:

```
CONTAB - Contabilidade Geral e Avançada - Possati (18-08-2026)
CONTAB - Contabilidade Geral e Avançada - Cardozo (18-08-2026)
```

**A mesma sigla nas duas é esperado e correto** — são a mesma disciplina nossa,
dois professores. Não forçar numa pasta só. Reconhecer o padrão sozinho, sem
perguntar ao usuário.

### Comprimento

O que manda **não é a soma dos tetos, é o caminho real chegar a 240**. Se chegar,
**quem encurta é o nome do ARQUIVO, nunca o da pasta** (REGRA 10): a pasta é
identidade e aparece em toda a base; o nome do arquivo é descrição e os títulos
do Estratégia trazem gordura de sobra. Encurtar pelo fim do tema, preservando
sempre `Aula NN`, a versão (`LS`/`LC`) e a data.

**Conferir a data de hoje no ambiente antes de montar o nome** — não copiar das
pastas vizinhas nem das datas citadas nesta skill. Erro real em 19-08-2026: tudo
nasceu com a data de ontem e obrigou a corrigir pastas, placeholders e planilhas.

## Passo 3: Procurar pasta existente antes de criar (detecção automática)

**Escopo da busca: só dentro da pasta informada no Passo 0** (a pasta padrão ou
o outro local que o usuário indicou) — nunca varrer o computador inteiro nem
outras pastas fora dali.

Com o nome definido no Passo 2, procurar dentro dessa pasta por uma subpasta já
existente que corresponda a essa matéria. **Comparação:**
- Ignorar maiúsculas/minúsculas e acentuação (ex: "direito constitucional" bate
  com "Direito Constitucional").
- Ignorar um eventual prefixo `(N-M)` (ex: `(10-20) Direito Constitucional
  (TCDF-ANACE)` bate com `Direito Constitucional (TCDF-ANACE)`).
- Ignorar o sufixo de data `(DD-MM-AAAA)` no final do nome (ex: `Direito
  Constitucional (TCDF-ANACE) (10-03-2026)` bate com `Direito Constitucional
  (TCDF-ANACE)`).

**Conferir o Curso ID do Estratégia antes de tratar como atualização —
crítico, confirmado pelo Elvis em 2026-08-18.** Se a pasta encontrada já tiver
uma planilha de metadados (ver "Planilha de metadados da disciplina" mais
abaixo), ela registra o Curso ID usado na última coleta (visível na URL
`/cursos/{id}/aulas`). Comparar esse ID registrado com o ID da URL fornecida
agora:
- **Se o ID for igual:** seguir normalmente como atualização da mesma pasta.
- **Se o ID for diferente:** **avisar o usuário logo no início, antes de
  prosseguir** — **não decidir sozinho se é o mesmo curso ou um curso novo.**
  Motivo: a Estratégia às vezes atribui um ID novo a um curso mantendo o
  mesmo conteúdo (mesmas disciplinas/aulas) — o ID muda mas não é
  necessariamente um curso diferente. **O critério real de identidade são as
  disciplinas e aulas em si, não o ID isolado.**
  - **Antes de avisar, já dar contexto pra decisão** — confirmado pelo Elvis
    em 2026-08-18: abrir a `Aula 00` (ou a primeira aula da listagem) tanto
    na planilha antiga quanto no site com o ID novo, e comparar o assunto
    registrado com o assunto atual. Incluir essa comparação no aviso, ex: "o
    Curso ID mudou de {antigo} pra {novo}; a Aula 00 registrada era
    '{assunto antigo}', a Aula 00 do novo ID é '{assunto novo}' — parecem o
    mesmo curso, mas confirma antes de eu atualizar?". Isso poupa o usuário
    de ter que investigar do zero um alerta seco.
  - Mesmo com essa comparação sugerindo que é o mesmo curso, sempre vale
    comparar o conteúdo completo (Passo 4 em diante) antes de concluir — a
    comparação da Aula 00 é só um indício rápido, não a decisão final.
  - Se não existir planilha de metadados ainda (pasta de uma coleta anterior
    a essa funcionalidade), não tem o que comparar — seguir normalmente e a
    planilha passa a registrar o ID a partir dessa execução.

**Se encontrar exatamente uma pasta correspondente:**

1. Listar o que já tem dentro: quantos `.pdf` já baixados, quantos `.txt`
   placeholder pendentes.
2. **Checar a idade da pasta pelo sufixo de data `(DD-MM-AAAA)` no nome**
   (ver Passo 2) — se fizer mais de **90 dias** desde essa data até hoje, o
   padrão sugerido muda: **oferecer Atualização Completa como padrão**, não
   Parcial, e avisar o usuário o motivo (ex: "essa pasta foi atualizada pela
   última vez há mais de 90 dias — o conteúdo pode ter sido revisado nesse
   meio tempo, sugiro Atualização Completa dessa vez"). Confirmado pelo Elvis
   em 2026-08-18. Se a pasta não tiver sufixo de data (de uma coleta anterior
   a essa regra existir), tratar como se fosse antiga — sugerir Completa.
3. Informar o usuário e perguntar como quer proceder, com três opções:
   - **Atualização Parcial** (padrão sugerido, exceto no cenário dos 90 dias
     acima) — baixa só as aulas que ainda estão faltando (travadas na coleta
     anterior, agora liberadas). Não mexe nos PDFs já baixados. Rápido.
   - **Atualização Completa** (padrão sugerido quando a pasta tem mais de 90
     dias) — além de baixar o que falta, reconfere **todos** os PDFs já
     baixados contra a versão atual no site e substitui os que tiverem sido
     revisados/atualizados desde a última coleta. Mais lento, porque precisa
     rebaixar cada aula já existente pra comparar.
   - **Criar pasta nova do zero** — mesmo já tendo uma pasta encontrada.
4. **Se optar por Atualização Parcial ou Atualização Completa:** esse vira o
   modo atualização pro resto da skill — usar essa pasta, seguir a lógica de
   "Modo atualização" do Passo 4 em diante, no sub-modo escolhido.
5. **Se optar por criar nova do zero:** perguntar também **se quer que a pasta
   antiga localizada seja apagada** (nunca apagar sem essa confirmação explícita
   — é uma ação destrutiva e irreversível) ou se prefere manter as duas
   coexistindo (nesse caso, a pasta nova precisa de um nome que não conflite,
   ex: sufixo " (nova)" — confirmar com o usuário como diferenciar).

**Se encontrar mais de uma pasta correspondente** (ex: uma pasta solta na raiz
da pasta padrão e outra dentro de algum pacote): **não escolher sozinho** —
listar todas as encontradas (caminho completo de cada uma) e perguntar ao
usuário qual delas é a certa antes de seguir.

**Se não encontrar nenhuma pasta correspondente:** é download novo — criar
`<pasta informada>/<Tipo de Curso>/<SIGLA> - <Disciplina> (<DD-MM-AAAA>)/` com
`mkdir -p`, no padrão do Passo 2. Não tem o que atualizar, então não precisa
perguntar mais nada sobre isso.

## Passo 4: Levantar a lista de aulas

**Montar UMA tabela única (ID + rótulo + assunto) antes de baixar qualquer
coisa — nunca separar essa extração em duas listas e cruzar de cabeça durante
o download.** Confirmado pelo Elvis em 2026-08-18: foi exatamente essa
pareação manual (uma lista de IDs de um lado, rótulos "lembrados" de outro)
que causou o bug mais sério encontrado numa validação em lote — duas aulas
"Parte II" inseridas no meio deslocaram a numeração de todas as aulas
seguintes, e em outros cursos o assunto virou genérico porque foi reconstruído
de memória no meio de um download longo em vez de lido de novo. A tabela
elimina os dois problemas ao mesmo tempo.

0. **Ler a listagem com a página recém-carregada, antes de clicar em qualquer
   aula** — confirmado em 19-08-2026. Depois do primeiro clique a SPA
   reorganiza o DOM e os rótulos passam a sair trocados (a mesma aula apareceu
   ora como "Aula 01", ora como "Aula 02"). Se precisar reler a listagem depois
   de já ter aberto alguma aula, **recarregar a página antes**.

0.1. **CRÍTICO — aula travada não é link, e some se a extração for só por
   `<a>`.** A aula ainda não liberada existe no DOM como header **sem** `<a>`
   de aula (o `href` aponta pra própria listagem). Extraindo só links, ela
   desaparece da tabela: não vira placeholder `.txt` (Passo 6) e o `(N-M)` do
   Passo 7 mente, dando o curso como completo. Descoberto em 19-08-2026 no
   curso de Noções de Primeiros Socorros, que parecia ter 1 aula quando tem 2.
   Iterar sempre por `.LessonCollapseHeader` e tratar como travada todo item
   de que não se consiga extrair `/aulas/{id}` — a data de liberação
   ("Disponível em DD/MM/AAAA") fica num elemento pai, não no header:
   ```js
   Array.from(document.querySelectorAll('.LessonCollapseHeader')).map(x => {
     const a = x.closest('a'), href = a ? a.getAttribute('href') : '';
     const m = href && href.match(/\/aulas\/(\d+)/);
     const h = x.querySelector('h2'), p = x.querySelector('p');
     let d = null, n = x;
     for (let k = 0; k < 6 && n; k++) {
       n = n.parentElement; if (!n) break;
       const t = n.textContent.replace(/\s+/g, ' ');
       const mm = t.match(/Dispon[ií]vel em\s*(\d{2}\/\d{2}\/\d{4})/);
       if (mm && t.length < 400) { d = mm; break; }
     }
     return { id: m ? m[1] : '', r: h ? h.textContent.trim() : '',
              c: p ? p.textContent.trim() : '', trav: m ? '' : (d ? d[1] : 'SEM-DATA') };
   });
   ```
   Esse mesmo `map` já entrega rótulo (`h2`) e assunto (`p`) separados, que é
   exatamente a tabela única pedida logo acima.

1. Na página `/aulas` do curso, extrair os IDs de aula via `javascript_tool` —
   **não filtrar só links que terminam em `/aulas/{aulaId}`**: algumas aulas
   linkam direto pra uma sub-página de vídeo (`/aulas/{aulaId}/videos/{videoId}`)
   e ficariam de fora se o filtro exigir fim exato de string (bug confirmado
   testando o curso de Direito Constitucional — aulas 03 e 04 tinham esse
   padrão e ficaram invisíveis até corrigir). Capturar o ID de aula em
   **qualquer posição** do href e deduplicar mantendo a ordem de aparição:
   ```js
   const links = Array.from(document.querySelectorAll('a'));
   const seen = new Set(); const ids = [];
   for (const a of links) {
     const m = (a.getAttribute('href')||'').match(/\/aulas\/(\d+)/);
     if (m && !seen.has(m[1])) { seen.add(m[1]); ids.push(m[1]); }
   }
   JSON.stringify(ids);
   ```
2. Na mesma página, ler o `get_page_text` da listagem. O texto vem em blocos
   repetidos e previsíveis — rótulo, depois assunto (quando existir), depois um
   marcador de status ("Não estudei", "Estudei", "Disponível em DD/MM/AAAA",
   "baixado"). Esse marcador de status é o separador confiável entre um bloco
   de aula e o próximo — usar ele pra quebrar o texto em blocos, um por aula,
   na mesma ordem em que aparecem na página.
3. **Zipar as duas extrações por posição** (a lista de IDs do passo 1 e os
   blocos do passo 2 estão na mesma ordem de exibição da página) pra montar
   uma tabela única: `[{posicao, aulaId, rotulo, assunto}, ...]`. O **rótulo**
   é a primeira linha do bloco (ex: "Aula 00", "Aula 01 - Parte II", "Aula
   Extra (Somente pdf)", ou um título sem número tipo "RESUMO - Parte Geral do
   CC"); o **assunto** é o resto do bloco antes do marcador de status.
4. Cruzar a quantidade de IDs (passo 1) com a quantidade de blocos (passo 2) —
   os dois devem bater. Se não bater, não seguir pro download: revisar a
   extração antes (sinal de que o separador de status não cobriu algum
   formato novo, ou que uma aula não tem link — nesse caso o ID fica vazio
   nessa posição, mas o rótulo/assunto ainda existem e devem constar na
   tabela mesmo assim).
5. **Salvar essa tabela no scratchpad antes de baixar a primeira aula** (um
   arquivo `.md` ou `.json` simples, uma linha por aula). Ela é a fonte única
   de verdade pro nome do arquivo — nunca reconstruir rótulo/assunto de
   memória durante o loop de download (Passo 5); sempre consultar essa tabela
   salva pela posição/ID da aula sendo processada no momento. Isso também
   serve de base pra Validação Final (Passo 8) quando o download acabou de
   acontecer na mesma execução — ver nota lá.

### Modo atualização — o que pular

Antes de baixar qualquer coisa, listar o que já existe na pasta. O comportamento
abaixo depende do sub-modo escolhido no Passo 3 (Atualização Parcial ou Completa):

- Arquivos `Aula NN - ... (DD-MM-AAAA).pdf` já baixados (data entre parênteses —
  ver "Nome do arquivo" no Passo 5):
  - **Atualização Parcial:** **pular essa aula**, já está completa. Não reconfere.
  - **Atualização Completa:** **não pular** — rebaixar essa aula (mesmo processo
    do Passo 5) e comparar a data extraída do PDF novo com a data que já está no
    nome do arquivo local (ver "Comparar e substituir PDF já baixado" no Passo 5).

- **Arquivo no formato ANTIGO, sem o sufixo `LS`/`LC`** (`Aula NN - Assunto
  (DD-MM-AAAA).pdf`, sem ` LS ` nem ` LC ` antes da data). O sufixo passou a ser
  obrigatório em 2026-08-20 — arquivo sem ele é de coleta anterior.
  - **Reconhecer como a mesma aula.** Casar pelo rótulo (`Aula NN`), **nunca** pelo
    nome completo — senão a skill acha que a aula não existe e baixa um duplicado ao
    lado do arquivo antigo.
  - **Atualização Parcial:** não rebaixar. Só **renomear** acrescentando o sufixo,
    deduzido assim: se `pdf_simplificado` existe na API **e** o número de páginas do
    arquivo local **difere** do PDF original, é `LS`; se for **igual** ao original, é
    `LC` (foi stub rebaixado — ver Passo 6.1). Se `pdf_simplificado` não existe, é
    `LC` direto, sem precisar conferir nada.
  - **Atualização Completa:** o rebaixe já resolve — gravar o nome novo com sufixo e
    apagar o arquivo antigo sem sufixo. **Conferir que sobrou só um arquivo por
    aula.**
- Arquivos `Aula NN - ... - DD-MM-AAAA.txt` (placeholder, data com traço — ver
  Passo 6) → em **qualquer** sub-modo, **checar de novo** se o livro já ficou
  disponível. Se sim: baixar o PDF normalmente e **apagar o `.txt` antigo** —
  **passo obrigatório, nunca esquecer:** sempre que um PDF real substitui um
  `.txt` placeholder, o `.txt` correspondente tem que ser apagado da pasta antes
  de seguir pra próxima aula. Se ainda não: deixar o `.txt` como está (pode
  atualizar a data prevista se ela mudou).
- Aulas que não aparecem na pasta nem como `.txt` → baixar normalmente.

**Lembrete de formato:** a data entre **parênteses** `(DD-MM-AAAA)` é a data real
de elaboração/atualização do PDF, extraída da própria primeira página do arquivo.
A data depois de um **traço** `- DD-MM-AAAA.txt` é só a previsão de liberação
informada pelo site pra uma aula ainda travada. Os dois formatos nunca se
confundem visualmente por causa disso.

**Atalho pra não precisar abrir aula por aula:** a própria página `/aulas`
(listagem) já mostra, pra cada aula, se ela está travada com "Disponível em
DD/MM/AAAA" ou liberada (sem essa tag, geralmente "Não estudei" / "baixado").
Usar `get_page_text` na listagem pra comparar com os `.txt` pendentes na pasta
antes de navegar pra qualquer aula individual — só vale a pena abrir a página
de uma aula específica (Passo 5) se ela aparecer sem tag de data (ou seja, já
liberada) e ainda não tiver PDF baixado na pasta.

## Passo 5A (CAMINHO PRINCIPAL): pegar todas as aulas e os links pela API interna

**Tentar sempre este caminho primeiro.** A API exige um `Bearer`, e o que
decide se ela passa é **o token nunca sair da página** — confirmado pelas duas
execuções de 19-08-2026: tentar trazer o token pro contexto (`fetch` em
`/oauth/token/` devolvendo o token, ou leitura do storage) volta como "Blocked
by classifier"; já rodar o `fetch` dentro do `javascript_tool`, guardar o token
numa variável da própria página e devolver só as assinaturas passa sem
problema — foi assim que saíram 227 PDFs num pacote inteiro. Sem o header, a
chamada morre no CORS.

**Se mesmo com esse padrão o classificador recusar**, não insistir: dois
"Blocked by classifier" seguidos e vai pro "CAMINHO PRINCIPAL: percorrer as
aulas dentro da própria SPA", mais abaixo neste mesmo passo, que não toca em
credencial nenhuma. **Não tentar rotas alternativas pra obter a credencial** —
esse bloqueio é correto.

Em vez de abrir a listagem e depois cada aula pra extrair o `a.LessonButton`,
buscar **o curso inteiro numa única chamada**:

```
GET https://api.estrategiaconcursos.com.br/api/aluno/curso/{cursoId}
Authorization: Bearer <token de GET /oauth/token/>
```

A resposta traz, para **cada** aula: `id`, `nome` (o rótulo exato), `conteudo`
(o assunto), `is_disponivel`, `data_publicacao`, `pdf` e `pdf_simplificado`
(links já assinados). Isso substitui uma navegação por aula por uma chamada por
curso — num curso de 40 aulas, 40 navegações viram 1.

Como usar sem violar a regra de credenciais:

- O `Bearer` **fica dentro do navegador**. Rodar o `fetch` via `javascript_tool`
  e trazer de volta **apenas os links assinados** (e os metadados das aulas).
  Nunca extrair o token pro shell — além de desnecessário, o classificador do
  Claude Code bloqueia isso, e com razão.
- A assinatura é **por aula**, mas a mesma serve tanto para `/pdf/download/{id}`
  quanto para `/pdfSimplificado/download/{id}`.
- **Os links duram pouco: ~20-30 minutos.** O campo `expiration` da URL vem com
  o relógio do servidor (umas 2h à frente do local) e **engana** — não usar ele
  como referência. Gerar as assinaturas e consumir na hora; se o lote passar de
  ~15 min, gerar de novo antes de continuar. Link vencido devolve HTTP 200 com
  a home em HTML, exatamente igual ao erro de User-Agent.
- Aula ainda não liberada vem com `pdf` nulo — tratar como travada (Passo 6).

Se a API falhar ou mudar, o caminho antigo (navegar aula por aula e ler o
`a.LessonButton`) continua válido como fallback — está descrito no Passo 5.

### CAMINHO B (fallback): percorrer as aulas dentro da própria SPA

**Confirmado na prática em 2026-08-18**, e usado de ponta a ponta no pacote
TCDF-ANACE em 19-08-2026 (17 matérias, 177 PDFs) — é uma rota testada, só mais
lenta que a API do Passo 5A. Usar quando a API não estiver disponível. Em vez de uma
chamada de `navigate` por aula, dá pra percorrer várias aulas **num único
`javascript_tool`**: a área do aluno é um SPA React, então clicar no `<a>` da
aula troca a página sem reload, e `history.back()` volta pra listagem. Num
pacote de 211 aulas isso trocou ~240 navegações por ~40 chamadas.

**Três ajustes que fazem esse método aguentar um curso inteiro** — aprendidos
em 19-08-2026, depois de perder lotes por timeout:

1. **Disparar o loop sem `await`** (fire-and-forget), acumulando em
   `window.__acc`, e ler o acumulador numa chamada seguinte. O executor de JS
   corta em 30s — se a chamada esperar o loop terminar, ela morre no timeout
   **e leva o loop junto**, perdendo o lote inteiro. Solto, o loop continua
   rodando no navegador e a chamada volta na hora. Com isso o limite de "no
   máximo 7 aulas por chamada" deixa de existir: dá pra disparar o curso todo.
2. **Esperar por polling (150ms) em vez de `sleep` fixo** até o botão daquela
   aula aparecer — cai de ~4s pra ~2,3s por aula.
3. **Nunca deixar dois loops rodando ao mesmo tempo.** Um loop antigo continua
   navegando por baixo e embaralha a coleta do novo (rótulos fora de ordem,
   aulas puladas) — foi o que fez os primeiros lotes voltarem com 1 ou 2
   itens. Como o loop é solto, a forma confiável de matar é **recarregar a
   página** antes de começar o próximo curso.

**Guardar o script em `sessionStorage`** e reinjetar com
`eval(sessionStorage.getItem('__boot'))` depois de cada reload, em vez de
recolar o código inteiro a cada curso. `sessionStorage` com código próprio
passa pelo classificador; `localStorage` da aplicação, não (é onde mora a
credencial) — não tentar.

**Trazer de volta só `id|tipos|expiration|signature`**, não a URL inteira: o
resto (`clienteId`, `resourceType`, `resourceId`) é template fixo, remontável
no shell.

```js
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const ids = Array.from(document.querySelectorAll('a[href*="/aulas/"]'))
    .map(a => a.getAttribute('href').split('/aulas/')[1].split('/')[0])
    .slice(0, 7);
  const out = [];
  for (const id of ids) {
    const a = document.querySelector('a[href*="/aulas/' + id + '"]');
    if (!a) { out.push('L:' + id + '|SEMLINK|'); continue; }
    a.click();
    let b = [];
    for (let i = 0; i < 25; i++) {
      await sleep(150);
      b = Array.from(document.querySelectorAll('a.LessonButton'))
            .filter(x => x.href.includes('/download/' + id));
      if (b.length) break;
    }
    const s = b.find(x => /simplificada/i.test(x.innerText));
    const o = b.find(x => /vers.o original/i.test(x.innerText));
    const pick = s || o;
    let q = '';
    if (pick) {
      const u = new URL(pick.href);
      q = u.searchParams.get('expiration') + '|' + u.searchParams.get('signature');
    }
    out.push('L:' + id + '|' + (s ? 'S' : o ? 'O' : 'X') + '|' + q);
    history.back();
    for (let i = 0; i < 20; i++) {
      await sleep(150);
      if (document.querySelector('a[href*="/aulas/' + id + '"]')) break;
    }
  }
  return out.join('\n');
})()
```

Pontos que fazem esse atalho funcionar (todos aprendidos apanhando):

- **Lote de no máximo 7 aulas por chamada.** Cada aula leva ~2,5-3s e o
  executor de JS corta em **30s** — lotes de 8+ estouram na metade e o
  trabalho da chamada inteira se perde. Ir fatiando a lista com `.slice()`.
- **Devolver só `expiration` e `signature`, não a URL inteira.** O resto da
  URL é template fixo
  (`.../api/aluno/{pdfSimplificado|pdf}/download/{id}?clienteId={cliente}&resourceType=pdf&resourceId={id}&expiration={exp}&signature={sig}`),
  remontável no shell. Num pacote grande isso economiza muito contexto.
- **O filtro `/download/{id}` não é opcional** — é ele que garante que a
  página nova já carregou (ver Passo 5, item 2).
- Alguns `href` da listagem vêm no formato `{aulaId}/videos/{videoId}` —
  por isso o `.split('/')[0]` ao extrair o ID.
- Vale a mesma validade curta de link da API: consumir o lote logo depois
  de coletar.

## Método de download: resultado da verificação (18-08-2026) — CONCLUÍDA

O Elvis pediu pra checar se dava pra baixar tudo por `fetch`, no mesmo molde das
skills do Bruno Bezerra. **Checagem feita e os três pontos passaram.** Não refazer
essa investigação a cada execução — o resultado está aqui.

| O que foi checado | Resultado |
|---|---|
| A API interna de aulas responde e cobre tudo | **Sim.** `GET /api/aluno/curso/{id}` devolve todas as aulas numa chamada (~4s) |
| Dá pra obter o link do PDF sem abrir a aula | **Sim — é a mesma chamada.** Ela já traz `pdf` e `pdf_simplificado` prontos de cada aula |
| O PDF baixa fora do navegador | **Sim.** Não depende de cookie de sessão: basta o link assinado + `User-Agent` de browser |

**Atualização de 19-08-2026: o que decide é como o `Authorization` é montado.**
Trazer o token pro contexto (`/oauth/token/` devolvendo o token, ou leitura do
storage da aplicação) é recusado pelo classificador — e deve ser mesmo. Já
manter o token dentro da página, usá-lo no mesmo `javascript_tool` e devolver
só `{aulaId: [expiration, signature]}` passa normalmente: foi o que rodou o
pacote ISS Manaus inteiro (21 matérias, 227 PDFs) no mesmo dia. Por isso a
**API é o caminho principal** e a SPA é o fallback — testado e válido, mas mais
lento.

**Vantagem sobre o método do Bezerra:** lá o download roda dentro do navegador;
aqui a API entrega os links assinados e o download acontece **fora** do navegador,
no shell, o que permite baixar em paralelo. Numa execução real: 24 cursos / ~480
aulas / 1,93 GB.

### Três armadilhas confirmadas na prática (não repetir)

1. **A assinatura do link dura ~20-30 minutos, não 2 horas.** O campo `expiration`
   da URL **engana**: vem com o relógio do servidor, que está ~2h à frente do
   local. Gerar as assinaturas e consumir na hora, em blocos curtos; se o lote
   passar de ~15 min, gerar de novo.
2. **`fetch` de dentro da página do Estratégia NÃO serve pra testar download.**
   Ele responde `302` e devolve HTML mesmo quando o download está funcionando
   perfeitamente por fora — foi observado o navegador falhando e o `curl`
   baixando o mesmo link com sucesso no mesmo instante. **Nunca concluir "a
   plataforma bloqueou" a partir desse teste**; testar sempre por fora.
3. **Depois de muitas centenas de downloads seguidos, a plataforma parece
   estrangular** (passa a devolver a home em HTML mesmo com assinatura recém-gerada
   e User-Agent correto). Não há regra conhecida nem número exato. Quando
   acontecer: parar, avisar o usuário e retomar mais tarde — algumas horas depois
   voltou a funcionar normalmente. Nunca insistir em laço.

## Passo 5B: Baixar o livro de cada aula (o núcleo do processo)

**Os itens 1 e 2 abaixo são FALLBACK** — só use se a API do Passo 5A falhar ou
mudar. Quando a API funcionar (o normal), você já tem `nome`, `conteudo`,
`is_disponivel`, `pdf` e `pdf_simplificado` de todas as aulas, então **pule
direto pro item 3**, sem navegar aula nenhuma.

**Do item 3 em diante vale para os dois caminhos** (API ou fallback): escolha
entre simplificada e original, download, validação, nome do arquivo, extração
de data e substituição são idênticos.

Para cada aula pendente, repetir:

1. *(fallback)* Navegar para `https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{id}/aulas/{aulaId}`
   (ou clicar no título da aula na lista) e esperar ~2s carregar. **Conferir o
   título da aba depois de navegar** — o próprio resultado do `navigate` já
   costuma trazer o título de volta. Se o título voltar genérico ("Área do
   Aluno", ou o mesmo título de antes de navegar) em vez do título da aula,
   a navegação falhou silenciosamente (transiente, observado várias vezes na
   prática) — **renavegar uma vez pra mesma URL antes de seguir**, em vez de
   extrair o `LessonButton` de uma página errada (o que geraria um download
   errado ou um erro sem explicação clara).
2. *(fallback)* **Não precisa clicar no card nem abrir aba nova.** O link de
   download já está no HTML da própria página, num `<a class="LessonButton">`.
   Extrair direto via JavaScript (`javascript_tool`):
   ```js
   const links = Array.from(document.querySelectorAll('a.LessonButton'))
     .map(a => ({ texto: a.textContent.replace(/\s+/g, ' ').trim(), href: a.href }));
   JSON.stringify(links);
   ```
   Isso retorna um link pra cada opção presente na aula (ex: "Baixar Livro
   Eletrônico versão simplificada...", "...versão original...", "...marcação
   dos aprovados"). **Só interessam os dois primeiros** (simplificada e
   original).

   **Sempre filtrar os botões pelo ID da aula antes de usar o link** —
   confirmado na prática em 2026-08-18. O `href` de download termina em
   `/download/{aulaId}`; se o link capturado apontar pra outro ID, é o botão
   da aula **anterior**, que ainda não saiu do DOM (a troca de página é
   assíncrona). Isso já gerou um download de 188 bytes sem erro aparente.
   Filtrar assim, e só considerar a página carregada quando aparecer pelo
   menos um botão do ID certo:
   ```js
   const links = Array.from(document.querySelectorAll('a.LessonButton'))
     .filter(a => a.href.includes('/download/' + aulaId));
   ```
3. **Se existir link de "versão simplificada":** usar esse.
4. **Se não existir simplificada mas existir "versão original":** usar esse
   como fallback.
5. **Se nenhum dos dois existir** (aula ainda não liberada pelo curso): ver Passo 6.
6. Baixar o PDF **direto pra pasta de destino**, com um **nome temporário** (a
   data só entra no nome final depois de extraída — ver abaixo), via `curl`
   (Bash) com `-L` (o link redireciona pra CDN assinada
   `cdn.estrategiaconcursos.com.br/.../....pdf?Expires=...&Signature=...`),
   sem passar pela pasta de Downloads:
   ```bash
   curl -sL -o "<pasta>/Aula NN - Assunto Sintetico.pdf.tmp" "<href capturado>" \
     -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36" \
     -H "Referer: https://www.estrategiaconcursos.com.br/" \
     -w "HTTP:%{http_code} SIZE:%{size_download}\n"
   ```

   **O `User-Agent` de browser é obrigatório** — confirmado na prática em
   2026-08-18: com o User-Agent padrão de `curl`/`python-requests` o servidor
   responde **HTTP 200 devolvendo a home do site em HTML (~238 KB)** no lugar
   do PDF. O `Referer` acompanha pelo mesmo motivo.

   **CRÍTICO — nunca validar o download só pelo tamanho.** Como a home em HTML
   tem ~238 KB, qualquer teste do tipo "HTTP 200 e SIZE não-trivial" aceita
   lixo como se fosse PDF. Isso já destruiu 27 PDFs bons numa execução real
   (eles foram apagados e substituídos pelo HTML). Antes de considerar o
   download válido, conferir **as três coisas**:

   1. `HTTP:200`;
   2. os **5 primeiros bytes do arquivo são `%PDF-`** (se o arquivo começa com
      `<`, é HTML: descartar o `.tmp` e repetir a tentativa);
   3. o `pypdf` abre o arquivo e retorna **número de páginas > 0**.

   ```bash
   head -c 5 "<arquivo>.tmp" | grep -q '%PDF-' && echo PDF_OK || echo RECUSADO
   ```

   **Só apagar/substituir o PDF antigo depois que os três testes passarem.**
   Enquanto não passarem, o arquivo que já estava na pasta continua intocado.
6.1. **CRÍTICO — o "simplificado" pode ser só um aviso, não a aula.**
   Confirmado na prática em 2026-08-18 (pacote Regular Controle: 19 aulas
   afetadas, 14 em Contabilidade Geral Avançada e 5 em Contabilidade
   Pública). Em algumas aulas o card "Baixar Livro Eletrônico versão
   simplificada" **existe e baixa normalmente**, mas o PDF tem só ~3 páginas
   e diz, em letras garrafais, que *aquela aula não possui PDF simplificado
   devido às suas características*. Ou seja: a presença do card não garante
   que existe versão simplificada de verdade — e o arquivo passa nos três
   testes acima (é um PDF válido).

   Depois de baixar a versão simplificada, antes de renomear pro nome final,
   checar: se o PDF tiver **8 páginas ou menos** e o texto das 4 primeiras
   páginas contiver ao mesmo tempo `possui` e `simplificado`, é um stub —
   **descartar o `.tmp` e rebaixar aquela aula na versão original**, sem
   perguntar nada ao usuário (é o mesmo fallback do item 4). Registrar a
   troca pra citar no resumo final.

   ```python
   if len(reader.pages) <= 8:
       chk = ' '.join((reader.pages[i].extract_text() or '')
                      for i in range(min(4, len(reader.pages))))
       if 'possui' in chk and 'simplificado' in chk:
           # stub: descartar e baixar a versão original dessa aula
   ```

   O limiar de páginas evita reabrir PDF grande à toa — o stub sempre veio
   com 3 páginas. **Nunca aceitar um simplificado curto sem essa checagem:**
   sem ela, a aula fica na pasta com cara de baixada e sem nenhum conteúdo.
7. Extrair a data da primeira página do PDF (ver "Extrair a data do PDF" abaixo)
   e renomear o `.tmp` pro nome final com a data. **Guardar também o número de
   páginas (`len(reader.pages)`) nessa mesma abertura** — é uma das colunas da
   planilha do Passo 9, e o arquivo já está aberto aqui. Sem isso é preciso
   reabrir todos os PDFs numa segunda passada só pra montar a planilha
   (confirmado em 19-08-2026: 227 reaberturas evitáveis no pacote ISS Manaus).
   Registrar página, data e `MATCH` num log único da execução e alimentar a
   planilha a partir dele.
8. Voltar pra lista de aulas e seguir pra próxima.

**Nota sobre cliques no navegador embutido (Browser pane):** testado que clicar
em coordenadas de tela em itens de listagem (cursos, cards) nem sempre navega
de forma confiável nesse navegador — prefira sempre extrair o `href` real via
`javascript_tool` e navegar direto pela URL, em vez de clicar às cegas. Isso
vale tanto pra essa etapa de download quanto pra navegar entre páginas do site
de forma geral.

**Nota sobre falha silenciosa de navegação:** de vez em quando o `navigate`
não chega na página pedida (fica na página anterior, ou cai na home/"Área do
Aluno") sem lançar erro — confirmado na prática em ambos os navegadores.
Conferir o título retornado pela própria chamada de `navigate` antes de seguir;
se não bater com o esperado (deveria trazer o nome do curso/aula), renavegar
pra mesma URL mais uma vez antes de extrair qualquer coisa da página — evita
processar uma aula errada ou perder tempo com um erro confuso mais adiante.

### Nome do arquivo

```
<Rótulo exato da aula, igual está no site> - Assunto Sintético [LS|LC] (DD-MM-AAAA).pdf
```

**O sufixo `LS` / `LC` é obrigatório** (Elvis, 2026-08-20) e entra **entre o assunto e a
data**:

| Sufixo | Significa | Quando usar |
|---|---|---|
| `LS` | **Livro Simplificado** | o arquivo baixado foi o `pdf_simplificado` |
| `LC` | **Livro Completo** (versão original) | o arquivo baixado foi o `pdf` original |

Exemplos:

```
Aula 03 - Fundações, empresas públicas e sociedades de economia mista LS (30-07-2026).pdf
Aula 18 - Improbidade administrativa - Lei 8.429-1992 LC (30-07-2026).pdf
```

**Por que isso existe.** O mapeamento de aulas ancora o aluno por **número de página**, e
o simplificado e o completo têm **paginações diferentes**. Como esta skill prioriza o
simplificado e cai pro original quando ele não existe (ou é stub — ver Passo 6.1), a
pasta fica **mista**. Sem o sufixo não há como saber, olhando o arquivo, a qual paginação
aquela âncora se refere. No pacote TCDF-ANACE isso atinge **54 de 180 aulas (30%)**, e
quatro disciplinas inteiras não têm simplificado nenhum.

**O sufixo tem que refletir o que foi REALMENTE baixado, não o que a API oferecia.**
Quando o Passo 6.1 detecta stub e rebaixa na versão original, o arquivo é `LC` — mesmo
que `pdf_simplificado` existisse na API. Esse é justamente o caso que engana quem tenta
deduzir a versão pela API depois.

- **O rótulo da aula tem que ser copiado exatamente como aparece na listagem do
  site, nunca um contador sequencial próprio** — confirmado pelo Elvis em
  2026-08-18. A ideia é que, só de olhar o nome do arquivo, dê pra identificar
  na hora qual aula é aquela dentro da plataforma. Exemplos reais observados na
  prática (todos copiados como estão, sem normalizar pra um padrão "Aula NN"
  genérico):
  - `Aula 00`, `Aula 01`, `Aula 02`... (caso comum)
  - `Aula 01 - Parte II` (quando o site quebra uma aula em mais de uma parte —
    manter "Parte II"/"Parte III" etc exatamente como está; **não** virar
    "Aula 02" só porque é o segundo arquivo baixado daquela matéria)
  - `Aula Extra` (aula bônus fora da numeração principal — manter "Extra" no
    rótulo, não inventar um número pra ela)
  - Títulos sem numeração, tipo `RESUMO - Parte Geral do CC` ou `Como Utilizar
    a Trilha Estratégica` — usar o próprio título da aula como rótulo
  - **Nunca substituir o rótulo real por uma contagem sequencial interna**
    (numerar 00, 01, 02... só pela ordem de download) quando o rótulo do site
    for diferente disso — isso já gerou nomes de arquivo que não batiam com o
    que o usuário via na própria plataforma ao abrir o curso.
- **Exceção: anotações de formato/equipe não entram no rótulo** — confirmado
  pelo Elvis em 2026-08-18. Tags que descrevem o *tipo de mídia* ou a *equipe*
  responsável pela aula, não o *assunto* tratado nela, ficam de fora do nome do
  arquivo — o que interessa é o título indicar o conteúdo, não esse tipo de
  metadado. Exemplos observados que **não** entram: `(Somente PDF)`, `(Somente
  em PDF)`, `(Aula em PDF)`, `(Equipe de Legislação)`, `(Somente Vídeo)`. Ex: o
  rótulo do site `Aula 20 (Somente PDF)` vira só `Aula 20` no nome do arquivo.
- **Nome de professor também não entra no rótulo** — confirmado pelo Elvis em
  2026-08-18. Alguns cursos rotulam a aula com o autor (ex: `Aula 00 - Prof.
  Diego Carvalho e Emannuelle Gouveia`, em Análise de Informações, ou `Aula 00
  - Prof. Leonardo Mathias`, na Monitoria). O professor é metadado de autoria,
  não assunto: o arquivo fica `Aula 00 - <assunto sintético>`. A autoria já
  está registrada na primeira página do próprio PDF. **Se aparecer
  algum outro tipo de anotação parecida (entre parênteses, junto ao número da
  aula) que não se encaixe claramente como "tipo de mídia/equipe" nem como
  parte do conteúdo, perguntar ao usuário antes de decidir se entra ou não** —
  não adivinhar sozinho pra esse caso novo.
- **A anotação nem sempre vem entre parênteses** — visto na prática:
  `Aula 16- Somente em PDF`, `Aula 15 - Somente em PDF`, `Aula Extra (Somente
  pdf)`. Tratar todas do mesmo jeito, com ou sem parênteses, com ou sem espaço
  antes do traço.
- **Exceção: créditos de professor também não entram no rótulo** — confirmado
  em 2026-08-18. O curso de Tecnologia da Informação nomeia as aulas como
  `Aula 00 - Prof. Diego Carvalho e Renato da Costa`. Nome de professor descreve
  *quem deu* a aula, não o *assunto* dela, então sai do rótulo pela mesma lógica
  das anotações de formato: vira só `Aula 00`. Regra prática: cortar tudo a
  partir de ` - Prof.` / ` - Profa.` até o fim do rótulo (isso já leva junto um
  eventual `(Somente em PDF)` no final). Cuidado pra não confundir com
  `Aula 01 - Parte II`, que **é** parte do rótulo e fica.
- **Rótulos repetidos no mesmo curso: desempatar pelo conteúdo.** Existem cursos
  com duas aulas de nome idêntico — em Administração Financeira e Orçamentária
  há **duas** `Aula Extra - Somente em PDF`, uma de "Questões Extras FGV" e
  outra de "Questões Extras CEBRASPE". Casando só pelo rótulo, os dois arquivos
  trocam de lugar (e ficam com o assunto errado no nome) ou um sobrescreve o
  outro. Quando o rótulo limpo aparecer mais de uma vez: comparar o `conteudo`
  da aula com o nome do arquivo local e parear o que tiver mais palavras em
  comum; **se nenhum arquivo bater, não parear** — deixar de fora e citar na
  Validação Final, em vez de arriscar sobrescrever o arquivo errado.
- Assunto sintetizado a partir do título/descrição da aula (não precisa copiar
  literalmente o texto enorme do currículo, resumir pro nome do arquivo ficar
  legível) — mas o **rótulo** (a parte antes do assunto) só é sintetizado ou
  abreviado **se o caminho completo do arquivo estiver perto do limite de 260
  caracteres do Windows** (ver "Limite de 260 caracteres de caminho no
  Windows" nos Detalhes técnicos) — nesse caso, abreviar o assunto primeiro, e
  só mexer no rótulo como último recurso, mantendo pelo menos o número/palavra
  que identifica a aula (ex: `Aula 01 - Parte II` pode virar `Aula 01-PII` se
  for realmente necessário, mas não virar `Aula 02`). Fora desse cenário de
  limite de caminho, o rótulo nunca é sintetizado nem abreviado — confirmado
  pelo Elvis em 2026-08-18.
- `(DD-MM-AAAA)` = data de elaboração/atualização do PDF, extraída da primeira
  página do próprio arquivo (ver abaixo) — **entre parênteses**, com traço (nunca
  barra). Se não for possível extrair nenhuma data (ver fallback abaixo), o
  arquivo fica sem esse sufixo mesmo.
- Sem acentos problemáticos ou caracteres especiais que possam dar problema em
  scripts (mas pode manter cedilha/acentuação normal do português nos nomes).

### Extrair a data do PDF (e checar o conteúdo contra o assunto esperado)

A maioria dos livros eletrônicos do Estratégia traz, na primeira página, a data
de elaboração/atualização daquele material. Depois de baixar o PDF (todo
download, não só em modo atualização), extrair essa data pra usar no nome do
arquivo — **e aproveitar essa mesma abertura do PDF pra checar, de graça, se o
conteúdo bate com o assunto esperado** (o `assunto` da tabela montada no
Passo 4) — confirmado pelo Elvis em 2026-08-18. Essa checagem roda inteira em
Python/local, nunca abre o conteúdo do PDF pro meu contexto (não gasta token):

```bash
python -c "
import re, sys, unicodedata
from pypdf import PdfReader

MESES = {'janeiro':1,'fevereiro':2,'marco':3,'abril':4,'maio':5,'junho':6,
         'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}
STOPWORDS = {'para','como','entre','sobre','pela','pelo','pelas','pelos','com',
             'sem','das','dos','que','uma','um','os','as','de','do','da','em',
             'na','no','por','seu','sua','ao','aos'}

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
def norm(s):
    return strip_accents(s).lower()

reader = PdfReader(sys.argv[1])
texto = reader.pages[0].extract_text() or ''

m = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
if m:
    data = f'{m.group(1)}-{m.group(2)}-{m.group(3)}'
else:
    m2 = re.search(r'(\d{1,2}) de ([A-Za-zçÇéÉ]+) de (\d{4})', texto)
    if m2:
        dia, mes_nome, ano = m2.groups()
        mes_num = MESES.get(strip_accents(mes_nome.lower()))
        data = f'{int(dia):02d}-{mes_num:02d}-{ano}' if mes_num else ''
    else:
        data = ''
print(data)

assunto = sys.argv[2] if len(sys.argv) > 2 else ''
if assunto:
    palavras = [w for w in re.findall(r'[A-Za-zÀ-ÿ0-9]+', assunto)
                if len(strip_accents(w)) >= 4 and norm(w) not in STOPWORDS]
    n_pages = min(6, len(reader.pages))
    texto_conteudo = ' '.join((reader.pages[i].extract_text() or '') for i in range(n_pages))
    texto_norm = norm(texto_conteudo)
    hits = sum(1 for w in palavras if norm(w) in texto_norm)
    print(f'MATCH:{hits}/{len(palavras)}' if palavras else 'MATCH:sem_palavras_chave')
else:
    print('MATCH:sem_assunto')
" "<caminho do .tmp>" "<assunto esperado, vindo da tabela do Passo 4>"
```

- **Duas datas por extenso** têm sido observadas na prática: numérica
  `DD/MM/AAAA` e escrita por extenso em português `DD de Mês de AAAA` (ex: "31
  de Julho de 2026" — confirmado testando no curso de Direito Administrativo,
  pacote Regular Fiscal). O script acima já cobre os dois formatos, tentando o
  numérico primeiro. Se aparecer um terceiro formato novo, adaptar o regex.
- **Segunda linha de saída (`MATCH:hits/total`):** compara palavras-chave do
  assunto esperado (≥4 letras, sem preposições comuns) contra o texto extraído.
  - `hits` igual a 0 com `total` maior que 0 → **nenhuma palavra-chave bateu**,
    sinal de possível conteúdo errado (aula baixada não corresponde ao rótulo
    esperado). Não travar o download por causa disso, mas **registrar essa
    aula como suspeita** pra citar na Validação Final (Passo 8) — é
    exatamente o tipo de erro que a validação por nome de arquivo sozinha não
    pega (aulaId pareado errado com o rótulo lá na origem, por exemplo).
  - `hits` maior que 0 → conteúdo consistente, seguir normalmente.
  - `MATCH:sem_assunto` ou `MATCH:sem_palavras_chave` → nada pra comparar
    (assunto muito curto ou não informado), seguir normalmente sem alarme.
  - **`total` igual a 1 ou 2 (poucas palavras-chave) é sinal de confiança
    baixa mesmo quando `hits` dá 0** — confirmado numa checagem em lote real
    em 2026-08-18: rodando essa checagem contra ~480 aulas já baixadas e
    confirmadas corretas por outros meios, todos os poucos casos de `0/total`
    encontrados eram assunto muito curto (1-3 palavras) cujo termo exato não
    aparecia no texto por variação de fraseado (ex: assunto "Noções
    Iniciais" vs. o PDF usando "Conceitos Iniciais"), não conteúdo errado de
    fato. Tratar `0/total` com `total` baixo como aviso fraco, não confirmação
    de erro — mencionar na Validação Final como "possível falso positivo,
    conferir manualmente se necessário", sem soar alarmista.
- **Checagem de conteúdo olha as primeiras 6 páginas do PDF, não só a
  primeira** — confirmado pelo Elvis em 2026-08-18: a página 1 desses livros
  costuma ser só uma capa (título, autor, data), sem o conteúdo da aula em si;
  o texto relevante só aparece a partir da página ~3-6 (depois de índice e
  apresentação do curso). Usar só a página 1 pra essa checagem gerava falso
  positivo em quase todo arquivo. A extração de **data** continua usando só a
  página 1 (isso sempre funcionou bem), é só a checagem de **conteúdo** que
  precisa olhar mais páginas.
- **Se der 0 acertos nas 6 primeiras páginas, ampliar pra ~25 antes de marcar
  como suspeita** — confirmado na prática em 2026-08-18 (pacote Regular
  Controle): das 211 aulas, 5 caíram como suspeitas e **todas as 5 eram falso
  positivo** — eram aulas cujo índice ocupa várias páginas, então em 6 páginas
  só tem capa e sumário. Ampliando a janela, o conteúdo aparece com folga (ex:
  a aula de SQL tinha 57 ocorrências de "sql" nas 25 primeiras páginas e 0 nas
  6 primeiras). A segunda passada só roda pras aulas que deram `0/total`, então
  custa quase nada. Só marcar `Suspeito` se continuar 0 depois dessa segunda
  passada — e mesmo aí vale a ressalva do `total` 1-2 (aviso fraco).
- Se `pypdf` não estiver instalado no ambiente, instalar com `pip install pypdf`
  antes de seguir.
- Se a página 1 tiver mais de uma data (raro), usar a primeira encontrada.
- **Fallback se não achar nenhuma data** (PDF escaneado sem texto, ou o padrão
  daquele curso for diferente): manter o nome do arquivo sem o sufixo de data
  (`Aula NN - Assunto Sintético.pdf`) e seguir normalmente — não travar o
  download por causa disso. Pode mencionar no resumo final que essa aula não
  teve data identificada.

### Comparar e substituir PDF já baixado (só em Atualização Completa)

Quando o sub-modo escolhido no Passo 3 for **Atualização Completa**, pra cada
aula que já tem PDF local:

1. Rebaixar o PDF normalmente (passos 1-8 acima) pra um arquivo temporário.
2. Extrair a data da primeira página do PDF novo.
3. Comparar com a data que já está no nome do arquivo local (entre parênteses).
4. **Se a data for igual:** apagar o `.tmp` recém-baixado, não mexer no arquivo
   existente.
5. **Se a data for diferente (ou o arquivo local não tiver data no nome, de uma
   coleta anterior à criação desse fluxo):** apagar o PDF antigo, renomear o
   `.tmp` pro nome final com a nova data. Vale registrar essa substituição pra
   mencionar no resumo final (ex: "Direito Constitucional, Aula 05: PDF
   atualizado de 12-03-2025 pra 08-07-2026").

## Passo 6: Aula ainda não disponível → placeholder `.txt`

Quando a aula não tiver nem "versão simplificada" nem "versão original" disponível
(o site costuma mostrar uma previsão de liberação no lugar do vídeo/PDF), **não
baixar nada** — criar um arquivo de texto no lugar, seguindo o mesmo padrão de nome
do PDF, só que terminando em mais um traço + a data prevista, extensão `.txt`:

```
Aula NN - Assunto Sintético - DD-MM-AAAA.txt
```

**Data com traço, nunca com barra** (`DD-MM-AAAA`, não `DD/MM/AAAA`) — barra não
é caractere válido em nome de arquivo no Windows e quebra a criação do arquivo.

Conteúdo do `.txt`: uma linha simples informando que o material ainda não estava
disponível na data da coleta e qual a previsão de liberação informada pelo site.

**Isso é um marcador importante:** sempre que encontrar um arquivo `.txt` nesse
formato dentro de uma pasta de curso, isso indica que aquela aula específica ainda
não tinha o livro liberado no momento em que os dados foram coletados — não é um
erro nem um arquivo esquecido.

## Passo 7: Fechar o nome da pasta — pendência `(N-M)` e data

> **Reescrito em 22-08-2026.** Duas mudanças em relação ao que estava aqui: o
> `(N-M)` passou do **começo para o FIM** do nome (REGRA 6), e a data do
> **pacote** deixou de ser atualizada (REGRA 9 — a data mora na disciplina).

Depois de processar todas as aulas:

1. Contar **M** = total de aulas do curso e **N** = quantas têm PDF de verdade
   (não os `.txt` placeholder do Passo 6).
2. **Se N < M**, a pasta recebe `(N-M)` **no fim do nome, antes da data**:

   ```
   LTRIB - Legislação Tributária Municipal (3-14) (22-08-2026)
   ```

   **Nunca no começo.** `(3-14) Legislação...` faz o parêntese ordenar antes de
   qualquer letra, e todas as pastas com pendência sobem juntas para o topo,
   agrupadas pelo **defeito** em vez de pela disciplina — brigando de frente com
   o prefixo de sigla, que existe justamente para agrupar.

   **Traço dentro do parêntese (`N-M`), nunca barra (`N/M`)** — barra é separador
   de caminho no Windows e quebra o `Rename-Item` com o erro "representa um
   caminho ou nome de dispositivo".
3. **Se N == M**, a pasta fica sem a marca: `LTRIB - Legislação Tributária Municipal (22-08-2026)`.
4. **Atualizar a data desta disciplina** para hoje, nessa mesma renomeação,
   independente de N ser igual ou menor que M.
5. **NÃO tocar na data da pasta do concurso.** Ela não tem data (REGRA 9). Se
   encontrar uma data lá, de execução antiga, **remover** — duas versões da mesma
   verdade divergem, e a do nível de cima mente assim que uma disciplina é
   atualizada sozinha.
6. **Antes de recalcular, limpar o que a pasta já tem**: remover marca `(N-M)`
   antiga (do começo ou do fim) e data antiga, para não acumular.
7. **Renomear em cima, sempre** (REGRA 4) — nunca apagar e recriar. Apagar perde
   os PDFs já baixados e, se o download falhar no meio, perde tudo.
8. **Atualizar o `renomear-pastas.csv`**: a coluna `pasta_atual_no_disco` recebe
   o nome novo, e o log `de -> para` vai para o CSV da pasta de logs.

## Passo 8: Validação final (obrigatória — sempre rodar antes de dar o curso como concluído)

**Confirmado pelo Elvis em 2026-08-18: essa validação é parte obrigatória da
skill, não um extra opcional — nunca reportar um curso como concluído sem
rodar esse passo.**

**Validação é só por nomenclatura, nunca reabrindo o conteúdo dos PDFs aqui** —
confirmado pelo Elvis em 2026-08-18: não vale a pena gastar tokens abrindo/lendo
cada PDF de novo nessa etapa. A checagem de conteúdo já aconteceu uma vez, de
graça, durante o download (ver "Extrair a data do PDF" no Passo 5, saída
`MATCH:hits/total`) — aqui só se **reporta** o que ela sinalizou, sem reabrir
nada. O cruzamento desse passo é puramente comparação de texto: rótulo da
listagem do site vs. nome do arquivo local.

Depois de processar todas as aulas:

1. **Conseguir a lista de rótulos atual do curso.** Se o download inteiro
   acabou de acontecer nessa mesma execução (sem intervalo relevante de
   tempo), **reaproveitar a tabela salva no Passo 4** em vez de gastar uma
   nova consulta ao site — não há motivo pra achar que algo mudou na
   plataforma nos últimos minutos. Só **re-consultar a listagem `/aulas` do
   site de novo** quando fizer sentido desconfiar que o estado pode ter
   mudado desde a coleta original (retomando um download de uma sessão
   anterior, ou um intervalo longo entre o Passo 4 e agora) — nesse caso, só
   o `get_page_text` da listagem, sem abrir aula por aula.
2. Listar os arquivos da pasta (`ls`), já com o nome renomeado no Passo 7.
3. **Cruzar as duas listas item a item, só pelo nome:**
   - Cada rótulo da listagem do site deve corresponder a exatamente um arquivo
     local (`.pdf` ou `.txt`) cujo nome começa com esse mesmo rótulo (ver regra
     de nomenclatura no Passo 5).
   - Rótulo do site sem arquivo local correspondente → aula não baixada de
     fato; investigar antes de considerar o curso concluído (aula travada que
     não virou `.txt`? erro silencioso no download?).
   - Arquivo local sem rótulo correspondente no site → pode ser rótulo digitado
     errado no nome do arquivo, ou aula que saiu da grade — investigar e, se for
     rótulo errado, renomear o arquivo pro rótulo certo (sem reabrir o PDF, só
     `mv`/`Rename-Item`).
4. Conferir que **N** (quantidade de `.pdf` reais) e **M** (total de itens na
   listagem do site) batem com o prefixo `(N-M)` aplicado no Passo 7.
5. **Listar as aulas sinalizadas como suspeitas pelo `MATCH:hits/total`** (ver
   Passo 5) — as que deram `0/total` durante o download. Não precisa reabrir o
   PDF aqui pra decidir; só trazer a lista pro resumo, junto com o resto.
6. **Reportar o resultado dessa validação pro usuário** — se bateu 100% por
   nome, se sobrou algo em algum lado, e se alguma aula ficou marcada como
   suspeita de conteúdo (item 5). Essa é a única parte do processo que sempre
   vale a pena resumir em texto no final, mesmo a skill normalmente não
   gerando relatório à parte.

O resultado final é a pasta em si, já com os arquivos dentro, o nome renomeado
com o progresso `(N-M)`, e a confirmação de que o cruzamento bateu.

## Passo 9: Planilha de metadados da disciplina (obrigatória, Google Sheets)

**Rodar sempre DEPOIS do Passo 7 (renomear a pasta).** A planilha grava o nome
da pasta no subtítulo (`Pasta: ...`), então se rodar antes da renomeação o
subtítulo já nasce desatualizado. Ordem correta do fecho:
downloads → Passo 7 (renomear) → Passo 9 (planilha) → Passo 8 (validação).

**Cuidado com o padrão "tenta abrir a aba, se falhar cria":** se o erro for de
quota (`429`) e não de aba inexistente, isso tenta criar uma aba que já existe
e devolve `400 Já existe uma página chamada "Legenda"`. Checar a existência da
aba pela lista de abas do arquivo, e só então limpar.

**Confirmado pelo Elvis em 2026-08-18: toda disciplina baixada ou atualizada
por essa skill tem uma planilha de metadados própria** — validada ao vivo com
o curso de Direito Administrativo antes de virar padrão. Ela serve de
histórico rápido (sem precisar reabrir PDF nem reconsultar o site) e é a base
pra checagem de Curso ID do Passo 3. **Escopo da atualização da planilha =
escopo da execução:** como essa skill processa uma disciplina só por vez, ela
sempre atualiza a planilha só dessa disciplina — nunca mexe na planilha de
outra matéria só porque estão no mesmo pacote (ver a mesma regra em escala
maior na skill `baixar-curso-completo-estrategia`, Passo 11).

1. **Sempre Google Sheets nativo, nunca `.xlsx` local** — confirmado pelo
   Elvis em 2026-08-18: essa é a preferência permanente, não uma opção entre
   outras. Usar `gspread` com as credenciais em `credenciais/` (escopos
   `spreadsheets` + `drive`). Achar o ID da pasta de destino no Drive
   replicando o caminho local por nome (`drive.files().list` com
   `mimeType = 'application/vnd.google-apps.folder'` e `'<parent_id>' in
   parents`), e criar com `gc.create(titulo, folder_id=...)` — isso já
   posiciona o arquivo na pasta certa sem precisar mover depois.
   **Se a autenticação falhar** (token expirado, credencial ausente, erro de
   escopo) — **não cair silenciosamente pro Excel local nem pular a
   planilha** — parar e pedir ao usuário pra fazer o login/reautorizar na
   hora, explicando o erro encontrado. Só considerar Excel local como último
   recurso se o próprio usuário disser que não vai conseguir reautorizar
   agora.
2. **Nome do arquivo:** `<SIGLA> - Metadados` — ex. `DCONST - Metadados`.
   **Reescrito em 22-08-2026:** o padrão antigo era
   `<Nome da Matéria> (SIGLA-SIGLA) - Metadados`, e foi exatamente ele que gerou
   o caminho de **263 caracteres**, acima do limite de 260 do Windows — repetia a
   disciplina que a pasta já dizia e o concurso que o nível de cima já dizia
   (REGRA 1). Sem sufixo de data: é documento único que se atualiza.
   **Disciplina sem sigla** (linha `pendente` no `renomear-pastas.csv`): usar o
   nome da pasta sem o concurso, ex. `Reforma Tributária - Metadados`.
2b. **Junto da planilha, gravar `_manifesto.csv` na mesma pasta**, com o mesmo
   conteúdo da aba `Aulas`. Planilha publicada é **vista, nunca fonte**: quem lê
   o levantamento (a base 2) não pode depender de OAuth nem de rede, e precisa de
   `git diff`. Os dois saem da **mesma estrutura em memória**, na mesma passada —
   nunca um a partir do outro, senão divergem. O CSV é gravado **antes** de
   qualquer chamada de rede, para que um `429` do Sheets não derrube a execução.
3. **Se já existir uma planilha de metadados na pasta** (modo atualização):
   abrir e **ler o Curso ID registrado antes de sobrescrever qualquer coisa**
   — é o dado que o Passo 3 usa pra comparar contra o ID atual da URL.
4. **Aba "Aulas"** — acrescentar, sem reescrever as existentes, as colunas
   `Sigla Disciplina`, `Hash Conteúdo` e `Alterado em`.
   **Por que `Sigla Disciplina` e não `Cód Mestre`:** o Cód Mestre é do TÓPICO, e
   bloco x tópico é **muitos para muitos** (`bases/DECISOES.md`, A14). Uma coluna
   única de Cód Mestre aqui afirmaria que uma aula tem um tópico só — o oposto do
   desenho. O vínculo com o tópico vive inteiro na tabela de pares da base 2.
   **Aviso obrigatório sobre o `Hash Conteúdo`:** o texto extraído do PDF local
   **contém a marca d'água** (`<CPF> - <Nome>`). Linha de base calculada sem
   filtrar faz todo hash futuro divergir e dá **falso positivo em 100% das
   aulas** na execução seguinte. Filtrar o padrão de 11 dígitos + hífen + nome
   antes de hashear (REGRA 8).
   Colunas originais: `Rótulo (Aula)`, `Assunto`, **`Versão do Livro`**,
   `Status` (Baixado/Baixado (conferido)/Suspeito, com cor condicional
   verde/vermelho — ver os três status logo abaixo), `Data de Elaboração (PDF)`,
   `Data desta Verificação`, `Palavras-chave batidas`, `Total palavras-chave`,
   `Nº de páginas do PDF`, `Nome do arquivo`. Linha de título mesclada +
   subtítulo com pasta, **Curso ID Estratégia** e nome do pacote/concurso. Linha
   de resumo com fórmulas (`COUNTA`, `COUNTIF`) pro total de aulas, confirmadas
   e suspeitas.

4.0-A. **Coluna `Versão do Livro`** (Elvis, 2026-08-20). Valores: `LS` (Livro
   Simplificado), `LC` (Livro Completo) ou `—` para categoria que não tem essa
   distinção. É o mesmo valor que vai no sufixo do nome do arquivo, e serve pra
   ver de relance quantas aulas da disciplina estão em cada paginação. Vale a pena
   uma célula no resumo com `=COUNTIF(<col>;"LS")` e `=COUNTIF(<col>;"LC")` —
   disciplina 100% `LC` é sinal de que aquela matéria não tem simplificado.

4.0-B. **Identificação do material e do pacote** (Elvis, 2026-08-20). O subtítulo
   passa a registrar, além de pasta e Curso ID:

   | Campo | Exemplo | Por que |
   |---|---|---|
   | **Tipo de Material** | `Curso Regular`, `Passo Estratégico`, `Bizu Estratégico`, `Trilha Estratégica`, `Monitoria`, `Rodadas de Simulados`, `Discursiva` | dizer o que é aquela pasta sem abrir os PDFs |
   | **Nome do Pacote** | `TCDF (Analista Administrativo... - ANACE) Pacotaço ... 2026 (Pós-Edital)` | é o nome exato de busca no catálogo |
   | **Pacote ID** | `393930` | volta direto no pacote |
   | **Link do Pacote** | `=HYPERLINK("https://www.estrategiaconcursos.com.br/app/dashboard/pacote/{pacoteId}";"Abrir pacote")` | um clique |

   **Por que o pacote importa tanto:** a matrícula é limitada a 3 produtos e o
   rodízio é constante, então achar de novo o pacote certo no catálogo é
   trabalhoso — e já custou tempo. Com o nome exato e o ID guardados, dá pra ir
   direto. Também é o que permite perceber que **um pacote saiu do ar**: se o
   `pacote/{id}` não abrir mais, o material daquela pasta virou histórico e não
   tem como ser atualizado.

   O `Tipo de Material` sai do `tipo_curso_id` de `GET /api/aluno/pacote/{id}`:
   `1`=Curso Regular, `3`=Monitoria, `5`=Trilha Estratégica, `7`=Passo
   Estratégico, `27`=Bizu Estratégico, `30`=Rodadas de Simulados.

   **Vale nos dois modos:** ao criar a planilha do zero e ao atualizar. Em
   planilha antiga que não tenha esses campos, **acrescentar** sem reescrever o
   resto — mesma lógica idempotente do item 4.0.
4.0. **Linha 3: link clicável pro curso no Estratégia** — confirmado pelo Elvis
   em 19-08-2026, depois de notar que nenhuma das 71 planilhas dos 4 pacotes já
   baixados dizia como voltar ao curso no site. Logo abaixo do subtítulo, antes
   da linha de resumo: `A3` = `Link do curso:` e `B3` (mesclada até `I3`) =
   `=HYPERLINK("https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{cursoId}/aulas";"Abrir no Estratégia")`,
   com o mesmo `{cursoId}` registrado no subtítulo. Em planilha antiga que já
   tenha conteúdo na linha 3, **inserir** uma linha nova (`insertDimension`) em
   vez de sobrescrever — o Sheets reajusta sozinho as referências das fórmulas
   de resumo. A regravação é idempotente: se `A3` já for `Link do curso:`, só
   atualizar o valor, sem inserir outra linha.
4.1. **Os três valores possíveis de `Status`** — confirmado pelo Elvis em
   2026-08-18:
   - **Baixado** — PDF salvo e conteúdo batendo com o assunto esperado.
   - **Baixado (conferido)** — a checagem automática não achou nenhuma
     palavra-chave, mas o PDF foi aberto e conferido na hora, e o conteúdo
     está certo. Serve pra não deixar registrado como suspeita uma aula que já
     foi verificada — sem esconder que a checagem automática falhou ali (as
     colunas de palavras-chave continuam mostrando `0/N`).
   - **Suspeito** — 0 palavras-chave batidas (mesmo depois de ampliar a janela
     de páginas) e **sem** conferência manual. É o único que fica vermelho.

   Na fórmula de resumo, "Confirmadas" conta os dois primeiros
   (`=COUNTIF(C7:C<fim>;"Baixado*")`), e a formatação condicional verde usa
   "começa com Baixado" pelo mesmo motivo.
5. **Aba "Legenda"** — explicação de cada coluna, igual ao protótipo, incluindo
   a distinção entre os três status acima.
6. **Formatação padrão** (ver preferência salva na memória — alinhamento
   centralizado horizontal e vertical, quebra de texto, largura de coluna
   ajustada ao conteúdo, remover excesso de linhas/colunas **deixando margem**
   de ~2-3 colunas e ~30 linhas depois do fim dos dados reais, nunca cortar
   rente).
7. **Separador de fórmula: `;`, nunca `,`** — confirmado em 2026-08-18: as
   planilhas desse workspace usam locale `pt_BR`, que exige ponto e vírgula
   como separador de argumento (`=COUNTIF(F7:F54;">0")`); vírgula gera
   `#ERROR!`. Fórmulas de um argumento só (`=COUNTA(...)`) não têm esse
   problema por não ter separador, o que mascara o erro se só se testar essas.
8. **Validar as fórmulas depois de escrever** — não existe `recalc.py`
   (LibreOffice) funcionando nesse ambiente Windows pra conferir
   automaticamente. Ler de volta cada célula de fórmula com
   `value_render_option='FORMATTED_VALUE'` (ou `UNFORMATTED_VALUE`) e
   confirmar que não é `#ERROR!`/`#REF!`/`#NAME?` antes de considerar a
   planilha pronta.
9. **Atualização parcial de aula por aula não é obrigatória** — pode
   regravar a aba "Aulas" inteira a cada execução com o estado atual (a data
   de verificação de cada linha já registra quando foi conferida); não
   precisa manter histórico de execuções anteriores linha a linha.
10. **Prever o limite de escrita por minuto da API do Sheets** — confirmado
    na prática em 2026-08-18. A cota é de **60 requisições de escrita por
    minuto por usuário**, e cada planilha consome várias (criar, `update`
    das duas abas, `resize`, `batch_update` de formatação). Numa disciplina
    só isso não incomoda, mas o script tem que aguentar o erro **HTTP 429**
    de qualquer jeito: envolver o processamento de cada planilha num retry
    com **espera de ~65s** (até ~6 tentativas) e deixar uma pausa de ~12s
    entre planilhas. **O mesmo retry tem que cobrir 5xx** (`503 The service
    is currently unavailable`) — confirmado em 19-08-2026: com o retry
    cobrindo só o 429, um 503 transiente derrubou planilhas que passaram
    normalmente na tentativa seguinte, sem nenhum outro ajuste. Sem isso a execução morre no meio, com parte das
    planilhas criadas. O script tem que ser **idempotente**: procurar pelo
    nome do arquivo na pasta de destino e reaproveitar a planilha existente
    em vez de criar uma duplicada ao retomar. Ver a mesma regra em escala de
    pacote na `baixar-curso-completo-estrategia`, Passo 11.

> ### O `nome_canonico` é congelado — nunca "arrumar"
>
> A coluna `nome_canonico` que sai nas planilhas e no `_manifesto.csv` é
> **irreversível, igual à sigla**. Motivo de plataforma: a Tutory reconhece que o
> aluno já estudou um assunto comparando **nome do assunto + nome da disciplina**;
> **um espaço a mais e ela trata como disciplina nova, e o histórico do aluno se
> perde**. Já existem hoje duas entradas de `Direito Administrativo` na Tutory que
> diferem por um único espaço.
>
> Portanto: **não corrigir** um nome canônico por parecer estranho, mal
> formatado ou inconsistente. Disciplina que a fonte fatia em vários cursos
> (`Tecnologia da Informação`, que o Estratégia parte em dois) tem **um nome
> canônico só**; o fatiamento vira apelido, na base 1.
>
> **Não confundir com o nome da PASTA**, que continua sendo o da fonte,
> sintetizado (REGRA 2). São coisas diferentes e podem divergir de propósito.
>
> O `conferir.py` da base 1 falha se algum nome divergir — uma "correção" bem
> intencionada derruba a conferência dela.

## Passo 9B: Índice do pacote (quando a matéria vive dentro de uma pasta de pacote)

**Confirmado pelo Elvis em 2026-08-19.** Se a pasta da matéria estiver dentro de
uma pasta de pacote (ex: `ISS Manaus (AFTM) 2026 (19-08-2026)/Curso Regular/
Direito Administrativo (ISS Manaus-AFTM) (19-08-2026)/`), a raiz do pacote tem
uma planilha `<Nome do Pacote> - Índice do Pacote`, com a aba `Produto` (as
variantes do produto no Estratégia — Curso Regular / Pacotaço / Pacotaço +
Sistema de Questões, com o `Pacote ID` e o link de cada uma) e a aba
`Disciplinas` (uma linha por matéria, com Curso ID, link, pasta e contagem).
O formato completo está no **Passo 11B da `baixar-curso-completo-estrategia`** —
essa skill não redefine o layout, só mantém a planilha em dia.

O que fazer aqui, sempre depois do Passo 9:

- **Se o índice existir:** atualizar só a linha da matéria processada agora
  (Curso ID, link, pasta, aulas baixadas, aulas pendentes, link da planilha de
  metadados) e a data da linha. Não mexer nas linhas das outras matérias.
- **Se não existir e a matéria estiver dentro de uma pasta de pacote:** criar o
  índice com a aba `Produto` preenchida (levantando as variantes no catálogo,
  conforme o Passo 11B) e a aba `Disciplinas` só com a matéria desta execução —
  as demais entram quando forem processadas.
- **Se a matéria for avulsa** (não está dentro de pasta de pacote), pular este
  passo. Não criar índice de pacote pra matéria solta.
- Se houve rodízio de matrícula nessa execução, refletir isso na coluna
  `Matriculado hoje` da aba `Produto`.

## Passo 10: Sugestões de melhoria pra skill (sempre, ao final de toda execução)

**Confirmado pelo Elvis em 2026-08-18: ao final de todo download/atualização
de curso, refletir se algo observado nessa execução sugere um ajuste na
própria skill, e apresentar pro usuário aprovar** — não é opcional, é parte
do encerramento normal do processo.

- A sugestão tem que ser **concreta e ligada a algo que realmente aconteceu**
  nessa execução (um padrão novo do site, uma pegadinha de nomenclatura, um
  erro que exigiu correção manual, uma repetição que dava pra automatizar) —
  não inventar sugestão genérica só pra preencher esse passo.
- **Se nada relevante surgiu na execução, dizer isso e seguir** — não forçar
  uma sugestão fraca só porque o passo pede uma.
- Apresentar a sugestão junto do resto do resumo final (validação +
  planilha), não como uma pergunta solta separada.
- **Só implementar depois que o usuário aprovar** — esse passo é só de
  levantar a sugestão pro aval dele, igual ao processo que gerou boa parte das
  regras já registradas nessa skill (todas nasceram de sugestões discutidas e
  aprovadas em sessões anteriores, não de decisão unilateral).

## Detalhes técnicos e pegadinhas (aprendidos na prática)

- **Limite de 260 caracteres de caminho no Windows** — o orçamento por nível está
  em `bases/NOMENCLATURA.md` e **este documento não o repete**, para não divergir.
  O que manda é o **caminho real chegar a 240**, não a soma dos tetos; e quando
  chegar, **quem encurta é o nome do ARQUIVO, nunca o da pasta** (REGRA 10).
  Medir sempre o caminho **absoluto**: `os.path.join(raiz, dirpath, f)` com
  `dirpath` vindo de `os.walk('.')` no Windows **descarta a raiz** quando o
  componente começa com barra invertida, e o número sai plausível (215 em vez de
  263) — usar `os.path.abspath`. Se a soma projetada passar de ~240
  caracteres (deixando margem de segurança), sintetizar o nome da matéria e/ou o
  assunto da aula no nome do arquivo até caber — está autorizado a fazer essa
  redução sozinho, sem perguntar ao usuário, priorizando manter a sigla e o
  número da aula intactos (é o que mais identifica o arquivo) e cortando a parte
  descritiva.
- **Contar a pasta já com o que o Passo 7 vai acrescentar depois** — confirmado
  em 19-08-2026: o Passo 7 renomeia a pasta somando o sufixo ` (DD-MM-AAAA)`
  (e, se o curso estiver incompleto, o prefixo `(N-M) `), ou seja **+13
  caracteres de uma vez em todos os arquivos daquela pasta**. Num pacote isso
  estourou 69 arquivos que tinham nascido dentro do limite. Ao projetar o
  caminho na hora de nomear, usar o nome **final** da pasta, não o nome base.
- **Se algum arquivo estourar mesmo assim, como consertar** — as duas saídas
  óbvias não funcionam nesse ambiente: o prefixo `\\?\` de caminho longo **não
  funciona no drive do Google Drive**, e caminho relativo também não resolve
  (o Windows soma o CWD antes de aplicar o limite). O que funciona é
  **renomear a pasta pra um nome curto temporário** (ex: `_x`), encurtar os
  arquivos lá dentro, e devolver o nome real — calculando o corte pelo
  comprimento do caminho final, não do temporário, e preservando o sufixo de
  data do arquivo.
- **Truncar nome de arquivo sem perder o que diferencia dois arquivos:** se dois
  arquivos da mesma matéria têm título quase idêntico e só diferem no final,
  truncar o texto genérico pra um tamanho fixo faz os dois ficarem com o mesmo
  nome e um sobrescreve o outro. Colocar o que diferencia **no início** do nome
  do arquivo, antes do texto que vai ser truncado.
- **Nem todo curso começa em "Aula 00"** — alguns começam direto em "Aula 01".
  Não assumir que "Aula 00" sempre existe; usar a primeira aula que realmente
  aparecer na listagem.
- **A primeira aula pode estar travada** (com "Disponível em DD/MM/AAAA") —
  trata-se normalmente como qualquer aula bloqueada: vira placeholder `.txt`
  (Passo 6), não é motivo pra pular pra segunda aula.
- **Nunca clicar às cegas em coordenadas fixas** achando que o layout é idêntico
  entre aulas — sempre esperar carregar (`wait` ~1.5-2s) e, se possível, confirmar
  com `screenshot` ou `read_page` antes de clicar, porque o scroll/posição dos
  cards muda de aula pra aula.
- **Fechar aba + navegar na mesma aba de controle no mesmo `browser_batch`** costuma
  falhar com erro de "tab not in same group" — fazer isso em duas chamadas
  separadas (fechar a aba do PDF numa chamada, navegar na outra).
- O link da CDN é assinado e temporário (parâmetro `Expires`), mas isso só afeta
  o **link de download** — o arquivo já baixado no disco é permanente como
  qualquer PDF.
- O Chrome do usuário precisa ficar aberto (pode minimizado) durante toda a
  execução — a extensão controla o navegador real dele, não existe navegador
  interno alternativo com a sessão logada.
- Ao repetir a lista de aulas depois de baixar uma, a página volta pro topo —
  rolar de novo até a aula desejada antes de clicar nela.
- **Atualização Completa é mais lenta e consome mais banda** — rebaixa todo PDF
  já existente só pra comparar a data. Não é o padrão sugerido; só usar quando o
  usuário pedir explicitamente ou aceitar a opção quando oferecida no Passo 3.
- Extração de data depende de `pypdf` (Python). Se o pacote não estiver
  instalado, instalar com `pip install pypdf` antes de processar a primeira aula.

## Regras gerais

- Não baixar vídeos, resumos, slides, mapas mentais ou cadernos de questões —
  só o livro eletrônico (PDF), simplificado ou original.
- Não pular a pergunta inicial (link + pasta) nem a confirmação do Passo 3
  (pasta existente encontrada → Atualização Parcial, Atualização Completa ou
  criar nova) mesmo que o usuário pareça claramente já ter dado essas
  informações antes — confirmar a cada execução da skill.
- Se o curso tiver dezenas de aulas, processar tudo sem pausar pra pedir confirmação
  a cada aula — só reportar progresso a cada poucas aulas ou no final.
