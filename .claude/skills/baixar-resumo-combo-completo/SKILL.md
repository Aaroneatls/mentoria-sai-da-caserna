---
name: baixar-resumo-combo-completo
description: >
  Baixa em lote os resumos esquematizados (PDF) de TODAS as matérias do curso
  "Resumos Esquematizados - Combo Completo | Parceria" do professor Bruno
  Bezerra (plataforma Tutory), organizando cada matéria numa pasta própria e
  nomeando cada arquivo pelo título impresso no próprio PDF. Pula automaticamente o Boas-vindas, o
  Sumário e o módulo de técnicas de revisão. Diferente da baixar-resumo-especifico (que baixa só UMA
  matéria), essa skill mapeia o curso inteiro e baixa tudo de uma vez. Use
  quando o usuário disser "baixa todos os resumos do Bruno Bezerra", "baixa o
  combo completo de resumos", "sincroniza a pasta Resumos Esquematizados
  inteira", "atualiza tudo dos resumos esquematizados".
---

# /baixar-resumo-combo-completo — Download de TODAS as matérias dos Resumos Esquematizados (Bruno Bezerra)

## O que essa skill faz

Usa o navegador (embutido por padrão, já logado) pra abrir o curso "Resumos
Esquematizados - Combo Completo | Parceria" do professor Bruno Bezerra, mapear
todas as matérias (playlists) que existem dentro dele, e baixar — direto no
disco — o PDF de resumo esquematizado de cada aula de cada matéria, organizado
em pastas por matéria.

**Curso fixo, nunca comprar nada:** o Elvis só tem acesso liberado ao curso
"Combo Área Fiscal + Receita Federal" (id `613765f9-f1e0-4149-a84f-ebac1314faa1`).
Os outros cards no dashboard ("Cursos premium", botão "Desbloquear") são pagos
e **nunca devem ser comprados nem clicados**. Login: ver referência salva na
memória (URL `https://alunoprofbrunobezerra.plataformatutory.com.br/dash`).

## Passo 0: Pergunta obrigatória no início

**Aviso obrigatório antes de qualquer outra coisa** (confirmado pelo Elvis em
2026-08-18, depois de um caso real de sessão derrubada durante um teste): a
plataforma do Bruno Bezerra **não permite login simultâneo em dois lugares**
— se o Elvis abrir a própria conta em outra aba/navegador enquanto essa skill
estiver rodando (e essa skill costuma rodar por muito mais tempo que a de
matéria única, com centenas de aulas), a sessão que a skill está usando é
derrubada ("Login compartilhado / Sessão encerrada por segurança"),
interrompendo o download no meio. **Avisar o Elvis, logo no início da
execução, que ele não deve acessar essa plataforma (nenhuma aba, nenhum outro
navegador) até a skill terminar.**

**Pasta padrão:** `G:\Meu Drive\Inteligência Artificial\Resumos Esquematizados`
— mesmo papel que a pasta `Estrategia` tem pras skills do Estratégia Concursos.
**Verificar que ela existe de fato no disco** antes de usar (`Test-Path`/`ls`)
— se não existir, avisar o usuário em vez de criar em outro lugar.

Perguntar: **Pasta** — confirmar a padrão acima ou indicar outro local. Não
seguir sem essa resposta.

Não precisa perguntar qual curso — só existe um curso liberado (ver acima).

