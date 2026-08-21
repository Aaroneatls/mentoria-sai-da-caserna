---
name: feedback-tec-navegador-bizus
description: Bizus técnicos pra navegar/automatizar o filtro de questões do TecConcursos sem quebrar
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-18T13:17:44.908Z
---

Ao automatizar a página `/questoes/filtrar` do TecConcursos (árvore de Matéria e assunto, Anos, etc.) via navegador:

1. **Se a árvore de seleção (matéria/assunto) ficar bagunçada** — cliques que expandem/colapsam itens errados, estado inconsistente entre o que a tela mostra e o que foi de fato selecionado — **a solução mais rápida é recarregar a página e recomeçar** a sequência de cliques, em vez de tentar consertar clicando mais. Ficar tentando corrigir em cima do estado bagunçado costuma piorar (cliques acabam reabrindo itens já fechados etc).
2. **Clique por coordenada de pixel (screenshot) é pouco confiável nessa página** — as linhas da árvore ficam muito próximas verticalmente e a escala do screenshot (imagem ~800px) não bate 1:1 com o viewport real (~1542px), então um clique "olhando pro print" frequentemente acerta a linha errada. **Prefira clicar por `ref` do `read_page`** (accessibility tree) — isso mapeia pro elemento certo independente de escala/posição visual.
3. **Todos os painéis de filtro (Matéria, Banca, Órgão, Ano, Área, etc.) coexistem simultaneamente no DOM**, não é lazy-load por aba — então a árvore de acessibilidade fica gigante (podem passar de 200k caracteres) assim que a matéria e outros filtros vão sendo expandidos. Pra achar um painel específico (ex: "Anos") sem estourar o limite de leitura, usar `read_page` com `depth` baixo (ex: 3) pra reduzir a profundidade das subárvores já expandidas (como a árvore de assuntos de uma matéria, que é bem funda) — isso costuma liberar espaço suficiente pra alcançar painéis mais pra frente no DOM dentro do limite de caracteres.
4. **`get_page_text` não é confiável nessa página** — quando há uma questão de amostra sendo exibida (o que acontece com frequência ao selecionar itens da árvore), ele prioriza o conteúdo do `<article>` da questão em vez do painel de filtros. Usar `read_page` (buscando por "Filtros ativos:" ou pela contagem de "questões encontradas") em vez de `get_page_text` pra conferir o estado dos filtros.

**Why:** essas travas custaram bastante tempo/tentativas numa sessão real de automação (2026-08-18) — documentar evita repetir o mesmo processo de tentativa e erro da próxima vez que a skill de mapeamento do Tec for construída/testada.

**How to apply:** ao construir a skill de mapeamento do TecConcursos que usa esse filtro, seguir essas 4 práticas desde o início em vez de descobrir na prática de novo.
