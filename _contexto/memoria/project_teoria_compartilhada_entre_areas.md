---
name: project-teoria-compartilhada-entre-areas
description: "Aula com a MESMA teoria em cursos de áreas diferentes deve receber o mesmo Cód Mestre e o mesmo nome mestre; o hash_teoria é a chave de identidade. Mais: resumos e mapas mentais do próprio Estratégia entram depois"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T23:03:49.761Z
---

Levantado por Elvis em 2026-08-19.

## 1. Teoria idêntica entre áreas usa o MESMO nome mestre

Quando a mesma aula aparece em cursos de áreas diferentes (Fiscal, Controle, Legislativa, e o
que vier), ela deve **consultar a base mestra e receber o mesmo Cód Mestre e o mesmo nome
mestre** — não gerar taxonomia nova.

**Benefício para o aluno:** quem migra de área descobre imediatamente quais aulas já estudou.
As questões mudam (banca e área diferentes), mas a teoria já vista continua valendo, e isso
encurta muito o replanejamento.

### A chave já existe: `hash_teoria`

Não precisa de heurística de nome. O Estratégia **monta o PDF de um mestre único de teoria e
troca só a seção de questões** por curso — verificado em 16 de 16 pares de aula, onde o
`sha256` do arquivo diferia e a teoria era byte a byte idêntica
(ver [[project_paginas_estrategia_sao_derivadas]]).

Logo: **mesmo `hash_teoria` = mesma teoria = mesmo Cód Mestre, mesmo nome mestre, mesmos blocos
de estudo, mesmos pontos.** Só as questões e os pesos mudam.

Confirmação independente: a Aula 00 do Regular Controle tem 125 páginas de arquivo mas teoria em
`p3-25`, com os mesmos cortes de subtópico da Aula 00 do Regular Fiscal.

### O que isso implica na arquitetura

- A **camada de teoria** (taxonomia, blocos, pontos, páginas) é **agnóstica de área** — uma só,
  compartilhada.
- A **camada de questões** (fichamento, pesos, cadernos) é **por área e por banca**.
- Ao processar um curso novo, o primeiro passo é **calcular o `hash_teoria` de cada aula e
  procurar na base**. Se achar, reaproveita tudo da teoria e ficha só as questões. Se não achar,
  é aula nova e entra o mapeamento completo.
- Isso corta drasticamente o custo de abrir uma área nova: só se paga o que é realmente novo.

**Cuidado:** a marca d'água do PDF é **por conta**, então o `hash_teoria` (texto normalizado da
teoria) só compara dentro da mesma conta. Ver [[project_conta_estrategia_compartilhada]].

## 2. Resumos e mapas mentais do próprio Estratégia — pendente

Além do livro eletrônico, o Estratégia produz **resumos próprios e mapas mentais**. Elvis está
tratando disso **em outra sessão**, para depois entrarem como mais uma indicação de material ao
lado do PDF de teoria e do resumo do Bezerra.

Conecta com a pendência já registrada de atualizar `baixar-curso-especifico-estrategia` e
`baixar-curso-completo-estrategia` para baixar também esses materiais
(ver [[project_skill_mapeamento_aulas_pendencias]], bloco C).

## Professor diferente entre as areas (Elvis, 21/08/2026)

O normal e o **mesmo professor** dar a materia nas duas areas: o texto e identico, o hash bate
sozinho e o Cod Mestre e compartilhado sem decisao nenhuma.

**Quando os professores diferem, o sistema PARA e pergunta ao Elvis** qual vira referencia. Nao
escolhe sozinho, nao decide pelo mais recente.

**E a escolha resolve so a identidade, nao a localizacao.** Um codigo, dois enderecos:

| | Compartilhado entre areas |
|---|---|
| Cod Mestre e nome do topico | **sim** |
| Ponto e fichamento | **sim** |
| **INICIE EM / TERMINE EM** | **nao**, e por curso |

Se o aluno de Controle abre o PDF do professor A e o de Fiscal o do professor B, a referencia de
pagina tem de ser a do arquivo **que aquele aluno tem na mao**. Referencia que aponta para um PDF
que ele nao tem transforma o ponto forte do material em defeito. Ver
[[feedback_nome_mestre_sintetiza_referencia_e_literal]] e [[feedback_pagina_sempre_do_arquivo_pdf]].
