---
name: feedback_sugestao_melhoria_final_execucao
description: Toda skill de download em massa ou de cadernos de questões termina a execução avaliando se há sugestão de melhoria pra ela mesma
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0e7e5d89-444b-45d1-ad2a-4f1e86517125
  modified: 2026-08-18T15:13:41.953Z
---

Regra geral (salva em `AGENTS.md`, seção "Sugestão de melhoria ao final de execução"): toda skill relacionada a **download de materiais em massa** (`baixar-curso-especifico-estrategia`, `baixar-curso-completo-estrategia`, `baixar-resumo-especifico`, `baixar-resumo-combo-completo`) ou a **elaboração de cadernos de questões** (futuras skills no TecConcursos) precisa, ao final de toda execução, avaliar se aprendeu algo que sugere ajuste na própria skill.

- Se identificar algo: apresentar a sugestão objetivamente, esperar aprovação do Elvis, só então editar o `SKILL.md` e rodar `/syncar`.
- Se nada de novo: avisar isso de forma curta, sem inventar sugestão.
- Nunca editar/sincronizar sem aprovação prévia.

**Why:** confirmado pelo Elvis em 2026-08-18, depois de validar esse padrão nas skills `baixar-resumo-especifico`/`baixar-resumo-combo-completo` (onde já rendeu vários ajustes reais: bug do `{domain}`, throttling de aba em segundo plano, extração de rótulo vazio, comparação por Sumário). Ele quer esse ciclo de aprendizado contínuo em qualquer skill nova desse tipo, sem precisar pedir de novo.

**How to apply:** ao criar uma skill nova de download em massa ou de cadernos de questões, já incluir esse passo final por padrão. Já retrofitado nas 4 skills existentes que se encaixam no critério (`baixar-curso-especifico-estrategia`, `baixar-curso-completo-estrategia`, `baixar-resumo-especifico`, `baixar-resumo-combo-completo`).
