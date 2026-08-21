---
name: feedback-pagina-sempre-do-arquivo-pdf
description: "REGRA GERAL: toda referência de página é a página do ARQUIVO PDF (a que o leitor mostra), nunca a numeração do sumário nem a impressa na folha"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T09:31:01.244Z
---

Regra geral confirmada por Elvis em 2026-08-19, válida para **qualquer** referência de página em
**qualquer** material — aulas do Estratégia, resumos do Bezerra, editais, e o que vier depois.

## A regra

A página referenciada é sempre a **posição real no arquivo PDF** — a que o leitor mostra como
"página X de Y". Tecnicamente: o índice de `PdfReader(...).pages`, contado a partir de 1.

**Nunca** usar:
- o número que aparece no **sumário/índice** interno do PDF;
- o número **impresso na folha** (rodapé/cabeçalho).

## Por quê

O sumário pode estar errado, e a numeração impressa costuma divergir da posição real por causa
de capa, contracapa, folha de rosto e páginas não numeradas. O único número que sempre bate com
o que Elvis vê ao abrir o arquivo é a posição no arquivo.

## Nota de verificação (2026-08-19)

Nos PDFs do Estratégia testados, os dois números **coincidem** — o rodapé da Aula 17 imprime
"2 87" na segunda folha e o `PdfReader` conta 87 páginas. Mas isso é característica da
diagramação atual, **não garantia**. A regra continua sendo posição no arquivo.

## A PÁGINA é a fonte; o sumário é só conferência (Elvis, 2026-08-20)

Elvis determinou que **nenhum número de página pode sair do sumário**. A fonte é a leitura
página a página do PDF. O sumário passa a ter dois usos, e só esses:

1. Dizer onde a **teoria acaba** e as questões começam.
2. **Sinalizar divergência** — se ele anuncia uma seção numa página e a leitura não acha título
   ali, isso é indício de **cabeçalho em banner gráfico** (que não sai no `extract_text()`), e
   aquela página entra na fila de **leitura visual** (renderizar como imagem).

Onde leitura e sumário concordam, confiança alta. Onde discordam, **a leitura prevalece** e a
divergência fica registrada em coluna.

**Ganhos medidos:** na Aula 16 (Improbidade) o sumário tinha **8 entradas** e a leitura das
páginas achou **20 títulos** — doze cortes que existiam no PDF e o sumário ignorava. Além disso,
só a leitura por página permite a indicação de **"do tópico X até o tópico Y"** dentro de uma
página com mais de um assunto, que o sumário jamais daria.

**Custo:** a extração de texto de todas as páginas é barata (2.152 páginas da disciplina em
segundos). O que custa é o julgamento sobre o que é título — ~20 decisões por aula, estimadas
300 a 400 na disciplina. Feito uma vez, e é o insumo que barateia a atualização depois.

**Nota de honestidade:** a suposição anterior de que o número impresso na folha coincide com a
posição no arquivo apoia-se em **uma única observação** (Aula 17, rodapé "2 87" na segunda
folha). Não foi comprovada em escala — mais uma razão para não depender dela.

## Onde o sumário ainda serve

Só para **delimitar onde a teoria acaba e as questões começam** — ele é legível por máquina e
confiável para isso (ver [[project_paginas_estrategia_sao_derivadas]]). Para localizar conteúdo,
vale a busca textual na página, não o número do sumário.

Ver também [[project_regras_quebra_estrategia_correlacao_bezerra]], que já trazia essa regra
restrita ao Bezerra — agora ela é geral.
