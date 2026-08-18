---
name: baixar-resumo-especifico
description: >
  Baixa em lote os resumos esquematizados (PDF) de UMA matéria/playlist
  específica do curso "Resumos Esquematizados - Combo Completo | Parceria" do
  professor Bruno Bezerra (plataforma Tutory), renomeando os arquivos com o
  rótulo exato de cada aula e organizando numa pasta local. Diferente da
  baixar-resumo-combo-completo (que baixa todas as matérias de uma vez), essa
  skill baixa só UMA matéria por vez. Use quando o usuário disser "baixa essa
  matéria do Bruno Bezerra", "baixa os resumos de [matéria]", "sincroniza essa
  playlist de resumos", "atualiza a matéria X que já baixei", ou mandar um link
  de playlist do alunoprofbrunobezerra.plataformatutory.com.br pedindo pra
  organizar os PDFs.
---

# /baixar-resumo-especifico — Download de UMA matéria dos Resumos Esquematizados (Bruno Bezerra)

## O que essa skill faz

Usa o navegador (embutido por padrão, já logado) pra navegar pelas aulas de uma
matéria (playlist) dentro do curso "Resumos Esquematizados - Combo Completo |
Parceria" do professor Bruno Bezerra, e baixa direto no disco o PDF de resumo
esquematizado de cada aula, renomeado com o rótulo exato da aula e organizado
numa pasta local.

