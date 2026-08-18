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
Elvis Aaron é mentor para concursos públicos, focado em ajudar militares a se tornarem Auditores (Fiscal/Controle). Monta planos de estudo pré e pós edital com base em material da Estratégia Concursos e TecConcursos, entregues via plataforma Tutori. Trabalha solo, com parcerias de plataforma e conteúdo (BTG, Estratégia Concursos, TecConcursos, Tutori, Você Concursado, Rabelo Concursos).

## O que mais fazemos aqui
- Montar planos de estudo pré e pós edital
- Elaborar cadernos de questões na plataforma TecConcursos
- Produzir conteúdo pro Instagram (prospecção de clientes)
- Organizar dados de editais em planilhas
- Cuidar da parte financeira do negócio

## Clientes e contexto
Negócio próprio, sem personalização individual por cliente — os planos de estudo são elaborados por Elvis e distribuídos em escala via plataforma Tutori.

## Tom de voz
Informal, com gírias do universo militar/concurseiro (ex: "bizu", "bizurado"). Nunca usar travessão. Evitar marcas de escrita "de IA" (contraposições genéricas, "mergulhar de cabeça", etc). O texto deve soar natural, como escrito por uma pessoa.

## Ferramentas conectadas
- Google Drive — acesso direto por sistema de arquivos (workspace já vive dentro da pasta sincronizada do Drive)
- Google Sheets — conectado via `gspread` com OAuth (Python). Credenciais em `credenciais/` (nunca commitar). Client: `credenciais/google-oauth-client.json`, token de sessão: `credenciais/google-oauth-token.json`
- Claude in Chrome (extensão) — acessa o navegador Chrome real do usuário, já logado nas plataformas (Estratégia Concursos, TecConcursos, Tutori). **Navegador embutido é o padrão para qualquer skill que precise navegar; só usar o Chrome real com autorização prévia do usuário na conversa, pedida a cada vez** (confirmado 2026-08-18).
- Pasta padrão de downloads do Estratégia Concursos: `G:\Meu Drive\Inteligência Artificial\Estrategia` (usada pelas skills `baixar-curso-especifico-estrategia` e `baixar-curso-completo-estrategia`).
- Plataforma dos Resumos Esquematizados do professor Bruno Bezerra (Tutory): login em `https://alunoprofbrunobezerra.plataformatutory.com.br/dash`. Pasta padrão de downloads: `G:\Meu Drive\Inteligência Artificial\Resumos Esquematizados` (usada pelas skills `baixar-resumo-especifico` e `baixar-resumo-combo-completo`).
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
