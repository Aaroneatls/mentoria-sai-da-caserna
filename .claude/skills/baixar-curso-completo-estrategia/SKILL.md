---
name: baixar-curso-completo-estrategia
description: >
  Baixa em lote os livros eletrônicos (PDF) de um PACOTE completo do Estratégia
  Concursos (várias matérias/categorias de uma vez — Curso Regular, Passo
  Estratégico, Bizu Estratégico etc), organizando tudo em pastas por categoria
  e por matéria. Diferente da baixar-curso-especifico-estrategia (que baixa só
  UM curso/matéria por vez), essa skill mapeia o pacote inteiro primeiro e
  pergunta quais categorias baixar. Use quando o usuário mandar um link de
  pacote do estrategiaconcursos.com.br (padrão
  `/app/dashboard/pacote/{id}`), ou disser "baixa esse pacote inteiro do
  Estratégia", "baixa o curso completo", "baixa tudo desse concurso no
  Estratégia", "sincroniza o pacote inteiro pra pasta".
---

# /baixar-curso-completo-estrategia — Download em lote de um PACOTE completo do Estratégia Concursos

## O que essa skill faz

Usa o Chrome real do usuário (via extensão Claude in Chrome, já logado no Estratégia
Concursos) pra abrir a página de um **pacote** (não um curso único), mapear todas as
matérias/categorias que existem dentro dele, perguntar ao usuário quais categorias
baixar, e então baixar — direto no disco, sem passar pela pasta de Downloads — o
livro eletrônico de cada aula de cada matéria selecionada, organizado em pastas por
categoria.

Se o link que o usuário mandar for de um curso único (`/app/dashboard/cursos/{id}/aulas`,
não um pacote), avisar e sugerir usar a skill `baixar-curso-especifico-estrategia` em vez
dessa.

## Passo 0: Perguntas obrigatórias no início

**Pasta padrão:** `G:\Meu Drive\Inteligência Artificial\Estrategia`
— é aqui que as pastas novas são criadas por padrão, salvo o usuário indicar
outro local. **Essa pasta vive dentro do Google Drive sincronizado**, então
antes de usar ela **verificar que ela existe de fato no disco** (`Test-Path` /
`ls`). Por ser uma pasta sincronizada, pode não estar montada/sincronizada no
momento — se não existir, avisar o usuário em vez de simplesmente criar uma
pasta nova do zero em outro lugar.

Sempre perguntar antes de fazer qualquer coisa (não assumir, não pular):

1. **Link do pacote** — a URL da página do pacote no Estratégia Concursos (padrão
   `https://www.estrategiaconcursos.com.br/app/dashboard/pacote/{id}`).
2. **Pasta:** perguntar se quer usar a **pasta padrão** (acima) ou indicar um
   **novo local**. Se confirmar a padrão, usar ela direto. Se pedir outro local,
   usar o caminho informado.

**Não perguntar aqui se é "novo ou atualização"** — isso é descoberto sozinho no
Passo 2, depois de identificar o concurso/cargo (Passo 1) e procurar
automaticamente por uma pasta de pacote já existente dentro do local informado.
Ver Passo 2.

3. **Base de siglas de disciplinas (pergunta temporária, perguntar sempre que
   a skill for carregada):** perguntar se já existe alguma planilha/tabela de
   referência com nome de disciplina → sigla. **Hoje essa base ainda não
   existe** — enquanto não existir, seguir usando o nome completo da matéria
   no nome da pasta (padrão atual do Passo 6). Quando o usuário criar essa
   base no futuro, ele vai indicar — a partir daí, usar a sigla da disciplina
   no lugar do nome completo ao montar o nome da pasta. Até lá, essa pergunta
   serve só de lembrete pro usuário, não bloqueia o fluxo. **Por que isso
   importa:** confirmado pelo Elvis em 2026-08-18, depois de um caso real em
   que somar o sufixo de data (Passo 6) ao nome já grande da matéria estourou
   o limite de 260 caracteres do Windows num arquivo — usar sigla no lugar do
   nome completo da matéria é a forma mais eficaz de ganhar margem de caminho
   de forma permanente, em vez de só sintetizar nome de arquivo caso a caso.

Não seguir em frente sem as respostas 1 e 2 acima.

**Reduzir o tamanho do caminho é uma preocupação constante, não só nos casos
óbvios** — confirmado pelo Elvis em 2026-08-18. Sempre que for nomear pasta ou
arquivo (pacote, categoria, matéria ou aula), já pensar no caminho completo
resultante (ver orçamento de caracteres nos "Detalhes técnicos" mais abaixo) e
preferir a versão mais curta que ainda deixe a aula identificável — não
esperar bater no limite pra só então cortar.

**PERGUNTA 0 — QUAL MODO?** Antes de qualquer outra: `baixar` (não existe no
disco) · `atualizar` (existe, atualiza só o que mudou) · `conferir` (só lê e
relata, não escreve nada). Se o usuário não disser, a existência da pasta do
pacote decide entre `baixar` e `atualizar` — confirmar antes de escrever.
**Se for `conferir`, não seguir a numeração dos passos:** ir direto ao caminho
curto descrito na seção abaixo e encerrar ali.

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

**Termina aqui, não entra nos passos de download.** "Faça tudo mas não escreva"
erra fácil, e o erro grava no Drive.

1. Levantar o pacote pela API: disciplinas, aulas, `is_disponivel`, e quais
   vídeos têm `resumo` / `mapa_mental`.
2. Levantar o disco: pastas de categoria e disciplina, PDFs, placeholders `.txt`,
   subpasta de apoio, `_manifesto.csv`.
3. Comparar e relatar, **por disciplina**: aula na plataforma e não no disco;
   aula no disco e não na plataforma; `hash_conteudo` divergente; apoio ainda não
   baixado; nome fora do padrão do `bases/NOMENCLATURA.md`; caminho passando de
   240 caracteres.
4. Encerrar com o relatório. **Nenhuma gravação** — nem PDF, nem planilha, nem
   manifesto, nem renomeação, nem troca de matrícula.

Divergência que não der para explicar: **parar e reportar ao Elvis**.

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

## Passo 1: Escolher o navegador, abrir o pacote e identificar concurso / cargo

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
     `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__browser_batch,mcp__claude-in-chrome__find,mcp__claude-in-chrome__form_input,mcp__claude-in-chrome__javascript_tool`
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

   - **Mecânica de download é a mesma nos dois navegadores** (ver Passo 7) —
     a diferença é só qual conjunto de tools chamar. Não depende de clicar em
     card nem abrir aba, então a instabilidade de clique em coordenadas
     observada no navegador embutido não afeta esse fluxo.
2. Navegar até o link do pacote. Se o navegador pedir aprovação de domínio (ou
   login, no caso do navegador embutido), é normal na primeira vez.
3. Ler o título da página pra extrair:
   - **Sigla do concurso** (ex: TCDF) — geralmente já vem entre parênteses no título.
   - **Cargo** (ex: Auditor Fiscal de Tributos Municipais).
4. **Sigla do cargo:** se não tiver uma sigla óbvia no título, pesquisar (na própria
   página ou na internet) pela sigla oficial do cargo pro concurso em questão, e
   decidir sozinho — não precisa confirmar com o usuário.
5. **Sigla do concurso quando não vem óbvia entre parênteses:** pesquisar no Google
   (cruzando com o próprio site do Estratégia Concursos como referência) pelo nome
   do concurso/edital pra achar a sigla oficial ou a forma abreviada mais usada.
   Manter a sigla como ela realmente é usada — não forçar juntar palavras num
   bloco só se o uso comum mantém espaço (ex: o concurso "ISS Manaus" usa a sigla
   com espaço mesmo, `ISS Manaus`, não `ISSMANAUS`).
