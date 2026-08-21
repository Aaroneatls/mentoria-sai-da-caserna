---
name: project_pacotes_regulares_estrategia
description: "No Estratégia Concursos, pacotes \"Regular <Área>\" (ex. Regular Fiscal, Regular Controle) são genéricos, cobrem matérias comuns a vários concursos da área — não têm um concurso/cargo específico associado."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9171338f-adf6-4abf-a949-98ec12c55576
  modified: 2026-08-17T23:57:27.071Z
---

Nem todo pacote do Estratégia Concursos é amarrado a um concurso/cargo
específico (tipo "TCDF-ANACE"). Existem pacotes **"Regular <Área>"** — ex.
"Curso Regular para Área Fiscal - Pacote Completo", e também existe um
"Regular Controle" — que são cursos de base cobrindo as matérias comuns a
vários concursos daquela área, usados como preparação geral antes/junto de um
edital específico sair.

**Why:** a skill `baixar-curso-completo-estrategia` (e a
`baixar-curso-especifico-estrategia`) foi desenhada assumindo que toda pasta
de matéria leva o sufixo `(SIGLA_CONCURSO-SIGLA_CARGO)`. Pra esses pacotes
"Regular", não existe essa sigla — confirmado pelo Elvis em 2026-08-17, que
pediu pra tratar como `(Regular <Área>)` no lugar da sigla concurso-cargo (ex:
`Direito Administrativo (Regular Fiscal)`). Essa mesma decisão já foi
registrada como caso especial dentro do `SKILL.md` da
`baixar-curso-completo-estrategia`, então essa memória é só o contexto de
por quê — ver [[feedback_skills_devem_ficar_no_git]] pro fluxo de manter as
skills atualizadas versionadas.

**Áreas já mapeadas** (confirmadas com o Elvis, não perguntar de novo):

- "Curso Regular para Área Fiscal" → `(Regular Fiscal)`
- "Concursos de Tribunais de Contas (Nível Superior) - Pacote Completo Cursos
  Regulares" → `(Regular Controle)` — confirmado em 2026-08-18. Tribunal de
  Contas é área de controle, então entra na mesma família do Regular Fiscal em
  vez de virar uma sigla própria de TC. A pasta-raiz do pacote segue o mesmo
  nome curto: `Regular Controle (DD-MM-AAAA)`.

**How to apply:** ao mapear um pacote novo (Passo 1 da skill), o sinal pra
reconhecer esse caso é a própria palavra **"Regular"** no nome do pacote (ex:
"Curso Regular para Área Fiscal" → pacote "Regular Fiscal"), não a ausência de
sigla de edital. Ao reconhecer, usar `(Regular <Área>)` no lugar da sigla —
sem perguntar de novo, já é padrão conhecido.
