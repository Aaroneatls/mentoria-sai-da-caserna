---
name: project-recencia-na-selecao-de-questoes
description: "Ao montar caderno, selecionar as questões mais recentes — mas dentro da cota de cada tópico, nunca no geral, e respeitando o marco legal de cada assunto"
metadata:
  type: project
---

Levantado pelo Elvis em 2026-08-20. **Ponto para debater antes de fechar a skill de cadernos.**

## O que ele pediu

A estatística continua saindo de **10 anos** de questões. Mas na hora de **selecionar** as que
entram no caderno, pegar as **mais recentes**. Se o levantamento tem 1.000 questões e o caderno
leva 50, que sejam as 50 mais novas — respeitando os outros critérios (concentração de
conteúdo, banca, nível).

## A armadilha: recência global destrói a cobertura

Pegar "as 50 mais recentes" do bolo inteiro é o jeito errado. As últimas 50 questões de uma
disciplina costumam se concentrar em 3 ou 4 tópicos — os que estiveram em alta nos últimos
concursos. O aluno recebe um caderno que ignora metade do edital.

**A recência tem que ser aplicada DENTRO da cota de cada tópico, não no bolo.**

```
1. Distribuir as 50 vagas entre os tópicos, pelo peso (Curva ABC)
2. Dentro de cada tópico, ordenar por data e pegar as mais recentes até preencher a cota
3. Se o tópico não tiver questões suficientes no período, alargar o período só naquele tópico
```

Assim a cobertura vem da cota e a atualidade vem da ordenação.

## Recência não é só preferência: existe marco legal

Em vários assuntos, questão antiga não é "menos boa" — é **inservível**, porque cobra texto
revogado:

| Assunto | Marco | O que acontece antes |
|---|---|---|
| Licitações | Lei 14.133/2021 | cobra a Lei 8.666, revogada |
| Improbidade | Lei 14.230/2021 | cobra dolo/culpa no regime antigo |
| Agentes públicos | EC 103/2019 | regras de aposentadoria antigas |

Então cada tópico precisa de uma **data-marco** própria: abaixo dela a questão é descartada, não
apenas despriorizada. Isso é diferente do "preferir a mais nova" e tem que ser um campo à parte
na base.

## Repetir questão entre níveis é PERMITIDO (Elvis, 2026-08-20)

O gerador do TecConcursos não repete questão entre cadernos
([[project_tec_gerador_nao_repete_questao]]), mas isso **não é uma restrição a respeitar**: o
Elvis liberou repetir quando fizer sentido. Tenta-se evitar, não se sacrifica qualidade por
isso.

**O Nível 1 leva as melhores questões**, não as sobras. Escalonamento por qualidade, e a
distribuição por Curva ABC garante a cobertura. Vale igual no pós-edital.

## O que ele realmente queria com "as mais recentes"

Esclarecido por ele: a preocupação **não é recência por si**, é **não entregar questão
desatualizada**. Então:

- **Marco legal = filtro duro.** Questão que cobra texto revogado sai, ponto.
- **Recência = critério de desempate** dentro da cota do tópico, depois do marco legal e da
  ordem de banca.

## O que isso exige da base

A **data da questão** precisa estar gravada no fichamento, junto com banca, órgão e ano. Sem
isso não há como ordenar. Ver [[project_banco_fichamento_questoes]].

Ver também [[project_niveis_caderno_tec_e_pesos]] (cotas por nível e Curva ABC) e
[[feedback_skill_cadernos_perguntar_parametros_iniciais]].
