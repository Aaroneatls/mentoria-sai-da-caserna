# Base 5 — Questoes do Tec

O acervo de questoes, com enunciado, alternativas e gabarito, mais a camada de **ponto** que sai da leitura. E a base que alimenta os cadernos.

## O que esta base produz

- A questao: enunciado, alternativas, gabarito, banca, ano, orgao
- O **ponto** que cada questao cobra, que so existe porque alguem leu
- O vinculo ponto -> Cod Mestre

## Do que ela depende

Da **impressao**, 1.000 questoes por dia, dentro do teto que o Tec publica. Ver `REGRAS.md` nesta pasta, que valem acima de qualquer conveniencia.

## A skill

`coletar-questoes-tec` com tres modos:

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
