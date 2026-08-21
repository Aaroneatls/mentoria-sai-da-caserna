---
name: feedback-tec-filtro-sem-memoria
description: "No TecConcursos o filtro não guarda o que já foi usado: cadernos manuais com o mesmo filtro saem idênticos, e o \"em série\" só vale enquanto a aba fica aberta"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c75d2df2-d078-420b-87c3-77d0347b7996
  modified: 2026-08-19T12:54:57.812Z
---

Teste medido em 19/08/2026 (conta Avançado, recorte fixo `Assunto = Crase` sem anuladas/desatualizadas = 8.596 questões, 10 questões por caderno, quantidade digitada linha a linha):

| Caderno | Modo | Popular com | Resultado |
|---|---|---|---|
| MANUAL A | sem série | Mais Recentes | conjunto X |
| MANUAL B | sem série | Mais Recentes | **conjunto X — as mesmas 10** |
| SERIE C | em série, 1º | Mais Recentes | conjunto X |
| SERIE D | em série, 2º na mesma aba | Mais Recentes | conjunto Y, zero sobreposição |
| SERIE E | em série, **após recarregar a página** | Mais Recentes | **conjunto X de novo** |
| ALEAT F / G | sem série | Aleatórias | conjuntos distintos, mas por sorteio |

Conclusões:

1. **Seleção manual NÃO desconsidera o caderno anterior.** O filtro é stateless e, com "Mais Recentes", determinístico: mesmo filtro + mesma quantidade = exatamente as mesmas questões. Montar 10 cadernos um a um com o mesmo filtro dá 10 cadernos idênticos.
2. **O "em série" não persiste.** O contador troca de "encontradas" para "restantes" e desconta (8.596 → 8.586 → 8.576), mas o estado morre ao recarregar/fechar a aba. Não dá pra montar a série em dias diferentes, e os cadernos já existentes na conta não são levados em conta.
3. **"Aleatórias" não resolve** — evita repetição por probabilidade, não por regra, e sacrifica o controle de pegar as questões mais recentes.

**Consequência para a skill de montagem de caderno:** o controle de "o que já foi distribuído" tem que ser **nosso**, numa planilha com os `#` por caderno, e a injeção feita por **"Adicionar questões por código"** (Configurações do caderno) — é a única rota que sobrevive a fechar o navegador e permite escolher questão específica.

Relacionados: [[feedback_tec_serie_nao_serve_plano_estudo]], [[reference_tecconcursos_manual_completo]] (seções 2.5 e 2.5-A do `_contexto/tecconcursos.md`).

**Why:** o Elvis pediu essa verificação específica antes de a gente desenhar a skill de cadernos; sem ela, a skill produziria cadernos repetidos sem ninguém perceber.

**How to apply:** nunca contar com o Tec pra evitar repetição entre cadernos. Manter registro externo dos `#` já usados e injetar por código.
