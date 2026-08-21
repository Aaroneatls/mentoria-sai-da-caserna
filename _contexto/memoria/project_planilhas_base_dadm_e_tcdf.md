---
name: project-planilhas-base-dadm-e-tcdf
description: "As duas planilhas do teste de 2026-08-19: Base DADM (Regular Controle, pré-edital) e Simulação Pós-Edital TCDF 2026 — URLs, abas e o que cada uma valida"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T22:11:49.805Z
---

Criadas em 2026-08-19, na pasta `Inteligência Artificial/Projetos/` do Drive. São o primeiro
teste do formato completo (taxonomia → pontos → fichamento → pesos → plano de cadernos).

## Planilha 1 — Base DADM, Regular Controle (pré-edital)

`https://docs.google.com/spreadsheets/d/1TPbze8gWTzgjtCJVXUbK_ZfXptPM_0F7YuTW-zEdO_0`

**Abas:** Taxonomia · Pontos · Questões Fichadas · Questão x Ponto · Pesos por Banca.

**Recorte:** Estratégia curso **Regular Controle**, Aulas 00, 01 e 17 (perfis diferentes de
propósito: conceitual, definicional e lei seca). Bezerra R00, R01 e R16. TecConcursos matéria 1,
área Controle, **Cebraspe + FGV + FCC**, 2017-2026, sem anuladas, desatualizadas nem inéditas.

**Números:** 178 questões (Cebraspe 125, FGV 46, FCC 7) · 10 tópicos mestres · 48 pontos.

## Planilha 2 — Simulação Pós-Edital TCDF 2026

`https://docs.google.com/spreadsheets/d/1Iyx9xHB0WcZ_XBM3EN74txt_5nIXglXio49lf9wNQ38`

**Abas:** Cruzamento do Edital · Pesos e Elegibilidade (Cebraspe) · Plano de Cadernos (N1).

Reaproveita a base de questões da planilha 1. Aplica o peso da **Cebraspe** com fallback pro
composto quando a amostra do ponto é menor que 3. **Nenhum caderno foi criado no Tec.**

## O que o teste validou

- Peso composto x peso por banca lado a lado, com alerta automático de amostra pequena.
- Elegibilidade por cobertura: ponto sem teoria em nenhuma fonte é excluído do Nível 1 e vira gap.
- Cruzamento edital → aula do curso do concurso → tópico mestre, com situação por item.
- **Dois gaps confirmados** em Direito Administrativo: **segregação de funções** e **verdade
  material** — nenhuma das duas fontes ensina.

## Limitação conhecida desta versão

A distribuição questão → ponto foi feita **pelo assunto do Tec**, não pela leitura de cada
questão. Resultado: 891 pares para 178 questões (~5 pontos por questão), irreal. O peso total
fica certo (cada questão distribui 1/N), mas **espalhado em vez de concentrado** — e é a
concentração que diz qual ponto é mais cobrado.

Comparação: nas 37 questões lidas de verdade antes, a atribuição saiu com 1 ou 2 pontos cada.

**Conclusão do teste: a estrutura está validada, o número ainda não.** Fechar exige a leitura
questão a questão. Ver [[project_banco_fichamento_questoes]].

## Lição operacional

Navegar a aba do navegador **apaga as variáveis da página** — o fichamento guardado em
`window.__F` se perdeu ao abrir as planilhas, e foi preciso rebuscar 178 enunciados. Ao rodar
coleta longa, **usar aba dedicada** e não navegar nela, ou persistir em disco antes de sair.