**Curso fixo, nunca comprar nada:** o Elvis só tem acesso liberado ao curso
"Combo Área Fiscal + Receita Federal" (id `613765f9-f1e0-4149-a84f-ebac1314faa1`)
dentro dessa plataforma — os outros cards que aparecem no dashboard ("Cursos
premium", botão "Desbloquear") são pagos e **nunca devem ser comprados nem
clicados** por essa skill. Login: ver referência salva na memória (URL
`https://alunoprofbrunobezerra.plataformatutory.com.br/dash`).

## Passo 0: Perguntas obrigatórias no início

**Pasta padrão:** `G:\Meu Drive\Inteligência Artificial\Resumos Esquematizados`
— mesmo papel que a pasta `Estrategia` tem pras skills do Estratégia Concursos.
**Verificar que ela existe de fato no disco** antes de usar (`Test-Path`/`ls`),
já que vive dentro do Google Drive sincronizado — se não existir, avisar o
usuário em vez de criar em outro lugar.

**Aviso obrigatório antes de qualquer outra coisa** (confirmado pelo Elvis em
2026-08-18, depois de um caso real de sessão derrubada durante um teste): a
plataforma do Bruno Bezerra **não permite login simultâneo em dois lugares**
— se o Elvis abrir a própria conta em outra aba/navegador enquanto essa skill
estiver rodando, a sessão que a skill está usando é derrubada ("Login
compartilhado / Sessão encerrada por segurança"), interrompendo o download no
meio. **Avisar o Elvis, logo no início da execução, que ele não deve acessar
essa plataforma (nenhuma aba, nenhum outro navegador) até a skill terminar.**

Sempre perguntar antes de fazer qualquer coisa:

1. **Qual matéria** — nome ou link da playlist (padrão
   `https://alunoprofbrunobezerra.plataformatutory.com.br/dash/cursos/613765f9-f1e0-4149-a84f-ebac1314faa1/playlists/{playlistId}`).
   Se o usuário só disser o nome da matéria, navegar até a página do curso
   (Passo 1) e localizar a playlist correspondente antes de seguir.
2. **Pasta:** perguntar se quer usar a pasta padrão (acima) ou indicar outro local.

Não seguir em frente sem essas respostas.

**Se a sessão cair no meio da execução** (página muda pra "Login
compartilhado"): parar imediatamente, avisar o Elvis, e esperar ele confirmar
que já logou de novo antes de continuar de onde parou — nunca tentar
digitar credenciais.

## Passo 1: Escolher o navegador e localizar a playlist

1. **Navegador embutido (Browser pane, `mcp__Claude_Browser__*`) é o padrão** —
   já vem carregado, não precisa de `ToolSearch`. Se a sessão estiver
   deslogada, avisar o usuário e esperar ele logar — nunca digitar credenciais.
   **Claude in Chrome só com autorização prévia pedida na própria conversa**,
   a cada vez.
2. Se só tiver o nome da matéria (sem link), navegar até
   `https://alunoprofbrunobezerra.plataformatutory.com.br/dash/cursos/613765f9-f1e0-4149-a84f-ebac1314faa1`
   e extrair a lista de playlists via JavaScript:
   ```js
   Array.from(document.querySelectorAll('a[href*="/playlists/"]'))
     .map(a => ({href: a.href, txt: a.textContent.replace(/\s+/g,' ').trim()}));
   ```
   Cada item vem como `"N AulasNome da Matéria - ParceriaProgresso0%x"` — o
   nome da matéria é o texto entre o número de aulas e " - Parceria". Localizar
   a playlist cujo nome bate com o pedido do usuário (ignorar acentuação/maiúsculas
   na comparação). Se não achar uma correspondência clara, listar as playlists
   disponíveis e perguntar.
3. Guardar o `playlistId` (parte final do href) — é usado no Passo 2.

## Passo 2: Definir o nome da pasta da matéria

```
<Nome da matéria, sem o sufixo " - Parceria"> (N-M) (DD-MM-AAAA)
```

Duas informações entre parênteses, sempre nessa ordem (padrão trazido das
skills do Estratégia e adaptado aqui, confirmado pelo Elvis em 2026-08-18):

- **`(N-M)`** — indicador de progresso/completude: **N** = quantas aulas têm
  hoje um `.pdf` confirmado na pasta (passou pela verificação de conteúdo do
  Passo 5, item 6 — não conta "não confirmado" nem "verificação de conteúdo
  falhou" nem o que foi pra `Descontinuados`); **M** = total de aulas da
  playlist. Só existe/é calculado no **fim** da execução (Passo 7), depois de
  processar todas as aulas — no meio do processo a pasta ainda não tem esse
  número. Se **N == M** (tudo certo, sem pendência), **omitir esse indicador
  por completo** — a pasta fica só com a data, sinal de que está 100% ok. Só
  aparece `(N-M)` quando sobrou alguma pendência.
- **`(DD-MM-AAAA)`** — data da última execução da skill sobre essa matéria,
  sempre presente (mesmo quando `(N-M)` some por estar tudo completo). Sempre
  a **data de hoje** na execução atual (download novo ou atualização).

Exemplos: matéria com as 9 aulas confirmadas → `Administração Financeira e
Orçamentária (18-08-2026)`. Matéria com 2 aulas pendentes de 9 → `Direito
Tributário (7-9) (18-08-2026)`.

**Caso especial — Flashcards:** se a playlist for `"Flashcards - Parceria"`,
usar o nome de pasta `Flashcards (DD-MM-AAAA)` (mesma regra de `(N-M)` acima,
não repetir "- Parceria").

**Limite de 260 caracteres de caminho no Windows:** com o sufixo de data (e
possivelmente `(N-M)`) somado ao nome já longo de alguns rótulos de aula
(alguns passam de 100 caracteres, ex: `R03 - Direito Administrativo -
Empresas Públicas, Fundações Públicas e Sociedades de Economia Mista.pdf`) e
à subpasta `Descontinuados`, o caminho completo pode chegar perto do limite
mais fácil aqui do que nas skills do Estratégia. Antes de criar a pasta ou
salvar um arquivo, estimar o caminho completo (`pasta raiz + \ + nome da
matéria com parênteses + \ + [Descontinuados\ se for o caso] + nome do
arquivo`). Se passar de ~240 caracteres (margem de segurança), está
autorizado a sintetizar o **assunto** do nome do arquivo (nunca o rótulo
inteiro, nunca o `R00`/código da aula) até caber — sem perguntar ao usuário
pra esse ajuste específico. **Colocar o que diferencia dois arquivos no
início do texto que for cortado**, não no fim — evita dois arquivos quase
idênticos ficarem com o mesmo nome truncado e um sobrescrever o outro (mesma
lição aprendida nas skills do Estratégia). Não sintetizar o nome da matéria
nem a data — só o assunto do arquivo, como último recurso.

## Passo 3: Procurar pasta existente (igual ao padrão das skills do Estratégia)

Buscar, só dentro da pasta informada no Passo 0, uma subpasta já existente que
bata com o nome da matéria definido no Passo 2 (ignorando maiúsculas,
acentuação, **e ignorando os sufixos `(N-M)` e `(DD-MM-AAAA)` na comparação**
— mudam a cada execução, não fazem parte da identidade da pasta). Se achar:

1. Listar quantos `.pdf` já existem dentro, e a data/indicador que estão no
   nome atual da pasta (última execução anterior).
2. **Conferir o Playlist ID antes de tratar como atualização** (mesmo
   princípio da checagem de Curso ID nas skills do Estratégia, confirmado
   pelo Elvis em 2026-08-18): se a pasta encontrada já tem uma planilha de
   metadados (Passo 8), ler o **Playlist ID Bezerra** registrado no
   subtítulo dela e comparar com o `playlistId` localizado agora pro mesmo
   nome de matéria.
   - **Igual:** seguir normalmente como atualização da mesma matéria.
   - **Diferente:** **avisar o Elvis antes de prosseguir, não decidir
     sozinho** — dar contexto pra decisão comparando o assunto da primeira
     aula (R00 ou a que vier primeiro) registrado na planilha antiga com o
     assunto da primeira aula da playlist atual, ex: "o Playlist ID mudou de
     {antigo} pra {novo}; a primeira aula registrada era '{assunto antigo}',
     a primeira aula do novo ID é '{assunto novo}' — parecem a mesma
     matéria, mas confirma antes de eu atualizar?". Mesmo se parecer a mesma
     matéria, comparar o conteúdo completo antes de concluir (a Aula 00 é só
     indício rápido).
   - Se a pasta não tiver planilha de metadados ainda (de antes dessa
     funcionalidade existir), não tem o que comparar — seguir normalmente, a
     planilha passa a registrar o ID a partir dessa execução.
3. Perguntar se quer **Atualização** (reconferir tudo — ver Passo 6, único modo
   de atualização que existe aqui, não tem "parcial" porque essa plataforma não
   sinaliza aula travada/pendente) ou **criar pasta nova do zero** (perguntar
   se apaga a antiga ou mantém as duas, igual ao padrão do Estratégia — nunca
   apagar sem confirmação explícita).
4. Se achar mais de uma pasta correspondente, listar todas e perguntar qual é
   a certa — não escolher sozinho.
5. **Ao final da execução (Passo 7), renomear a pasta pra atualizar a data e o
   indicador `(N-M)`**
   pra data de hoje, removendo a data antiga do nome — mesmo que nenhum PDF
   tenha mudado de conteúdo, a data reflete "quando foi a última vez que essa
   matéria foi conferida contra a plataforma", não só "quando o conteúdo
   mudou pela última vez". **Renomear a pasta existente, nunca apagar e
   recriar** (mesma regra das skills do Estratégia).

Se não achar nenhuma: é download novo, criar a pasta já com a data de hoje.

## Passo 4: Levantar a lista de aulas da playlist

1. Navegar para a URL da playlist
   (`.../cursos/613765f9-.../playlists/{playlistId}`) — a página redireciona
   automaticamente pra primeira aula da playlist.
2. Na página da aula, a barra lateral já lista todas as aulas da playlist.
   Extrair via JavaScript, deduplicando por `aulaId`. **Cuidado: o mesmo
   `aulaId` pode aparecer mais de uma vez no DOM com textos diferentes** — em
   especial, um link sem texto (ícone) pode vir **antes** do link com o rótulo
   de verdade (bug confirmado testando "Direito Administrativo": a aula R01
   ficou com rótulo vazio até a extração ser corrigida pra preferir o primeiro
   texto **não-vazio** encontrado pra cada `aulaId`, em vez de travar no
   primeiro texto que aparecer):
   ```js
   const links = Array.from(document.querySelectorAll('a[href*="/aulas/"]'));
   const map = new Map();
   for (const a of links) {
     const m = a.href.match(/\/playlists\/([0-9a-f-]+)\/aulas\/([0-9a-f-]+)/);
     if (!m) continue;
     const id = m[2];
     const txt = a.textContent.replace(/\s+/g,' ').trim();
     if (!map.has(id) || (!map.get(id).rotulo && txt)) {
       map.set(id, {playlistId: m[1], aulaId: id, rotulo: txt});
     }
   }
   JSON.stringify(Array.from(map.values()));
   ```
3. Cruzar a quantidade extraída com o número de aulas informado no cabeçalho
   da página (`"N aulas · M concluídas"`). Se não bater, revisar antes de
   seguir — **conferir também se sobrou algum item com `rotulo` vazio**, sinal
   de que algum `aulaId` só apareceu em links sem texto.
4. **Salvar essa lista no scratchpad antes de baixar a primeira aula** (mesma
   lógica de "fonte única de verdade" usada nas skills do Estratégia — nunca
   reconstruir rótulo de memória durante o loop de download).

## Passo 5: Baixar o PDF de cada aula (o núcleo do processo)

Para cada aula da lista:

1. Navegar para `https://alunoprofbrunobezerra.plataformatutory.com.br/dash/cursos/613765f9-.../playlists/{playlistId}/aulas/{aulaId}`.
   Conferir que o título retornado bate com o esperado; se voltar genérico,
   renavegar uma vez antes de seguir (mesma cautela de falha silenciosa de
   navegação usada nas skills do Estratégia).
2. Extrair o(s) link(s) de material via JavaScript — **mas com espera e
   novas tentativas embutidas na própria chamada, não só um `wait` fixo
   curto**. Confirmado testando "Direito Administrativo": o conteúdo da aula
   às vezes demora **10-15 segundos** pra renderizar (bem mais que os ~2s
   usados nas skills do Estratégia), e nesse intervalo a página mostra só o
   título, sem a seção de Materiais — o que pareceria "aula sem PDF" se
   checado cedo demais:
   ```js
   (async () => {
     let links = [];
     for (let i = 0; i < 6; i++) {
       await new Promise(r => setTimeout(r, 2500));
       links = Array.from(document.querySelectorAll('a[href*="/dash/downloads/"]'))
         .map(a => ({texto: a.getAttribute('aria-label') || a.textContent, href: a.href}));
       if (links.length) break;
     }
     return JSON.stringify(links);
   })();
   ```
   Isso espera até ~15s, checando a cada 2,5s, antes de desistir.
   **Só depois desse loop completo sem achar nada** é que se considera aula
   sem PDF (ex: vídeo de boas-vindas, ou Flashcards que hoje não expõe
   material nessa rota) — pular a aula, sem criar nenhum arquivo. Não é erro.
   - **Se acontecer de várias aulas seguidas voltarem vazias mesmo depois do
     loop completo** (não só uma isolada): pode ser um travamento passageiro
     da SPA da plataforma (observado depois de várias navegações rápidas em
     sequência, com erros React #310/#418 no console) — não são realmente
     aulas sem material. Nesse caso, esperar uns 15-20s parado (sem navegar) e
     tentar de novo a mesma aula antes de marcar como "sem material" de
     verdade.
   - **Usar o `wait` do host (`computer` / esperar entre chamadas), não um
     loop de `setTimeout` dentro do próprio JavaScript, quando a espera for
     longa** — confirmado em 2026-08-18: se o painel do navegador ficar fora
     de foco/visível durante a execução, o próprio Chrome pode limitar
     (throttle) os timers de JavaScript da aba, fazendo um loop de espera em
     JS estourar por timeout sem nunca reconferir de verdade. Preferir
     esperas curtas fora da página (poucos segundos por vez) intercaladas com
     checagens rápidas e diretas no DOM (sem `setTimeout` embutido), repetindo
     esse par (espera curta + checagem) até achar o material ou desistir.
   - **Renavegar a partir da listagem da playlist, não só recarregar a mesma
     URL da aula, se a aula continuar sem "Materiais" depois de várias
     tentativas** — confirmado em 2026-08-18: em pelo menos um caso, recarregar
     a própria URL da aula repetidas vezes não resolveu, mas navegar de novo
     pra URL da playlist (que redireciona pra ela) e esperar resolveu.
   - **Pausa preventiva adaptativa, não um número fixo:** confirmado testando
     "Direito Administrativo" — esse travamento tende a aparecer depois de
     ~8-10 aulas processadas em sequência rápida (navegar aula → navegar
     material → chamar API → próxima aula, sem pausa nenhuma). Ponto de
     partida sugerido: pausa curta (`wait` de ~2-3s) a cada 5-6 aulas
     processadas — mas **ajustar esse ritmo durante a própria execução**
     (confirmado pelo Elvis em 2026-08-18), não é uma regra fixa:
     - Se começar a notar sinais de lentidão (loop de espera do item 2 batendo
       no limite com mais frequência, título da aba demorando mais que o
       normal pra atualizar, `bodyText`/`innerText` vindo raso): **aumentar a
       pausa** e/ou **diminuir o intervalo de aulas entre pausas** (ex: pausar
       a cada 3 aulas em vez de 5-6, ou aumentar a pausa pra 5s).
     - Se a execução estiver fluindo rápida e sem nenhum sinal de lentidão por
       várias aulas seguidas: pode manter o ritmo padrão ou até espaçar mais
       as pausas — não precisa ser conservador à toa quando não há indício de
       problema.
     - Essa recalibração pode acontecer quantas vezes for preciso ao longo do
       download de uma playlist ou do combo completo inteiro — o objetivo é
       reagir ao comportamento real da plataforma naquele momento, não seguir
       um número travado do início ao fim.
3. **Se vier um ou mais links:** pra cada um, seguir a cadeia de redirecionamento
   pra obter a URL assinada real do arquivo:
   - Navegar (`navigate`) pro `href` do material. Isso mostra uma página
     "Seu arquivo está sendo preparado" que redireciona sozinha pra
     `https://pdfs.plataformatutory.com.br/?token={token}&domain={domain}`.
   - **Bug frequente confirmado em 2026-08-18 (aconteceu 2x no mesmo teste,
     não é raro):** às vezes o redirecionamento não acontece sozinho e a
     página fica travada em "Seu arquivo está sendo preparado" — o servidor
     devolveu o `domain` como o texto literal `{domain}` (não substituído)
     dentro do JSON embutido em
     `#__NEXT_DATA__` (`props.pageProps.redirect`), o que quebra o
     redirecionamento automático do lado do cliente. **Se depois de ~5-8s a
     página não tiver saído dessa tela:** extrair o `token` direto desse JSON
     (via `javascript_tool`, lendo
     `JSON.parse(document.getElementById('__next_data__')?.textContent ||
     document.querySelector('#__NEXT_DATA__').textContent).props.pageProps.redirect`
     — o `token` está dentro da query string desse valor) e navegar
     manualmente pra `https://pdfs.plataformatutory.com.br/?token={token}&domain=alunoprofbrunobezerra.plataformatutory.com.br`
     (usando sempre esse domínio fixo, já que o valor vindo do servidor está
     quebrado). Segue o fluxo normal a partir daí.
   - Rodar JavaScript na página resultante pra chamar a API que devolve a URL
     assinada da S3 (**válida por só 5 minutos — baixar em seguida, sem
     demora**):
     ```js
     (async () => {
       const token = new URLSearchParams(location.search).get('token');
       const domain = new URLSearchParams(location.search).get('domain');
       const res = await fetch(`${location.protocol}//${domain}/api/student/pdf?token=${encodeURIComponent(token)}`);
       const json = await res.json();
       return JSON.stringify(json);
     })();
     ```
     (usar `javascript_tool` com `action: "javascript_exec"` — o `await` só
     funciona dentro de uma função async imediatamente invocada, como acima).
   - O `uri` retornado é um link assinado da AWS S3 (`X-Amz-Expires=300`).
     **Se ainda não existir arquivo local com o nome final** (download novo,
     fora do modo atualização): baixar direto pro nome final via
     `curl -sL -o "<pasta>/<rótulo>.pdf" "<uri>"` — não precisa passar por
     arquivo temporário nesse caso, confirmado testando "Direito
     Administrativo". **Se já existir um arquivo com esse nome** (modo
     atualização, Passo 6): baixar pra um arquivo temporário
     (`curl -sL -o "<pasta>/tmp_<aulaId>.pdf" "<uri>"`) pra poder comparar por
     hash antes de decidir se substitui. Em ambos os casos, conferir
     `HTTP:200` e `SIZE` não-trivial no retorno do `curl`.
4. **Nome final do arquivo:** o **rótulo exato da aula**, igual está na barra
   lateral (Passo 4) — **confirmado pelo Elvis em 2026-08-18: sem inventar
   numeração própria, sem adicionar sufixo de data no nome**. Exemplo:
   `R00 - Direito Financeiro (AFO) - Sistema Constitucional de Planejamento e Orçamento.pdf`.
   Se o rótulo já vier com extensão/pontuação estranha, manter como está — é
   pra bater exatamente com o que aparece no site, **inclusive erros de
   digitação do próprio site** (ex: "Lei de Acesso á Informação" — o site usa
   acento agudo em vez de crase, é gramaticalmente errado, mas o nome do
   arquivo replica exatamente assim, sem corrigir a gramática).
   - **Acento/cedilha/caractere especial que dá problema no nome do arquivo:**
     confirmado pelo Elvis em 2026-08-18 — diferente das skills do Estratégia
     (que mantêm acentuação normal), aqui está autorizado a **remover** acento
     ou cedilha (ex: `ç`→`c`, `ã`→`a`) só quando isso realmente ameaçar
     desconfigurar o nome do arquivo. **O traço (`-`) nunca precisa ser
     removido** — não causa esse tipo de problema, manter como está no rótulo
     original.
5. **Download novo:** já baixou direto pro nome final no item 3, nada mais a
   fazer aqui. **Modo atualização:** ver Passo 6 pra comparar o arquivo
   temporário com o existente antes de decidir se substitui.
6. **Verificação de correspondência — obrigatória em todo download, novo ou
   atualização** (confirmado pelo Elvis em 2026-08-18, depois dele perguntar
   como a skill se protege contra baixar/nomear a aula errada): **a validação
   por nome de arquivo do Passo 7 não é suficiente sozinha** — ela só confere
   que existe um arquivo com o nome esperado, não que o *conteúdo* dele é o
   PDF certo. Existe um risco real (raro, mas observado indiretamente pelos
   erros React #310/#418 de estado corrompido na SPA — ver Passo 5, item 2)
   de a página estar mostrando o material de uma aula errada no momento da
   extração do link, o que resultaria num arquivo com o **nome certo mas
   conteúdo errado**. Pra pegar esse caso, depois de cada download (antes de
   dar como concluído):
   - Extrair o texto da **primeira página** do PDF baixado (usar `pypdf`,
     igual já é feito nas skills do Estratégia pra achar a data — aqui é só
     pra conferir o assunto, não precisa de regex de data):
     ```bash
     python -c "
     from pypdf import PdfReader
     import unicodedata, re
     def norm(s):
         s = unicodedata.normalize('NFD', s)
         s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
         return re.sub(r'[^a-z0-9 ]', ' ', s.lower())
     texto = PdfReader(r'<arquivo>.pdf').pages[0].extract_text() or ''
     print(norm(texto)[:600])
     "
     ```
   - Comparar (ignorando acento/caixa) se as palavras significativas do
     **assunto** da aula (a parte do rótulo depois do código `R00 -
     Matéria -`, ex: "Sistema Constitucional de Planejamento e Orçamento")
     aparecem no texto da primeira página. Não precisa bater 100% palavra por
     palavra — o objetivo é pegar um **assunto completamente diferente**
     (sinal de aula errada), não exigir correspondência perfeita de redação.
   - **Bateu:** seguir normalmente.
   - **Não bateu (ou a primeira página não tem texto extraível, ex: PDF
     escaneado):** **não apagar o arquivo nem seguir como se estivesse tudo
     certo** — parar, registrar esse caso específico no relatório final como
     **"verificação de conteúdo falhou"** com o nome do arquivo e o texto
     extraído da primeira página (pra o Elvis comparar visualmente), e seguir
     pras próximas aulas normalmente (não trava o restante do download por
     causa de uma aula suspeita).

## Passo 6: Atualização — comparar por conteúdo, não por data no nome

Essa plataforma **não** mostra, na listagem, qual aula foi atualizada
recentemente (diferente do Estratégia, que tem um selo de "Disponível em
DD/MM/AAAA" pra aula travada) — por isso não dá pra saber de antemão o que
mudou. **O único jeito confiável é baixar de novo e comparar o conteúdo**,
confirmado pelo Elvis em 2026-08-18.

Quando o modo escolhido no Passo 3 for **Atualização**:

1. Baixar o PDF de cada aula normalmente (Passo 5) pra um arquivo temporário,
   mesmo que já exista um arquivo local com esse rótulo.
2. **Se não existir arquivo local com esse nome ainda:** é aula nova (ex.
   matéria ganhou conteúdo desde a última coleta) — renomear o temporário pro
   nome final normalmente.
3. **Se já existir:** comparar o conteúdo dos dois arquivos por hash (evita
   comparação binária ingênua e não depende de nenhuma data no nome do
   arquivo):
   ```bash
   powershell -NoProfile -Command "(Get-FileHash '<arquivo_novo_tmp>').Hash -eq (Get-FileHash '<arquivo_existente>').Hash"
   ```
   - **Hash igual:** apagar o temporário, não mexer no arquivo existente.
   - **Hash diferente:** apagar o arquivo antigo, renomear o temporário pro
     nome final. Registrar essa substituição pra mencionar no resumo final
     (ex: "Administração Financeira e Orçamentária, R03: PDF atualizado").
4. **Aula que tinha PDF baixado antes e agora aparece sem material** (mesmo
   depois do loop de espera completo do Passo 5): **não apagar o arquivo local
   existente** — isso quase certamente é uma falha temporária de carregamento
   da plataforma (ver nota sobre travamento da SPA no Passo 5), não uma
   remoção de conteúdo real pelo professor. Manter o arquivo antigo como está
   e **reportar esse caso no resumo final** como "não confirmado" pra revisão
   manual, em vez de decidir sozinho.
5. Como não existe sinalização de "aula ainda não tem PDF" nessa plataforma,
   não existe conceito de placeholder `.txt` aqui — se uma aula não tiver
   material, ela simplesmente não gera arquivo (Passo 5, item 2), em qualquer
   modo.
6. **Aula que sumiu inteira da playlist (rótulo nem aparece mais na lista do
   Passo 4)** — caso diferente do item 4 acima (que é sobre aula que ainda
   existe na lista mas ficou sem material). Aqui é sobre um arquivo local
   `.pdf` cujo rótulo **não bate com nenhuma aula da lista atual da playlist**
   — sinal de que o professor removeu aquele assunto do curso (confirmado
   pelo Elvis em 2026-08-18: diferente de uma aula que só teve o PDF
   atualizado mantendo o mesmo assunto/rótulo, que é tratado normalmente
   pelos itens 1-3 acima como substituição simples).
   - **Nunca apagar esse arquivo.** Antes de tratar como removido de verdade,
     **confirmar duas vezes** (mesma cautela do item 4 — a lista de aulas
     também pode falhar momentaneamente de carregar completa): reconferir a
     extração do Passo 4 uma segunda vez antes de concluir que o rótulo
     realmente não existe mais na playlist.
   - **Confirmado o sumiço:** mover (não copiar, não apagar) o arquivo local
     pra uma subpasta `Descontinuados` dentro da própria pasta da matéria
     (ex: `Direito Administrativo/Descontinuados/R00 - Direito Administrativo
     - Princípios da Administração.pdf`). Criar a subpasta se ainda não
     existir. O nome do arquivo não muda — mantém o rótulo original, só troca
     de pasta.
   - Registrar cada arquivo movido assim no resumo final (Passo 7), pra o
     Elvis conferir manualmente se o assunto foi realmente descontinuado ou
     só migrou/foi fundido em outra aula com rótulo diferente (algo que a
     skill não tenta inferir sozinha, já que exigiria comparar o conteúdo
     semanticamente).

## Passo 7: Validação final

Depois de processar todas as aulas da playlist:

1. Cruzar a lista de rótulos salva no Passo 4 com os arquivos `.pdf`
   presentes na pasta da matéria (mesma lógica de comparação por nome usada
   nas skills do Estratégia — sem reabrir o conteúdo dos PDFs de novo). **A
   subpasta `Descontinuados` (se existir) fica de fora dessa comparação** —
   os arquivos lá dentro não devem bater com nenhum rótulo da playlist atual,
   isso é esperado.
2. Rótulo sem arquivo correspondente → investigar (aula sem material é
   esperado só se realmente não tiver "Materiais" na página; qualquer outro
   caso merece checagem).
3. **Calcular `(N-M)` (Passo 2) e renomear a pasta** com a data atualizada e o
   indicador de progresso:
   - **M** = total de aulas da playlist (lista salva no Passo 4).
   - **N** = quantas dessas aulas têm hoje, na pasta, um `.pdf` confirmado —
     ou seja, **não** conta as marcadas como "não confirmado" (Passo 6, item
     4), "verificação de conteúdo falhou" (Passo 5, item 6), nem as que foram
     pra `Descontinuados` (Passo 6, item 6), nem aulas genuinamente sem
     material na plataforma (essas nem entram na conta de pendência — não é
     um problema, é assim mesmo).
   - **Se N == M:** pasta fica só `<Matéria> (DD-MM-AAAA)`, sem `(N-M)` —
     sinal de que está tudo certo.
   - **Se N < M:** pasta fica `<Matéria> (N-M) (DD-MM-AAAA)`.
   - **Sempre renomear a pasta existente (`Rename-Item`), nunca apagar e
     recriar** — em download novo a pasta já nasce com o nome final direto,
     sem precisar desse passo de renomear depois.
4. Reportar pro usuário: quantas aulas tinham PDF, quantas foram baixadas/
   atualizadas nessa execução, quantas não tinham material (e por quê, se
   souber), quantas ficaram marcadas como **"não confirmado"** (Passo 6, item
   4 — aula que tinha PDF salvo mas não foi possível reconfirmar o material
   nessa execução) pra revisão manual, quantas ficaram marcadas como
   **"verificação de conteúdo falhou"** (Passo 5, item 6) pra revisão manual,
   e **quantos arquivos foram movidos pra `Descontinuados`** (Passo 6, item
   6), listando o rótulo de cada um pra o Elvis conferir se é descontinuação
   real ou migração pra outro rótulo.

## Passo 8: Planilha de metadados da disciplina (obrigatória, Google Sheets)

**Confirmado pelo Elvis em 2026-08-18: toda matéria baixada ou atualizada por
essa skill tem uma planilha de metadados própria** — mesmo padrão validado nas
skills do Estratégia (`baixar-curso-especifico-estrategia`, Passo 9), adaptado
pra essa plataforma. Serve de histórico rápido (sem reabrir PDF nem
reconsultar o site) e é a base pra checagem de Playlist ID do Passo 3.

1. **Sempre Google Sheets nativo, nunca `.xlsx` local** — mesma preferência
   permanente das outras planilhas desse workspace. Usar `gspread` com as
   credenciais em `credenciais/`. Achar/criar a pasta certa no Drive
   replicando o caminho local por nome, e criar com `gc.create(titulo,
   folder_id=...)`. **Se a autenticação falhar, parar e pedir ao usuário pra
   reautorizar na hora** — nunca cair silenciosamente pro Excel local nem
   pular a planilha.
2. **Nome do arquivo:** `<Nome da Matéria> (Resumos Bezerra) - Metadados` —
   sem sufixo de data (documento único que se atualiza, não recriado a cada
   execução). Salvar dentro da própria pasta da matéria no Drive.
3. **Se já existir uma planilha na pasta** (modo atualização): abrir e **ler
   o Playlist ID registrado antes de sobrescrever qualquer coisa** — é o dado
   que o Passo 3 usa pra checagem.
4. **Aba "Aulas"** — colunas: `Código (Aula)`, `Assunto`, `Status`, `Data de
   Atualização (PDF)`, `Data desta Verificação`, `Palavras-chave batidas`,
   `Total palavras-chave`, `Nº de páginas do PDF`, `Nome do arquivo`.
   - `Status` = `Verificado` (bateu na checagem de conteúdo do Passo 5, item
     6), `Suspeito` (verificação de conteúdo falhou), ou `Não confirmado`
     (Passo 6, item 4) — **cor condicional**: verde pra Verificado, vermelho
     pra Suspeito/Não confirmado.
   - `Data de Atualização (PDF)` vem do **metadado interno do PDF**
     (`/ModDate`, fallback `/CreationDate` via `pypdf`) — não confundir com a
     data no nome da pasta, que é da execução da skill, não do conteúdo em
     si.
   - Título mesclado + subtítulo com pasta, **Playlist ID Bezerra** e nome do
     curso. Linha de resumo com **fórmulas de verdade** (`COUNTA`/`COUNTIF`,
     não valores estáticos digitados) pro total de aulas, confirmadas e
     suspeitas — assim a linha de resumo continua correta se alguém editar
     manualmente uma célula de status depois.
   - **Aulas movidas pra `Descontinuados` (Passo 6, item 6) saem dessa aba**
     — não fazem mais parte da playlist atual. Ver aba "Descontinuados"
     abaixo pra não perder esse histórico.
   - Regravar a aba inteira com o estado atual a cada execução (não precisa
     manter histórico linha a linha de execuções anteriores — a coluna "Data
     desta Verificação" já registra a mais recente).
5. **Aba "Descontinuados"** (só criar se já existir pelo menos um caso) —
   colunas: `Código (Aula)`, `Assunto`, `Data em que foi descontinuada`,
   `Nome do arquivo`. Registrar aqui cada arquivo movido pra subpasta
   `Descontinuados` (Passo 6, item 6), pra manter um histórico visível mesmo
   depois do arquivo sair da aba "Aulas" — sem isso, a informação ficaria só
   no nome da subpasta no Explorer.
6. **Aba "Legenda"** — explicação de cada coluna (das duas abas acima).
7. **Formatação padrão** (preferência salva na memória): alinhamento
   centralizado horizontal e vertical, quebra de texto ativada, largura de
   coluna ajustada ao conteúdo, remover excesso de linhas/colunas deixando
   margem (~2-3 colunas e ~30 linhas depois do fim dos dados reais).
8. **Separador de fórmula `;`, nunca `,`** — locale `pt_BR` desse workspace
   exige `;` como separador de argumento (`=COUNTIF(C7:C24;"Verificado")`);
   vírgula gera `#ERROR!`.
9. **Validar as fórmulas depois de escrever** — ler de volta cada célula de
   fórmula (`value_render_option='FORMATTED_VALUE'`) e confirmar que não é
   `#ERROR!`/`#REF!`/`#NAME?` antes de considerar a planilha pronta.

## Regras gerais

- Só baixar o PDF de resumo esquematizado — não baixar vídeo, nem tentar
  interagir com o "Fórum" da aula, nem seguir os links de "QUESTÕES" (por
  enquanto isso fica de fora — decisão do Elvis em 2026-08-18).
- **Nunca clicar em "Desbloquear" nem navegar pra `pay.plataformatutory.com.br`**
  — são cursos pagos que não pertencem ao Elvis.
- Link assinado da S3 expira em 5 minutos — baixar logo depois de obter o
  `uri`, sem processar várias aulas em paralelo esperando.
- Se o curso tiver muitas aulas na matéria, processar tudo sem pausar pra
  confirmação a cada aula — só reportar progresso periodicamente.