**Se a sessão cair no meio da execução** (página muda pra "Login
compartilhado"): parar imediatamente, avisar o Elvis, e esperar ele confirmar
que já logou de novo antes de continuar de onde parou — nunca tentar
digitar credenciais.

## Passo 1: Escolher o navegador e mapear as matérias do curso

1. **Navegador embutido (Browser pane, `mcp__Claude_Browser__*`) é o padrão** —
   já vem carregado, não precisa de `ToolSearch`. Se a sessão estiver
   deslogada, avisar o usuário e esperar ele logar. **Claude in Chrome só com
   autorização prévia pedida na própria conversa**, a cada vez.
2. Navegar para
   `https://alunoprofbrunobezerra.plataformatutory.com.br/dash/cursos/613765f9-f1e0-4149-a84f-ebac1314faa1`.
3. Extrair a lista completa de matérias (playlists) via JavaScript — **todas
   as 33 já estão no DOM mesmo com o carrossel mostrando só algumas visíveis
   na tela**, não precisa clicar em "Ver mais"/"Mostrar menos". Essa é a
   **única** vez que se lê o DOM: da lista de aulas em diante é tudo `fetch`
   (Passo 4):
   ```js
   Array.from(document.querySelectorAll('a[href*="/playlists/"]'))
     .map(a => ({href: a.href, txt: a.textContent.replace(/\s+/g,' ').trim()}));
   ```
   Cada item vem como `"N AulasNome da Matéria - ParceriaProgresso0%x"` — extrair
   o número de aulas e o nome (texto entre o número de aulas e " - Parceria").
4. Cruzar a quantidade de playlists extraídas com o total informado no
   cabeçalho da página ("33 playlists") — se não bater, revisar a extração
   antes de seguir.
5. **Salvar essa lista (nome da matéria + playlistId + nº de aulas) no
   scratchpad antes de baixar qualquer coisa** — é a fonte única de verdade
   pro loop de download do Passo 4.

## Passo 2: Excluir matérias fora do escopo

**Nunca baixar as três playlists abaixo** (confirmado pelo Elvis em
2026-08-18 — não são disciplinas, não fazem parte do conteúdo de resumo em
si):

- `Boas-vindas aos Resumos Esquematizados - Parceria`
- `Sumário - completo - Parceria`
- `Curso sobre revisões e materiais de revisão - Parceria`

Todas as outras playlists entram no download — só as disciplinas de verdade
(e os Flashcards, que vão pra pasta própria — ver Passo 3).

## Passo 3: Definir pasta de cada matéria

```
<Nome da matéria, sem o sufixo " - Parceria"> (N-M) (DD-MM-AAAA)
```

Mesma convenção da skill `baixar-resumo-especifico` (Passo 2 dela — ver lá o
detalhe completo de como calcular `(N-M)` e o limite de 260 caracteres de
caminho no Windows, que fica ainda mais apertado aqui por conta de rótulos de
aula longos):

- **`(N-M)`** — N aulas com PDF confirmado / M total daquela matéria. **Omitir
  esse indicador quando N == M** (matéria 100% ok, sem pendência) — só
  aparece quando sobrou alguma pendência (não confirmado, verificação de
  conteúdo falhou, ou movido pra `Descontinuados`).
- **`(DD-MM-AAAA)`** — data de hoje, sempre presente. Ao encontrar uma pasta
  já existente pra uma matéria (Passo 4, item 1), recalcular `(N-M)` e
  atualizar a data no final do processamento daquela matéria, mesmo que nada
  tenha mudado — renomear a pasta existente, nunca apagar e recriar.

**Caso especial — Flashcards:** hoje a playlist `Flashcards - Parceria` tem
uma aula só e **nenhum material na plataforma** — a aula manda o aluno pra uma
pasta pública do Google Drive com baralhos do Anki (confirmado em 2026-08-18).
Nesse cenário **não criar pasta nem planilha de Flashcards**, só registrar no
relatório final. Se um dia a playlist passar a expor PDF, aí sim ela ganha
pasta própria `Flashcards (DD-MM-AAAA)` (mesma regra de `(N-M)`; dentro da
pasta raiz do Passo 0, no mesmo nível das pastas de matéria).

Não sintetizar nem abreviar os nomes de matéria aqui — são curtos.

## Passo 4: Baixar cada matéria (reaproveitar a mecânica da skill de matéria específica)

Pra cada playlist da lista do Passo 1 (exceto as três excluídas no Passo 2),
repetir exatamente a mecânica dos **Passos 3 a 7 da skill
`baixar-resumo-especifico`** — em especial o **Passo 4 (levantamento por
`fetch`, sem navegar)** e o **Passo 5 (download + nome vindo do PDF)**, que
foram reescritos em 2026-08-18 depois de baixar o combo inteiro:

1. Procurar pasta existente pra essa matéria dentro da pasta raiz (detecção
   automática — comparação ignorando maiúsculas, acentuação, **e os sufixos
   `(N-M)` e `(DD-MM-AAAA)`** — mudam a cada execução, não fazem parte da
   identidade da pasta). **Se achar pasta com planilha de metadados
   (Passo 6), conferir o Playlist ID registrado nela contra o `playlistId`
   atual dessa matéria antes de tratar como atualização** — mesma checagem
   (com o mesmo aviso ao Elvis se for diferente) do Passo 3, item 2 da skill
   `baixar-resumo-especifico`. Fazer essa checagem matéria por matéria, não
   só uma vez pro combo inteiro.
2. **Instalar as funções `__lessons` / `__mats` / `__sign` / `__prep` uma vez
   só** (Passo 4 da skill irmã) e reusar pro combo inteiro — elas ficam no
   `window` da página aberta. **Não navegar depois disso**, senão elas se
   perdem e é preciso reinstalar. O `window.__cache` guarda a lista de aulas
   por playlist, então chamar `__prep(pid, ini, fim)` em lotes da mesma
   matéria não refaz o levantamento.
3. Baixar o PDF de cada aula em **lotes de 11 a 14 aulas**: uma chamada
   `__prep` devolve o TSV com `materialId`, `X-Amz-Date` e `X-Amz-Signature`,
   e o download por `curl` vem **logo em seguida** (o link assinado dura 5
   minutos). Playlist grande = 2-3 lotes; playlists pequenas podem ser
   agrupadas numa chamada só, desde que o total de aulas do lote fique dentro
   do limite (o `javascript_tool` corta em 30s, ~1,5s por aula).
   - Nome do arquivo: **título impresso na capa do PDF quando ele divergir do
     rótulo do site** (Passo 5.1 da skill irmã), mantendo código e matéria.
   - **Validação obrigatória do arquivo baixado, antes de nomear ou substituir
     qualquer coisa** (Passo 5 da skill irmã): baixar sempre pra um
     `tmp_<materialId>.pdf`, mandar `User-Agent` de browser + `Referer` no
     `curl`, e só aceitar se passar nos três testes — `HTTP:200`, primeiros 5
     bytes iguais a `%PDF-`, e `pypdf` abrindo com páginas > 0. **Nunca validar
     só por "HTTP 200 + tamanho não-trivial":** em 2026-08-18, nas skills do
     Estratégia, o servidor respondeu 200 com uma página HTML de ~238 KB no
     lugar do PDF e essa checagem frouxa deixou passar — 27 arquivos bons foram
     destruídos. Vale também antes da comparação por hash do item 5: hash de um
     HTML contra o PDF antigo dá "diferente" e substituiria o arquivo bom.
     Se um lote inteiro for recusado, parar e avisar (sessão derrubada por login
     simultâneo, ou bloqueio por volume) — nunca insistir em laço.
   - **Verificação de conteúdo obrigatória** (Passo 5.2 da skill irmã).
   - **Extrair o Sumário da aula** (Passo 5.3 da skill irmã) — usado na
     comparação de atualização (item 5) e na planilha (Passo 6).
4. Aula sem material (aviso, cronograma, Flashcards) não gera arquivo e não é
   erro. Não existe placeholder `.txt` nessa plataforma.
5. Modo atualização (se a pasta da matéria já existir e o usuário confirmar
   atualização — perguntar por matéria encontrada, ou perguntar uma vez só no
   início "atualizar todas as matérias que já existem?"): baixar de novo,
   comparar por hash (`Get-FileHash`) com o arquivo local existente — hash
   igual descarta o novo, hash diferente substitui e registra a mudança.
   **Antes de descartar o arquivo antigo, comparar o Sumário dele com o do
   novo** (Passo 6, item 3 da skill irmã) e registrar no relatório o que
   mudou de verdade (tópico removido/adicionado), não só "PDF atualizado".
   Atenção: **arquivo que mudou de nome pela regra do Passo 5.1 não é aula
   nova** — cruzar também pelo `Rótulo na plataforma` registrado na planilha
   antes de concluir que sumiu ou que apareceu.
6. **Aula que sumiu inteira da playlist daquela matéria** (rótulo de um
   arquivo local não bate com nenhuma aula da lista atual): **nunca apagar**
   — confirmado dobrando a checagem (Passo 6, item 6 da skill irmã), mover o
   arquivo pra uma subpasta `Descontinuados` dentro da própria pasta daquela
   matéria (ex: `Direito Administrativo/Descontinuados/...pdf`), mantendo o
   nome original. Registrar cada um no relatório final (Passo 5) pra revisão
   manual do Elvis — a skill não decide sozinha se foi descontinuação real ou
   migração pra outro rótulo.
7. **Não é preciso pausa preventiva nesse método** (a antiga pausa adaptativa
   existia por causa do travamento da SPA ao navegar aula por aula, que não
   acontece mais). Referência de 2026-08-18: 336 aulas, ~40 minutos, sem
   nenhum travamento. Se ainda assim aparecer lentidão ou erro repetido,
   diminuir o tamanho do lote antes de pensar em pausa.

**Diferença em relação à skill de matéria específica:** aqui, em vez de
perguntar pasta-a-pasta se já existe e como proceder, é mais prático perguntar
**uma única vez no começo**: se alguma pasta de matéria já existir dentro da
pasta raiz, avisar quais e perguntar se quer **Atualização** (reconferir
essas) ou **pular as que já existem** e baixar só as matérias que ainda não
têm pasta. Ainda assim, **se aparecer mais de uma pasta correspondente pra uma
mesma matéria**, listar e perguntar qual é a certa antes de seguir (não
escolher sozinho).

## Passo 5: Progresso e validação final

1. Processar as matérias sem pausar pra confirmação a cada uma — reportar
   progresso a cada poucas matérias concluídas (ex: "5/31 matérias
   processadas").
2. Ao final de cada matéria, cruzar a lista de rótulos salva com os `.pdf`
   presentes na pasta (mesma lógica de validação por nome da skill irmã).
3. **Relatório final obrigatório**, cobrindo o combo inteiro:
   - Quantas matérias processadas, quantas puladas por já não fazerem parte do
     escopo (Sumário/revisão).
   - Quantas aulas baixadas no total, quantas atualizadas (se modo atualização),
     quantas sem material (aula sem PDF disponível).
   - Quantas marcadas como "não confirmado" (aula que tinha PDF mas não deu
     pra reconfirmar o material nessa execução) e quantos arquivos movidos pra
     `Descontinuados` (Passo 4, item 6 desta skill), listando matéria + rótulo
     de cada um pra revisão manual.
   - **Quais arquivos ficaram com nome vindo da capa do PDF** em vez do
     rótulo do site (Passo 5.1 da skill irmã), listando o "de → para" — é
     mudança de nomenclatura, o Elvis precisa ver.
   - Situação dos Flashcards: hoje essa playlist não expõe PDF na plataforma
     (a aula manda pra uma pasta pública do Drive com baralhos do Anki), então
     **não se cria pasta nem planilha de Flashcards** — só registrar isso no
     relatório. Se um dia passar a ter PDF, aí sim vale a pasta própria
     (Passo 3).
   - Confirmar quantas planilhas de metadados foram criadas/atualizadas
     (Passo 6).

## Passo 6: Planilha de metadados de cada disciplina (obrigatória, Google Sheets)

**Confirmado pelo Elvis em 2026-08-18: toda matéria processada nessa execução
ganha uma planilha de metadados própria, na mesma pasta dela** — mesmo
processo e mesmo formato validado na skill `baixar-resumo-especifico` (ver
Passo 8 dela: Google Sheets nativo via `gspread`, nunca `.xlsx` local; abas
"Aulas" + "Descontinuados" (se aplicável) + "Legenda"; colunas
`Rótulo na plataforma (quando diferente)` e `Observação` no fim da aba
"Aulas", pra registrar os casos em que o nome veio da capa do PDF; Playlist
ID no subtítulo; fórmulas com `;`; formatação padrão; ler de volta pra conferir que
não deu erro).

**Diferença de escala:** repetir esse passo pra **cada matéria processada
nessa execução**, uma planilha por pasta de disciplina (não uma planilha
única pro combo inteiro) — mantém a granularidade de "atualizar só uma
matéria sem mexer nas outras". Flashcards também ganha sua própria planilha,
na pasta única dela, **só se de fato tiver algum PDF baixado** (hoje a
playlist de Flashcards costuma não expor material nessa rota — nesse caso não
tem sentido criar planilha vazia).

**Escopo da atualização da planilha = escopo da execução** (mesma regra das
skills do Estratégia):
- Matéria pulada nessa execução (já tinha pasta e o Elvis escolheu "pular as
  que já existem" no Passo 4) → planilha dela **não é tocada**.
- Matéria efetivamente processada (download novo ou atualização) → planilha
  dela é criada/atualizada.
- Em nenhum caso atualizar a planilha de uma matéria que não foi processada
  nessa execução.

## Regras gerais

- Só baixar o PDF de resumo esquematizado — não baixar vídeo, não seguir links
  de "QUESTÕES" nem interagir com o Fórum da aula (decisão do Elvis em
  2026-08-18, pode mudar no futuro).
- **Nunca clicar em "Desbloquear" nem navegar pra `pay.plataformatutory.com.br`.**
- Link assinado da S3 expira em 5 minutos — baixar logo depois de obter cada
  `uri`, um de cada vez.
- Se o usuário pedir só uma matéria específica em vez do combo inteiro, usar a
  skill `baixar-resumo-especifico` em vez dessa.

## Passo 7: Sugestão de melhoria da skill (obrigatória ao final de toda execução)

**Mesma regra da skill `baixar-resumo-especifico` (Passo 9 dela), confirmado
pelo Elvis em 2026-08-18:** ao final do relatório do Passo 5, avaliar se algo
aprendido nessa execução do combo sugere um ajuste numa das duas skills (essa
ou a de matéria específica, já que compartilham a mesma mecânica). Apresentar
a sugestão ao Elvis, esperar aprovação, e só então editar o(s) `SKILL.md` e
rodar `/syncar`. Se nada de novo surgiu, dizer isso de forma curta e objetiva.
Nunca editar/sincronizar sem aprovação prévia.
