---
name: feedback-never-delete-recreate-folder
description: Never delete and recreate a folder to apply a fix — always rename/update the existing folder in place
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 08cf9e27-2d4e-401d-bf2e-2826b24d6223
  modified: 2026-08-17T13:28:29.712Z
---

Nunca apagar uma pasta (ou árvore de pastas) inteira e recriar do zero pra aplicar uma correção ou ajuste. Sempre atualizar/renomear a pasta já existente no lugar (`Rename-Item` ou equivalente).

**Why:** Durante os testes das skills de download do Estratégia Concursos, apaguei a pasta raiz de teste inteira pra corrigir os nomes dos arquivos dentro dela, e recriei do zero com um nome de pasta diferente. O usuário apontou que isso conta como "criar uma pasta nova", não "atualizar a existente" — mesmo que o conteúdo final pareça igual, perde-se a identidade da pasta original (e, num caso real, perderia PDFs já baixados que não deveriam ser re-baixados).

**How to apply:** Em qualquer automação que mexa em arquivos/pastas do Drive do usuário (não só as skills do Estratégia Concursos), preferir sempre editar/renomear em cima do que já existe. Se uma pasta precisa de correção de nome ou conteúdo, listar o que tem, ajustar os arquivos necessários e renomear a pasta existente — nunca `Remove-Item -Recurse` seguido de recriação, mesmo que pareça mais simples.
