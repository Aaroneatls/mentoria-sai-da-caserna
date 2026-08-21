---
name: project-material-padrao-simplificado-e-passo
description: "Qual material entra no plano de estudo: Curso Regular pelo PDF simplificado; Passo Estratégico é exceção, com avaliação adiada pro primeiro pós-edital"
metadata: 
  node_type: memory
  type: project
  originSessionId: 72f48c50-c074-40da-aadd-30e541792bed
  modified: 2026-08-20T12:16:24.656Z
---

Decidido por Elvis em 2026-08-20, ao fim da investigação de tipos de material
(`_contexto/estrategia-tipos-de-material.md`).

## O material padrão é o Curso Regular

O aluno faz **só o Curso Regular**. É o único material que entra no plano por padrão.

## O arquivo de referência é o PDF SIMPLIFICADO

O mapeamento por página se faz sobre o **livro em versão simplificada**, não sobre o
original. É o que a skill de download já vinha priorizando, então é o que está na pasta
do Drive.

**Ressalva medida no pacote TCDF-ANACE (2026-08-20): o simplificado não existe sempre.**

| | Aulas |
|---|---|
| Curso Regular do pacote | 180 |
| Com `pdf_simplificado` | **126 (70%)** |
| Só com original | 54 (30%) |

Quatro disciplinas inteiras **não têm nenhum** simplificado: Língua Portuguesa, Lei
Orgânica do DF, Lei Orgânica do TCDF e Regime Jurídico dos Servidores. Outras têm
parcial (Direito Administrativo: 14 de 21).

**Consequência para o mapeamento:** como a skill de download cai pro original quando não
há simplificado, **a pasta é mista e o nome do arquivo não diz qual versão é**. Antes de
mapear, é preciso saber qual versão está em mãos — as paginações são diferentes, e a
âncora de página só vale pro arquivo que o aluno tem. Ver
[[project_paginas_estrategia_sao_derivadas]].

O campo `pdf_simplificado` é confiável no endpoint de curso (ao contrário de
`pdf_grifado` e `videos`, que só aparecem no endpoint de aula).

## O Passo Estratégico é exceção, não regra

É **teoria** (não material de revisão), mas **não entra no plano por padrão**. O uso
previsto é estreito: **matéria de peso baixo**, em que se pode recomendar o Passo no
lugar da aula regular. Mesmo aí, é uso incomum.

**Nunca é referência de mapeamento no Curso Regular.** A referência é o simplificado.

## Pendência com gatilho definido

**No primeiro pós-edital que a gente montar e que tenha Passo Estratégico**, fazer a
análise de como (e se) o Passo entra: em que matérias, substituindo ou somando à aula, e
como isso muda a conta de páginas do cronograma.

Não antecipar essa análise. O gatilho é o primeiro pós-edital real.

Ver [[project_regras_quebra_estrategia_correlacao_bezerra]] e
[[project_detector_tipografico_titulos_estrategia]].
