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

Não seguir em frente sem as respostas 1 e 2 acima.

**Reduzir o tamanho do caminho é uma preocupação constante, não só nos casos
óbvios** — confirmado pelo Elvis em 2026-08-18. Sempre que for nomear pasta ou
arquivo, já pensar no caminho completo resultante (ver orçamento de
caracteres nos "Detalhes técnicos" mais abaixo) e preferir a versão mais curta
que ainda deixe a aula identificável — não esperar bater no limite pra só
então cortar.

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
   sigla de edital. Ao identificar esse padrão, usar `(Regular <Área>)` no
   lugar de `(SIGLA_CONCURSO-SIGLA_CARGO)` no nome da pasta (ex: `Direito
   Administrativo (Regular Fiscal)`). Não precisa perguntar ao usuário quando
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

## Passo 2: Definir o nome da pasta do curso

Padrão fixo (sempre seguir esse formato):

```
Matéria (SIGLA_CONCURSO-SIGLA_CARGO) (DD-MM-AAAA)
```

Exemplo: `Direito Constitucional (TCDF-ANACE) (18-08-2026)`

- Sintetizar o nome da matéria se for muito extenso.
- Sempre entre parênteses: sigla do concurso, traço, sigla do cargo.
- **A data no final, entre parênteses, é a data da última vez que essa pasta
  foi criada/atualizada por essa skill** — confirmado pelo Elvis em
  2026-08-18. Na criação da pasta (download novo), é a data de hoje (data do
  carregamento inicial das aulas). Numa atualização (Passo 3), essa data é
  **recalculada pra hoje** no final do processo (Passo 7) — nunca acumular
  datas antigas, sempre substituir pela mais recente. Serve pra saber, só
  olhando o nome da pasta, quando aquela disciplina específica foi mexida pela
  última vez — importante porque é comum atualizar só uma disciplina por vez,
  sem tocar nas outras do mesmo pacote.
