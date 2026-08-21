---
name: feedback-tec-serie-nao-serve-plano-estudo
description: "\"Gerar cadernos em série\" do TecConcursos distribui por frequência histórica e não serve pra plano de estudo — usar seleção dirigida de quantidade por assunto"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c75d2df2-d078-420b-87c3-77d0347b7996
  modified: 2026-08-19T11:55:17.567Z
---

O recurso **"Gerar cadernos em série"** do TecConcursos distribui as questões **proporcionalmente à frequência histórica do banco**, e não conforme o edital. Não usar pra montar plano de estudo do Elvis.

Teste medido em 19/08/2026 (Língua Portuguesa + Área Fiscal, sem anuladas/desatualizadas = 13.916 questões em 73 assuntos): pedindo cadernos de 20 questões, o Tec entrega **5 de Interpretação de Textos (25% do caderno) + 1 em cada um de outros 15 assuntos + 57 assuntos zerados**. Gerei três cadernos em série e **a composição temática saiu idêntica nos três** — as questões não se repetem, mas os mesmos 16 assuntos aparecem sempre e a cauda longa nunca entra.

Dois problemas, ambos apontados pelo Elvis antes do teste:
1. **Caderno monotemático** — o assunto dominante come um quarto de cada caderno, o que é maçante pro aluno.
2. **A cauda longa não chega** — assunto com poucas questões só entra se o total do caderno for grande, e assunto pequeno no banco pode ser exatamente o que o edital cobra.

**Onde "em série" serve:** simulado (a proporção histórica imita a prova) e fatiar um caderno já consolidado em blocos.

**O que usar no lugar, pra plano de estudo:**
- `Editar quantidades` linha a linha (Relevância apenas assuntos + Mais Recentes), com teto por assunto e piso ≥1 pra ninguém zerar;
- ou um caderno por assunto/bloco do edital;
- ou "Adicionar questões por código" nas Configurações do caderno, montando a lista de ids fora da plataforma.

Regra: **a relevância do Tec é diagnóstico, não distribuidor automático.** Ela diz o que a banca cobra mais; quem diz quantas questões o aluno faz de cada assunto é o plano de estudo.

Relacionado: [[reference_tecconcursos_manual_completo]] (seções 2.5 e 2.5-A do `_contexto/tecconcursos.md`).

**Why:** o Elvis levantou essa limitação e pediu a verificação prática; sem ela, uma skill de montagem de caderno sairia entregando cadernos desbalanceados e com buracos no edital.

**How to apply:** em qualquer skill que monte caderno de questões no Tec a partir de edital, definir a quantidade por assunto explicitamente e nunca delegar a distribuição ao "gerar em série".
