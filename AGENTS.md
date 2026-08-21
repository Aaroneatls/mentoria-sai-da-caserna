# Mentoria Sai da Caserna — Claude Code OS

## O que é esse workspace
Workspace principal da Mentoria Sai da Caserna. Aqui Elvis organiza planos de estudo, conteúdo de marketing, prospecção de clientes e a operação financeira do negócio.

**Estrutura de pastas:**
- `_contexto/` — memória do sistema (não apagar)
- `planos-de-estudo/` — materiais fonte (Estratégia Concursos, TecConcursos) e planos de estudo pré/pós edital
- `marketing/` — conteúdo pro Instagram (@mentoria.elvis.aaron), e futuramente YouTube
- `financeiro/` — controle financeiro do negócio
- `dados/` — arquivos brutos pra análise (PDFs de edital, planilhas de origem)
- `tarefas.md` — lista de tarefas corrente
- `templates/skills/` — templates de skills prontos pra personalizar com /mapear
- `templates/ferramentas/catalogo.md` — APIs e ferramentas disponíveis pra usar em skills

## Sobre o negócio
Elvis Aaron é mentor para concursos públicos, focado em ajudar militares a se tornarem Auditores (Fiscal/Controle). Monta planos de estudo pré e pós edital com base em material da Estratégia Concursos e TecConcursos, entregues via plataforma Tutory. Trabalha solo, com parcerias de plataforma e conteúdo (BTG, Estratégia Concursos, TecConcursos, Tutory, Você Concursado, Rabelo Concursos).

## O que mais fazemos aqui
- Montar planos de estudo pré e pós edital
- Elaborar cadernos de questões na plataforma TecConcursos
- Produzir conteúdo pro Instagram (prospecção de clientes)
- Organizar dados de editais em planilhas
- Cuidar da parte financeira do negócio

## Clientes e contexto
Negócio próprio, sem personalização individual por cliente — os planos de estudo são elaborados por Elvis e distribuídos em escala via plataforma Tutory.

## Tom de voz
Informal, com gírias do universo militar/concurseiro (ex: "bizu", "bizurado"). Nunca usar travessão. Evitar marcas de escrita "de IA" (contraposições genéricas, "mergulhar de cabeça", etc). O texto deve soar natural, como escrito por uma pessoa.

## Ferramentas conectadas
- Google Drive — acesso direto por sistema de arquivos (workspace já vive dentro da pasta sincronizada do Drive)
- Google Sheets — conectado via `gspread` com OAuth (Python). Credenciais em `credenciais/` (nunca commitar). Client: `credenciais/google-oauth-client.json`, token de sessão: `credenciais/google-oauth-token.json`
- Claude in Chrome (extensão) — acessa o navegador Chrome real do usuário, já logado nas plataformas (Estratégia Concursos, TecConcursos, Tutory). **Navegador embutido (Claude Browser) é o padrão para QUALQUER pedido de abrir link, site ou plataforma — dentro ou fora de skill — reaproveitando a janela/aba já aberta; só usar o Chrome real com autorização prévia do usuário na conversa, pedida a cada vez** (confirmado 2026-08-18, generalizado em 2026-08-19).
- Estratégia Concursos — **limite de 3 produtos matriculados por vez**. Curso/pacote não matriculado não abre: em `/app/dashboard/assinaturas`, clicar `DESMATRICULAR` no que vai sair e digitar `CORUJA`, depois buscar o produto desejado na aba PACOTES, clicar `MATRICULAR` e digitar `CORUJA` de novo, e recarregar. **A palavra `CORUJA` vale nos dois sentidos, matrícula e desmatrícula.** É reversível, e **qualquer pacote pode entrar ou sair do rodízio** — inclusive o da PRF — quando a tarefa pedida pelo Elvis exigir.

  **Rodízio é livre, não precisa pedir autorização** (Elvis, 2026-08-20). A única checagem obrigatória antes de matricular ou desmatricular é: **alguma sessão em andamento está usando, baixando ou acessando aquele produto?** Se não estiver, desmatricular e matricular à vontade pra executar a tarefa. Não é mais necessário conferir placeholder `.txt` nem avisar antes — placeholder só interessa se o que vai sair estiver em uso naquele momento.

  **Onde procurar cada coisa no catálogo** (corrigido 2026-08-20):
  - **Pacote completo de um concurso** → aba **PACOTES**. É o que o Elvis chama de "curso".
  - **Material granular** (Bizu Estratégico, Passo Estratégico, Monitoria, Trilha, Discursiva) → aba **CURSOS**. Esses **não aparecem** na aba PACOTES, e buscar por eles ali devolve zero, o que engana.
  - A aba **não troca com clique por coordenada** — usar `element.click()` no `<button>` e conferir a classe `Tab isActive`. A busca é **fuzzy (OR)**: contagem alta não significa acerto. Ver `reference_estrategia_busca_catalogo_abas` na memória.
  - Dentro de um pacote já matriculado, `GET /api/aluno/pacote/{id}` traz `tipo_curso_id`: 1=Regular, 3=Monitoria, 5=Trilha, 7=Passo Estratégico, 27=Bizu Estratégico, 30=Rodadas Avançadas de Simulados.
