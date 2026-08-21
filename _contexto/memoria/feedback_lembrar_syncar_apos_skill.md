---
name: feedback_lembrar_syncar_apos_skill
description: "Sempre que uma skill for criada, instalada ou atualizada, lembrar o usuário de sincronizar com o GitHub (via /syncar) e perguntar se ele quer fazer isso agora."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9171338f-adf6-4abf-a949-98ec12c55576
  modified: 2026-08-17T23:49:37.219Z
---

Toda vez que uma skill for criada do zero, instalada, ou tiver seu SKILL.md
atualizado/ajustado, lembrar o usuário de rodar a sincronização com o GitHub
(commit + push, fluxo da skill `syncar`) e perguntar se ele quer que isso seja
feito agora — não fazer silenciosamente sem perguntar, e não deixar de
mencionar achando que ele vai lembrar sozinho.

**Why:** as skills do workspace ficam salvas primeiro só localmente (arquivo
gravado em disco); "salvar" não significa "estar no GitHub" até rodar o
`/syncar`. O usuário pediu explicitamente esse lembrete depois de uma sessão em
que ajustou duas skills e só percebeu depois que elas não tinham sido
versionadas — inclusive descobrindo que `.claude/skills/*` estava no
`.gitignore` do kit (ver [[feedback_skills_devem_ficar_no_git]]), o que já foi
corrigido.

**How to apply:** ao final de qualquer tarefa que envolveu criar, instalar
(via plugin/marketplace) ou editar uma skill em `.claude/skills/` (local) ou
`~/.claude/skills/` (global, se aplicável ao repositório), perguntar algo como
"Quer que eu sincronize essa skill com o GitHub agora (/syncar)?" antes de
encerrar a resposta.
