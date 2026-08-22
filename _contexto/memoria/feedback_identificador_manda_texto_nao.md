---
name: feedback_identificador_manda_texto_nao
description: quando existir id, usar o id; casar por texto erra porque os nomes se contem uns aos outros e o significado nao acompanha
metadata:
  type: feedback
---

**Quando existir identificador, usar o identificador. Texto serve para humano ler, nao para
maquina decidir.**

Tres casos do mesmo padrao, todos medidos:

1. **Estrategia, selecao de produto** (22/08/2026): um seletor que casava por "Sistema de
   Questoes" desmatriculou o **TCDF** em vez do Controle, porque o nome completo do TCDF **tambem**
   termina assim e ele vinha antes na lista. **Os nomes dos produtos se contem uns aos outros.**
   O certo e selecionar pelo **id no href**.

2. **Estrategia, busca do catalogo**: a busca e **fuzzy (OR)**, entao contagem alta nao significa
   acerto. Ver [[reference_estrategia_busca_catalogo_abas]].

3. **TecConcursos, filtro por Formacao**: nao serve para achar concurso de area especializada,
   porque concurso que **aceita** formacao em TI nao e concurso **de** TI. O texto casa, o
   significado nao.

**O padrao:** texto parece identificar e nao identifica. Ou porque um nome contem o outro, ou
porque a busca e permissiva, ou porque a palavra tem dois sentidos. Sempre que houver id, chave,
href ou codigo, e ele que manda.

Vale tambem para o nosso proprio projeto: e por isso que o **Cod Mestre** e o que vai no campo que
a Tutory usa para casar "ja estudou", e nao o nome do topico.