- Pasta padrão de downloads do Estratégia Concursos: `G:\Meu Drive\Inteligência Artificial\Estrategia` (usada pelas skills `baixar-curso-especifico-estrategia` e `baixar-curso-completo-estrategia`).
- Plataforma dos Resumos Esquematizados do professor Bruno Bezerra (Tutory): login em `https://alunoprofbrunobezerra.plataformatutory.com.br/dash`. Pasta padrão de downloads: `G:\Meu Drive\Inteligência Artificial\Resumos Esquematizados` (usada pelas skills `baixar-resumo-especifico` e `baixar-resumo-combo-completo`). **Organização da pasta** (a partir do download do combo completo em 18/08/2026): uma subpasta por matéria, nomeada `<Matéria> (DD-MM-AAAA)` — ganha `(N-M)` antes da data só quando sobrou pendência; dentro dela os PDFs (nome = título impresso na capa do PDF) e uma planilha Google Sheets `<Matéria> (Resumos Bezerra) - Metadados`. Hoje são 29 matérias / 332 PDFs. Os Flashcards não têm PDF na plataforma (a aula aponta pra uma pasta pública do Drive com baralhos do Anki), então não têm pasta própria.
*(atualizar conforme MCPs forem instalados)*

---

## Como este workspace é organizado (Claude Code e Codex)

- **Instruções:** `AGENTS.md` é a fonte (este arquivo). `CLAUDE.md` tem só `@AGENTS.md`. Nunca escrever conteúdo no `CLAUDE.md`.
- **Skills:** em `.claude/skills/<nome>/SKILL.md`. Pro Codex enxergar, existe `.agents/skills` apontando pra `.claude/skills` (criado pelo `/setup`, não vai pro git). No Windows a ponte é cópia: skill nova precisa de `/atualizar` pra re-sincronizar.

---

## Contexto do negócio

No início de toda conversa, ler os seguintes arquivos (se existirem e estiverem configurados):

1. `_contexto/empresa.md` — quem é o usuário, o que faz, como funciona o negócio
2. `_contexto/preferencias.md` — tom de voz, estilo de escrita, o que evitar
3. `_contexto/estrategia.md` — foco atual, prioridades, o que pode esperar
4. `_contexto/agora.md` — contexto vivo: onde paramos, decisões recentes, pendências (atualizado a cada sessão)

Usar essas informações como base pra qualquer resposta ou decisão. Ao sugerir prioridades, formatos ou abordagens, considerar o foco atual descrito em `estrategia.md`.

Para qualquer tarefa visual (carrossel, proposta, slide, landing page), consultar `marca/design-guide.md` como referência de estilo.

Não é necessário listar o que foi lido nem confirmar a leitura. Apenas usar o contexto naturalmente.

---

## Fluxo de trabalho

Antes de executar qualquer tarefa, verificar se existe uma skill relevante em `.claude/skills/` (Claude Code) ou `.agents/skills/` (Codex).
Se encontrar, seguir as instruções da skill.
Se não encontrar, executar a tarefa normalmente.

Ao concluir uma tarefa que não tinha skill mas parece repetível (o usuário provavelmente vai pedir de novo no futuro), perguntar:

> "Isso pode virar uma skill pra próxima vez. Quer que eu crie?"

Não perguntar pra tarefas pontuais ou perguntas simples. Só quando o padrão de repetição for claro.

---

## Aprender com correções

Quando o usuário corrigir algo, melhorar uma resposta ou dar uma instrução que parece permanente (frases como "na verdade é assim", "não faça mais isso", "prefiro assim", "sempre que...", "evita...", "da próxima vez..."), perguntar:

> "Quer que eu salve isso pra não precisar repetir?"

Se sim, identificar onde faz mais sentido salvar:

- **Sobre o negócio** (quem são os clientes, como funciona a empresa, serviços, mercado) → adicionar em `_contexto/empresa.md`
- **Sobre preferências e estilo** (tom de voz, formato de resposta, o que evitar, como estruturar textos) → adicionar em `_contexto/preferencias.md`
- **Sobre prioridades e foco atual** (projetos em andamento, metas do momento, prazos importantes, o que é prioridade agora) → adicionar em `_contexto/estrategia.md`
- **Regra de comportamento nessa pasta** (onde salvar arquivos, como nomear, fluxos específicos) → adicionar no próprio `AGENTS.md`

