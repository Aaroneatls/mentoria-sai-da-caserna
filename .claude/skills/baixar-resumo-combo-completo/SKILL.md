---
name: baixar-resumo-combo-completo
description: >
  Baixa em lote os resumos esquematizados (PDF) de TODAS as matérias do curso
  "Resumos Esquematizados - Combo Completo | Parceria" do professor Bruno
  Bezerra (plataforma Tutory), organizando cada matéria numa pasta própria e os
  flashcards numa pasta separada. Pula automaticamente o Boas-vindas, o
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
   na tela**, não precisa clicar em "Ver mais"/"Mostrar menos":
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

**Caso especial — Flashcards:** a playlist `Flashcards - Parceria` vai pra uma
pasta própria, separada das matérias: `Flashcards (DD-MM-AAAA)` (mesma regra
de `(N-M)` acima; dentro da pasta raiz definida no Passo 0, mesmo nível das
pastas de matéria — confirmado pelo Elvis em 2026-08-18).

Não sintetizar nem abreviar os nomes de matéria aqui — são curtos.

## Passo 4: Baixar cada matéria (reaproveitar a mecânica da skill de matéria específica)

Pra cada playlist da lista do Passo 1 (exceto as três excluídas no Passo 2),
repetir exatamente a mecânica dos **Passos 3 a 7 da skill
`baixar-resumo-especifico`**:

1. Procurar pasta existente pra essa matéria dentro da pasta raiz (detecção
   automática — comparação ignorando maiúsculas, acentuação, **e os sufixos
   `(N-M)` e `(DD-MM-AAAA)`** — mudam a cada execução, não fazem parte da
   identidade da pasta). **Se achar pasta com planilha de metadados
   (Passo 6), conferir o Playlist ID registrado nela contra o `playlistId`
   atual dessa matéria antes de tratar como atualização** — mesma checagem
   (com o mesmo aviso ao Elvis se for diferente) do Passo 3, item 2 da skill
   `baixar-resumo-especifico`. Fazer essa checagem matéria por matéria, não
   só uma vez pro combo inteiro.
2. Levantar a lista de aulas da playlist (extração da barra lateral,
   deduplicada por `aulaId`).
3. Baixar o PDF de cada aula:
   - Extrair o link de material (`a[href*="/dash/downloads/"]`) — se não tiver,
     pular a aula sem criar arquivo.
   - Navegar pro link, capturar `token`/`domain` da URL resultante
     (`pdfs.plataformatutory.com.br/?token=...&domain=...`), chamar
     `{domain}/api/student/pdf?token=...` via `javascript_tool` (função async
     imediatamente invocada) pra obter o `uri` assinado da S3 (**válido só 5
     minutos** — baixar em seguida). Cuidado com o bug do `{domain}` não
     substituído (Passo 5, item 3 da skill irmã).
   - `curl -sL -o "<pasta>/tmp_<aulaId>.pdf" "<uri>"`, conferir `HTTP:200`.
   - Nome final = **rótulo exato da aula**, sem numeração inventada nem sufixo
     de data. Remover acento/cedilha/caractere especial só se ameaçar
     desconfigurar o nome do arquivo (traço nunca precisa ser removido).
   - **Verificação de conteúdo obrigatória** (Passo 5, item 6 da skill irmã):
     conferir se o assunto da primeira página do PDF bate com o rótulo
     esperado, antes de aceitar o download como certo — pega o caso raro de
     baixar a aula errada por causa de estado corrompido na SPA.
4. Modo atualização (se a pasta da matéria já existir e o usuário confirmar
   atualização — perguntar por matéria encontrada, ou perguntar uma vez só no
   início "atualizar todas as matérias que já existem?"): baixar de novo,
   comparar por hash (`Get-FileHash`) com o arquivo local existente — hash
   igual descarta o novo, hash diferente substitui e registra a mudança.
5. Não existe placeholder `.txt` nessa plataforma — aula sem material
   simplesmente não gera arquivo, em qualquer modo.
6. **Aula que sumiu inteira da playlist daquela matéria** (rótulo de um
   arquivo local não bate com nenhuma aula da lista atual): **nunca apagar**
   — confirmado dobrando a checagem (Passo 6, item 6 da skill irmã), mover o
   arquivo pra uma subpasta `Descontinuados` dentro da própria pasta daquela
   matéria (ex: `Direito Administrativo/Descontinuados/...pdf`), mantendo o
   nome original. Registrar cada um no relatório final (Passo 5) pra revisão
   manual do Elvis — a skill não decide sozinha se foi descontinuação real ou
   migração pra outro rótulo.
7. **Pausa preventiva entre aulas, adaptativa (não um número fixo):** o
   travamento passageiro da SPA (Passo 5, item 2 da skill irmã) fica mais
   provável ainda aqui, com centenas de aulas no total. Ponto de partida:
   pausa de ~2-3s a cada 5-6 aulas. **Ajustar esse ritmo ao longo de toda a
   execução do combo** (entre aulas de uma mesma matéria e entre matérias
   diferentes) sempre que perceber sinais de lentidão — aumentar a pausa e/ou
   diminuir o intervalo entre pausas; relaxar de novo se a plataforma voltar a
   responder rápido. Confirmado pelo Elvis em 2026-08-18.

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
   - Confirmar que os Flashcards foram tratados à parte, na pasta `Flashcards`.
   - Confirmar quantas planilhas de metadados foram criadas/atualizadas
     (Passo 6).

## Passo 6: Planilha de metadados de cada disciplina (obrigatória, Google Sheets)

**Confirmado pelo Elvis em 2026-08-18: toda matéria processada nessa execução
ganha uma planilha de metadados própria, na mesma pasta dela** — mesmo
processo e mesmo formato validado na skill `baixar-resumo-especifico` (ver
Passo 8 dela: Google Sheets nativo via `gspread`, nunca `.xlsx` local; abas
"Aulas" + "Descontinuados" (se aplicável) + "Legenda"; Playlist ID no
subtítulo; fórmulas com `;`; formatação padrão; ler de volta pra conferir que
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
