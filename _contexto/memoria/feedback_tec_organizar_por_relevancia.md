---
name: feedback-tec-organizar-por-relevancia
description: "Ao exportar assuntos do Tec em \"Editar quantidades\", usar sempre \"Organizar por: Relevância\", não \"Hierarquia\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-18T14:14:37.010Z
---

Na tela "Editar quantidades" do TecConcursos (`/questoes/filtrar`), o campo "Organizar por:" tem pelo menos duas opções: "Hierarquia" (árvore aninhada com código tipo "01.02.03", matérias como nós-pai) e **"Relevância (apenas assuntos)"** — uma lista PLANA só dos assuntos-folha (sem as matérias/categorias-pai como linha própria), ordenada por frequência decrescente, com colunas: Assuntos | Questões encontradas | Frequência Acumulada (barra + %) | Questões no caderno.

O padrão a usar sempre pra exportação de mapeamento é **"Relevância (apenas assuntos)"**, não "Hierarquia" (que foi usado por engano na primeira exportação de teste, Direito Administrativo/Fiscal, em 2026-08-18, e precisou ser refeita).

**Why:** Elvis corrigiu explicitamente e confirmou com print — é esse o formato que interessa pra base de mapeamento (assunto + peso individual + acumulado, sem o ruído dos nós de categoria/matéria intermediários da árvore).

**How to apply:** ao exportar qualquer assunto do Tec pra planilha (nessa ou em qualquer skill futura de mapeamento do Tec), clicar no link "Organizar por: Relevância (apenas assuntos)" na tela "Editar quantidades" — fica logo abaixo do contador de questões — antes de clicar em "Exportar para planilha". Se uma planilha já foi exportada com "Hierarquia" por engano, re-exportar com Relevância e substituir os dados.

**Segundo padrão (mesma tela, confirmado 2026-08-18):** o campo ao lado, "Popular com questões:" (tem as opções "Mais Recentes" e "Aleatórias"), também deve ficar sempre em **"Mais Recentes"** por padrão, não "Aleatórias". Ajustar os dois campos ("Organizar por" e "Popular com questões") juntos antes de exportar.