Salvar com uma linha nova clara, sem reformatar o arquivo inteiro. Confirmar o que foi salvo mostrando a linha adicionada.

---

## Checklist de encerramento de sessão

**Sempre que o Elvis perguntar se pode encerrar a sessão** (ou disser "posso
fechar?", "tem mais alguma coisa?", "está tudo certo?"), rodar esta verificação
**antes** de responder — e já corrigir o que estiver fora do lugar, não só
reportar. Confirmado pelo Elvis em 2026-08-18.

1. **Git** — `git status --short` limpo, e comparar `HEAD` com `origin/main`
   (`git log origin/main..HEAD --oneline`) pra garantir que não ficou commit
   sem push. Working tree limpo não significa sincronizado.
2. **Ponte do Codex (`.agents/skills`)** — no Windows ela é **cópia**, não link:
   toda skill editada em `.claude/skills/` fica desatualizada lá até ser
   recopiada, e o Codex passa a ler uma versão antiga. Comparar arquivo a
   arquivo e **ressincronizar** se divergir:
   ```bash
   for d in .claude/skills/*/; do n=$(basename "$d"); mkdir -p ".agents/skills/$n"; cp -r "$d." ".agents/skills/$n/"; done
   ```
   Essa pasta é ignorada pelo git de propósito — ressincronizar não gera
   mudança no repositório.
3. **Entregável da sessão** — se a tarefa mexeu em arquivos (downloads,
   planilhas, pastas), conferir a integridade do resultado, não só que "rodou":
   contagem de arquivos, formato real (ver a regra de download logo abaixo),
   nomes/datas no padrão, e nenhum `.tmp` órfão.
4. **Processos e watchers em segundo plano** — não basta olhar os scripts de
   trabalho (worker/runner/python). **Os `Monitor` e os comandos de espera que
   eu mesmo armei também contam**: `tail -f` e laços `until ... do sleep`
   nunca terminam sozinhos e continuam aparecendo como "tarefa em execução"
   pro Elvis, mesmo com o trabalho já concluído. Parar cada um com `TaskStop`
   (guardar os ids dos monitores criados na sessão) e depois confirmar que não
   sobrou nada — **ignorando os processos do próprio comando de verificação**,
   que casam com o filtro e geram falso positivo. Se aparecer processo de outra
   sessão, apenas mencionar, não matar.
5. **Pendências** — listar o que ficou em aberto e o que depende do Elvis,
   separando o que é bloqueante do que não é.

6. **Memória portátil** — copiar `~/.claude/projects/<projeto>/memory/*.md` para
   `_contexto/memoria/`. A memória do Claude fica **fora do repositório**, então quem
   abrir o projeto no ChatGPT, no Codex ou numa máquina nova não a enxerga. Sem essa
   cópia, o aprendizado se perde numa reinstalação. Fazer **antes** do commit final,
   para o conteúdo entrar no push.

---

## Tudo que a gente produz tem de ser portátil

O Elvis pode abrir este projeto em outro assistente, em especial o ChatGPT. Então **decisão,
regra ou aprendizado que só existe dentro do Claude não existe**.

| Onde escrever | O que vai |
|---|---|
| `bases/DECISOES.md` | decisões fechadas com o Elvis |
| `bases/<n>/APRENDIZADO.md` | lição aprendida trabalhando naquela base |
| `bases/05-questoes-tec/REGRAS.md` | regras de acesso ao TecConcursos |
| `_contexto/tarefas-mapeamento.md` | lista viva de tarefas e decisões pendentes |
| `_contexto/memoria/` | cópia portátil da memória do Claude |
| `AGENTS.md` | regra de comportamento permanente do workspace |

A memória do Claude continua sendo a cópia de trabalho, pela velocidade de recall. Mas **a fonte
de verdade é o repositório**, porque é o que qualquer assistente consegue ler.

---

## Regra geral: nunca sobrescrever arquivo bom com download não validado

Vale pra **qualquer** skill que baixe arquivo em massa, em qualquer plataforma —
inclusive skills novas criadas no futuro. Confirmado em 2026-08-18, depois de um
caso real em que 27 PDFs bons foram apagados e substituídos por lixo.

O erro: o servidor respondeu **HTTP 200 devolvendo uma página HTML** (~238 KB) no
lugar do PDF, e a skill validava o download só por "HTTP 200 + tamanho não-trivial".
Página de erro, tela de login expirado, sessão derrubada ou bloqueio por volume
costumam vir assim — com status 200 e corpo grande.

Portanto, em toda skill de download:

1. Baixar **sempre** pra um arquivo temporário, nunca direto pro nome final.
2. Validar o **tipo real** do arquivo, não só o tamanho: PDF tem que começar com
   os bytes `%PDF-` e abrir no `pypdf` com número de páginas > 0. Se o conteúdo
   começa com `<`, é HTML — descartar e repetir.
3. **Só apagar ou substituir o arquivo antigo depois que a validação passar.**
   Enquanto não passar, o que já estava na pasta fica intocado.
4. Mandar `User-Agent` de browser (e `Referer` do domínio) nas requisições —
   várias plataformas recusam o User-Agent padrão de `curl`/`python-requests`.
5. Se um lote inteiro for recusado, **parar e avisar o usuário** em vez de
   insistir em laço: costuma ser sessão derrubada ou limite da conta.

**Ao automatizar por fora da skill** (montar script próprio pra dar conta do
volume, em vez de seguir os passos um a um), portar **todas** as travas da skill
pro script — não só as que vierem à cabeça na hora. Foi assim que o caso acima
aconteceu.

---

## Sugestão de melhoria ao final de execução (skills de download em massa e de cadernos de questões)

Toda skill relacionada a **download de materiais em massa** (ex: `baixar-curso-especifico-estrategia`, `baixar-curso-completo-estrategia`, `baixar-resumo-especifico`, `baixar-resumo-combo-completo`) ou a **elaboração de cadernos de questões** (ex: futura skill de cadernos no TecConcursos) precisa terminar toda execução com um passo de "sugestão de melhoria":

1. Depois do relatório final da execução, avaliar se algo aprendido nessa rodada (bug novo, comportamento inesperado da plataforma, passo lento/repetitivo, oportunidade de deixar algo mais robusto) sugere um ajuste na própria skill.
2. **Se identificar algo:** apresentar a sugestão de forma objetiva (o que aconteceu, o que mudaria), perguntar se o usuário aprova, e só então editar o `SKILL.md` e rodar `/syncar` pra sincronizar com o GitHub.
3. **Se nada de novo surgiu:** avisar isso de forma curta e objetiva — não inventar sugestão só pra ter o que falar.
4. Nunca editar a skill nem sincronizar sem aprovação prévia do usuário.

Isso vale por padrão pra qualquer skill nova criada dentro desses dois critérios — incluir esse passo já na criação, sem precisar que o usuário peça de novo.

Não perguntar se a correção for óbvia de contexto imediato (ex: "na verdade o arquivo se chama X"). Só perguntar quando a informação tiver valor duradouro.

---

## Manter contexto atualizado

Ao terminar uma tarefa que mudou algo relevante no projeto (novo cliente, nova skill, mudança de foco, novo processo, ferramenta instalada, estrutura de pastas alterada), perguntar:

> "Isso mudou algo no teu contexto. Quer que eu atualize os arquivos de memória?"

Se sim, identificar o que precisa atualizar:

- **Novo cliente, serviço, ferramenta, equipe** → `_contexto/empresa.md`
- **Mudança de prioridade ou foco** → `_contexto/estrategia.md`
- **Correção de tom ou estilo** → `_contexto/preferencias.md`
- **Nova pasta, regra de organização, skill criada** → `AGENTS.md`
- **Mudança visual (cores, fontes, logo)** → `marca/design-guide.md`

Mostrar o que vai mudar antes de salvar. Não reformatar o arquivo inteiro, só adicionar ou editar a linha relevante.

**Quando NÃO perguntar:**
- Tarefas pontuais que não mudam o contexto (ex: escrever um email, criar um post avulso)
- Perguntas simples ou conversas sem ação
- Mudanças que já foram salvas pelo bloco "Aprender com correções"

**Dica:** se o usuário não sabe se algo mudou, rodar `/atualizar` faz uma varredura completa.

---

## Criação de skills

Quando o usuário pedir pra criar uma nova skill:

1. Verificar se existe um template relevante em `templates/skills/`. Se existir, usar como base e adaptar pro contexto do usuário
2. Perguntar: "Essa skill é específica pra esse projeto ou vai ser útil em qualquer projeto?"
   - Específica desse negócio → salvar em `.claude/skills/nome-da-skill/SKILL.md` (local)
   - Útil em qualquer projeto → salvar em `~/.claude/skills/nome-da-skill/SKILL.md` (global)
3. Ler `_contexto/empresa.md` e `_contexto/preferencias.md` pra calibrar o conteúdo da skill ao contexto do negócio
4. Se a skill precisar de arquivos de apoio (templates, referências, exemplos), criar dentro da pasta da skill
5. Seguir o fluxo da skill-creator nativa do Claude Code
