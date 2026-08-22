# ESP-DISCIPLINAS

**Base 1 — a tabela mestra das disciplinas.** É de onde sai a sigla que abre todo Cód Mestre.

| | |
|---|---|
| **Possui** | `bases/01-disciplinas/` inteiro |
| **Entrega** | `dados/disciplinas.csv` · `dados/apelidos.csv` · `dados/areas.csv` · `dados/renomear-pastas.csv` · `conferir.py` · `SEM-DONA.md` |
| **Skill** | `montar-base-disciplinas` (`criar` · `atualizar` · `conferir`) |
| **Nunca toca** | o Estratégia (não entra na plataforma), as pastas do Drive, as skills de download |

## Como ele trabalha

O `atualizar` roda **offline**: diffa `fontes/*.txt` contra os CSV. Quem está logado atualiza os
`.txt`; ele compara. Assim nunca disputa vaga do rodízio de matrículas.

## Estado em 22/08/2026

`21 disciplinas · 431 apelidos · 31 áreas · 34 pastas (31 prontas, 3 pendentes)`
`conferir.py` com 10 blocos passando · amostragem cega da Tutory 30/30, semente 20260822

**Pendente do Elvis:** a pasta `Reforma Tributaria` (guarda `LTRIB` e `REFTRI` juntas), se os cursos
220891 e 220896 são `LTRIB`, e as 8 entradas do balde 1 do `SEM-DONA.md`.
