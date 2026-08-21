---
name: feedback-navegador-preferido-tecconcursos
description: "Preferência de navegador ao acessar o TecConcursos — usar o navegador próprio (Claude Browser) por padrão, não o Chrome"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ce5ff9fc-c989-4e45-8b04-17cdc1a3f08e
  modified: 2026-08-18T09:34:04.253Z
---

Ao acessar o TecConcursos (questões, resoluções de professor, etc), dar preferência ao navegador próprio (Claude Browser / `mcp__Claude_Browser__*`) em vez da extensão Claude in Chrome. Testado em 2026-08-18: o navegador próprio já mantém sessão logada no Tec (conta aaroncelular@gmail.com, plano grátis) e consegue abrir a resolução do professor normalmente.

**Why:** Elvis prefere reservar o Chrome real (logado com a conta avançada, `saidacasernacadastros@gmail.com`) só pra quando for estritamente necessário — o navegador próprio já resolve a maioria dos casos de leitura/consulta no Tec.

**How to apply:** ao precisar abrir algo no TecConcursos, tentar primeiro com `mcp__Claude_Browser__*`. Se não for possível (ex: recurso exige plano avançado, ou login não persiste), avisar o Elvis explicitamente e só então usar o Chrome (`mcp__claude-in-chrome__*`) como alternativa.
