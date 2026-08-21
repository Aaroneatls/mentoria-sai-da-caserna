---
name: feedback-skill-tec-filtros-padrao
description: "Roteiro fixo de perguntas no início da skill de mapeamento do TecConcursos: disciplina, ano (padrão 10 anos), banca (padrão todas/Cebraspe+FCC+FGV), área (Fiscal ou Gestão e Controle) — e sempre remover anuladas/desatualizadas"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-18T13:21:59.121Z
---

Toda vez que a skill de mapeamento do TecConcursos (ver [[project_tres_skills_mapeamento]]) rodar, ela precisa abrir com um roteiro fixo de perguntas, nesta ordem, antes de gerar a base de assuntos:

1. **Qual a disciplina/matéria que deseja mapear?** — sem valor padrão, pergunta obrigatória.
2. **A partir de qual ano?** — recomendar **últimos 10 anos** como padrão (se hoje é 2026, recomendar 2017-2026), mas deixar claro que é só uma recomendação e o usuário pode pedir outro intervalo.
3. **Qual banca?** — recomendar **"todas as bancas"** como padrão, mas oferecer como alternativa o combo **Cebraspe + FCC + FGV** (as três bancas principais que o usuário mais usa), ou o usuário pode indicar outra combinação.
4. **Qual área (carreira)?** — recomendar **Fiscal** ou **Gestão e Controle** como as opções mais prováveis, já avisando que "Gestão e Controle" se subdivide (Tribunais de Contas, Controladorias, e uma parte só de "Gestão" separada de "Controle") — o usuário pode querer só uma sub-área específica, não o nó inteiro. Sem perguntar a área, a base de dados fica sem escopo claro e não dá pra comparar entre execuções.

**Sempre aplicar automaticamente, sem perguntar** (regra fixa, não filtro opcional, em todas as execuções):
- **Remover questões anuladas**
- **Remover questões desatualizadas**

(No painel "Editar quantidades" / filtros do Tec, isso aparece como os links "Remover anuladas" e "Remover desatualizadas" na seção "OPÇÕES".)

**Why:** Elvis quer consistência entre execuções da skill — sem esse roteiro fixo de perguntas, a base fica poluída com questões anuladas/desatualizadas e sem escopo claro de disciplina/período/banca/área, o que inviabiliza comparação entre execuções diferentes. A área em especial precisa ficar sempre registrada explicitamente na planilha gerada, porque impacta a base de dados inteira.

**How to apply:** ao rodar a skill de mapeamento do Tec, abrir SEMPRE com essas 4 perguntas na ordem acima (disciplina → ano → banca → área), aplicar os filtros na página `/questoes/filtrar`, sempre remover anuladas/desatualizadas antes de exportar ou ler os pesos por assunto, e registrar a área usada na planilha de saída.
