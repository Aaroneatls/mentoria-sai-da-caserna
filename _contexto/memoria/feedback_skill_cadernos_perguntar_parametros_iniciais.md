---
name: feedback-skill-cadernos-perguntar-parametros-iniciais
description: "A skill de gerar cadernos do Tec sempre abre perguntando os parâmetros iniciais da rodada, antes de abrir a plataforma"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T18:52:37.613Z
---

Definido por Elvis em 2026-08-19, na primeira execução de teste de cadernos de Nível 1.

A skill de montagem de cadernos do TecConcursos (`gerar-cadernos-tecconcursos`, nome provisório — ver [[project_niveis_caderno_tec_e_pesos]]) **sempre começa perguntando os parâmetros iniciais da rodada**. Não assume nada por conta própria, não herda silenciosamente o filtro da execução anterior, e não abre a plataforma antes de ter as respostas.

Parâmetros a perguntar na abertura:

1. **Disciplina e faixa de Cód Mestre** — quais tópicos da taxonomia entram nessa rodada (ver [[project_taxonomia_codigo_mestre_e_atualizacao]]).
2. **Nível(is) de caderno** — qual dos 7 níveis está sendo gerado.
3. **Filtro de banca e área** — três perguntas específicas, sempre nessa ordem (formato definido por Elvis em 2026-08-19):
   - **"Qual área vamos usar?"** — Fiscal ou Controle. Se for Controle, no Tec a seleção é dentro de "Gestão e Controle", especificamente **Controladorias e Tribunais de Contas** (a área "Gestão e Controle" crua é ampla demais).
   - **"Qual o limite de tempo?"** — o padrão já é **até 10 anos**, regredindo ano a ano até fechar a meta de ~1.000 questões. Só confirmar/ajustar.
   - **"Qual a banca do caso concreto?"** — a banca de referência de onde parte a busca. Se ela não fechar a meta, complementa na ordem de fallback da área (Controle: Cebraspe → FGV → FCC; Fiscal: Cebraspe → FCC → FGV — ver [[project_niveis_caderno_tec_e_pesos]]).
4. **Momento** — pré-edital ou pós-edital (muda o escopo de banca e o tamanho de vários níveis).
5. **Nomenclatura do caderno** na plataforma.
6. **Onde registrar** as questões usadas (aba/planilha de controle externo de repetição).
7. **Como tratar tópicos que não fecham 1-para-1** com o Tec (sem assunto correspondente, sem aula do Estratégia, ou assunto compartilhado entre tópicos mestres).

Depois de receber os parâmetros iniciais, a skill segue perguntando o que for surgindo caso a caso — Elvis pediu explicitamente pra perguntar ao longo do processo, não acumular dúvida.

Os filtros que já são padrão fixo e **não** precisam ser perguntados: remover questões anuladas e desatualizadas; "Organizar por: Relevância (apenas assuntos)"; "Popular com questões: Mais Recentes" (ver [[feedback_skill_tec_filtros_padrao]] e [[feedback_tec_organizar_por_relevancia]]).

**Why:** os parâmetros mudam completamente o caderno gerado, e errar isso só aparece depois que o aluno já está estudando o material errado. Perguntar custa uma mensagem; refazer custa a rodada inteira.

**How to apply:** já escrever a skill com esse bloco de abertura no passo 1, antes de qualquer navegação.
