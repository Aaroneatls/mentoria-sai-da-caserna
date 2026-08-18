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

3. **Base de siglas de disciplinas (pergunta temporária):** perguntar se já
   existe alguma planilha/tabela de referência com nome de disciplina → sigla.
   **Hoje essa base ainda não existe** — enquanto não existir, seguir usando o
   nome completo da matéria no nome da pasta (padrão atual do Passo 2). Quando o
   usuário criar essa base no futuro, ele vai indicar — a partir daí, usar a
   sigla da disciplina no lugar do nome completo ao montar o nome da pasta. Até
   lá, essa pergunta serve só de lembrete pro usuário, não bloqueia o fluxo.

Não seguir em frente sem as respostas 1 e 2 acima.

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

**Se encontrar exatamente uma pasta correspondente:**

1. Listar o que já tem dentro: quantos `.pdf` já baixados, quantos `.txt`
   placeholder pendentes.
2. Informar o usuário e perguntar como quer proceder, com três opções:
   - **Atualização Parcial** (padrão sugerido) — baixa só as aulas que ainda
     estão faltando (travadas na coleta anterior, agora liberadas). Não mexe
     nos PDFs já baixados. Rápido.
   - **Atualização Completa** — além de baixar o que falta, reconfere **todos**
     os PDFs já baixados contra a versão atual no site e substitui os que
     tiverem sido revisados/atualizados desde a última coleta. Mais lento,
     porque precisa rebaixar cada aula já existente pra comparar.
   - **Criar pasta nova do zero** — mesmo já tendo uma pasta encontrada.
3. **Se optar por Atualização Parcial ou Atualização Completa:** esse vira o
   modo atualização pro resto da skill — usar essa pasta, seguir a lógica de
   "Modo atualização" do Passo 4 em diante, no sub-modo escolhido.
4. **Se optar por criar nova do zero:** perguntar também **se quer que a pasta
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
   curl -sL -o "<pasta>/Aula NN - Assunto Sintetico.pdf.tmp" "<href capturado>" -w "HTTP:%{http_code} SIZE:%{size_download}\n"
   ```
   Conferir que retornou `HTTP:200` e um `SIZE` não-trivial.
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
  em PDF)`, `(Equipe de Legislação)`, `(Somente Vídeo)`. Ex: o rótulo do site
  `Aula 20 (Somente PDF)` vira só `Aula 20` no nome do arquivo. **Se aparecer
  algum outro tipo de anotação parecida (entre parênteses, junto ao número da
  aula) que não se encaixe claramente como "tipo de mídia/equipe" nem como
  parte do conteúdo, perguntar ao usuário antes de decidir se entra ou não** —
  não adivinhar sozinho pra esse caso novo.
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

### Extrair a data do PDF

A maioria dos livros eletrônicos do Estratégia traz, na primeira página, a data
de elaboração/atualização daquele material. Depois de baixar o PDF (todo
download, não só em modo atualização), extrair essa data pra usar no nome do
arquivo:

```bash
python -c "
import re, sys, unicodedata
from pypdf import PdfReader

MESES = {'janeiro':1,'fevereiro':2,'marco':3,'abril':4,'maio':5,'junho':6,
         'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

texto = PdfReader(sys.argv[1]).pages[0].extract_text() or ''

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
" "<caminho do .tmp>"
```

- **Duas datas por extenso** têm sido observadas na prática: numérica
  `DD/MM/AAAA` e escrita por extenso em português `DD de Mês de AAAA` (ex: "31
  de Julho de 2026" — confirmado testando no curso de Direito Administrativo,
  pacote Regular Fiscal). O script acima já cobre os dois formatos, tentando o
  numérico primeiro. Se aparecer um terceiro formato novo, adaptar o regex.
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

**Validação é só por nomenclatura, nunca abrindo o conteúdo dos PDFs** —
confirmado pelo Elvis em 2026-08-18: não vale a pena gastar tokens abrindo/lendo
cada PDF de novo nessa etapa (isso já foi feito uma vez, na hora do download, pra
extrair a data — não precisa repetir). O cruzamento é puramente comparação de
texto: rótulo da listagem do site vs. nome do arquivo local.

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
5. **Reportar o resultado dessa validação pro usuário** — se bateu 100% ou se
   sobrou algo em algum lado. Essa é a única parte do processo que sempre vale
   a pena resumir em texto no final, mesmo a skill normalmente não gerando
   relatório à parte.

O resultado final é a pasta em si, já com os arquivos dentro, o nome renomeado
com o progresso `(N-M)`, e a confirmação de que o cruzamento bateu.

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
