# Base 3 — Taxonomia do Tec

A arvore de assuntos do TecConcursos, por materia. Serve de palpite inicial para o topico mestre e de vocabulario comum com a plataforma.

> **Antes de comecar, ler `../DECISOES.md`.** As decisoes fechadas com o Elvis estao la, e
> nao devem ser reabertas sem motivo novo.

## O que esta base produz

- A arvore completa, com id, nome e hierarquia (`01.02.03`)
- O vinculo assunto do Tec -> Cod Mestre

## Do que ela depende

De uma chamada por materia (`/api/assuntos?materia={id}&hierarquico=true`). ~146 chamadas para a plataforma inteira, uma vez so.

## A skill

`mapear-taxonomia-tec` com tres modos:

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
