# Base 6 — Editais

O programa de cada concurso, item a item, ligado ao Cod Mestre. E a fonte que manda no pos-edital: define o que entra e o que fica de fora.

## O que esta base produz

- Um registro por item de edital, com o texto literal
- O vinculo item -> Cod Mestre
- Os itens **sem** correspondencia, que sao o alerta

## Do que ela depende

Dos PDFs de edital. **Nao depende do Tec.**

## A skill

`mapear-editais` com tres modos:

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
