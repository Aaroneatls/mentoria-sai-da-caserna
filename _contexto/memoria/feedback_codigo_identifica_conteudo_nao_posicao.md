---
name: feedback-codigo-identifica-conteudo-nao-posicao
description: "REGRA DURA: Cód Mestre e Cód do Ponto identificam o CONTEÚDO, nunca a posição. Renomear pode; trocar o conteúdo exige código novo, senão as questões perdem a correlação"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T19:51:56.521Z
---

Alerta levantado por Elvis em 2026-08-19. **A skill de taxonomia tem que ter isso como
verificação ativa, não como lembrete pra alguém se lembrar.**

## A regra

O `Cód Mestre` (`DADM-001`) e o `Cód do Ponto` (`DADM-001.P05`) identificam **o conteúdo**,
não o lugar na lista. Ver [[project_taxonomia_codigo_mestre_e_atualizacao]] e
[[project_banco_fichamento_questoes]].

**Exemplo do próprio Elvis:**
- "Princípio da legalidade" → "Princípio administrativo da legalidade" = **mesma coisa escrita
  diferente**. Mantém o código. Sem problema nenhum.
- "Princípio da legalidade" → "Princípio da impessoalidade" = **outro conteúdo**. Proibido
  reaproveitar o código. Tem que nascer um código novo, senão todas as questões fichadas
  naquele ponto passam a apontar para um conteúdo que elas não cobram.

## Os quatro casos de mudança

| Caso | O que fazer com o código | O que acontece com as questões |
|---|---|---|
| **Renomeação** (mesmo conteúdo, redação nova) | mantém | nada |
| **Substituição** (virou outro conteúdo) | código novo; o antigo vira **descontinuado** e **nunca é reaproveitado** | precisam ser refichadas |
| **Desdobramento** (um ponto vira dois) | o original mantém o código; o novo recorte ganha código novo | precisam ser redistribuídas entre os dois |
| **Fusão** (dois pontos viram um) | sobrevive um código; o outro vira **alias** apontando pra ele | migram para o código sobrevivente |

Número de código descontinuado **nunca** é reutilizado por outro conteúdo.

## O que a skill precisa fazer (não é opcional)

1. Ao atualizar, **comparar nome antigo x nome novo** de cada código.
2. Se mudou e o código **tem questões fichadas**, **parar e perguntar ao Elvis** qual dos
   quatro casos é. Nunca decidir sozinha — o julgamento "é a mesma coisa?" é semântico e errar
   é silencioso.
3. Ao perguntar, mostrar o **raio de impacto**: quantas questões estão fichadas nesse código e
   em quantos cadernos já criados elas aparecem.
4. Só depois de decidido, propagar em cascata: ponto → questões fichadas → cadernos no Tec →
   planos de estudo.

**Heurística de apoio (não substitui a pergunta):** se a **âncora legal** do ponto continuou a
mesma, provavelmente é renomeação; se a âncora mudou, provavelmente é conteúdo novo.

**Why:** o erro aqui não gera exceção, não quebra fórmula e não aparece na planilha. Ele só
aparece lá na frente, quando o aluno recebe um caderno cheio de questão que não tem nada a ver
com o tópico que ele acabou de estudar. É o tipo de defeito que só se descobre pelo prejuízo.

**How to apply:** escrever esse bloco de verificação no modo "atualizar" da skill de taxonomia
desde a primeira versão, junto com a cascata já prevista.
