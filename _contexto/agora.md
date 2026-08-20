# Onde paramos — 20/08/2026

## O que existe hoje

**Três planilhas vivas:**

| Planilha | O que tem |
|---|---|
| [Base Direito Administrativo](https://docs.google.com/spreadsheets/d/1NTCKDD5gnjXrgrl9WLxYocNtxHpJFhUu97Y7ppo_e4U) | 95 blocos, amarrados ao edital do TCDF, com colunas de área e aba de cobertura |
| [Base Curso Regular Controle (multidisciplina)](https://docs.google.com/spreadsheets/d/1_p7bfZ9lMyoBnF8MMuLGjLrFOw8AvSM_-lcyKKCd8sI) | 395 blocos em 8 disciplinas, com nível de confiança por disciplina |
| [Banco de Fichamento — esquema](https://docs.google.com/spreadsheets/d/1smaWxs7p36ihz08e1RizwRd25AnXyn-H9BCoMmeM_64) | as 3 abas com as colunas do BIZURITO já criadas |

## O método, em uma frase

Os títulos saem da **tipografia do PDF** (o corpo de fonte é medido em cada arquivo, não fixado),
o corte é **em ponto de título** com alvo de 10 páginas, e a página é sempre a **do arquivo**.
Nada vem do sumário.

## O que está travado

**TecConcursos: HTTP 401.** A API precisa da sessão logada no navegador. Sem o Elvis, não dá para
fichar questão nem gerar caderno. Isso bloqueia, em cascata: a Curva ABC própria, os cadernos dos
7 níveis e o BIZURITO (que só nasce de questão fichada).

## O que precisa de decisão

1. As 8 matérias escolhidas foram as do Regular Controle que casam com o edital do TCDF. Confirmar.
2. **Administração Pública** e **Auditoria Governamental** saíram com confiança BAIXA — título e
   corpo usam o mesmo tamanho de fonte. Precisa do detector de nível 2 por par de linhas roxas.
3. Formato do Cód Mestre específico de edital: `DADM-TCDF-001`.
4. Os 7 pontos de decisão de `estrategia-padroes-pdf.md` e a seção 7 de `briefing-bizurito.md`.

## Próximo passo natural

Implementar o detector de nível 2 (par de linhas roxas + tipografia, exigidos juntos), que
destrava as duas disciplinas de confiança BAIXA e é pré-requisito para Português e Direito
Constitucional em outros pacotes.

Depois, com o Elvis presente: fichamento no Tec → Curva ABC própria → cadernos → BIZURITO.
