---
name: project-fichamento-duas-passadas
description: "O fichamento tem duas profundidades: enunciado de TODAS as questões, comentário só das que viram linha de BIZURITO"
metadata:
  type: project
---

Decidido pelo Elvis em 2026-08-21 (opção D, entre quatro apresentadas).

## Por que não dá para ler tudo de tudo

Em Direito Administrativo são **5.463 questões** (Cebraspe, FGV e FCC, janela de 5 a 10 anos).

| | Tamanho típico | Custo para as 5.463 |
|---|---|---|
| Enunciado | ~400 caracteres | ~600 mil tokens |
| Comentário do professor | 2.000 a 4.000 caracteres | ~4 milhões de tokens |

O comentário é **7 vezes** maior. É ele que inviabiliza ler tudo de tudo.

## As duas passadas

**Passada 1 — o enunciado de TODAS as questões.** Barata, e já basta para tudo que os
**cadernos** precisam:

- em qual **ponto** a questão cai
- **Principal ou Secundário** (onde o gabarito se decide)
- se é **resolvível pela aula**
- o **marco legal**

Todas as questões são olhadas, uma a uma. O Elvis fez questão disso e está certo: é o que
garante a qualidade e evita o casamento por palavra-chave.

**Passada 2 — o comentário, só dos pontos que viram BIZURITO.** O comentário só é necessário
para **escrever a frase** da folha, e a folha tem 5 a 10 linhas por tópico. São 40 a 60
questões por BIZURITO, não 5.463.

## Teste controlado combinado (21/08/2026)

Para medir se a profundidade extra aparece na qualidade: **dois tópicos levam a passada
completa** — enunciado e comentário de todas as questões — e as folhas são comparadas lado a
lado com as feitas pela regra das duas passadas.

O BIZURITO é o material que o Elvis vende como diferencial, então vale medir em vez de supor.

## Operação: incremental e persistido

O fichamento **não cabe numa sessão**. A janela de contexto é compactada no meio. Então:
fichar um lote, **gravar na planilha**, continuar. Se a sessão cair, retomar de onde parou —
mesma lógica do coletor de base.

Ver [[project_banco_fichamento_questoes]] e [[reference_tec_api_desempenho_e_filtros]].
