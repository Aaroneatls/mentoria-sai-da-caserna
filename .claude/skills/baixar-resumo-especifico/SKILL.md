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
  Passo 5.2 — não conta "não confirmado" nem "verificação de conteúdo
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

## Passo 4: Levantar a lista de aulas da playlist (por `fetch`, sem navegar)

**Método principal, confirmado em 2026-08-18 baixando o combo inteiro (336
aulas, ~40 min, zero travamento):** não navegue aula por aula. A partir de
**uma única página aberta** do domínio da plataforma (qualquer URL do
`/dash`), tudo é feito com `fetch` de mesma origem via `javascript_tool`.
Isso elimina de uma vez os problemas que a versão antiga tinha: travamento da
SPA (React #310/#418), espera de 10-15s pro conteúdo renderizar, throttling de
timer quando o painel do navegador está escondido, e o bug do `{domain}`
(nunca se passa pela tela "Seu arquivo está sendo preparado").

Instalar as funções auxiliares uma vez na página (elas se perdem se você
navegar — por isso o método evita navegação):

```js
const C = '613765f9-f1e0-4149-a84f-ebac1314faa1';                  // curso fixo
const ACT = '4026556a4374d30db4fb6a89cdf8dae9bb9015b9a9';          // server action "materiais da aula"

// 1) todas as aulas da playlist (id + rótulo), de uma vez
window.__lessons = async function (pid) {
  const base = '/dash/cursos/' + C + '/playlists/' + pid;
  let r = await fetch(base, {headers: {RSC: '1'}, credentials: 'include'});
  let t = await r.text();
  const m = t.match(/aulas\/([0-9a-f-]{36})/);          // a playlist redireciona pra 1a aula
  if (!m) return null;
  r = await fetch(base + '/aulas/' + m[1], {headers: {RSC: '1'}, credentials: 'include'});
  t = await r.text();
  const i = t.indexOf('"queryKey":["playlist","lessons"');
  if (i < 0) return null;
  const s = t.lastIndexOf('{"dehydratedAt"', i);
  return [...t.slice(s, i).matchAll(/"id":"([0-9a-f-]{36})","title":"((?:[^"\\]|\\.)*)"/g)]
    .map(x => ({id: x[1], titulo: JSON.parse('"' + x[2] + '"')}));
};

// 2) materiais de uma aula (server action, não precisa renderizar a página)
window.__mats = async function (pid, lid) {
  const r = await fetch('/dash/cursos/' + C + '/playlists/' + pid + '/aulas/' + lid, {
    method: 'POST', credentials: 'include',
    headers: {'Accept': 'text/x-component', 'next-action': ACT, 'Content-Type': 'text/plain;charset=UTF-8'},
    body: JSON.stringify([{lessonId: lid}])});
  const t = await r.text();
  const mm = t.match(/^1:(\[.*)$/m);
  try { return JSON.parse(mm[1]); } catch (e) { return []; }
};

// 3) link assinado da S3 do material
window.__sign = async function (matId) {
  const r = await fetch('/dash/downloads/' + matId, {credentials: 'include'});
  const t = await r.text();
  const m = t.match(/token=([A-Za-z0-9%._~-]+)/);
  if (!m) return null;
  const j = await (await fetch('/api/student/pdf?token=' + m[1])).json();
  if (!j.uri) return null;
  const u = new URL(j.uri);
  return {d: u.searchParams.get('X-Amz-Date'), s: u.searchParams.get('X-Amz-Signature')};
};

// 4) TSV pronto de um lote de aulas:  p<TAB>materialId<TAB>X-Amz-Date<TAB>X-Amz-Signature<TAB>rótulo
window.__cache = window.__cache || {};
window.__prep = async function (pid, ini, fim) {
  if (!window.__cache[pid]) window.__cache[pid] = await window.__lessons(pid);
  const ls = window.__cache[pid];
  let out = '#' + ls.length + '\n';
  for (const L of ls.slice(ini, fim)) {
    const pdfs = (await window.__mats(pid, L.id)).filter(m => m.isPdf);
    if (!pdfs.length) { out += '-\t\t\t\t' + L.titulo + '\n'; continue; }
    for (const mt of pdfs) {
      const mid = mt.downloadUrl.split('/').pop();
      const sg = await window.__sign(mid);
      out += sg ? ('p\t' + mid + '\t' + sg.d + '\t' + sg.s + '\t' + L.titulo + '\n')
                : ('-\t\t\t\t' + L.titulo + '\n');
    }
  }
  return out;
};
```

Cuidados desse passo:

1. **Nada de `await` solto** na chamada do `javascript_tool` — envolver numa
   função async imediatamente invocada: `(async()=>await window.__prep(...))()`.
2. **Lotes de 11 a 14 aulas por chamada.** O `javascript_tool` corta em 30s;
   com ~1,5s por aula, 5 playlists numa tirada só estoura (aconteceu em
   2026-08-18). Playlist grande = 2-3 chamadas.
3. **Nunca usar `setTimeout` dentro do JS pra pausar** — com o painel do
   navegador escondido o Chrome faz throttling do timer e a chamada estoura o
   limite sem fazer nada. Não é preciso pausa nenhuma nesse método.
4. Conferir o `#N` da primeira linha (total de aulas da playlist) com o número
   que aparece no card do curso. **Rótulo vazio não acontece mais** nesse
   método (o título vem do JSON, não do texto de um link).
5. **Salvar o TSV no scratchpad antes de baixar** — segue valendo a regra de
   fonte única de verdade; nunca reconstruir rótulo de memória.

## Passo 5: Baixar o PDF de cada aula

O `uri` assinado da S3 **vale 5 minutos** — baixe o lote logo depois do
`__prep`. Montar a URL a partir dos 3 campos do TSV (o resto do link é fixo):

```
https://tutory-membros.s3.us-east-1.amazonaws.com/student-pdfs/{materialId}-{email-urlencoded}
  ?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD
  &X-Amz-Credential=AKIAW6QESTNCR46ISSX5%2F{AAAAMMDD}%2Fus-east-1%2Fs3%2Faws4_request
  &X-Amz-Date={X-Amz-Date}&X-Amz-Expires=300&X-Amz-Signature={X-Amz-Signature}
  &X-Amz-SignedHeaders=host&x-id=GetObject
```

Baixar com `curl -sL -o "<pasta>/<nome final>.pdf" "<url>"`, conferindo
`HTTP:200` e tamanho não-trivial. Em modo atualização (Passo 6), baixar antes
pra um `tmp_<materialId>.pdf` pra poder comparar por hash.

- **É o PDF licenciado que interessa** (`student-pdfs/...`, com o rodapé
  "Licenciado para <nome>, e-mail..."). Existe também uma cópia sem marca em
  `tutory-membros.s3.amazonaws.com/12295/materiais/aulas/{aulaId}` (a que o
  visualizador usa, aberta, sem token) — **não usar**: mudaria o conteúdo do
  arquivo e quebraria a comparação por hash das atualizações futuras.
- **Aula sem material** (`-` no TSV) não gera arquivo e não é erro. Nessa
  plataforma existem aulas de aviso/cronograma e a de Flashcards, que não
  expõem PDF. Não existe placeholder `.txt` aqui.
- Se um lote inteiro voltar sem material, desconfie de sessão derrubada
  (login simultâneo) antes de concluir que as aulas não têm PDF.

### Passo 5.1: Nome do arquivo — o que vale é o nome impresso no PDF

**Regra confirmada pelo Elvis em 2026-08-18:** o rótulo da aula na plataforma
é só o ponto de partida. **Sempre conferir o rótulo contra o título impresso
no próprio PDF (capa da 1ª página e 1º tópico do Sumário). Havendo
divergência, vale o nome que está dentro do PDF.**

1. Extrair o texto da 1ª página (`pypdf`) e descartar as linhas de rodapé
   (`www.profbrunobezerra.com.br`, `Licenciado para...`, `Direitos Autorais
   reservados...`) e as linhas iniciais que são só o nome da matéria (a capa
   costuma vir como `DIREITO / CIVIL / <assunto>`).
2. O que sobra é o **título do PDF**. Comparar (ignorando acento e caixa) com
   o assunto do rótulo da plataforma:
   - **Bate:** usar o rótulo da plataforma, como já era feito.
   - **Diverge:** montar o nome final como
     `<código> - <matéria> - <título do PDF>`, mantendo o código (R00, R01...)
     e o nome da matéria do rótulo, e trocando **só o assunto**.
   - **Capa que lista vários assuntos em vez de um título** (mais de 4 linhas
     úteis ou mais de ~90 caracteres — ex: `R04 - Contabilidade Pública -
     Demonstrações Contábeis`, cuja capa lista Balanço Financeiro, Balanço
     Orçamentário, DVP etc): **manter o rótulo da plataforma**, que nesse caso
     é o guarda-chuva correto, e registrar a observação na planilha.
3. A capa vem em CAIXA ALTA — converter pra caixa de título: preposições e
   conjunções em minúscula (`de, da, do, das, dos, e, em, na, no, a, o, ao,
   às, para, por, com, ou`) e **siglas preservadas** (`LINDB, DVP, DFC, DMPL,
   PCASP, MCASP, IBS, CBS, IPI, IRPF, IRPJ, IRRF, ICMS, ITCMD, LGPD, CPC,
   SQL...`, além de qualquer palavra sem vogal).
4. **Registrar o rótulo antigo**: quando o nome vier do PDF, guardar o rótulo
   original da plataforma na coluna `Rótulo na plataforma (quando diferente)`
   da planilha (Passo 8) — é o que permite achar a aula no site depois.
5. Fora isso valem as regras de sempre: **sem numeração inventada, sem sufixo
   de data**, espaço sobrando no começo/fim do rótulo é aparado, caracteres
   proibidos no Windows (`\ / : * ? " < > |`) trocados (`:` vira ` -`), e
   acentuação/traço mantidos como estão.

### Passo 5.2: Verificação de conteúdo (obrigatória em todo download)

Depois de cada download, antes de dar a aula como concluída: normalizar
(sem acento, minúsculo) as palavras com mais de 3 letras do assunto e conferir
quantas aparecem no texto da 1ª página + Sumário. Metade ou mais = 
**Verificado**. Abaixo disso = **Suspeito**.

- Na prática, **"Suspeito" quase sempre significa que o rótulo da plataforma
  não bate com o PDF** — que é exatamente o caso tratado no Passo 5.1. Rodar
  o Passo 5.1 primeiro e revalidar: se o nome passou a vir do PDF, a aula
  volta pra Verificado sozinha.
- Sobrando Suspeito depois disso (ou 1ª página sem texto extraível, ex: PDF
  escaneado): **não apagar o arquivo**, registrar no relatório final com o
  nome do arquivo e o texto lido da primeira página, e seguir para as demais
  aulas.

### Passo 5.3: Sumário da aula

Extrair a lista de tópicos do "Sumário" (procurar nas 4 primeiras páginas a
página que contenha a palavra "Sumário"; limpar o pontilhado + número de
página no fim de cada linha e as linhas de rodapé). Serve de referência
legível do que a aula cobre, alimenta a comparação de versões do Passo 6 e vai
pra planilha do Passo 8. Não achou Sumário: seguir com lista vazia e registrar
como observação, não como erro.

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
     **Antes de apagar o arquivo antigo**, extrair o Sumário dele (Passo 5,
     item 7) e comparar com o Sumário do arquivo novo — a diferença entre as
     duas listas de tópicos (o que saiu, o que entrou) vai no resumo final
     junto com o aviso de atualização, ex: "R03: PDF atualizado — tópico
     'Jurisprudência aplicada' foi removido, tópico 'Novo entendimento do STJ'
     foi adicionado". Isso dá visibilidade de **o que mudou de verdade**, não
     só "mudou". Se o Sumário for idêntico mesmo com hash diferente (ex: só
     mudou formatação/diagramação, sem alterar conteúdo), mencionar isso
     também (ex: "R03: PDF atualizado, mas o Sumário não mudou — provável
     ajuste visual").
4. **Aula que tinha PDF baixado antes e agora aparece sem material** (mesmo
   depois do loop de espera completo do Passo 5): **não apagar o arquivo local
   existente** — isso quase certamente é uma falha temporária de carregamento
   da plataforma (ver Passo 5), não uma
   remoção de conteúdo real pelo professor. Manter o arquivo antigo como está
   e **reportar esse caso no resumo final** como "não confirmado" pra revisão
   manual, em vez de decidir sozinho.
5. Como não existe sinalização de "aula ainda não tem PDF" nessa plataforma,
   não existe conceito de placeholder `.txt` aqui — se uma aula não tiver
   material, ela simplesmente não gera arquivo (Passo 5), em qualquer
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
     4), "verificação de conteúdo falhou" (Passo 5.2), nem as que foram
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
   **"verificação de conteúdo falhou"** (Passo 5.2) pra revisão manual,
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
   `Total palavras-chave`, `Nº de páginas do PDF`, `Nome do arquivo`,
   `Tópicos do Sumário`, `Rótulo na plataforma (quando diferente)`,
   `Observação`.
   - `Tópicos do Sumário` = lista de tópicos extraída do Passo 5.3,
     unida com `" | "`. Serve de referência legível pra saber o que aquela
     aula cobre sem abrir o PDF, e é usada no Passo 6 pra comparar versões
     numa atualização (o que mudou de verdade, não só "mudou").
   - `Rótulo na plataforma (quando diferente)` só é preenchida quando o nome
     do arquivo veio da capa do PDF em vez do rótulo do site (Passo 5.1) —
     guarda o rótulo antigo pra localizar a aula na plataforma depois.
     `Observação` guarda a nota da skill sobre aquela aula (ex: "nome vindo da
     capa do PDF", "capa lista vários assuntos, mantido o rótulo do site").
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

## Passo 9: Sugestão de melhoria da skill (obrigatória ao final de toda execução)

**Confirmado pelo Elvis em 2026-08-18:** sempre que essa skill terminar de
processar um pacote de download (matéria nova ou atualização), depois do
relatório final (Passo 7), avaliar se algo aprendido nessa execução sugere um
ajuste na própria skill — bug novo encontrado, comportamento inesperado da
plataforma, passo que ficou lento/repetitivo, oportunidade de deixar algo mais
robusto. Isso é o mesmo tipo de aprendizado que já gerou boa parte dos passos
atuais (bug do `{domain}`, throttling de aba em segundo plano, extração de
rótulo vazio etc.) — a ideia é continuar capturando isso a cada execução, não
só quando o Elvis perguntar.

- **Se identificar algo:** apresentar a sugestão ao Elvis de forma objetiva
  (o que aconteceu, o que mudaria na skill), perguntar se aprova, e **só
  então** editar o `SKILL.md` (dessa skill e/ou da `baixar-resumo-combo-completo`,
  se for aplicável às duas) e rodar `/syncar` pra sincronizar com o GitHub.
- **Se nada de novo surgiu** nessa execução (tudo correu dentro do que já
  está documentado): dizer isso explicitamente e curto — não inventar
  sugestão só pra ter o que falar.
- Nunca editar a skill nem sincronizar sem essa aprovação — a sugestão é
  sempre apresentada primeiro.
