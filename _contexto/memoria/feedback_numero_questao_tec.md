---
name: feedback-numero-questao-tec
description: "No TecConcursos, o número identificador da questão é o que aparece com o símbolo # (ex. #3972960), não o \"Questão N de 30\" do caderno"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ce5ff9fc-c989-4e45-8b04-17cdc1a3f08e
  modified: 2026-08-18T09:35:35.469Z
---

No TecConcursos, cada questão tem um número identificador único que aparece com o símbolo `#` ao lado do nome da banca (ex: `#3972960 CEBRASPE (CESPE) - 2026 - Técnico Administrativo (TCE RN)`). Esse é o número da questão em si — diferente do "Questão 1 de 30", que é só a posição dela dentro do caderno específico que está sendo resolvido.

**Why:** Elvis quer esse número registrado em tabelas/relatórios de questões pra poder identificar e referenciar a questão de forma inequívoca (o link direto é `tecconcursos.com.br/questoes/{numero}`).

**How to apply:** sempre que for listar ou tabular questões do Tec (ex: pra gerar bizus, comparar questões similares), incluir essa numeração com `#`, extraída do elemento ao lado da banca.