6. **Pacote "Regular" sem concurso específico:** alguns pacotes não são de um
   concurso/edital específico — são pacotes genéricos por área, cobrindo
   matérias comuns a vários concursos daquela área. **O sinal pra reconhecer
   esse caso é a própria palavra "Regular" no nome do pacote** (ex: título
   "Curso Regular para Área Fiscal - Pacote Completo" → é o pacote "Regular
   Fiscal"; existe também "Regular Controle"), não a ausência de sigla de
   edital. Ao identificar esse padrão, usar `(Regular <Área>)` no lugar de
   o identificador do concurso **na pasta do nível 1** (ex: `Regular Fiscal`), e NUNCA no nome da pasta da disciplina (REGRA 1) (ex: `Direito
   Administrativo (Regular Fiscal)`). Não precisa perguntar ao usuário quando
   reconhecer esse padrão — só confirmar se o próprio nome da área ficar
   ambíguo.
7. **"Reforma Tributária" conta como disciplina própria, e pode aparecer mais
   de uma vez no mesmo pacote** — confirmado pelo Elvis em 2026-08-17. Não é
   pra descartar nem tratar como "extra". Quando o nome "Reforma Tributária"
   aparecer em mais de um item do pacote (ex: "Legislação Tributária sobre o
   Consumo (LTC) - Reforma Tributária...", "Reforma Tributária - Lei
   Complementar nº 227/2026...", "Reforma Tributária (LC nº 227/2026)" — cada
   um cobrindo uma frente diferente da reforma, não duplicados), tratar como
   **uma matéria "Reforma Tributária" com uma subpasta por curso**:
   `Curso Regular/Reforma Tributária (Regular <Área>)/<nome curto do curso
   específico>/` — o nome de cada subpasta sintetizado a partir do que
   diferencia aquele curso dos outros (diploma legal e/ou professor), já que
   os títulos completos tendem a ser grandes e parecidos entre si. Reconhecer
   esse padrão sozinho, sem precisar perguntar ao usuário.

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

## Passo 2: Procurar pasta de pacote existente antes de criar (detecção automática)

**Escopo da busca: só dentro da pasta informada no Passo 0** (a pasta padrão ou
o outro local que o usuário indicou) — nunca varrer o computador inteiro nem
outras pastas fora dali.

Com o identificador do concurso definido no Passo 1, procurar dentro
dessa pasta por uma pasta de pacote já existente que corresponda a esse
concurso/cargo — o nome raiz do pacote é livre, então o jeito confiável de
identificar é abrir as pastas de primeiro nível encontradas e checar se as
subpastas de categoria/matéria lá dentro usam essa mesma sigla (ex: `Direito
Constitucional (TCDF-ANACE)`). **Comparação:** ignorar maiúsculas/minúsculas,
acentuação, um eventual prefixo `(N-M)` nas subpastas, e o sufixo de data
`(DD-MM-AAAA)` no final tanto da pasta do pacote quanto de cada subpasta de
matéria.

**A varredura tem que descer até os arquivos, não parar no primeiro nível** —
confirmado em 2026-08-18, depois de um erro real: uma matéria pode ter
**subpastas** (a própria skill cria isso pra Reforma Tributária, ver Passo 1.7),
então os PDFs podem estar dois níveis abaixo da pasta de matéria. Numa execução
a pasta `Reforma Tributária (Regular Fiscal)` foi dada como vazia quando na
verdade tinha 33 PDFs em 3 subpastas — porque a listagem parou num nível acima.
Usar varredura recursiva (`os.walk` / `find`) ao contar o que já existe, nunca
só `ls` do primeiro nível. Vale também pro Passo 4 e pro `(N-M)` do Passo 9:
numa matéria com subpastas, **N e M são a soma de todas elas**, e o prefixo e a
data vão na pasta da matéria (a mãe), não em cada subpasta.

**Se encontrar exatamente uma pasta de pacote correspondente:**

1. Resumir o que já tem: quais categorias existem, quantas matérias em cada uma,
   e quantas já estão completas vs incompletas (olhando o prefixo `(N-M)` de
   cada subpasta — ver Passo 9).
2. Informar o usuário e perguntar como quer proceder, com três opções:
   - **Atualização Parcial** (padrão sugerido) — baixa só as aulas que ainda
     estão faltando em cada matéria (travadas na coleta anterior, agora
     liberadas). Não mexe nos PDFs já baixados. Rápido.
   - **Atualização Completa** — além de baixar o que falta, reconfere **todos**
     os PDFs já baixados do pacote inteiro contra a versão atual no site e
     substitui os que tiverem sido revisados/atualizados desde a última coleta.
     Bem mais lento num pacote grande, porque precisa rebaixar cada aula já
     existente pra comparar.
   - **Criar pasta nova do zero** — mesmo já tendo uma pasta encontrada.
3. **Se optar por Atualização Parcial ou Atualização Completa:** esse vira o
   modo atualização pro resto da skill — usar essa pasta como a pasta do
   pacote, seguir a partir do Passo 4 (mapear o que já existe localmente e
   cruzar com o site), no sub-modo escolhido.
4. **Se optar por criar nova do zero:** perguntar também **se quer que a pasta
   antiga localizada seja apagada** (nunca apagar sem essa confirmação explícita
   — é uma ação destrutiva e irreversível) ou se prefere manter as duas
   coexistindo (nesse caso, a pasta nova precisa de um nome que não conflite —
   confirmar com o usuário como diferenciar, ex: sufixo com a data da coleta).

**Se encontrar mais de uma pasta de pacote correspondente** (ex: mais de um
pacote baixado pro mesmo concurso/cargo): **não escolher sozinho** — listar
todas as encontradas (caminho completo de cada uma) e perguntar ao usuário qual
delas é a certa antes de seguir.

**Se não encontrar nenhuma pasta correspondente:** é download novo — a pasta do
pacote vai ser criada do zero dentro do local informado (ver Passo 6). Não tem
o que atualizar, então não precisa perguntar mais nada sobre isso.

## Passo 3: Mapear todas as matérias do pacote e categorizar

1. Usar `get_page_text` na página do pacote pra listar todos os cursos/blocos que
   aparecem (cada linha é um item clicável).
2. **Classificar cada item por padrão de nome:**

   | Padrão no nome | Categoria | Padrão de download |
   |---|---|---|
   | Nome de matéria puro (sem prefixo/sufixo especial) | **Curso Regular** | livro simplificado + original (fallback) |
   | Começa com "Passo Estratégico de " | **Passo Estratégico** | livro único por aula |
   | É exatamente "Bizu Estratégico" (curso único, matérias viram "aulas" dentro dele) | **Bizu Estratégico** | livro único por aula |
   | Começa com "Simulado" | **Simulado** | livro único por aula (simulado + gabarito são aulas separadas) |
   | É "Discursiva Sem Correção" | **Discursiva** | livro único por aula |
   | Contém "Trilha Estratégica" | **Trilha Estratégica** | livro único por aula (numeração "Trilha NN" em vez de "Aula NN") |
   | Começa com "Monitoria" | **Monitoria** | livro único por aula (**tem** livro eletrônico — confirmado em 2026-08-18) |
   | Qualquer outro padrão não reconhecido | **Outra categoria** — criar uma categoria nova com nome descritivo baseado no padrão observado | testar ao abrir a primeira aula (Passo 6) |

   **Monitoria** é curso único, com poucas aulas (5 no pacote Regular
   Controle), sobre ciclo de estudos, análise estatística de banca e
   estratégia de revisão — não é matéria de conteúdo. Vira **uma pasta só**
   dentro da categoria, igual Bizu/Trilha/Simulado (ver Passo 6).

3. **Todas as categorias têm livro eletrônico pra baixar**, inclusive Simulado,
   Discursiva e Trilha Estratégica — confirmado na prática: cada uma delas segue
   o mesmo padrão de card único "Baixar Livro Eletrônico versão original" que o
   Passo Estratégico e o Bizu Estratégico usam (ver Passo 7). Não existe categoria
   "sem livro" por padrão — todas entram como opção de download no Passo 5.
4. Se aparecer algum item cuja categoria não dá pra determinar só pelo nome, abrir
   o curso (Passo 6) rapidamente pra checar o card de "Baixar Livro Eletrônico"
   antes de decidir em qual grupo de padrão de download ele se encaixa.
5. **Dois itens com o nome exatamente igual e Curso IDs diferentes → perguntar,
   não escolher sozinho.** Confirmado na prática em 2026-08-18: o pacote Regular
   Controle trazia duas "Trilha Estratégica" com título idêntico, IDs `226812` e
   `369916` — uma com as aulas descritas como "(Pré-Edital)" e outra com
   numeração limpa, ou seja, edições diferentes do mesmo material. **O ID maior
   costuma ser o mais recente, mas isso não é garantia** e o usuário pode querer
   as duas. Abrir a listagem de cada uma pra descrever a diferença (quantas
   aulas, como as aulas estão descritas) e perguntar: só a mais nova, só a
   antiga, ou as duas. Se ele pedir as duas, criar **uma subpasta por edição**
   dentro da pasta da categoria, pra não misturar arquivos de mesmo rótulo.

## Passo 4: Modo atualização — mapear o que já existe localmente e cruzar com o site

**Só se aplica se o Passo 2 resultou em atualização.** Em modo novo, pular direto
pro Passo 5.

1. Listar a pasta do pacote (localizada no Passo 2): quais pastas de categoria
   existem (`Curso Regular`, `Passo Estratégico`, etc), e dentro de cada uma,
   quais subpastas de matéria/bloco já existem.
2. Pra cada subpasta de matéria já existente, ler o nome (extrair o prefixo
   `(N-M)` se tiver — ver Passo 9) e contar os arquivos reais dentro: quantos
   `.pdf` (já baixados, com a data entre parênteses no nome — ver Passo 7) e
   quantos `.txt` (placeholder de aula ainda não disponível na coleta anterior,
   com a data prevista depois de um traço).
3. Pra cada matéria com `.txt` pendente, abrir a listagem `/aulas` dela no site
   (usando o mapeamento do Passo 3 pra achar o link certo) e comparar: quais
   aulas que antes estavam travadas ("Disponível em DD/MM/AAAA") já aparecem
   liberadas agora ("Não estudei"/estudada)? Essas são as aulas **atualizáveis**.
4. **Conferir o Curso ID de cada matéria antes de tratar como atualização —
   crítico, confirmado pelo Elvis em 2026-08-18.** Mesma lógica da skill
   `baixar-curso-especifico-estrategia` (ver "Conferir o Curso ID do
   Estratégia" no Passo 3 dela, incluindo a comparação do assunto da Aula 00
   antiga vs. nova pra dar contexto no aviso): se a matéria já tem planilha
   de metadados (Passo 11 abaixo), comparar o Curso ID registrado nela com o
   ID da URL atual daquela matéria. Se diferente, **avisar o usuário logo no
   início** em vez de decidir sozinho — a Estratégia às vezes atribui ID novo
   a um curso mantendo o mesmo conteúdo, então ID diferente não é prova de
   curso diferente; o critério real é comparar disciplinas/aulas. Fazer essa
   checagem matéria por matéria, não só uma vez pro pacote inteiro.
5. Apresentar um resumo pro usuário, por categoria e matéria, por exemplo:

   ```
   O que já existe na pasta informada:
   - Curso Regular
     - (10-20) Direito Administrativo — 3 aulas novas liberadas desde a última coleta
     - (20-20) Direito Constitucional — completo, nada pra atualizar
   - Passo Estratégico
     - (5-19) Economia — 1 aula nova liberada
   ```

5. Perguntar: **"Quer que eu atualize essas pastas?"** — com a opção de
   confirmar todas de uma vez, ou escolher manualmente quais matérias atualizar.
   Não seguir pro download sem essa confirmação.
6. **Se o sub-modo escolhido no Passo 2 for Atualização Parcial:** matérias que
   existem localmente mas não têm nenhuma aula nova liberada não precisam de
   ação — só mencionar no resumo que já estão em dia (ou completas).
7. **Se o sub-modo escolhido no Passo 2 for Atualização Completa:** toda matéria
   com PDF já baixado entra na lista de processamento, mesmo as completas — vai
   ser reconferida no Passo 7 (rebaixar e comparar data). No resumo, marcar essas
   como "completa — será reconferida" em vez de "nada pra atualizar".

## Passo 5: Apresentar o mapeamento e perguntar quais categorias baixar

**Modo novo:** mostrar pro usuário um resumo tipo:

```
Categorias encontradas nesse pacote:
- Curso Regular (20 matérias) — livro simplificado + original
- Passo Estratégico (19 matérias) — livro único por aula
- Bizu Estratégico (1 bloco, várias matérias como aulas) — livro único por aula
- Discursiva Sem Correção (1 bloco) — livro único por aula
- Trilha Estratégica (1 bloco) — livro único por aula (numeração "Trilha NN")
- Simulado (1 bloco) — livro único por aula (simulado + gabarito)
```

Perguntar (com uma opção padrão recomendada) quais categorias baixar:

- **Só Curso Regular** (padrão sugerido — é o material principal, com livro
  simplificado)
- **Só Passo Estratégico**
- **Todas as categorias**
- **Escolher manualmente** (usuário lista quais categorias específicas quer)

Não seguir pro download sem essa resposta.

**Modo atualização:** essa pergunta já foi respondida no Passo 4 (quais matérias
atualizar) — não repetir. Seguir direto pro Passo 6 só com as matérias
confirmadas lá. Se o usuário quiser, nesse modo, também baixar matérias/categorias
novas que apareceram no pacote desde a última coleta (e ainda não têm pasta
local), perguntar isso separadamente antes de prosseguir.

## Passo 6: Criar a estrutura de pastas (padrão `bases/NOMENCLATURA.md`)

> **Reescrito em 22-08-2026, autorizado pelo Elvis** (`agentes/AUTORIZACOES.md`).
> O padrão antigo — `<Pacote> (DD-MM-AAAA)/<Categoria>/<Matéria> (SIGLA-SIGLA) (DD-MM-AAAA)/`
> — **está extinto**. Ele repetia o concurso dentro da pasta da matéria e punha
> data em dois níveis; foi a causa medida do caminho de 263 caracteres contra o
> limite de 260 do Windows, com 157 arquivos acima de 240.

```
<pasta raiz>/<Concurso> (<Sigla>) <Ano>/          <- SEM data (REGRA 9)
├── Curso Regular/
│   ├── DCONST - Direito Constitucional (18-08-2026)/
│   ├── CONTAB - Contabilidade Geral e Avançada - Possati (18-08-2026)/
│   └── ...
├── Passo Estratégico/
│   ├── DCONST - Direito Constitucional (18-08-2026)/
│   └── ...
├── Bizu Estratégico/
│   └── Bizu Estratégico (18-08-2026)/        <- pasta única, não separa por matéria
├── Trilha/
│   └── Trilha Estratégica (18-08-2026)/      <- pasta única
└── Rodadas Avançadas/
    └── Rodadas Avançadas (18-08-2026)/       <- pasta única
```

### As quatro regras que mudaram

1. **A data mora na disciplina, não no concurso** (REGRA 9). Com o modo
   `atualizar`, a atualização é **por disciplina**: uma data no nível do pacote
   passa a mentir assim que uma única matéria for atualizada sozinha. **Não pode
   ficar nos dois lugares** — são duas versões da mesma verdade, e divergem. Se
   encontrar data na pasta do concurso, de execução antiga, **remover**.
2. **A pasta da disciplina é `<SIGLA> - <Nome que a fonte usa> (<DD-MM-AAAA>)`**,
   e **nunca repete** o concurso, o cargo ou a categoria (REGRA 1). A sigla vem
   de `bases/01-disciplinas/dados/renomear-pastas.csv`, casando pela coluna
   `pasta_atual_no_disco` **por igualdade**. Linha `pendente`: **sem prefixo**,
   nunca chutar sigla.
3. **O nome da fonte pode ser sintetizado, nunca traduzido** (REGRA 2). Quem
   procura na plataforma tem de achar pelo nome que está lá.
4. **Tipo de curso é nível próprio e existe mesmo quando só há um**, porque a
   estrutura tem de ser previsível para a skill que lê. Valores fixos:
   `Curso Regular` · `Passo Estratégico` · `Bizu Estratégico` · `Monitoria` ·
   `Trilha` · `Rodadas Avançadas`.

### A pasta `Reforma Tributária` fica como está

**Não desmembrar por curso** (revisado pelo Elvis em 22-08-2026). A pasta guarda
três cursos (`336350`, `371461`, `389109`), mas **o 336350 sozinho já tem os dois
conteúdos dentro**: Lei Kandir (parte geral) é `LTRIB`, e LC 214/2025, LC 227/2026
e EC 132/2023 são `REFTRI`. Um curso, dois códigos.

Separar pasta ou curso gasta trabalho e **continua com os dois conteúdos
misturados** dentro de um deles. **A separação é de BLOCO**, feita na base 2 lendo
os PDFs. Ver `bases/DECISOES.md`, seção "O curso 336350 é COMPARTILHADO".

### Categorias que são um curso só

Bizu Estratégico, Trilha, Monitoria e Rodadas Avançadas já são um curso único no
site, não um curso por matéria — então viram **uma pasta só** dentro da categoria,
com todos os PDFs dentro, e **sem prefixo de sigla** (não são disciplina).

### Duas matérias com o mesmo nome

Diferenciar pelo professor, mantendo **a mesma sigla** nas duas (é a mesma
disciplina nossa, dois professores):

```
CONTAB - Contabilidade Geral e Avançada - Possati (18-08-2026)/
CONTAB - Contabilidade Geral e Avançada - Cardozo (18-08-2026)/
```

### Comprimento

O que manda é o **caminho real chegar a 240**, não a soma dos tetos. Chegando,
**quem encurta é o ARQUIVO, nunca a pasta** (REGRA 10). Medir sempre o caminho
**absoluto** — `os.path.join` com componente iniciado por barra invertida
descarta a raiz e devolve número plausível e errado.

**Conferir a data de hoje no ambiente antes de montar qualquer nome.** Erro real
em 19-08-2026 (pacote ISS Manaus): as pastas existentes eram de `(18-08-2026)`,
a skill cita essa data em vários pontos, e o pacote inteiro nasceu com o sufixo
de ontem — 22 pastas, 30 placeholders e 21 planilhas corrigidos depois.

## Método de download: qual caminho usar (atualizado em 19-08-2026)

O Elvis pediu pra checar se dava pra baixar tudo por `fetch`, no mesmo molde das
skills do Bruno Bezerra. A checagem foi feita e a API interna **funciona e é o
caminho padrão** — desde que o token nunca saia da página (ver logo abaixo). O
caminho pela SPA continua documentado e é o fallback quando a API não estiver
disponível. Não refazer essa investigação a cada execução — o resultado está
aqui.

| O que foi checado | Resultado |
|---|---|
| A API interna de aulas responde e cobre tudo | **Sim.** `GET /api/aluno/curso/{id}` devolve todas as aulas numa chamada (~4s) |
| Dá pra obter o link do PDF sem abrir a aula | **Sim — é a mesma chamada.** Ela já traz `pdf` e `pdf_simplificado` prontos de cada aula |
| O PDF baixa fora do navegador | **Sim.** Não depende de cookie de sessão: basta o link assinado + `User-Agent` de browser |
| **Dá pra montar o `Authorization` da API?** | **Sim, com o token ficando dentro da página.** Ver logo abaixo |

**A API é o caminho principal, e o que decide se ela passa é o token nunca
sair da página** — confirmado em 19-08-2026 pelas duas execuções do mesmo dia:

- **Pacote TCDF-ANACE (manhã): recusado.** Tentar trazer o `Bearer` pro lado de
  fora — `fetch` em `/oauth/token/` devolvendo o token, ou leitura do storage
  da aplicação — volta como "Blocked by classifier" nas duas formas.
- **Pacote ISS Manaus (noite): passou, 21 matérias e 227 PDFs pela API.** O
  `fetch` em `/oauth/token/` roda **dentro** do `javascript_tool`, o token fica
  numa variável da própria página (`window.__tok`) e é usado no mesmo script; o
  que volta é só `{aulaId: [expiration, signature]}` por aula.

Ou seja: **usar o token dentro da página passa; extrair o token não passa.** O
bloqueio da extração é correto e não deve ser contornado — nada de rotas
alternativas pra tirar credencial dali, e nada de `localStorage` da aplicação.
Chamar a API sem o header, com `credentials:'include'`, morre no CORS
(`Failed to fetch`) — não é alternativa.

**Se mesmo com esse padrão o classificador recusar**, não insistir: dois
"Blocked by classifier" seguidos e vai pro caminho da SPA (a primeira das duas
seções de caminho no Passo 7), que não toca em credencial nenhuma e entrega o
mesmo resultado, só mais devagar.

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

## Passo 7: Baixar o livro de cada aula de cada matéria selecionada

Para cada matéria dentro de cada categoria selecionada (Passo 5) ou confirmada
pra atualização (Passo 4), repetir o mesmo processo da skill
`baixar-curso-especifico-estrategia` (Passos 4 a 6 dela), com uma diferença por
categoria:

### CAMINHO B (fallback): colher rótulos e links pela própria SPA

**Usar quando a API do CAMINHO A (logo abaixo) não estiver disponível** — o
classificador recusou o `fetch` do token mesmo com ele ficando na página, ou a
API mudou. Não toca em credencial nenhuma: só lê o DOM da área do aluno, que já
está logada. Foi o caminho da execução TCDF-ANACE (17 matérias, 177 PDFs), então
é uma rota testada de ponta a ponta, só mais lenta que a API.

São duas etapas por matéria — **primeiro a listagem inteira, depois as
assinaturas**, nessa ordem, e nunca misturadas.

**Etapa 1 — ler a listagem com a página recém-carregada.** Navegar pra
`/cursos/{id}/aulas` com reload forçado e ler a listagem **antes de clicar em
qualquer aula**. Isso é obrigatório: depois do primeiro clique a SPA
reorganiza o DOM e os rótulos passam a sair trocados (visto na prática — a
mesma aula apareceu ora como "Aula 01", ora como "Aula 02"). Se precisar
reler a listagem depois de ter aberto alguma aula, recarregar a página antes.

**CRÍTICO — aula travada não é link.** Não iterar por `a.Collapse-header`: a
aula ainda não liberada existe no DOM como header **sem** `<a>` de aula (o
`href` aponta pra própria listagem), então ela simplesmente **some** da
coleta. Consequência real (pacote TCDF-ANACE, 19-08-2026): a aula travada não
vira placeholder `.txt` (Passo 8) e o `(N-M)` do Passo 9 mente, dando o curso
como completo. Iterar sempre por `.LessonCollapseHeader`, e tratar como
travada todo item de que não se consiga extrair `/aulas/{id}`:

```js
window.__lista = () => Array.from(document.querySelectorAll('.LessonCollapseHeader')).map(x => {
  const a = x.closest('a'), href = a ? a.getAttribute('href') : '';
  const m = href && href.match(/\/aulas\/(\d+)/);
  const h = x.querySelector('h2'), p = x.querySelector('p');
  let d = null, n = x;                                  // "Disponível em DD/MM/AAAA" fica num pai
  for (let k = 0; k < 6 && n; k++) {
    n = n.parentElement; if (!n) break;
    const t = n.textContent.replace(/\s+/g, ' ');
    const mm = t.match(/Dispon[ií]vel em\s*(\d{2}\/\d{2}\/\d{4})/);
    if (mm && t.length < 400) { d = mm; break; }
  }
  return { id: m ? m[1] : '', r: h ? h.textContent.trim() : '',
           c: p ? p.textContent.trim().slice(0, 120) : '',
           trav: m ? '' : (d ? d[1] : 'SEM-DATA') };
});
```

**Etapa 2 — colher as assinaturas, uma aula por vez, em background.** Clicar
no `<a>` da aula troca a página sem reload e os botões de download aparecem;
`history.back()` é dispensável, dá pra pular direto de aula em aula. Dois
detalhes que fazem a diferença entre funcionar e travar:

- **Disparar o loop sem `await`** (fire-and-forget) e ler o acumulador depois.
  O executor de JS corta em 30s: se a chamada esperar o loop terminar, ela
  morre no timeout e leva o loop junto. Disparado solto, ele continua rodando
  no navegador e a chamada volta na hora.
- **Esperar por polling, não por `sleep` fixo** — checar a cada 150ms se o
  botão daquela aula já apareceu. Dá ~2,3s por aula, contra ~4s de sleep fixo.

```js
window.__colher = async function (ids) {
  const s = ms => new Promise(r => setTimeout(r, ms));
  const btns = id => Array.from(document.querySelectorAll('a.LessonButton'))
                          .filter(y => y.href.includes('/download/' + id));
  for (const id of ids) {
    let L = btns(id);
    if (!L.length) {
      const a = document.querySelector('a[href*="/aulas/' + id + '"]'); if (a) a.click();
      for (let i = 0; i < 40; i++) { await s(150); L = btns(id); if (L.length) break; }
    }
    if (L.length) {
      const u = new URL(L[0].href);
      window.__acc.push(id + '|' +
        L.map(y => y.href.match(/api\/aluno\/([^/]+)\/download/)[1]).join(',') + '|' +
        encodeURIComponent(u.searchParams.get('expiration')) + '|' + u.searchParams.get('signature'));
    } else window.__acc.push(id + '|||');
  }
  window.__done = true;
};
```

**Guardar esse código em `sessionStorage`** (`sessionStorage.setItem('__boot', ...)`)
e reinjetar com `eval(sessionStorage.getItem('__boot'))` depois de cada reload.
Num pacote de 17 matérias isso reduz cada matéria a uma chamada de setup, em
vez de recolar o script inteiro toda vez. `sessionStorage` com código próprio
passa pelo classificador; `localStorage` da aplicação, não (é onde mora a
credencial) — não tentar.

**Nunca deixar dois loops rodando ao mesmo tempo.** Um loop antigo continua
navegando por baixo e embaralha a coleta do novo (rótulos fora de ordem,
aulas puladas). Como o loop é solto, a forma confiável de matar é
**recarregar a página** antes de começar a próxima matéria.

**Devolver só `id|tipos|expiration|signature`**, não a URL inteira: o resto é
template fixo (`clienteId`, `resourceType`, `resourceId`), remontável no
shell. Num pacote grande isso corta uns 60% do texto que passa pelo contexto.

### CAMINHO A (principal): API interna

**Tentar sempre esta primeiro** — foi por ela que saíram as 21 matérias e os
227 PDFs do pacote ISS Manaus em 19-08-2026, em minutos em vez de horas. A
condição é uma só: **o token fica dentro da página e nunca volta pro contexto**
(ver "Método de download: qual caminho usar"). Se mesmo assim o classificador
recusar, não insistir — dois "Blocked by classifier" seguidos e vai pro CAMINHO
B (SPA), logo acima.

Em vez de abrir a listagem e depois cada aula pra extrair o `a.LessonButton`,
buscar **o curso inteiro numa única chamada**:

```
GET https://api.estrategiaconcursos.com.br/api/aluno/curso/{cursoId}
Authorization: Bearer <token de GET /oauth/token/>
```

A resposta traz, para **cada** aula: `id`, `nome` (o rótulo exato), `conteudo`
(o assunto), `is_disponivel`, `data_publicacao`, `pdf` e `pdf_simplificado`
(links já assinados). Num pacote de 24 cursos / ~480 aulas isso troca centenas
de navegações por 24 chamadas — a diferença entre horas e minutos.

Como usar sem violar a regra de credenciais:

- O `Bearer` **fica dentro do navegador**. Rodar o `fetch` via `javascript_tool`
  e trazer de volta **apenas os links assinados** (e os metadados das aulas).
  Nunca extrair o token pro shell — além de desnecessário, o classificador do
  Claude Code bloqueia isso, e com razão. Padrão exato que passou em
  19-08-2026, tanto pra catálogo quanto pra assinatura:

  ```js
  // catálogo: rótulo, assunto, disponibilidade e previsão de todas as aulas
  (async()=>{const t=await (await fetch('/oauth/token/',{credentials:'include'})).json();
   const tok=t.access_token||t.token; const o={};
   for(const id of [/* 4 a 8 cursos */]){
     const r=await (await fetch('https://api.estrategiaconcursos.com.br/api/aluno/curso/'+id,
       {headers:{Authorization:'Bearer '+tok}})).json();
     const c=r.data||r;
     o[id]=(c.aulas||[]).map(a=>[a.id,a.nome,(a.conteudo||'').replace(/\s+/g,' ').slice(0,80),
                                 a.is_disponivel?1:0,a.pdf_simplificado?1:0,
                                 (a.data_publicacao||'').slice(0,10)]);}
   return JSON.stringify(o);})()

  // assinaturas: só expiration + signature por aula, geradas na hora de baixar
  (async()=>{const t=await (await fetch('/oauth/token/',{credentials:'include'})).json();
   const tok=t.access_token||t.token; const o={};
   for(const id of [/* mesmo bloco */]){
     const r=await (await fetch('https://api.estrategiaconcursos.com.br/api/aluno/curso/'+id,
       {headers:{Authorization:'Bearer '+tok}})).json();
     const c=r.data||r;
     for(const a of (c.aulas||[])){const u=a.pdf||a.pdf_simplificado; if(!u)continue;
       const p=new URL(u).searchParams;
       o[a.id]=[p.get('expiration'),p.get('signature')];}}
   return JSON.stringify(o);})()
  ```

  O token só existe dentro dessas duas closures e não aparece em nenhum
  retorno. A URL de download é remontada no shell a partir do template fixo:
  `…/api/aluno/{pdf|pdfSimplificado}/download/{aulaId}?clienteId={id}&resourceType=pdf&resourceId={aulaId}&expiration={exp}&signature={sig}`.
- A assinatura é **por aula**, mas a mesma serve tanto para `/pdf/download/{id}`
  quanto para `/pdfSimplificado/download/{id}`.
- **Os links duram pouco: ~20-30 minutos.** O campo `expiration` da URL vem com
  o relógio do servidor (umas 2h à frente do local) e **engana** — não usar ele
  como referência. Gerar as assinaturas imediatamente antes de cada bloco. Link
  vencido devolve HTTP 200 com a home em HTML, exatamente igual ao erro de
  User-Agent.
- **Tamanho de bloco que se mostrou seguro: 4 a 8 cursos por vez (~50 aulas),
  com 4 downloads em paralelo** — confirmado na execução do pacote ISS Manaus
  (AFTM) em 19-08-2026: 21 matérias, 227 PDFs, 705 MB, **zero** recusa por
  volume e zero assinatura vencida. Blocos de 2-3 cursos (recomendação
  anterior) funcionam, mas custam o dobro de idas ao navegador sem ganho de
  segurança.
- Aula ainda não liberada vem com `pdf` nulo — tratar como travada (Passo 8).
- **A previsão de liberação da aula travada sai do próprio `data_publicacao`**
  — não precisa ler o "Disponível em DD/MM/AAAA" da listagem HTML. Economiza
  uma consulta por matéria e é o que alimenta o nome do `.txt` do Passo 8
  (confirmado nos 30 placeholders do pacote ISS Manaus).
- **`pdf_simplificado` nulo já diz que aquela aula não tem versão
  simplificada** — dá pra decidir entre simplificado e original **antes** de
  baixar, sem gastar um download. A checagem das 8 páginas + "possui
  simplificado" (Curso Regular, mais acima) continua valendo como rede de
  segurança pro caso do card existir e o PDF ser só o aviso.
- Uma forma compacta de trazer os dados sem inflar o contexto: pedir ao
  navegador só `id:assinatura` por aula e casar com a tabela de rótulos que já
  foi montada no Passo 3.

Se a API falhar ou mudar, o caminho antigo (navegar aula por aula e ler o
`a.LessonButton`) continua válido como fallback — ver os itens 1 e 2 da
"Mecânica de download", mais adiante neste mesmo Passo 7.

### Nome do arquivo — rótulo exato da aula (regra geral, vale pra todas as categorias)

**Sufixo `LS` / `LC` no Curso Regular** (Elvis, 2026-08-20). Toda aula de **Curso
Regular** carrega no nome qual versão do livro é, **entre o assunto e a data**:

```
Aula 03 - Fundações, empresas públicas e sociedades de economia mista LS (30-07-2026).pdf
Aula 18 - Improbidade administrativa - Lei 8.429-1992 LC (30-07-2026).pdf
```

| Sufixo | Significa |
|---|---|
| `LS` | **Livro Simplificado** — baixou o `pdf_simplificado` |
| `LC` | **Livro Completo** (original) — baixou o `pdf` |

**Só o Curso Regular leva sufixo.** Passo Estratégico, Bizu, Trilha, Monitoria e
Rodadas têm um card único, sem distinção de versão — nome sem sufixo.

**Por quê:** o mapeamento de aulas ancora o aluno por **número de página**, e as duas
versões têm paginações diferentes. Como a skill prioriza o simplificado e cai pro
original quando não existe, a pasta fica mista — no TCDF-ANACE, **54 de 180 aulas (30%)**
só têm o completo, e quatro disciplinas não têm simplificado nenhum.

**O sufixo reflete o que foi REALMENTE baixado, não o que a API oferecia.** Quando a
detecção de stub rebaixa a aula na versão original, o arquivo é `LC` mesmo com
`pdf_simplificado` presente na API. É esse caso que impede deduzir a versão pela API
depois do fato.


**O rótulo da aula (a parte "Aula NN" nos exemplos abaixo) tem que ser copiado
exatamente como aparece na listagem do site, nunca um contador sequencial
próprio dado por quem baixou** — confirmado pelo Elvis em 2026-08-18. Exemplos
reais observados: `Aula 00`, `Aula 01`, `Aula 01 - Parte II` (quando o site
quebra uma aula em mais de uma parte — manter "Parte II" tal como está, não
virar "Aula 02"), `Aula Extra` (aula bônus fora da numeração principal), ou até
títulos sem número tipo `RESUMO - Parte Geral do CC` — usar o próprio título
da aula como rótulo nesse caso. Nunca substituir o rótulo real dado no site
pela numeração sequencial da ordem de download.

**Exceção: anotações de formato/equipe não entram no rótulo** — confirmado
pelo Elvis em 2026-08-18. Tags que descrevem o *tipo de mídia* ou a *equipe*
responsável pela aula, não o *assunto* tratado nela, ficam de fora do nome do
arquivo. Exemplos que **não** entram: `(Somente PDF)`, `(Somente em PDF)`,
`(Aula em PDF)`, `(Equipe de Legislação)`, `(Somente Vídeo)`. Ex: `Aula 20
(Somente PDF)` no site vira só `Aula 20` no arquivo.

**Exceção: nome de professor também não entra no rótulo** — confirmado pelo
Elvis em 2026-08-18. Alguns cursos do pacote rotulam a aula com o autor (ex:
`Aula 00 - Prof. Diego Carvalho e Emannuelle Gouveia`, em Análise de
Informações; `Aula 00 - Prof. Leonardo Mathias`, na Monitoria). O professor é
metadado de autoria, não assunto — o arquivo fica `Aula 00 - <assunto
sintético>`, e a autoria já está registrada na primeira página do próprio PDF.
Num pacote isso costuma valer pra **todas** as aulas da mesma matéria, não só
uma. **Se aparecer algum outro tipo de anotação
parecida que não se encaixe claramente como "tipo de mídia/equipe" nem como
parte do conteúdo, perguntar ao usuário antes de decidir** — não adivinhar
sozinho pra esse caso novo.

**A anotação nem sempre vem entre parênteses.** Visto na prática:
`Aula 16- Somente em PDF`, `Aula 15 - Somente em PDF`, `Aula Extra (Somente
pdf)`. Tratar todas do mesmo jeito, com ou sem parênteses, com ou sem espaço
antes do traço.

**Exceção: créditos de professor também não entram no rótulo** — confirmado em
2026-08-18. O curso de Tecnologia da Informação nomeia as aulas como
`Aula 00 - Prof. Diego Carvalho e Renato da Costa`. Nome de professor descreve
*quem deu* a aula, não o *assunto* dela, então sai do rótulo pela mesma lógica
das anotações de formato: `Aula 00 - Prof. Diego Carvalho e Renato da Costa`
vira só `Aula 00`. Regra prática: cortar tudo a partir de ` - Prof.` /
` - Profa.` até o fim do rótulo (isso já leva junto um eventual `(Somente em
PDF)` no final). Cuidado pra não confundir com `Aula 01 - Parte II`, que **é**
parte do rótulo e fica.

**Rótulos repetidos na mesma matéria: desempatar pelo conteúdo.** Existem cursos
com duas aulas de nome idêntico — em Administração Financeira e Orçamentária há
**duas** `Aula Extra - Somente em PDF`, uma de "Questões Extras FGV" e outra de
"Questões Extras CEBRASPE". Casando só pelo rótulo, os dois arquivos trocam de
lugar (e ficam com o assunto errado no nome) ou um sobrescreve o outro. Quando
o rótulo limpo aparecer mais de uma vez no mesmo curso:

1. comparar o `conteudo` da aula (vem da API) com o nome do arquivo local e
   parear o que tiver mais palavras em comum;
2. **se nenhum arquivo bater, não parear** — deixar aquela aula de fora e citar
   na Validação Final, em vez de arriscar sobrescrever o arquivo errado.

**Exceção: limite de caminho do Windows.** Se o caminho completo do arquivo
estiver perto do limite de 260 caracteres (ver "Limite de 260 caracteres de
caminho no Windows" nos Detalhes técnicos), é permitido sintetizar/abreviar o
rótulo — abreviar o assunto primeiro, e só mexer no rótulo como último
recurso, mantendo pelo menos o número/palavra que identifica a aula (ex:
`Aula 01 - Parte II` pode virar `Aula 01-PII` se for realmente necessário, mas
não virar `Aula 02`). Fora desse cenário de limite de caminho, o rótulo nunca
é sintetizado nem abreviado.

### Curso Regular

- Igual à skill original: preferir "Baixar Livro Eletrônico versão simplificada";
  se não existir, usar "versão original" como fallback.
- **CRÍTICO — o "simplificado" pode ser só um aviso, não a aula.** Confirmado
  na prática em 2026-08-18 (pacote Regular Controle: 19 aulas afetadas, 14 em
  Contabilidade Geral Avançada e 5 em Contabilidade Pública). Em algumas aulas
  o card "versão simplificada" existe e baixa normalmente, mas o PDF tem só
  ~3 páginas e diz que *aquela aula não possui PDF simplificado devido às suas
  características*. A presença do card não garante conteúdo — e o arquivo é um
  PDF válido, então passa em qualquer checagem de formato. Depois de baixar a
  simplificada, antes de renomear: se o PDF tiver **8 páginas ou menos** e o
  texto das 4 primeiras páginas contiver ao mesmo tempo `possui` e
  `simplificado`, descartar o `.tmp` e **rebaixar aquela aula na versão
  original**, sem perguntar ao usuário. Citar as trocas no resumo final. Ver o
  trecho de código na `baixar-curso-especifico-estrategia` (Passo 5, item 6.1).
  **Num pacote isso tende a se concentrar em disciplinas inteiras** (as de
  norma comentada/esquematizada), então não é um caso isolado: se aparecer numa
  aula, esperar mais na mesma matéria.
- Nome do arquivo: `Aula NN - Assunto Sintético [LS|LC] (DD-MM-AAAA).pdf`, dentro da
  subpasta da matéria (data extraída da primeira página do PDF — ver "Extrair a
  data do PDF" abaixo). **O sufixo `LS`/`LC` é obrigatório aqui** — ver a regra geral
  de nome do arquivo acima.

### Passo Estratégico

- Só existe um card: "Baixar Livro Eletrônico" (sem distinção simplificada/original).
  Clicar nesse card direto.
- Nome do arquivo: `Aula NN - Assunto Sintético (DD-MM-AAAA).pdf`, dentro da
  subpasta da matéria.

### Bizu Estratégico

- Mesma lógica de único card "Baixar Livro Eletrônico" do Passo Estratégico.
- **Diferença:** como todas as aulas desse curso único já são matérias diferentes,
  o nome do arquivo usa o **nome da matéria da aula** em vez de "Aula NN":
  `Nome da Matéria (DD-MM-AAAA).pdf` (ex: `Auditoria (DD-MM-AAAA).pdf`,
  `Língua Portuguesa (DD-MM-AAAA).pdf`), todos dentro da mesma pasta
  `Bizu Estratégico (<DD-MM-AAAA>)/` — categoria que é curso único não leva sigla de disciplina.

### Discursiva Sem Correção

- Mesmo card único "Baixar Livro Eletrônico versão original".
- Curso já é um bloco só (não por matéria) — nome do arquivo:
  `Aula NN - Assunto Sintético (DD-MM-AAAA).pdf`, todos dentro da pasta única
  `Discursiva Sem Correção (<DD-MM-AAAA>)/`. **A Discursiva não é disciplina** (`bases/DECISOES.md`, 22/08/2026) — baixar só se o usuário pedir a categoria explicitamente. Algumas aulas vêm marcadas "(Somente
  PDF)" no título do site — é só uma informação do site, não muda o processo.

### Trilha Estratégica

- Mesmo card único "Baixar Livro Eletrônico versão original".
- **Diferença de nomenclatura:** o site numera como "Trilha NN" em vez de "Aula
  NN" — usar esse mesmo padrão no nome do arquivo: `Trilha NN - Assunto
  Sintético (DD-MM-AAAA).pdf`, dentro da pasta única `Trilha Estratégica
  (<DD-MM-AAAA>)/`. Tem também um item inicial "Como utilizar a Trilha
  Estratégica" sem número — tratar como uma aula normal, nomeando o arquivo pelo
  próprio título (`Como Utilizar a Trilha Estratégica (DD-MM-AAAA).pdf`).

### Simulado

- Mesmo card único "Baixar Livro Eletrônico versão original".
- Cada simulado do bloco tem normalmente **duas aulas associadas**: o simulado
  em si e o "Gabarito" correspondente — são duas aulas separadas na listagem,
  cada uma com seu próprio card de download. Baixar as duas.
- Nome do arquivo baseado no título da aula (geralmente já traz a data do
  simulado em si) + a data extraída do PDF entre parênteses no final, dentro da
  pasta única `Rodadas Avançadas (<DD-MM-AAAA>)/`. Ex: `Simulado Especial -
  23-08-2026 (DD-MM-AAAA).pdf` e `Simulado Especial - 23-08-2026 - Gabarito
  (DD-MM-AAAA).pdf` (barra da data do título trocada por traço, mesma regra do
  Passo 8; a data entre parênteses no final é a de elaboração do PDF, pode ser
  diferente da data do simulado no título).

### Extrair a data do PDF (e checar o conteúdo contra o assunto esperado)

Depois de baixar cada PDF (todo download, não só em modo atualização), extrair
a data de elaboração/atualização que aparece na primeira página, pra usar no
nome do arquivo — **e aproveitar essa mesma abertura pra checar, de graça, se
o conteúdo bate com o assunto esperado da tabela** (mesmo script e mesma
lógica da skill `baixar-curso-especifico-estrategia`, ver "Extrair a data do
PDF" lá pra explicação completa da checagem — confirmado pelo Elvis em
2026-08-18):

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
" "<caminho do PDF baixado com nome temporário>" "<assunto esperado>"
```

- **Duas formas de data já observadas na prática:** numérica `DD/MM/AAAA` e
  escrita por extenso em português `DD de Mês de AAAA` (ex: "31 de Julho de
  2026" — confirmado testando no curso de Direito Administrativo, pacote
  Regular Fiscal). O script acima cobre os dois, tentando o numérico primeiro.
- **Segunda linha de saída (`MATCH:hits/total`):** `hits` igual a 0 com
  `total` maior que 0 → possível conteúdo errado — não travar o download,
  só registrar essa aula como suspeita pra citar na Validação Final (Passo 10).
  **`total` igual a 1 ou 2 é sinal de confiança baixa mesmo com `hits` 0** —
  confirmado numa checagem em lote real em 2026-08-18 contra ~480 aulas já
  confirmadas corretas: os poucos `0/total` encontrados eram todos assunto
  curto (1-3 palavras) com variação de fraseado no PDF, não conteúdo errado.
  Tratar como aviso fraco nesse caso, não como erro confirmado.
- **Checagem de conteúdo olha as primeiras 6 páginas, não só a primeira** —
  confirmado pelo Elvis em 2026-08-18: a página 1 costuma ser só capa (título,
  autor, data), o conteúdo real da aula só aparece depois do índice/apresentação
  do curso. A extração de **data** continua só na página 1 (sempre funcionou
  bem); é a checagem de **conteúdo** que precisa olhar mais páginas.
- **Se der 0 acertos nas 6 primeiras páginas, ampliar pra ~25 antes de marcar
  como suspeita** — confirmado na prática em 2026-08-18 (pacote Regular
  Controle): das 211 aulas, 5 caíram como suspeitas e **todas as 5 eram falso
  positivo** — aulas cujo índice ocupa várias páginas, então em 6 páginas só
  tem capa e sumário. Ampliando a janela o conteúdo aparece com folga (a aula
  de SQL tinha 57 ocorrências de "sql" nas 25 primeiras páginas e 0 nas 6
  primeiras). A segunda passada só roda pras aulas que deram `0/total`, então
  custa quase nada — e num pacote isso é o que separa um relatório final limpo
  de uma lista de suspeitas que o usuário vai ter que conferir na mão.
- Baixar sempre com nome temporário (`.tmp`), extrair a data, e só então renomear
  pro nome final com a data.
- **Aproveitar essa mesma abertura pra guardar o número de páginas do PDF** —
  confirmado em 19-08-2026 (pacote ISS Manaus): o arquivo já está aberto no
  `pypdf` aqui, e o `len(reader.pages)` é uma das colunas da planilha do Passo
  11. Sem isso, é preciso reabrir todos os PDFs numa segunda passada só pra
  montar as planilhas (foram 227 reaberturas evitáveis naquela execução).
  Registrar página, data e `MATCH` num log único por execução, e alimentar a
  planilha a partir dele.
- Se `pypdf` não estiver instalado, instalar com `pip install pypdf` antes de
  processar a primeira aula.
- **Fallback se não achar data:** manter o nome do arquivo sem o sufixo
  `(DD-MM-AAAA)` e seguir normalmente — não travar o download. Mencionar no
  resumo final quais aulas ficaram sem data identificada.

### Mecânica de download (igual em todas as categorias)

**Os itens 1 e 2 abaixo são FALLBACK** — só use se a API do "Caminho principal"
falhar ou mudar. Quando a API funcionar (o normal), você já tem `nome`,
`conteudo`, `is_disponivel`, `pdf` e `pdf_simplificado` de todas as aulas do
curso, então **pule direto pro item 3**, sem navegar aula nenhuma.

**Do item 3 em diante vale para os dois caminhos**: download, validação, nome do
arquivo, extração de data e substituição são idênticos.

1. *(fallback)* Navegar para `https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{id}/aulas/{aulaId}`
   (ou clicar no título da aula na lista) e esperar ~2s carregar. **Conferir o
   título da aba depois de navegar** — se voltar genérico ("Área do Aluno", ou
   o mesmo título de antes) em vez do título real da aula/curso, a navegação
   falhou silenciosamente (transiente, observado várias vezes na prática) —
   **renavegar uma vez pra mesma URL antes de seguir**, em vez de extrair o
   `LessonButton` de uma página errada.
2. *(fallback)* **Não precisa clicar no card nem abrir aba nova.** O link de download já
   está no HTML da própria página, num `<a class="LessonButton">`. Extrair
   direto via JavaScript (`javascript_tool`):
   ```js
   const links = Array.from(document.querySelectorAll('a.LessonButton'))
     .map(a => ({ texto: a.textContent.replace(/\s+/g, ' ').trim(), href: a.href }));
   JSON.stringify(links);
   ```
   Isso retorna um link pra cada card presente na aula — escolher o que
   corresponde à categoria (ver acima).

   **Sempre filtrar os botões pelo ID da aula antes de usar o link** —
   confirmado na prática em 2026-08-18. O `href` de download termina em
   `/download/{aulaId}`; se o link capturado apontar pra outro ID, é o botão
   da aula **anterior**, que ainda não saiu do DOM (a troca de página é
   assíncrona). Isso já gerou um download de 188 bytes sem erro aparente:
   ```js
   const links = Array.from(document.querySelectorAll('a.LessonButton'))
     .filter(a => a.href.includes('/download/' + aulaId));
   ```
   O mesmo filtro serve pra saber que a página da aula certa já carregou.

2.1. **Coleta em lote pela própria SPA (recomendado num pacote).** A área do
   aluno é um SPA React: clicar no `<a>` da aula troca a página sem reload e
   `history.back()` volta pra listagem — então dá pra colher os links de
   **várias aulas num único `javascript_tool`**, em vez de um `navigate` por
   aula. Num pacote de 211 aulas isso trocou ~240 navegações por ~40 chamadas
   (confirmado em 2026-08-18). O script completo está na
   `baixar-curso-especifico-estrategia`, seção "CAMINHO B (fallback): percorrer as
   aulas dentro da própria SPA". Regras que valem sempre:
   - **Disparar o loop sem `await` e ler o acumulador depois.** O executor de
     JS corta em 30s: chamada que espera o loop terminar morre no timeout e
     leva o loop junto. Com fire-and-forget dá pra mandar o curso inteiro de
     uma vez (o antigo teto de 7 aulas por chamada valia só pro modo
     `await`). Ver os três ajustes detalhados na skill específica.
   - **Devolver só `expiration` e `signature`** de cada aula, não a URL
     inteira: o resto é template fixo, remontável no shell. Num pacote grande
     isso economiza muito contexto.
   - Alguns `href` vêm como `{aulaId}/videos/{videoId}` — extrair o ID com
     `.split('/')[0]`.
   - Consumir o lote logo depois de coletar: **os links assinados vencem em
     poucos minutos**. Link vencido devolve HTML/arquivo minúsculo no lugar do
     PDF — nesse caso, recoletar a assinatura daquela aula e repetir.
3. Baixar o PDF **direto pra pasta de destino**, com nome temporário, via `curl`
   (Bash) com `-L` (o link redireciona pra CDN assinada
   `cdn.estrategiaconcursos.com.br/.../....pdf?Expires=...&Signature=...`), sem
   passar pela pasta de Downloads:
   ```bash
   curl -sL -o "<pasta>/<nome do arquivo>.pdf.tmp" "<href capturado>" \
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

   **Bloqueio por volume:** depois de algumas centenas de downloads seguidos na
   mesma conta (~600 numa execução real), a plataforma passa a responder
   **HTTP 302 → HTML** para qualquer PDF — inclusive quando o download é feito
   de dentro do próprio navegador logado. Não é User-Agent nem assinatura
   vencida: é limite da conta. Quando isso acontecer, **parar os downloads,
   avisar o usuário e retomar as matérias que faltaram noutro momento** — nunca
   insistir em laço, e nunca deixar o `.tmp` recusado substituir arquivo bom.
4. Extrair a data (ver acima) e renomear o `.tmp` pro nome final.
5. Voltar pra lista de aulas da matéria e seguir pra próxima aula. Depois de
   esgotar as aulas da matéria, voltar pra página do pacote e ir pra próxima
   matéria/categoria.

**Nota sobre cliques no navegador embutido (Browser pane):** clicar em
coordenadas de tela em itens de listagem (cursos, cards) nem sempre navega de
forma confiável nesse navegador — prefira sempre extrair o `href` real via
`javascript_tool` e navegar direto pela URL, em vez de clicar às cegas.

### Modo atualização — o que baixar

O Passo 4 já identificou, por matéria, quais aulas estão atualizáveis (antes
travadas, agora liberadas). O que fazer com o resto depende do sub-modo
escolhido no Passo 2:

- Arquivos `.txt` placeholder cuja aula agora está liberada (identificado no
  Passo 4) → em **qualquer** sub-modo, baixar o PDF normalmente e **apagar o
  `.txt` antigo** — **passo obrigatório, nunca esquecer:** sempre que um PDF
  real substitui um `.txt` placeholder, o `.txt` correspondente tem que ser
  apagado da pasta antes de seguir pra próxima aula/matéria.
- Arquivos `.txt` placeholder cuja aula continua travada → deixar como está (pode
  atualizar a data prevista se ela mudou no site).
- Arquivos já baixados (`.pdf` com data entre parênteses no nome):
  - **Atualização Parcial:** **pular** — não reconfere.
  - **Atualização Completa:** **não pular** — rebaixar (mesmo processo da
    "Mecânica de download" acima), extrair a data do PDF novo e comparar com a
    data no nome do arquivo local:
    - Data igual → apagar o `.tmp`, não mexer no arquivo existente.
    - Data diferente (ou arquivo antigo sem data no nome, de coleta anterior a
      esse fluxo) → apagar o PDF antigo, renomear o `.tmp` pro nome final com a
      data nova. Registrar essa substituição pra citar no resumo final.

- **Arquivo do Curso Regular no formato ANTIGO, sem o sufixo `LS`/`LC`** (sem ` LS `
  nem ` LC ` antes da data). O sufixo virou obrigatório em 2026-08-20; arquivo sem
  ele é de coleta anterior.
  - **Casar pelo rótulo da aula (`Aula NN`), nunca pelo nome completo** — senão a
    skill não reconhece a aula e baixa um duplicado ao lado do arquivo antigo.
  - **Atualização Parcial:** não rebaixar; só **renomear** acrescentando o sufixo.
    Dedução: se `pdf_simplificado` **não** existe na API → `LC`. Se existe, comparar
    o número de páginas do arquivo local com o do PDF original — igual significa que
    houve rebaixe por stub, logo `LC`; diferente significa `LS`.
  - **Atualização Completa:** o rebaixe resolve — gravar com sufixo e apagar o
    arquivo antigo. **Conferir que sobrou só um arquivo por aula.**
  - Vale só pro **Curso Regular**. As outras categorias nunca tiveram sufixo.

## Passo 8: Aula ainda não disponível → placeholder `.txt`

Mesma regra da skill original: quando a aula não tiver livro disponível ainda,
não baixar nada — criar um `.txt` no lugar, mesmo nome do PDF que seria criado,
terminando em `- DD-MM-AAAA.txt` (data com traço, nunca com barra — barra quebra
nome de arquivo no Windows).

```
Aula NN - Assunto Sintético - DD-MM-AAAA.txt      (Curso Regular / Passo Estratégico)
Nome da Matéria - DD-MM-AAAA.txt                   (Bizu Estratégico)
```

Conteúdo do `.txt`: uma linha simples informando que o material ainda não estava
disponível na data da coleta e qual a previsão de liberação informada pelo site.

**Lembrete de formato:** a data entre **parênteses** `(DD-MM-AAAA)` num `.pdf` é
a data real de elaboração/atualização do arquivo, extraída da própria primeira
página (ver Passo 7). A data depois de um **traço** `- DD-MM-AAAA.txt` é só a
previsão de liberação informada pelo site pra uma aula ainda travada. Os dois
formatos nunca se confundem visualmente por causa disso.

## Passo 9: Fechar o nome de cada pasta de disciplina — `(N-M)` e data

> **Reescrito em 22-08-2026.** Duas mudanças: o `(N-M)` passou do **começo para o
> FIM** do nome (REGRA 6), e **a data da pasta do pacote deixou de existir**
> (REGRA 9 — a data mora na disciplina).

Para cada disciplina processada:

1. **M** = total de aulas do curso; **N** = quantas têm PDF de verdade (não os
   `.txt` placeholder do Passo 8).
2. **Se N < M**, a marca vai **no fim, antes da data**:
   `LTRIB - Legislação Tributária Municipal (3-14) (22-08-2026)`.
   **Nunca no começo:** o parêntese ordena antes de qualquer letra, e todas as
   pastas com pendência sobem juntas para o topo, agrupadas pelo **defeito** em
   vez de pela disciplina — brigando com o prefixo de sigla, que existe para
   agrupar. Traço (`N-M`), nunca barra: barra é separador de caminho no Windows
   e quebra o `Rename-Item`.
3. **Se N == M**, sem marca.
4. **Atualizar a data daquela disciplina** para hoje, na mesma renomeação.
5. **NÃO criar nem atualizar data na pasta do pacote.** Se houver data lá, de
   execução antiga, **remover**.
6. **Limpar antes de recalcular**: tirar marca `(N-M)` antiga (do começo ou do
   fim) e data antiga, para não acumular.
7. **Renomear em cima, sempre** (REGRA 4). Nunca apagar e recriar.
8. **Devolver o estado**: atualizar `pasta_atual_no_disco` no
   `bases/01-disciplinas/dados/renomear-pastas.csv` e gravar o log `de -> para`
   num CSV na pasta de logs.

## Passo 10: Validação final (obrigatória — sempre rodar antes de dar o pacote como concluído)

**Confirmado pelo Elvis em 2026-08-18: essa validação é parte obrigatória da
skill, não um extra — nunca reportar o pacote (ou uma matéria dele) como
concluído sem rodar esse passo.**

**Validação é só por nomenclatura, nunca reabrindo o conteúdo dos PDFs aqui** —
confirmado pelo Elvis em 2026-08-18: não vale a pena gastar tokens
abrindo/lendo cada PDF de novo nessa etapa. A checagem de conteúdo já
aconteceu uma vez, de graça, durante o download (ver "Extrair a data do PDF"
no Passo 7, saída `MATCH:hits/total`) — aqui só se **reporta** o que ela
sinalizou, sem reabrir nada. O cruzamento desse passo é puramente comparação
de texto: rótulo da listagem do site vs. nome do arquivo local.

Depois de processar todas as categorias/matérias selecionadas:

1. Listar a árvore de pastas criada (`ls` recursivo por categoria), já com os
   prefixos `(N-M)` renomeados.
2. **Pra cada matéria/bloco processado, conseguir a lista de rótulos atual.**
   Se essa matéria acabou de ser baixada nessa mesma execução (sem intervalo
   relevante de tempo), **reaproveitar a tabela salva no Passo 4/5** em vez de
   gastar uma nova consulta ao site. Só **re-consultar a listagem `/aulas` do
   site de novo** quando fizer sentido desconfiar que o estado mudou desde a
   coleta original (retomando de uma sessão anterior, ou intervalo longo) —
   nesse caso, só o `get_page_text` da listagem, sem abrir aula por aula. Em
   qualquer um dos dois casos, cruzar item a item com os arquivos locais dessa
   matéria/bloco, só pelo nome:
   - Cada rótulo de aula da listagem deve corresponder a exatamente um arquivo
     local (`.pdf` ou `.txt`) cujo nome começa com esse mesmo rótulo.
   - Rótulo sem arquivo correspondente → aula não baixada, investigar antes de
     considerar aquela matéria concluída.
   - Arquivo local sem rótulo correspondente → rótulo digitado errado ou aula
     que saiu da grade — investigar e, se for rótulo errado, renomear o
     arquivo pro rótulo certo (sem reabrir o PDF, só `mv`/`Rename-Item`).
3. Conferir que **N** (quantidade de `.pdf` reais) e **M** (total de itens na
   listagem do site) batem com o prefixo `(N-M)` aplicado no Passo 9 de cada
   matéria/bloco.
4. **Listar as aulas sinalizadas como suspeitas pelo `MATCH:hits/total`**
   durante o download (ver Passo 7) — as que deram `0/total` mesmo depois da
   janela ampliada de páginas. Não precisa reabrir PDF nenhum aqui, só trazer
   a lista consolidada pro resumo. **Se sobrarem poucas (até ~5 num pacote),
   vale abrir só essas na hora e conferir** — na prática elas costumam ser
   falso positivo, e conferir ali evita entregar pro usuário uma lista de
   pendências que não é pendência. As que forem conferidas e estiverem certas
   entram na planilha como `Baixado (conferido)` (ver Passo 11).
5. Reportar o resultado dessa validação pro usuário — matéria por matéria, se
   bateu 100% por nome, se sobrou algo em algum lado, e se alguma aula ficou
   marcada como suspeita de conteúdo (item 4) — mesmo a skill normalmente não
   gerando relatório à parte, essa validação final é sempre resumida em texto.

O resultado final é a estrutura de pastas em si, já com os arquivos dentro,
cada matéria/bloco renomeado com o progresso `(N-M)`, mais a confirmação de
que o cruzamento bateu em cada uma.

## Passo 11: Planilha de metadados de cada disciplina (obrigatória, Google Sheets)

> **Atualizado em 22-08-2026.** Três mudanças, todas herdadas do Passo 9 da
> `baixar-curso-especifico-estrategia`, que é onde o layout está descrito:
>
> 1. **Nome do arquivo:** `<SIGLA> - Metadados` (ex. `DCONST - Metadados`). O
>    padrão antigo `<Matéria> (SIGLA-SIGLA) - Metadados` **está extinto** — foi
>    ele que gerou o caminho de 263 caracteres, repetindo a disciplina que a
>    pasta já diz e o concurso que o nível de cima já diz (REGRA 1). Disciplina
>    sem sigla (`pendente` no `renomear-pastas.csv`): nome da pasta sem o
>    concurso, ex. `Reforma Tributária - Metadados`.
> 2. **`_manifesto.csv` na mesma pasta**, com o mesmo conteúdo da aba `Aulas`,
>    gerado da **mesma estrutura em memória** e gravado **antes** de qualquer
>    chamada de rede — assim um `429` do Sheets não derruba a execução, e quem
>    lê o levantamento não precisa de OAuth.
> 3. **Colunas novas na aba `Aulas`:** `Sigla Disciplina`, `Hash Conteúdo` e
>    `Alterado em`; e **aba nova `Apoio`** (`Tipo` R/MM · `Assunto` · `Arquivo` ·
>    `Aulas` como lista · `Fonte do nome` capa/vídeo · `Páginas` ·
>    `Páginas conteúdo` · `Sigla Disciplina`).
>    **`Sigla Disciplina` e não `Cód Mestre` nas duas abas:** o Cód Mestre é do
>    TÓPICO, e bloco x tópico é muitos para muitos (`bases/DECISOES.md`, A14).
>    Coluna única mentiria na aba Aulas (uma aula tem vários tópicos) e na aba
>    Apoio (um resumo serve vários assuntos — é a própria razão da REGRA 7).
>    **Hash:** o texto do PDF local **contém a marca d'água**; linha de base sem
>    filtrar dá falso positivo em 100% das aulas na execução seguinte (REGRA 8).

**Confirmado pelo Elvis em 2026-08-18: toda matéria/bloco processado ganha uma
planilha de metadados própria, na mesma pasta dela** — mesmo processo e mesmo
formato validado na skill `baixar-curso-especifico-estrategia` (ver "Planilha
de metadados da disciplina" no Passo 9 dela — Google Sheets nativo via
`gspread` como preferência permanente, nunca `.xlsx` local; se a autenticação
falhar, parar e pedir ao usuário pra fazer login/reautorizar na hora em vez
de cair pro Excel silenciosamente; abas "Aulas" + "Legenda"; Curso ID no
subtítulo; fórmulas com `;` por causa do locale `pt_BR`; ler de volta pra
conferir que não deu `#ERROR!`/`#REF!`/`#NAME?`, já que não há `recalc.py`
funcionando nesse ambiente).

**Linha 3 com o link clicável pro curso** — confirmado pelo Elvis em
19-08-2026: `A3` = `Link do curso:` e `B3` (mesclada até `I3`) =
`=HYPERLINK("https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{cursoId}/aulas";"Abrir no Estratégia")`.
Sem isso não há como voltar do arquivo pro curso no site — as 71 planilhas dos
4 primeiros pacotes nasceram sem o link e tiveram que ser corrigidas depois.
Detalhes de layout e idempotência: ver o item 4.0 do Passo 9 da
`baixar-curso-especifico-estrategia`. Num pacote isso vale por matéria, cada
uma com o **seu** Curso ID — nunca o ID do pacote.

**Coluna `Versão do Livro` e identificação de material/pacote** (Elvis,
2026-08-20). Além do que já existe, cada planilha de disciplina passa a trazer:

- **Coluna `Versão do Livro`** na aba "Aulas": `LS` (Livro Simplificado), `LC`
  (Livro Completo) ou `—` para categoria sem essa distinção. Mesmo valor do
  sufixo do nome do arquivo. Duas células no resumo com
  `=COUNTIF(<col>;"LS")` / `=COUNTIF(<col>;"LC")` — disciplina 100% `LC` avisa
  que aquela matéria não tem simplificado.
- **No subtítulo**, junto com pasta e Curso ID: `Tipo de Material`
  (`Curso Regular`, `Passo Estratégico`, `Bizu Estratégico`, `Trilha
  Estratégica`, `Monitoria`, `Rodadas de Simulados`, `Discursiva`), `Nome do
  Pacote` (exato, como está no catálogo), `Pacote ID` e link do pacote
  (`=HYPERLINK(".../app/dashboard/pacote/{pacoteId}";"Abrir pacote")`).

Num pacote isso é ainda mais importante que na skill irmã: as subpastas de
categoria já separam Curso Regular de Passo e de Bizu, mas **quem abre uma
planilha solta não tem esse contexto**. E gravar o nome exato + ID do pacote em
toda planilha é o que permite, mais tarde, voltar direto ao produto certo no
catálogo — ou perceber que ele **saiu do ar**, se o `pacote/{id}` não abrir mais.

O `Tipo de Material` sai do `tipo_curso_id` de `GET /api/aluno/pacote/{id}`:
`1`=Curso Regular, `3`=Monitoria, `5`=Trilha Estratégica, `7`=Passo Estratégico,
`27`=Bizu Estratégico, `30`=Rodadas de Simulados. Detalhes de layout e
idempotência: item 4.0-A e 4.0-B do Passo 9 da `baixar-curso-especifico-estrategia`.

**Vale nos dois modos** — ao criar do zero e ao atualizar. Em planilha antiga sem
esses campos, **acrescentar** sem reescrever o resto.

**Quota do Google Sheets:** a API permite **60 requisições de escrita por
minuto por usuário**, e montar uma planilha (update + formatações + freeze +
aba Legenda) gasta ~10 delas — ou seja, o teto é de ~6 planilhas por minuto.
Num pacote com 20+ matérias isso estoura e vem `APIError [429] Quota exceeded`
(aconteceu em 2026-08-18: 8 planilhas passaram, 14 falharam). Espaçar as
planilhas (~11s entre uma e outra) e, ao pegar um 429, **esperar ~65s e tentar
de novo** em vez de dar a planilha como perdida. Cuidado também com o padrão
"tenta abrir a aba, se falhar cria": se o erro for de quota e não de aba
inexistente, isso tenta criar uma aba que já existe e devolve
`400 Já existe uma página chamada "Legenda"`. Checar a existência da aba pela
lista de abas do arquivo, e só então limpar.

**Rodar sempre DEPOIS do Passo 9 (renomear).** A planilha grava o nome da pasta
no subtítulo (`Pasta: ...`), então se rodar antes da renomeação o subtítulo
nasce desatualizado.

**Diferença de escala:** num pacote inteiro, repetir esse passo pra **cada
matéria/bloco processado nessa execução**, uma planilha por pasta de
disciplina (não uma planilha única pro pacote inteiro) — mantém a
granularidade de "atualizar só uma matéria sem mexer nas outras" (mesma lógica
do sufixo de data por pasta, Passo 9). Bizu/Discursiva/Trilha/Simulado (pastas
únicas, sem separação por matéria) também ganham sua própria planilha, na
pasta única deles.

**Escopo da atualização da planilha = escopo da execução, confirmado pelo
Elvis em 2026-08-18:**
- Se o usuário pedir pra atualizar **só uma disciplina específica** dentro do
  pacote, só a planilha dessa disciplina é atualizada — as outras matérias do
  mesmo pacote ficam intocadas.
- Se o usuário pedir pra atualizar **o curso/pacote inteiro** (ou uma
  categoria inteira), **todas** as planilhas das disciplinas efetivamente
  processadas nessa execução são atualizadas — uma por matéria tocada.
- Em nenhum caso atualizar a planilha de uma matéria que não foi processada
  nessa execução, mesmo que esteja no mesmo pacote.

**Limite de escrita do Sheets — atenção redobrada num pacote.** Confirmado na
prática em 2026-08-18: a cota é de **60 requisições de escrita por minuto por
usuário**, e cada planilha consome várias (criar, `update` das duas abas,
`resize`, `batch_update` de formatação). Com 12 disciplinas de uma vez o erro
**HTTP 429** aparece por volta da sétima planilha e derruba a execução no meio.
Montar o script assim desde o começo:

- Retry por planilha, com espera de ~65s e até ~6 tentativas, **para 429 e
  também para 5xx** (`503 The service is currently unavailable`). Confirmado em
  19-08-2026: com o retry cobrindo só o 429, duas das 21 planilhas do pacote
  ISS Manaus morreram num 503 transiente e tiveram que ser refeitas na mão —
  o 503 passa na tentativa seguinte sem nenhum outro ajuste.
- **Deixar o script aceitar uma lista de matérias como argumento**, pra
  reprocessar só as que falharam sem repetir as 20 que já deram certo.
- Pausa de ~12s entre planilhas.
- **Idempotência obrigatória:** antes de criar, procurar pelo nome do arquivo
  dentro da pasta de destino no Drive e reaproveitar a planilha existente —
  senão, ao retomar depois do 429, as primeiras disciplinas ganham planilhas
  duplicadas.
- Como o processo é longo, imprimir o progresso planilha a planilha
  (`flush=True`) pra dar pra retomar sabendo onde parou.

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

## Passo 11B: Índice do pacote na pasta raiz (obrigatório, Google Sheets)

**Confirmado pelo Elvis em 2026-08-19.** As planilhas de metadados do Passo 11
resolvem a disciplina, mas nenhuma delas diz **como voltar ao pacote** nem qual
produto do Estratégia foi matriculado pra chegar lá. Sem isso, toda vez que o
pacote sai do rodízio de matrículas (limite de 3 — ver Passo 1) é preciso
garimpar o catálogo de novo pra descobrir qual dos produtos abre aquele
material.

Rodar **depois** do Passo 11, na pasta **raiz do pacote** (a que contém as
subpastas de categoria, ex: `ISS Manaus (AFTM) 2026 (19-08-2026)/`).

- **Nome do arquivo:** `<Nome do Pacote> - Índice do Pacote` — sem data no
  nome (documento único que se atualiza, igual às planilhas de metadados).
- **Se já existir**, atualizar em cima; nunca apagar e recriar.

### Aba `Produto` — as variantes do Estratégia

O mesmo concurso/cargo costuma aparecer no catálogo em **três embalagens
diferentes**, e o link é diferente em cada uma:

1. **Curso Regular / Pacote Teórico** — só o teórico das matérias.
2. **Pacotaço — Pacote Teórico + Pacote Passo Estratégico** — teórico + Passo.
3. **Pacotaço + Sistema de Questões** — os dois acima mais o Sistema de
   Questões.

Uma linha por variante encontrada no catálogo pra aquele concurso/cargo, com as
colunas: `Variante`, `Nome exato no catálogo`, `Pacote ID`, `Link`
(`=HYPERLINK("https://www.estrategiaconcursos.com.br/app/dashboard/pacote/{id}";"Abrir pacote")`),
`Matriculado hoje` (Sim/Não), `Origem desta execução` (Sim só na variante que
foi efetivamente usada pra baixar).

Como levantar as variantes sem depender de estar matriculado: em
`/app/dashboard/assinaturas`, usar a busca do bloco "Matricular em novos
produtos" na aba **PACOTES** com o nome do concurso (ex: `ISS Manaus`), e ler
os resultados.

**Duas armadilhas da busca do catálogo** (aprendidas apanhando em 2026-08-20 —
ver `reference_estrategia_busca_catalogo_abas` na memória):

1. **A aba não troca com clique por coordenada.** Continua listando PACOTES e a
   busca volta zero, o que parece resultado legítimo. Trocar com
   `element.click()` no `<button>` e conferir a classe `Tab isActive`.
2. **A busca é fuzzy (OR).** "Bizu Receita Federal" devolve 3772 itens casando
   só "Receita". Contagem alta não significa acerto — ler os primeiros itens.

**Material granular (Bizu, Passo, Monitoria, Trilha, Discursiva) não aparece na
aba PACOTES** — só na aba **CURSOS**, onde é produto avulso e matriculável (há
122 Bizus no catálogo, por exemplo). Se o objetivo for achar uma categoria
específica e não o pacotão, buscar em CURSOS. Os matriculados já expõem o `href` `/app/dashboard/pacote/{id}`
direto no DOM; pros não matriculados, pegar o id junto ao botão `MATRICULAR`.
Se alguma variante não aparecer no catálogo, registrar a linha assim mesmo com
`Pacote ID` = `não encontrado em DD-MM-AAAA` — a ausência é informação.

### Aba `Disciplinas` — uma linha por matéria baixada

Colunas: `Categoria` (Curso Regular / Passo Estratégico / Bizu / ...),
`Matéria`, `Curso ID`, `Link do curso`
(`=HYPERLINK(".../app/dashboard/cursos/{cursoId}/aulas";"Abrir curso")`),
`Pasta local`, `Aulas baixadas`, `Aulas pendentes`, `Planilha de metadados`
(`=HYPERLINK` pra planilha do Passo 11 daquela matéria).

Os dados todos já existem no fim da execução — é consolidação do que o Passo 11
gravou disciplina a disciplina, não uma nova coleta no site.

### Formatação e regras

- Título mesclado na linha 1 e subtítulo na linha 2 com `Pasta: ...` e a data
  desta atualização, no mesmo padrão das planilhas de metadados.
- Alinhamento centralizado, quebra de texto ligada e aparar linhas/colunas em
  excesso, como em toda planilha nova do workspace.
- **Escopo = escopo da execução:** atualizar as linhas das disciplinas
  processadas agora e as variantes conferidas agora; linhas de matérias que não
  entraram nessa rodada ficam como estavam, com a data antiga.
- No relatório final (Passo 10), citar o link do índice junto do resumo.

## Passo 12: Sugestões de melhoria pra skill (obrigatória ao final de toda execução)

**Confirmado pelo Elvis em 2026-08-18: ao final de todo download/atualização
de pacote, refletir se algo observado nessa execução sugere um ajuste na
própria skill, e apresentar pro usuário aprovar** — não é opcional, é parte do
encerramento normal do processo. É a regra geral do workspace pra skills de
download em massa e de cadernos de questões (ver `AGENTS.md`), e vale igual na
`baixar-curso-especifico-estrategia` (Passo 10 dela).

Depois do relatório final (Passo 10) e das planilhas (Passo 11), avaliar se
algo aprendido nessa execução sugere um ajuste: bug novo, comportamento
inesperado do site, passo lento/repetitivo, oportunidade de deixar algo mais
robusto.

- Sugestão tem que ser **concreta e ligada a algo que realmente aconteceu**
  nessa execução — não inventar sugestão genérica só pra preencher esse passo.
- **Se identificar algo:** apresentar ao Elvis de forma objetiva (o que
  aconteceu, o que mudaria na skill), perguntar se aprova, e só então editar o
  `SKILL.md` (dessa skill e/ou da `baixar-curso-especifico-estrategia`, se
  aplicável às duas) e rodar `/syncar`.
- **Se nada de novo surgiu:** dizer isso de forma curta e objetiva — não
  forçar uma sugestão fraca só pra ter o que falar.
- Apresentar junto do resto do resumo final (validação + planilhas), não como
  pergunta solta separada.
- **Nunca editar a skill nem sincronizar sem aprovação prévia.**

## Detalhes técnicos e pegadinhas (aprendidos testando esse pacote)

- **Limite de 260 caracteres de caminho no Windows** — o orçamento por nível está
  em `bases/NOMENCLATURA.md` e **este documento não o repete**, para não divergir.
  O que manda é o **caminho real chegar a 240**, não a soma dos tetos; chegando,
  **quem encurta é o ARQUIVO, nunca a pasta** (REGRA 10). Medir sempre o caminho
  **absoluto**: no Windows, `os.path.join(raiz, dirpath, f)` com `dirpath` vindo
  de `os.walk('.')` **descarta a raiz** quando o componente começa com barra
  invertida — o número sai plausível (215 em vez de 263) e engana. Usar
  `os.path.abspath`.
- **Reservar desde já os caracteres que o Passo 9 vai acrescentar depois** —
  confirmado na prática em 19-08-2026 (pacote TCDF-ANACE): os arquivos nasceram
  todos dentro do limite, mas o Passo 9 renomeia a pasta da matéria somando o
  sufixo de data ` (DD-MM-AAAA)` — **+13 caracteres de uma vez em todos os
  arquivos daquela pasta**. Foram **69 arquivos** que passaram do limite depois
  do fato e ficaram inacessíveis pela API do Windows. Ao projetar o caminho na
  hora de nomear o arquivo, contar a pasta **já com** o sufixo de data (e com o
  prefixo `(N-M) `, que também só entra no Passo 9), não com o nome base.
- **Se mesmo assim algum arquivo estourar, como consertar** (aprendido no mesmo
  caso — as duas saídas óbvias não funcionam nesse ambiente):
  - o prefixo `\\?\` de caminho longo **não funciona no drive do Google Drive**
    (devolve "não pode encontrar o caminho especificado");
  - caminho relativo também não resolve, porque o Windows soma o CWD antes de
    aplicar o limite.
  - O que funciona: **renomear a pasta da matéria pra um nome curto temporário**
    (ex: `_x`), encurtar os arquivos lá dentro, e devolver o nome real da pasta.
    Ao calcular o novo nome, usar o comprimento do caminho **final** (com a
    pasta já de volta ao nome real), não o do caminho temporário. Preservar o
    sufixo de data `(DD-MM-AAAA)` do arquivo e cortar só a parte descritiva.
- **Truncar nome de arquivo sem perder o que diferencia dois arquivos:** se dois
  arquivos da mesma matéria têm título quase idêntico e só diferem no final (ex:
  "Simulado Especial ... (23/08/2026)" vs "... (23/08/2026) Gabarito"), truncar
  o texto genérico pra um tamanho fixo faz os dois ficarem com o mesmo nome e um
  sobrescreve o outro. Colocar o que diferencia (`Gabarito`, número da parte,
  etc) **no início do nome do arquivo**, antes do texto que vai ser truncado.
- **Nem todo curso começa em "Aula 00"** — alguns (ex: Direito Processual Penal
  nesse pacote) começam direto em "Aula 01". Não assumir que "Aula 00" sempre
  existe; usar a primeira aula que realmente aparecer na listagem.
- **"Primeira aula que aparece" pode estar travada** (com "Disponível em
  DD/MM/AAAA") — trata-se normalmente como qualquer aula bloqueada: vira
  placeholder `.txt` (Passo 8), não é motivo pra pular pra segunda aula.

## Detalhes técnicos e pegadinhas (herdados da baixar-curso-especifico-estrategia)

- **Nunca clicar às cegas em coordenadas fixas** — sempre esperar carregar
  (`wait` ~1.5-2s) e confirmar com `screenshot` ou `read_page`/`find` antes de
  clicar, porque o layout muda de aula pra aula e de categoria pra categoria.
- **Fechar aba + navegar na mesma aba de controle no mesmo `browser_batch`**
  costuma falhar — fazer em chamadas separadas.
- O campo de busca da página do pacote (`Pesquisar por curso...`) filtra a lista
  em tempo real — útil pra localizar rápido um curso específico dentro do
  pacote, mas usar `find` + `form_input` pra digitar nele (o `type` direto às
  vezes não funciona se o campo perdeu o foco).
- O link da CDN é assinado e temporário (parâmetro `Expires`), mas isso só afeta
  o **link de download** — o arquivo já baixado no disco é permanente.
- O Chrome do usuário precisa ficar aberto (pode minimizado) durante toda a
  execução.
- Um pacote pode ter 40+ itens — processar tudo sem pausar pra confirmação a
  cada matéria, só reportar progresso a cada poucas matérias ou ao trocar de
  categoria.
- **Atualização Completa é bem mais lenta num pacote grande** — rebaixa todo PDF
  já existente do pacote inteiro só pra comparar a data. Não é o padrão sugerido;
  só usar quando o usuário pedir explicitamente ou aceitar a opção quando
  oferecida no Passo 2.
- Extração de data depende de `pypdf` (Python). Se o pacote não estiver
  instalado, instalar com `pip install pypdf` antes de processar a primeira aula.

## Regras gerais

- Não baixar vídeos, resumos, slides, mapas mentais ou cadernos de questões —
  só o livro eletrônico (PDF), em qualquer categoria.
- Não pular as perguntas do Passo 0 (link + pasta), do Passo 2 (pasta de pacote
  existente encontrada → Atualização Parcial, Atualização Completa ou criar
  nova), do Passo 4 (modo atualização — confirmar quais matérias atualizar) e
  do Passo 5 (modo novo — quais categorias baixar), mesmo que o usuário pareça
  já ter dado essas informações antes — confirmar a cada execução da skill.
- Se o link mandado for de um curso único (não um pacote), avisar e sugerir a
  skill `baixar-curso-especifico-estrategia`.

### Conferir versão/integridade sem baixar o PDF (técnica do `Range`)

**Descoberta em 2026-08-20, e é o jeito barato de auditar uma pasta inteira.**

O endpoint de download **aceita requisição parcial**. Pedindo `Range: bytes=0-99` o
servidor responde `206` com o header `Content-Range: bytes 0-99/<TAMANHO TOTAL>` — ou
seja, **100 bytes trazem o tamanho exato do arquivo remoto**.

```python
UA = {'User-Agent': '<UA de browser>', 'Referer': 'https://www.estrategiaconcursos.com.br/',
      'Range': 'bytes=0-99'}
r = requests.get(url_assinada, headers=UA, timeout=60)
tamanho_remoto = int(r.headers['Content-Range'].split('/')[-1])   # status 206
```

Comparando com `os.path.getsize()` do arquivo local dá pra saber **qual versão está na
pasta**, sem baixar nada:

| Diferença local x remoto | Significa |
|---|---|
| dezenas de bytes (4 a 30 na prática) | é o mesmo arquivo — a variação é a marca d'água gerada na hora |
| megabytes | é outra versão |

Limiar usado: `dif < max(2000, tamanho_local * 0.002)`.

**Como identificar o stub do Passo 6.1 por aqui:** o stub tem sempre ~**699 KB**, e é
esse tamanho que volta no `pdf_simplificado` das aulas rebaixadas. Se o remoto vier em
~699 KB e o local for muito maior, aquele arquivo é `LC` (rebaixe por stub), mesmo com
`pdf_simplificado` presente na API.

**Cuidado — HEAD não funciona:** o endpoint devolve `404` para `HEAD`. Só `GET` com
`Range`. E **não dá pra fazer isso pelo `javascript_tool`**: `Content-Range` não é header
seguro de CORS e volta `null` no navegador. Tem que ser do shell, com o link assinado.

**Onde isso vale:** auditar uma pasta inteira depois de um mutirão, conferir se o PDF
local ainda bate com o do site antes de decidir rebaixar em Atualização Completa, e
preencher o sufixo `LS`/`LC` de coleta antiga sem refazer download. Em 2026-08-20 essa
técnica conferiu 56 aulas de Contabilidade do Regular Controle e achou **exatamente os
19 rebaixes por stub** que a skill já tinha registrado — validação independente do método.

### ARMADILHA: assunto que termina em "LC" ou "LS"

**Custou um rótulo errado silencioso em 2026-08-20.** Não repetir.

Ao decidir se um arquivo **já tem** o sufixo, é tentador testar o fim do nome:

```python
re.search(r' L[SC] \(\d\d-\d\d-\d\d\d\d\)\.pdf$', nome)   # ERRADO
```

Isso casa por acidente com assunto que **termina** em `LC` ou `LS` — e `LC` é comum em
matéria jurídica (Lei Complementar). O caso real:

```
Aula 12 - Previdência complementar - LC 108-2001 e LC (22-07-2026).pdf
```

O arquivo **não tinha sufixo**, foi tratado como se tivesse, ficou de fora do lote, e
depois foi lido como `LC` quando na verdade era `LS`. Num acervo de 1096 PDFs, um único
caso — e sem a conferência por `Range` ele passaria batido.

**Como fazer certo:**

1. **Nunca deduzir a versão lendo o nome do arquivo.** A fonte é a API (ou o log da
   coleta). O nome é rótulo para humano, não campo de dado.
2. Para saber se o lote já rodou, **conferir a contagem**: nº de PDFs na pasta contra
   nº de linhas no log de renomeação. Divergência de 1 já é sinal.
3. Se precisar mesmo testar pelo nome, exigir que **o token anterior ao sufixo não seja
   ele próprio** ambíguo — na prática, comparar com a lista de aulas da API em vez de
   confiar na regex.
4. **Sempre fechar com conferência por amostra** (ver a técnica do `Range` acima). Foi
   ela que pegou este caso.
