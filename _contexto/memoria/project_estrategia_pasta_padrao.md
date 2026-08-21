---
name: project-estrategia-pasta-padrao
description: "Default folder where Estratégia Concursos course/package downloads are saved, used by the two download skills"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08cf9e27-2d4e-401d-bf2e-2826b24d6223
  modified: 2026-08-17T13:28:39.624Z
---

Os materiais baixados do Estratégia Concursos (livros eletrônicos em PDF, por curso específico ou por pacote completo) ficam salvos, por padrão, em `G:\Meu Drive\Inteligência Artificial\Estrategia` — pasta sincronizada com o Google Drive.

**Why:** Essa pasta foi definida como padrão durante a criação/ajuste das skills [[baixar-curso-especifico-estrategia]] e [[baixar-curso-completo-estrategia]]. Antes se chamava `Estrategia Concursos`; foi renomeada pra `Estrategia` pra encurtar o caminho e reduzir risco de estourar o limite de 260 caracteres do Windows. Deliberadamente **não** se renomeou a pasta-mãe `Inteligência Artificial` pra `IA`, porque essa pasta também contém o workspace do Claude Code (`Claude Code\ccos-ratos`) e mexer nela traria risco pra memória/sessão do Claude Code.

**How to apply:** Ao rodar qualquer uma das duas skills de download do Estratégia Concursos, essa é a pasta padrão oferecida — o usuário pode confirmar ou indicar outro local a cada execução. Também existe (ainda não criada) a ideia de uma planilha de referência com sigla de disciplinas, que no futuro vai substituir o nome completo da matéria no nome das pastas — até lá, segue usando o nome completo.
