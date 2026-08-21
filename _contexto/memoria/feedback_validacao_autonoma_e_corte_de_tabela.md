---
name: feedback-validacao-autonoma-e-corte-de-tabela
description: "Claude resolve a validação sozinho e só escala caso crítico, sempre com sugestão; e nunca corta tabela/quadro ao meio ao delimitar um bloco de estudo"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T09:41:59.257Z
---

Definido por Elvis em 2026-08-20.

## 1. Nunca cortar tabela ou quadro ao meio

Ao delimitar um bloco de estudo, o corte tem que respeitar **o fim da tabela ou do quadro**.
Se a página termina no meio de uma tabela, o bloco vai **até o fim dela**, não até a borda da
página. O mesmo vale para figuras, fluxogramas e quadros comparativos.

A referência entregue ao aluno usa **título ou subtítulo** como limite — nunca um ponto
arbitrário que parta o assunto no meio.

Isso importa porque os PDFs do Estratégia são cheios de quadros que atravessam a virada de
página, e cortar ali deixa o aluno com meia tabela.

## 2. Claude resolve a validação sozinho

Elvis **não quer ser consultado** em cada dúvida de validação. A regra:

- **Resolver sozinho** sempre que possível — inclusive conferindo visualmente a página, agora
  que há renderizador (`pymupdf`, instalado em 2026-08-20 com autorização dele).
- **Escalar só caso crítico**, e **sempre acompanhado de sugestão de solução**, nunca como
  pergunta aberta.
- **Salvar cada caso resolvido na memória**, para que o mesmo tipo de dúvida não volte a virar
  pergunta.

## Casos já resolvidos (não perguntar de novo)

**BANNER GRÁFICO SÓ SE DESCOBRE OLHANDO — regra corrigida em 2026-08-20.**

Houve uma hipótese errada, verificada e derrubada no mesmo dia: supôs-se que banner gráfico
sempre deixa fragmentos na extração. **É falso.** Comprovado renderizando:

| Página | O que a extração devolveu | O que existe de verdade |
|---|---|---|
| Aula 16, p3 | `I / MPROBIDADE / ADMINISTRATIVA / Noções gerais` | banner, extraído em pedaços |
| Aula 17, p3 | `Lei de Acesso à Informação` na linha 8 | banner no meio da página, extraiu inteiro |
| **Aula 02, p3** | **nada** — texto começa direto na prosa | **banner "ORGANIZAÇÃO ADMINISTRATIVA" existe** |

O mesmo template produz os três comportamentos. **Não há sinal textual confiável.**

**Regra:** página que seria início de bloco e não tem título detectado → **renderizar e olhar**,
sempre. Com `pymupdf` isso é barato: basta o topo da página, ~40% da altura, a 110 dpi. Não é
último recurso, é o método.

**Primeira página de teoria sem título detectado** também entra nessa regra — pode ter banner
(Aula 02) ou realmente não ter (a saudação da Aula 17 vem antes do banner). Só olhando se sabe.

**Imagens do PDF não distinguem nada:** todas as páginas do Estratégia carregam as mesmas 5
imagens (fundo 793x1122 e faixas 793x90 e 793x86). É decoração do template — inspecionar
XObject de imagem **não serve** para detectar banner de título.

**Caixa de diagrama parece título:** palavras isoladas em caixas de fluxograma (ex.:
`Consequências`, `Atos de improbidade`) passavam no filtro de título. **Regra que resolve:
título de verdade é seguido de prosa** — alguma das 3 linhas seguintes tem mais de 80
caracteres. Sem isso, é caixa de diagrama ou célula de quadro.

**Célula de tabela parece título:** linhas com tabulação (`\t`) e aglomerados de 3+ candidatos
em linhas consecutivas são tabela, não título.

## 3. Normalização de caixa nos títulos

Título em CAIXA ALTA é convertido para caixa de sentença: primeira letra maiúscula, resto
minúsculo, preservando siglas (STF, CF, LIA, LAI, EP, SEM, OAB…) e nomes próprios. Preposições
e artigos no meio ficam minúsculos.

`LEI DE ACESSO À INFORMAÇÃO` → `Lei de Acesso à Informação`

Ver [[feedback_pagina_sempre_do_arquivo_pdf]] e [[feedback_nomenclatura_nome_mestre]].
