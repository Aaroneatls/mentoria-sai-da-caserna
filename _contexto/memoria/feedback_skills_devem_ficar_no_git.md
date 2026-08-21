---
name: feedback_skills_devem_ficar_no_git
description: Todas as skills em .claude/skills/ devem ser versionadas no GitHub — não deixar nenhuma de fora via .gitignore.
metadata: 
  node_type: memory
  type: project
  originSessionId: 9171338f-adf6-4abf-a949-98ec12c55576
  modified: 2026-08-17T23:49:45.974Z
---

O `.gitignore` do workspace costumava excluir `.claude/skills/*` (com exceção
só das 6 skills do kit original: setup, iniciar, syncar, mapear,
novo-projeto, atualizar), deixando skills criadas depois (como
`baixar-curso-especifico-estrategia` e `baixar-curso-completo-estrategia`)
locais, fora do GitHub. Essa exceção foi removida em 2026-08-17 — agora todas
as skills em `.claude/skills/` são versionadas.

**Why:** o usuário quer todas as skills salvas no GitHub, sem distinção entre
"skills do kit" e "skills criadas depois". Perceber isso levou também ao
lembrete permanente em [[feedback_lembrar_syncar_apos_skill]].

**How to apply:** não recriar essa exclusão no `.gitignore` ao editar esse
arquivo no futuro. Qualquer skill nova em `.claude/skills/` deve entrar
normalmente no próximo `/syncar`.