- **Matéria com nome repetido no mesmo pacote:** se já existir (ou vier a
  existir) outra pasta de matéria com esse mesmo nome dentro do mesmo pacote
  — caso real: um pacote com duas matérias "Contabilidade Geral e Avançada",
  uma por professor — usar um diferenciador no nome da pasta pra não colidir.
  O mais confiável costuma ser o nome do professor, que aparece no título
  completo do curso no site (ex: "Curso Básico de Contabilidade Geral e
  Avançada (Prof. Gilmar Possati)" → pasta `Contabilidade Geral e Avançada -
  Gilmar Possati (SIGLA-SIGLA)`). Se não houver professor único, usar outro
  elemento do título que diferencie (diploma legal, sigla de norma etc).
  Reconhecer esse padrão sozinho ao notar o nome duplicado — não precisa
  perguntar ao usuário. Confirmado pelo Elvis em 2026-08-18.
- Esse é o padrão definitivo — não trocar sem o usuário pedir explicitamente.
- **Limite de caminho do Windows (260 caracteres):** antes de criar a pasta,
  estimar o tamanho do caminho completo (`pasta raiz + \ + nome da matéria +
  \ + nome de arquivo mais longo esperado`). Está autorizado a sintetizar o
  nome da matéria (e, se precisar, o nome dos arquivos de aula) sempre que
  isso ameaçar estourar o limite — não é preciso perguntar ao usuário toda vez,
  só nos casos ambíguos. Ver orçamento de caracteres sugerido nos "Detalhes
  técnicos e pegadinhas" abaixo.

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
`<pasta informada>/<Matéria (SIGLA-SIGLA)>/` com `mkdir -p`. Não tem o que
atualizar, então não precisa perguntar mais nada sobre isso.

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

## Atalho recomendado: pegar todas as aulas de uma vez pela API interna

**Confirmado em 2026-08-18.** Em vez de abrir a listagem e depois cada aula pra
extrair o `a.LessonButton`, dá pra buscar **o curso inteiro numa única chamada**:

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

### Fallback rápido: percorrer as aulas dentro da própria SPA

**Confirmado na prática em 2026-08-18**, quando o classificador do Claude Code
bloqueou a extração do `Bearer` e a API interna ficou indisponível. Em vez de
uma chamada de `navigate` por aula, dá pra percorrer várias aulas **num único
`javascript_tool`**: a área do aluno é um SPA React, então clicar no `<a>` da
aula troca a página sem reload, e `history.back()` volta pra listagem. Num
pacote de 211 aulas isso trocou ~240 navegações por ~40 chamadas.

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

## Verificação pendente (pedido do Elvis em 2026-08-18): dá pra baixar tudo por `fetch`?

**Fazer essa checagem no começo da próxima execução desta skill e reportar o
resultado ao Elvis no relatório final.** Não travar o download por causa dela:
se a resposta for "não dá" ou ficar duvidoso, seguir normalmente com o método
atual desta skill.

Contexto: nas skills do Bruno Bezerra (`baixar-resumo-especifico` /
`baixar-resumo-combo-completo`) o download inteiro passou a ser feito por
`fetch` de mesma origem, a partir de **uma única página aberta**, sem navegar
aula por aula — o que eliminou travamento da SPA, esperas longas de
renderização e throttling de timer, e derrubou o tempo do combo inteiro (336
aulas) pra ~40 minutos. O Elvis pediu pra conferir se o mesmo vale aqui.

O que checar no Estratégia (`estrategiaconcursos.com.br`), com o curso já
aberto e logado:

1. **Lista de aulas** — esta skill já usa a API interna (ver "Atalho
   recomendado: pegar todas as aulas de uma vez pela API interna"). Confirmar
   se ela continua respondendo e se cobre tudo que a barra lateral mostra.
2. **Link do PDF de cada aula sem abrir a aula** — procurar o endpoint que a
   página chama pra montar o botão de download do livro eletrônico (olhar
   `read_network_requests` filtrando por `api`, e o payload embutido na
   página). Se existir, é o equivalente ao "server action de materiais" do
   Bezerra.
3. **Download direto por `curl`** — testar se a URL final do PDF funciona fora
   do navegador (como no Bezerra, onde `/api/student/pdf?token=...` responde
   sem cookie de sessão) ou se depende de cookie/sessão, o que obriga a manter
   o download dentro do navegador.

**Se os três passarem:** reescrever o passo de download desta skill no mesmo
molde do Passo 4/5 da `baixar-resumo-especifico` — mas só **depois de
apresentar a proposta ao Elvis e ter o aval dele** (regra do passo de sugestão
de melhoria, que vale igual aqui).

**Se algum falhar:** registrar no relatório final o que falhou e por quê, pra
não ficar refazendo a mesma investigação em toda execução.

## Passo 5: Baixar o livro de cada aula (o núcleo do processo)

Para cada aula pendente, repetir:

1. Navegar para `https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{id}/aulas/{aulaId}`
   (ou clicar no título da aula na lista) e esperar ~2s carregar. **Conferir o
   título da aba depois de navegar** — o próprio resultado do `navigate` já
   costuma trazer o título de volta. Se o título voltar genérico ("Área do
   Aluno", ou o mesmo título de antes de navegar) em vez do título da aula,
   a navegação falhou silenciosamente (transiente, observado várias vezes na
   prática) — **renavegar uma vez pra mesma URL antes de seguir**, em vez de
   extrair o `LessonButton` de uma página errada (o que geraria um download
   errado ou um erro sem explicação clara).
2. **Não precisa clicar no card nem abrir aba nova.** O link de download já
   está no HTML da própria página, num `<a class="LessonButton">`. Extrair
   direto via JavaScript (`javascript_tool`):
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
   e renomear o `.tmp` pro nome final com a data.
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
<Rótulo exato da aula, igual está no site> - Assunto Sintético (DD-MM-AAAA).pdf
```

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

## Passo 7: Nomear a pasta com indicador de progresso (N-M) e data de atualização

Depois de processar todas as aulas do curso:

1. Contar **M** = total de aulas do curso e **N** = quantas delas realmente têm
   PDF baixado (arquivos `.pdf` de verdade, não os `.txt` placeholder do Passo 6).
2. **Se N < M** (curso incompleto): renomear a pasta pra começar com `(N-M) `,
   ex: `(10-20) Direito Administrativo (SIGLA-SIGLA) (18-08-2026)` (10 aulas
   com PDF já disponível, de um total de 20 aulas no curso). O indicador fica
   **entre parênteses, colado direto no nome da matéria** — sem traço
   separando os dois, só um espaço. **Usar traço dentro do parênteses (`N-M`),
   nunca barra (`N/M`)** — barra é separador de caminho no Windows e quebra o
   `Rename-Item` (confirmado na prática: tentar renomear com `/` lança erro
   "representa um caminho ou nome de dispositivo").
3. **Se N == M** (curso completo): a pasta fica sem o prefixo `(N-M)`, só
   `Direito Administrativo (SIGLA-SIGLA) (18-08-2026)`.
4. **Atualizar também o sufixo de data no final do nome pra data de hoje** (ver
   regra no Passo 2) — nessa mesma operação de renomear, sempre, independente
   de N ser igual ou menor que M. Isso registra quando essa disciplina
   específica foi mexida pela última vez.
5. **Modo atualização:** antes de recalcular, remover qualquer prefixo `(N-M) `
   e qualquer sufixo de data antigo que a pasta já tenha (de uma execução
   anterior) pra não acumular — sempre recalcular do zero e renomear com os
   números e a data atuais.
6. **Sempre renomear a pasta existente com `Rename-Item` (ou equivalente) —
   nunca apagar a pasta e recriar do zero pra aplicar esse prefixo/data.**
   Apagar e recriar perde a pasta original (e qualquer PDF real já baixado
   nela) e conta como criar uma pasta nova, não atualizar a existente.
7. **Se essa pasta de matéria estiver dentro de uma estrutura de pacote**
   (identificável por ter uma pasta de categoria como `Curso Regular` ou
   `Passo Estratégico` entre a pasta raiz do pacote e a pasta da matéria —
   ver `baixar-curso-completo-estrategia`), **atualizar também o sufixo de
   data da pasta do pacote** (a pasta-avó, dois níveis acima) pra data de
   hoje — mesmo mexendo só nessa disciplina, o pacote como um todo teve
   atividade recente e isso deve refletir no nome da pasta-mãe.

Isso deixa visível, só olhando o nome da pasta no Explorer, se o curso ainda tem
aula pendente de liberação pelo site ou já está 100% baixado, e quando essa
disciplina foi mexida pela última vez.

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
2. **Nome do arquivo:** `<Nome da Matéria> (SIGLA-SIGLA) - Metadados` — sem o
   sufixo de data (é um documento único que se atualiza, não recriado a cada
   execução).
3. **Se já existir uma planilha de metadados na pasta** (modo atualização):
   abrir e **ler o Curso ID registrado antes de sobrescrever qualquer coisa**
   — é o dado que o Passo 3 usa pra comparar contra o ID atual da URL.
4. **Aba "Aulas"** — mesmas colunas validadas no protótipo: `Rótulo (Aula)`,
   `Assunto`, `Status` (Baixado/Baixado (conferido)/Suspeito, com cor
   condicional verde/vermelho — ver os três status logo abaixo),
   `Data de Elaboração (PDF)`, `Data desta Verificação`, `Palavras-chave
   batidas`, `Total palavras-chave`, `Nº de páginas do PDF`, `Nome do
   arquivo`. Linha de título mesclada + subtítulo com pasta, **Curso ID
   Estratégia** e nome do pacote/concurso. Linha de resumo com fórmulas
   (`COUNTA`, `COUNTIF`) pro total de aulas, confirmadas e suspeitas.
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
    entre planilhas. Sem isso a execução morre no meio, com parte das
    planilhas criadas. O script tem que ser **idempotente**: procurar pelo
    nome do arquivo na pasta de destino e reaproveitar a planilha existente
    em vez de criar uma duplicada ao retomar. Ver a mesma regra em escala de
    pacote na `baixar-curso-completo-estrategia`, Passo 11.

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

- **Limite de 260 caracteres de caminho no Windows** — orçamento sugerido pra não
  estourar: pasta raiz (~50 caracteres, ex: a pasta padrão já usa isso) + nome da
  pasta da matéria até ~70 caracteres (`(N-M) Matéria (SIGLA-SIGLA)`) + nome do
  arquivo da aula até ~80 caracteres. Se a soma projetada passar de ~240
  caracteres (deixando margem de segurança), sintetizar o nome da matéria e/ou o
  assunto da aula no nome do arquivo até caber — está autorizado a fazer essa
  redução sozinho, sem perguntar ao usuário, priorizando manter a sigla e o
  número da aula intactos (é o que mais identifica o arquivo) e cortando a parte
  descritiva.
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

## Passo 10: Sugestão de melhoria da skill (obrigatória ao final de toda execução)

**Regra geral do workspace pra skills de download em massa e de cadernos de
questões, confirmado pelo Elvis em 2026-08-18** (ver `AGENTS.md`): depois do
relatório final (Passo 8), avaliar se algo aprendido nessa execução sugere um
ajuste na própria skill — bug novo, comportamento inesperado do site, passo
lento/repetitivo, oportunidade de deixar algo mais robusto.

- **Se identificar algo:** apresentar a sugestão ao Elvis de forma objetiva (o
  que aconteceu, o que mudaria na skill), perguntar se aprova, e só então
  editar o `SKILL.md` (dessa skill e/ou da `baixar-curso-completo-estrategia`,
  se aplicável às duas) e rodar `/syncar`.
- **Se nada de novo surgiu:** dizer isso de forma curta e objetiva — não
  inventar sugestão só pra ter o que falar.
- Nunca editar a skill nem sincronizar sem aprovação prévia.
