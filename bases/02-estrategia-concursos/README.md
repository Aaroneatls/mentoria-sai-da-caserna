# Base 2 — Estrategia Concursos

Os blocos de estudo cortados dos PDFs do Estrategia: onde o aluno estuda cada topico, com pagina de inicio e de fim.

> **Antes de comecar, ler `../DECISOES.md`.** As decisoes fechadas com o Elvis estao la, e
> nao devem ser reabertas sem motivo novo.

## O que esta base produz

- Um bloco por trecho de 5 a 12 paginas, cortado em ponto de titulo
- `INICIE EM` e `TERMINE EM`, **literais do PDF**
- O hash da teoria, que e o que permite dizer se duas areas compartilham o mesmo topico

## Do que ela depende

Dos PDFs baixados. **Nao depende do Tec.**

## A skill

`mapear-blocos-estrategia` com tres modos:

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
