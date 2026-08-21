---
name: project_cod_mestre_formato_e_ordem
description: Cod Mestre e SIGLA-NNN com 001-499 do Regular e 501+ de pos-edital; a ordem pertence ao PLANO, nao ao topico
metadata:
  type: project
---

**Formato do Cod Mestre** (Elvis, 21/08/2026): `SIGLA-NNN`, sem prefixo de edital.

- **001 a 499** — topicos que vem do **Curso Regular**
- **501 em diante** — topicos que nascem em **pos-edital**
- **500 nunca existe**, e a fronteira, assim como 000

A origem NAO entra no codigo, entra em **coluna**. Motivo: o codigo identifica **conteudo**, e o
mesmo topico pode aparecer em varios editais. Como prefixo (`DADM-TCDF-001`), o mesmo conteudo
ganharia um codigo por concurso, que e exatamente o que o eixo existe para impedir. Ver
[[feedback_codigo_identifica_conteudo_nao_posicao]].

## A ordem pertence ao PLANO, nao ao topico

O mesmo topico ocupa posicoes diferentes em planos diferentes: 18o no Regular, 22o no TCDF, 7o
num plano so de Curva A. Uma coluna `ordem` no topico serviria a um plano e mentiria para os
outros.

| Tabela | Guarda |
|---|---|
| `topico` | Cod Mestre, nome, disciplina — a identidade |
| `plano` | "Regular Controle", "TCDF 2026", "Curva A Fiscal" |
| `plano_topico` | plano + Cod Mestre + **ordem** |

**A ordem se guarda como ANCORA, nao como numero.** O topico de pos-edital registra "vem depois
de DADM-017"; a sequencia final e calculada na hora de gerar o plano. Duas vantagens:

1. **Sobrevive a reordenacao** do Curso Regular, porque a referencia e o vizinho.
2. **Resolve a Curva ABC de graca**: filtrando so os A, a sequencia e recalculada e sai 1, 2, 3
   contigua para a Tutory, em vez de 1, 4, 9, 15 com buracos.

A ordem de referencia inicial e a do proprio Curso Regular do Estrategia.
