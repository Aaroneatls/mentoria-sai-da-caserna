---
name: project-marca-dagua-cpf-no-texto-extraido
description: "PDF do Estratégia traz CPF e nome do titular DENTRO do texto extraível — filtrar na extração, antes de qualquer uso, senão vaza dado pessoal no material do aluno"
metadata:
  node_type: memory
  type: project
---

Todo PDF do Estratégia é **marcado por download**, e a marca está **na camada de texto**, não só na imagem. Em praticamente toda página do livro, do resumo e do mapa mental aparece `02055447114 - Gisilene Tatianne Santos de Lima` — CPF e nome completo de pessoa real (a conta compartilhada, ver [[project-conta-estrategia-compartilhada]]). Descoberto em 22-08-2026.

**Por que é grave:** esse texto sai junto na extração. Se passar para âncora de prosa, citação no BIZURITO, fichamento ou qualquer material distribuído, o Elvis publica o CPF da esposa em escala.

**A regra:** descartar linhas que casem com `\d{11}\s*-\s*<Nome>` **na extração**, antes de qualquer consumo — não só antes de hashear. É trava de vazamento, não higiene de hash.

**Efeito no `hash_teoria` (medido):** 4 downloads do mesmo arquivo deram 4 hashes de **arquivo** diferentes, mas o **texto extraído foi idêntico nos quatro** (4.598 caracteres, mesmo hash), sem normalizar — a marca é constante para a mesma conta. O problema é **entre contas** (coleta x produção): mesmo conteúdo, hash diferente, falha silenciosa, e o aluno estuda duas vezes o mesmo tópico. Com a normalização, o `hash_teoria` volta a valer ([[project-teoria-compartilhada-entre-areas]]).

**Não confundir:** hash do **arquivo** morreu (muda a cada download; identidade é o nome do arquivo no CDN — ver [[project-apoio-resumo-mapa-mental-estrategia]]); `hash_teoria` sobre texto normalizado continua vivo.
