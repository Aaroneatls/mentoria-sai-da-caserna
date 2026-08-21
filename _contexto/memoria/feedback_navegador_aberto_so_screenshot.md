---
name: feedback-navegador-aberto-so-screenshot
description: "No navegador próprio (Claude Browser), só é preciso deixar o painel visível/aberto quando eu for tirar screenshot — as demais ações (clicar, navegar, ler texto) funcionam com o painel minimizado"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ce5ff9fc-c989-4e45-8b04-17cdc1a3f08e
  modified: 2026-08-18T09:41:33.186Z
---

O navegador próprio (`mcp__Claude_Browser__*`) consegue clicar, navegar entre páginas e ler texto (`get_page_text`, `read_page`) mesmo com o painel minimizado/não visível. A única ação que trava é o `screenshot` — ele dá erro "the Browser pane is not displayed, so the page is not compositing frames" se o painel não estiver visível na tela.

**Why:** Elvis quer poder minimizar o navegador e trabalhar em outra coisa enquanto eu executo tarefas nele, sem precisar ficar com a janela aberta o tempo todo.

**How to apply:** ao iniciar uma tarefa no navegador próprio que EU sei que vai precisar de screenshot (ex: debugar algo visualmente, confirmar layout), avisar Elvis no começo que preciso que ele deixe o painel aberto por um tempo. Assim que eu não precisar mais de screenshot (só cliques/leitura de texto), avisar que ele já pode minimizar e ir pra outra aba/seção.
