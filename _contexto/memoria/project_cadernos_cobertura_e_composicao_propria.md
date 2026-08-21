---
name: project-cadernos-cobertura-e-composicao-propria
description: "O caderno é composto por nós para cobrir o máximo de assuntos, distribuindo as questões de cada ponto entre os níveis; o gerador do Tec não serve para isso"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T23:58:18.640Z
---

Definido pelo Elvis em 2026-08-20, depois do primeiro teste real de criação de cadernos.

## O objetivo é COBERTURA, não evitar repetição

O caderno tem que alcançar o **máximo de assuntos**. A distribuição das questões de um mesmo
ponto entre os níveis segue esta lógica:

```
ponto com 5 questões  ->  1 no N1, 1 no N2, 1 no N3, 1 no N4, 1 no N5
ponto com 2 questões  ->  1 no N1, 1 no N2, e no N3/N4 REPETE as duas
```

**Repetir é aceitável e esperado** quando o acervo do ponto acaba. O que não se aceita é o
aluno chegar ao N3 sem ter revisto um assunto que ele viu no N1.

## O gerador do Tec NÃO serve para compor

Ele só ordena por **recência** ou **aleatório**, sem nenhuma noção de cobertura por assunto.
Medido em 2026-08-20 com cadernos reais de Direito Administrativo:

| Comparação | Sobreposição |
|---|---|
| N1 dentro do N2 (mesmo assunto) | 6 de 15 |
| N1 dentro do N3 | **0 de 15** |
| N1 dentro do N5 | **0 de 15** |
| N2 dentro do N3 | **0 de 30** |
| N3 dentro do N5 | 30 de 40 |
| N6 Ouro da aula dentro do N7 Ouro da disciplina | 10 de 10 |

Os zeros **não são diversidade, são buraco de cobertura**: com escopo amplo e ordem por
recência, o N3 e o N5 pegam as mais recentes da disciplina inteira e nunca alcançam as do
tópico que o aluno treinou.

**A composição tem que ser nossa**, distribuindo ponto a ponto, e injetada por
`adicionar-questoes-por-codigo`. O gerador do Tec vira ferramenta de **contagem**, não de
composição.

## Pré-requisito que faltava

**Registrar em planilha nossa quais questões entraram em cada caderno.** O Tec não expõe isso
na API (`/api/cadernos/{id}/questoes` dá 404) e o link do caderno só mostra na tela. Sem esse
registro não há controle de cobertura nem de repetição.

## Bancas: só três

`OURO GERAL` + **Cebraspe**, **FGV** e **FCC**. Não abrir bloco para outras bancas.

⚠️ **Não filtrar por banca no fichamento.** Filtrando na entrada, todas as questões saem da
mesma banca e o bloco de banca fica idêntico ao geral. A banca é **coluna do fichamento**, não
filtro de entrada. Puxar todas e separar depois.

## Ponto que derruba entra mesmo sozinho

A regra "só entra ponto com mais de uma questão" descartava, num caso real, justamente a
questão de **44,3% de acerto** — a que mais derrubava no tópico. Regra corrigida:

> entra o ponto com **mais de uma questão** **ou** com **índice de acerto abaixo de 50%**

Ver [[project_bizurito_fontes_e_validacao]], [[project_niveis_caderno_tec_e_pesos]] e
[[reference_tec_api_desempenho_e_filtros]].
