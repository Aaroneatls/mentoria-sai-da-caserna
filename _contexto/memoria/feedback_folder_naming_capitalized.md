---
name: feedback-folder-naming-capitalized
description: Pastas criadas (Drive ou local) devem começar com letra maiúscula
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-17T13:34:07.113Z
---

Toda pasta criada para o usuário (Google Drive ou sistema de arquivos local) deve ter a primeira letra do nome em maiúscula. Ex: "Projetos", não "projetos".

**Why:** o usuário corrigiu depois que a pasta "projetos" foi criada em minúsculo no Google Drive — prefere consistência visual com o padrão de nomes do Drive dele.

**How to apply:** ao criar qualquer pasta nova (Drive API, `mkdir`, etc.), capitalizar a primeira letra do nome antes de criar. Não se aplica a arquivos, só a nomes de pasta.
