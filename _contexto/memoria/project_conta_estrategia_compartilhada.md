---
name: project_conta_estrategia_compartilhada
description: "A conta do Estratégia Concursos usada nas skills de download às vezes aparece logada como Gisilene Tatianne Santos de Lima, esposa do Elvis — conta legítima, compartilhada."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9171338f-adf6-4abf-a949-98ec12c55576
  modified: 2026-08-17T23:56:06.573Z
---

Ao usar o navegador (embutido ou Claude in Chrome) pra baixar cursos do
Estratégia Concursos, a conta logada pode aparecer com o nome "Gisilene
Tatianne Santos de Lima" em vez do nome do Elvis. Confirmado pelo Elvis em
2026-08-17: Gisilene é esposa dele, e essa é uma conta legítima/compartilhada
usada pro negócio.

**Why:** evita alarme falso de "conta errada logada" em execuções futuras das
skills `baixar-curso-especifico-estrategia` e `baixar-curso-completo-estrategia`.

**How to apply:** não tratar esse nome como sinal de conta incorreta. Se
aparecer um nome totalmente diferente (nem Elvis nem Gisilene), aí sim vale
confirmar com o usuário antes de prosseguir.
