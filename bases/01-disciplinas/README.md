# Base 1 — Disciplinas

O nome canonico de cada disciplina e a sigla que abre o Cod Mestre. E a base mais simples e a mais importante: **e dela que sai a numeracao de todo o resto**.

## O que esta base produz

- Nome canonico da disciplina, com os apelidos que aparecem em cada fonte
- A sigla de tres a cinco letras (`DADM`, `AFO`, ...)
- O registro do proximo numero livre em cada sigla

## Do que ela depende

Dos nomes dos cursos que ja estao baixados. **Nao depende do Tec.**

## A skill

`montar-base-disciplinas` com tres modos:

| Modo | O que faz |
|---|---|
| `criar` | monta a base do zero |
| `atualizar` | roda o diff e aplica so o que mudou |
| `conferir` | roda as verificacoes **sem escrever nada** |

O modo `conferir` existe porque em 21/08/2026 foi conferindo antes de executar que se
descobriu um filtro faltando, o que teria gasto ~600 chamadas para produzir dado errado.

## Aprendizado

Ver `APRENDIZADO.md` nesta pasta. **Toda licao aprendida aqui entra la**, inclusive as que
vierem depois. Aprendizado nao se arquiva.
