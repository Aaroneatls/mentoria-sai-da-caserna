---
name: feedback-qualidade-acima-de-economia-de-tokens
description: "Elvis prefere gasto maior de tokens a risco de erro: abrir o PDF e olhar a imagem vale mais que inferir para economizar"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T10:06:48.434Z
---

Dito pelo Elvis em 2026-08-20, no contexto do mapeamento de aulas do Estratégia.

**A regra:** quando houver escolha entre inferir (barato) e conferir de fato abrindo o arquivo
e olhando a imagem (caro), **conferir**. Custo de token não é critério.

**Por quê:** o produto final é a experiência de leitura do aluno. Ele abre o PDF na página que
a gente indicou e precisa encontrar exatamente o tópico indicado, tanto no começo quanto no
fim. Uma referência que não bate gera dúvida e derruba a confiança no material inteiro. Vale
mais entregar com certeza do que entregar rápido.

**Também pesa:** a informação precisa ter condição de ser **atualizada** depois. Solução que só
funciona uma vez, ou que depende de eu ter adivinhado certo, não serve.

**Na prática, isso autoriza:**
- renderizar página (ou faixa de título) como imagem e ler visualmente, em vez de confiar só na
  extração de texto — ver [[project_detector_tipografico_titulos_estrategia]], onde 23% das
  faixas do curso são imagem rasterizada e não têm camada de texto
- ler as páginas uma a uma quando o resultado depender disso
- refazer uma extração inteira quando surgir dúvida, em vez de remendar

Relacionado: [[feedback_validacao_autonoma_e_corte_de_tabela]] (resolver sozinho e só escalar
caso crítico) e [[feedback_nome_mestre_sintetiza_referencia_e_literal]] (a referência tem que
bater com o que está impresso).
