---
name: montar-base-disciplinas
description: Monta, atualiza ou confere a Base 1 do projeto de mapeamento (a tabela mestra das 21 disciplinas, com as siglas que abrem todo Cód Mestre, os apelidos que cada fonte usa e as áreas). Use quando o usuário disser "montar a base de disciplinas", "atualizar as siglas", "conferir a base 1", "surgiu matéria nova no Estratégia", "o Bezerra lançou matéria nova", ou quando outra base precisar da sigla de uma disciplina e ela não existir ainda.
---

# Base 1 — Disciplinas

A tabela mestra das **21 disciplinas**. É a base mais simples e a mais crítica: **nada pode ser
numerado antes dela**, e o código publicado na Tutory **nunca pode mudar**, porque é por ele que
a plataforma reconhece que o aluno já estudou aquilo.

Ler antes: `bases/IMPACTOS.md`, `bases/01-disciplinas/ROTEIRO.md` e o `DECISOES.md` daquela pasta.

## Os três modos

| Modo | O que faz | Escreve? |
|---|---|---|
| `conferir` | roda as 8 validações e relata | **não** |
| `criar` | monta do zero | sim |
| `atualizar` | diffa as fontes contra os CSV e aplica só o que mudou | sim, só o que mudou |

**`conferir` é o modo padrão quando houver dúvida.** Rodar antes de qualquer `criar` ou
`atualizar`:

```bash
python bases/01-disciplinas/conferir.py
```

## Onde o dado mora

```
fontes/     materia-prima bruta, uma por camada de fonte. NUNCA editada a mao pela skill.
dados/      a FONTE DE VERDADE, em CSV, versionada no git.
SEM-DONA.md leitura gerada do filtro `status`. Nunca editar a mao.
```

A planilha do Google é **vista descartável**, regerável do CSV a qualquer hora. Se as duas
divergirem, **o CSV ganha** e a planilha se refaz.

### Os arquivos

| Arquivo | O que guarda |
|---|---|
| `dados/disciplinas.csv` | `sigla, nome_canonico, observacao` — as 21, transcrição da seção A8 |
| `dados/apelidos.csv` | `sigla, fonte, camada, id_na_fonte, nome_na_fonte, status, professor, observacao` |
| `dados/areas.csv` | `sigla, area, evidencia` — uma linha por par, **nunca** coluna |
| `dados/renomear-pastas.csv` | contrato com a skill de download: nome exato no disco → nome novo |

## As sete regras que não se quebram

**1. O contador NÃO se guarda, se DERIVA.** O próximo número de uma sigla é o maior usado mais
um, lido do registro de tópicos. Contador gravado desincroniza: se um mapeamento falhar no meio,
ele avança sem os tópicos existirem e some um número. Enquanto a base 2 não produzir, tudo é
`0001`.

**2. Área é LISTA, nunca coluna.** Jamais criar colunas `Fiscal` e `Controle`. Uma linha por par
`(sigla, area)`, para a área **Legislativa** entrar depois sem mexer em nada. **Fonte também é
lista**, pelo mesmo motivo.

**3. O `nome_na_fonte` é LITERAL, byte a byte.** Não consertar acento, não consertar maiúscula,
não consertar erro de digitação. `Direito Tribubário` vai com dois B. Ele é **chave de busca
dentro da fonte**, não texto de leitura: o nosso nome identifica, o da fonte **localiza**.

**4. A coluna `camada` existe porque `drive` e `plataforma` têm granularidade diferente.**
Medido em 22/08/2026: o Regular Fiscal tem **22 pastas para 25 cursos**, porque quem criou as
pastas consolidou três Reformas numa e não baixou a Discursiva. **Nome de pasta é dado derivado;
nome de plataforma é dado bruto.** Montar apelido só pela pasta esconde disciplina.

