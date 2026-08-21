---
name: feedback-abrir-links-navegador-proprio
description: "Regra geral: qualquer pedido de abrir link/site vai no navegador próprio (Claude Browser), na mesma janela já aberta — Chrome real só com autorização explícita"
metadata:
  node_type: memory
  type: feedback
---

Sempre que o Elvis pedir pra abrir um link, site ou plataforma (Estratégia, Tec, Tutory, qualquer um), o padrão é o navegador próprio (`mcp__Claude_Browser__*`), reaproveitando a janela/aba que já está aberta em vez de abrir uma nova. Confirmado em 2026-08-19. Generaliza o que já valia só pro Tec em [[feedback-navegador-preferido-tecconcursos]].

**Why:** Elvis quer o fluxo todo acontecendo na própria janela do Claude, sem ficar alternando pro Chrome real; o Chrome fica reservado pros casos em que o navegador próprio não dá conta.

**How to apply:** abrir direto com `preview_start`/`navigate` do Claude Browser, sem perguntar qual navegador usar. Só considerar a extensão Claude in Chrome (`mcp__claude-in-chrome__*`) quando o navegador próprio falhar (login não persiste, recurso exige sessão do Chrome) — e aí pedir autorização explícita antes. Lembrar que screenshot exige o painel visível ([[feedback-navegador-aberto-so-screenshot]]); as demais ações rodam com ele minimizado.
