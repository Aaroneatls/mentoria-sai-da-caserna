---
name: feedback-skill-testing-workflow
description: "User's preferred workflow when creating or adjusting a skill — test live before finalizing, simulate with placeholders to save cost, only do real actions when explicitly asked"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 08cf9e27-2d4e-401d-bf2e-2826b24d6223
  modified: 2026-08-17T13:28:19.741Z
---

Sempre testar ao vivo (navegando no site/sistema real, não só supondo comportamento) antes de considerar uma instrução de skill como definitiva. Durante os testes, preferir simular com arquivos `.txt` placeholder em vez de executar a ação real (ex: baixar PDF de verdade), só fazendo a ação real quando o usuário pedir explicitamente.

**Why:** Ficou confirmado repetidamente ao longo da criação das skills [[baixar-curso-especifico-estrategia]] e [[baixar-curso-completo-estrategia]] — o usuário corrigiu suposições erradas (categorias sem livro que na verdade tinham, formato `N/M` que quebrava no Windows) só depois de testar ao vivo, e pediu explicitamente pra usar `.txt` em vez de PDF real nos testes "pra não gastar banda/token à toa".

**How to apply:** Ao criar ou ajustar qualquer skill que interage com um site/sistema externo (navegação, scraping, downloads), propor um teste ao vivo antes de fechar a instrução como definitiva. No teste, usar placeholders/simulação por padrão; só executar a ação real (download, envio, etc) se o usuário pedir isso especificamente. Perguntar ao usuário se ele quer ver o resultado do mapeamento/estrutura antes de seguir pro passo seguinte, em vez de assumir e prosseguir.
