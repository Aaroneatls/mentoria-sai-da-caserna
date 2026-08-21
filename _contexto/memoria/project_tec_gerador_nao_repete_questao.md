---
name: project-tec-gerador-nao-repete-questao
description: O gerador de cadernos do Tec exclui sozinho questões já usadas em cadernos anteriores da conta — pedir N não garante receber N
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T19:15:56.797Z
---

Descoberto em 2026-08-19, na primeira execução real de cadernos de Nível 1 (DADM-001 a DADM-010).

Ao gerar cadernos em sequência, o TecConcursos **exclui automaticamente as questões que já
estão em cadernos anteriores da conta**. Não avisa, não dá erro — simplesmente entrega menos
questões do que o pedido.

**Prova concreta:** o assunto 497 ("Origem, Conceito e Fontes do Direito Administrativo")
tinha 16 questões no filtro. O caderno do DADM-001 pediu 10 e levou 10. O do DADM-002, com
**filtro exatamente igual**, pediu 13 e recebeu **só as 6 restantes**. Intersecção entre os
dois: zero. Nos 10 cadernos gerados, as 90 questões saíram todas distintas.

## O que isso muda no desenho

1. **Conferir sempre o resultado**, nunca assumir que o caderno saiu com a quantidade pedida.
   Ler `GET /api/cadernos/{id}/gabarito` depois de gerar.
2. **A ordem de geração importa.** Quem gera primeiro fica com as questões mais recentes
   (quando se usa "Mais Recentes"). Gerar na ordem de prioridade do plano de estudo.
3. **O controle externo em planilha continua valendo**, mas muda de papel: deixa de ser a
   única barreira contra repetição e passa a ser **registro e conferência** — saber qual
   questão foi pra qual caderno, e detectar caderno que saiu menor que o previsto.
4. Isso **não** substitui o controle nosso nos casos em que a repetição é desejada (níveis 2
   a 7 podem precisar reaproveitar questão quando não há alternativa no banco — ver
   [[project_niveis_caderno_tec_e_pesos]]). Ainda não sabemos se dá pra desligar o
   comportamento.

**Ainda não verificado:** se a exclusão vale contra cadernos de sessões antigas ou só contra
os gerados na mesma sequência. Os 10 cadernos do teste foram criados na mesma rodada.

**Why:** a regra que estava desenhada partia do princípio de que o Tec não controlava
repetição e que tudo dependia de planilha nossa. Metade disso é falso, e a outra metade tem
um efeito colateral perigoso — caderno saindo menor que o planejado sem ninguém perceber.

**How to apply:** na skill de cadernos, incluir passo obrigatório de conferência pós-geração
comparando pedido x recebido, e sinalizar diferença no relatório. Ver
[[feedback_skill_cadernos_perguntar_parametros_iniciais]].
