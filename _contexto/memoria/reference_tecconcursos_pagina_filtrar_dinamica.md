---
name: reference-tecconcursos-pagina-filtrar-dinamica
description: "Como a página /questoes/filtrar do TecConcursos funciona por dentro — estrutura, taxonomia de assuntos, comportamentos e bugs observados durante automação via navegador"
metadata: 
  node_type: memory
  type: reference
  originSessionId: ce5ff9fc-c989-4e45-8b04-17cdc1a3f08e
  modified: 2026-08-19T01:05:00.598Z
---

Mapeamento da página `https://www.tecconcursos.com.br/questoes/filtrar`, feito em 2026-08-18 via automação de navegador (Claude Browser), pra servir de base pra skill de mapeamento de aulas/questões ([[project_projetos_planilha_mapeamento_aulas]], [[project_skill_mapeamento_aulas_pendencias]]).

## Estrutura da página
- Abas do filtro (um dropdown/lista lateral): Matéria e assunto, Banca, Órgão e cargo, Ano, Área (Carreira), Escolaridade, Formação, Região, Favoritas, Enunciados, Opções.
- Seletor "Universo": Global / Concursos / OAB / CFC / ENEM e Vestibular.
- Tipo de questão: Objetivas (todas) / Objetivas (inéditas) / Discursivas.
- Todos os painéis de todas as abas ficam sempre presentes no DOM simultaneamente (não é lazy-load por aba) — a árvore de acessibilidade fica gigante (80k+ caracteres) quando expandida.

## Taxonomia de "Matéria e assunto"
- Busca por nome retorna dois grupos: **Matérias** que batem com o termo e **Assuntos** específicos (dentro de outras matérias) que contêm o termo.
- Ao selecionar uma matéria (ex: "Direito Administrativo (Doutrina e Leis Federais)"), abre árvore de até 4 níveis: Matéria → Tópico → Subtópico → Sub-subtópico. Cada nível tem uma opção "Todo o conteúdo de [X]" pra marcar tudo de uma vez.
- Essa árvore já vem oficialmente organizada pelo Tec (ex: "Controle da Administração" já vem pré-dividido em Controle Legislativo/Parlamentar → Direto/Político x Indireto/Tribunais de Contas, Controle Jurisdicional etc) — não precisamos deduzir esse agrupamento manualmente, dá pra puxar direto da taxonomia do próprio Tec.

## Comportamento confirmado
- O contador "questões encontradas" ATUALIZA em tempo real ao selecionar um filtro (testado: 4.087.546 sem filtro → 134.943 com "Direito Administrativo" selecionado).
- Ao clicar em "Todo o conteúdo de [X]", às vezes a página renderiza uma **prévia de questão de amostra** (um `<article>` com enunciado e alternativas) — isso confundiu a extração de texto via `get_page_text` (que prioriza `<article>`), fazendo parecer que nada tinha mudado no filtro. Usar `read_page` com busca por texto (`Filtros ativos:`, `encontradas`) é mais confiável que `get_page_text` nessa página.

## Corrigido em 2026-08-18 (segunda rodada, conta grátis)
- O "Editar quantidades" **abre normalmente** via automação, inclusive no Plano Grátis. A anotação anterior de que não abria estava errada. A tela traz "Organizar por" (Hierarquia / Relevância com matéria / Relevância apenas assuntos), "Popular com questões" (Mais Recentes / Aleatórias), tabela editável por assunto e "Exportar para planilha".
- Melhor ainda: não é preciso clicar na árvore. A página aceita filtros por URL (`?formato=OBJETIVA&f[0].tipo=ASSUNTO&f[0].id=5886&f[1].tipo=ANO&f[1].id=2024`) e existe API interna em `/api/...` que devolve tudo em JSON. Ver [[reference_tecconcursos_manual_completo]].

## Contas usadas nos testes
- `aaroncelular@gmail.com` (Plano Grátis) — testado antes, resoluções de professor davam "renove sua assinatura" em várias questões (limitação real de plano, confirmada comparando com a conta avançada).
- `saidacasernacadastros@gmail.com` (Plano Avançado) — conta usada a partir de 2026-08-18 pra construir a skill de mapeamento, tem pastas de cadernos já organizadas por concurso (TCDF, TCU, SEFAZ CE, SEFAZ DF, SEFAZ RN, Manaus, Campina Grande, Caxias do Sul, etc).

**Why:** entender a mecânica real da página de filtro (taxonomia, comportamento do contador, bugs de extração) antes de automatizar a skill de mapeamento evita construir a skill em cima de suposições erradas.

**How to apply:** ao construir a skill de mapeamento que usa esse filtro, preferir ler o contador via `read_page`/busca textual em vez de `get_page_text`; usar a árvore de assuntos do próprio Tec como fonte da taxonomia em vez de reclassificar manualmente; contornar a limitação do "Editar quantidades" usando o contador geral por filtro aplicado individualmente por assunto, se precisar de quantidade por assunto.
