---
name: feedback-contagem-questoes-pdf-aulas
description: "Regras de contagem de \"Nº de Questões\" ao extrair dados de PDFs de aula (anuladas, duplicadas, inéditas)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-18T09:17:00.011Z
---

Ao contar o total de questões de um PDF de aula (coluna "Nº de Questões" na planilha de mapeamento, ver [[project_projetos_planilha_mapeamento_aulas]]), seguir estas três regras, confirmadas por Elvis em 2026-08-18:

1. **Questão anulada** (marcada como "X" ou similar no gabarito): conta normalmente, não descarta.
2. **Blocos idênticos de questões repetidas** (mesmo enunciado aparecendo mais de uma vez no PDF — ex: uma vez como "correção/comentário" e outra vez só como a questão pura, pra treino): conta **uma única vez**. Isso é o padrão normal do material (Questões Comentadas + Lista de Questões do mesmo tópico/banca são a mesma leva, não soma dobrado).
3. **Questões inéditas** (bloco de questões autorais da própria equipe/curso, ex: "Questões Inéditas"): conta e **soma** ao total — não é duplicata, é conteúdo adicional.

**Why:** o objetivo é registrar o número real de questões únicas disponíveis pra prática em cada aula, sem inflar por repetição do mesmo enunciado, mas sem descartar questão que realmente é conteúdo novo (inédita) ou que só está anulada (mas ainda existe como questão).

**How to apply:** sempre que uma skill ou extração automática processar PDFs de aula pra preencher a coluna "Nº de Questões", aplicar essas três regras. Vale tanto pra extração manual quanto pra qualquer agente/script que fizer esse trabalho no futuro.