**5. A pasta NUNCA é fonte do `.txt`.** O `fontes/estrategia.txt` guarda o nome **como a
plataforma mostra**, e só muda quando o Estratégia mudar. O nome da pasta é derivado dele. Ler o
Drive para regenerar o `.txt` importaria a **nossa** sigla de volta para dentro de um arquivo que
existe para registrar o nome **da fonte**, e a base passaria a "descobrir" na fonte um nome que
nós mesmos inventamos.

**6. O `atualizar` roda OFFLINE.** Ele diffa `fontes/*.txt` contra os CSV. **A base 1 nunca entra
no Estratégia**, e assim nunca disputa vaga do rodízio de matrícula. Quem já está logado atualiza
o `.txt`; a skill compara. **Exceção única:** o Tec, cuja lista de matérias ninguém mais puxa.

**7. Nunca gravar o texto da marca d'água.** Os PDFs do Estratégia trazem `<CPF> - <Nome>` na
camada de texto. É dado pessoal de pessoa real. A validação 7 do `conferir.py` procura por CPF em
todos os CSV e falha se achar.

## Modo `criar`

1. `disciplinas.csv` a partir da **seção A8** do `bases/DECISOES.md`. Transcrição, zero
   interpretação.
2. Levantar as fontes que faltarem em `fontes/`. A única que a skill puxa sozinha é o Tec:
   `GET /api/materias?universo=&formato=OBJETIVA` — **1 chamada**, e vale o
   `bases/05-questoes-tec/REGRAS.md` (429 = o dia acabou, sem retentativa; CAPTCHA é do Elvis).
3. Conciliar cada fonte contra as 21, gerando uma linha por par. **O casamento é
   muitos-para-muitos nos dois sentidos**: o Tec junta AFO com Contabilidade Pública numa matéria
   só (id 69), e fatia TI em nove.
4. O que não casar recebe `status` e vai para o `SEM-DONA.md`, **nunca é forçado dentro de uma
   sigla nem ignorado em silêncio**.
5. `areas.csv` pela evidência de qual Regular **de fato** tem o curso.
6. Rodar `conferir.py`. **Só publicar depois que passar.**

## Modo `atualizar`

1. Rodar `conferir.py` **antes**.
2. Diffar `fontes/*.txt` contra `dados/*.csv`.
3. **Nunca sobrescrever o que não mudou.** Escrever em `.tmp` e renomear só depois da validação.
4. **Sigla existente NUNCA muda.** Se um nome de fonte mudou, muda o `nome_na_fonte`, não a
   sigla. Disciplina nova ganha sigla nova; disciplina que sumiu da fonte é **marcada**, nunca
   apagada, porque pode haver aluno com o código publicado.
5. Registrar em `bases/IMPACTOS.md` o que mudou e **qual base isso afeta**.

## Modo `conferir`

Roda `conferir.py` e relata. Não escreve nada. Os 8 blocos: as 21 e o formato da sigla;
integridade referencial; nenhuma linha de fonte perdida; área como lista; ausência de contador
gravado; orçamento de 45 caracteres da nomenclatura; **ausência de CPF**; e toda sigla com pelo
menos um apelido e uma área.

## Com quem esta base conversa

| Base | O que puxa daqui |
|---|---|
| 2 · Estratégia | a **sigla** (nome de pasta e numeração) e o **apelido** (qual pasta abrir) |
| 3 · Taxonomia do Tec | a sigla, e o **`id_na_fonte` da matéria do Tec**, que é o parâmetro da chamada dela |
| 4 · Parceiros | o apelido do Bezerra, e o registro de **"não cobre"** quando ele não tem a matéria |
| 5 · Questões do Tec | a sigla, para pendurar a questão no tópico certo |
| 6 · Editais | o apelido do edital, para avisar o aluno quando o nome divergir do nosso |

## Ao terminar

Avaliar se algo aprendido nesta rodada sugere ajuste na própria skill. Se sim, apresentar a
sugestão e **pedir aprovação antes de editar**. Se nada novo surgiu, dizer isso de forma curta,
sem inventar sugestão. Nunca editar a skill nem sincronizar sem aprovação.
