# O que esta base precisa saber

> Extrato de `../DECISOES.md`, so com o que afeta esta base. O arquivo central continua sendo a
> referencia completa; aqui esta o essencial, para a sessao nao gastar contexto com decisao de
> outra base.

## As 21 disciplinas e suas siglas

`AFO` `ADMPUB` `AUDIT` `CONTAB` `CONTPU` `CUSTOS` `CTREXT` `DADM` `DCIVIL` `DCONST` `DEMPRE`
`DPENAL` `DTRIB` `ECOFIN` `ESTAT` `LTRIB` `MATFIN` `PORT` `RACLOG` `REFTRI` `TECINF`

Sigla de 4 a 6 letras, com `AFO` como unica excecao de 3. A lista completa com os nomes esta na
secao A8 do arquivo central.

## O formato do codigo

`SIGLA-NNNN`, quatro digitos.

| Faixa | O que e |
|---|---|
| `0001` a `4999` | vem do Curso Regular |
| `5000` | **nunca existe**, e a fronteira |
| `5001` em diante | nasce em pos-edital |

**A origem e coluna, nunca prefixo.** O codigo identifica **conteudo**; o mesmo topico pode
aparecer em varios concursos.

## Area e LISTA, nao coluna

Nunca criar colunas `Fiscal` e `Controle`. Uma linha por par (disciplina, area), para a area
**Legislativa** entrar depois sem mexer em nada.

## Apelidos: cada fonte guarda o nome dela

O nosso nome **identifica**; o da fonte **localiza**. Uma linha por par (disciplina, fonte, nome
na fonte). E por esse nome que o aluno acha o material dentro daquela fonte.

```
TECINF | Estrategia Regular Controle | "Analise de Informacoes"
TECINF | Estrategia Regular Fiscal   | "Informatica"
TECINF | Bezerra                     | "Tecnologia"
```

## O escopo vem do Curso Regular

O que nao esta no Curso Regular **nao entra** por padrao. Foi assim que Direito Processual Civil
ficou de fora: aparecia no ciclo de estudo, mas nao existe em nenhum dos dois Regulares.

## A familia tributaria sao quatro disciplinas

| | O que e | Quando existe |
|---|---|---|
| `DTRIB` | Direito Tributario | sempre |
| `REFTRI` | Reforma Tributaria | sempre (o conteudo hoje esta dentro de `DTRIB` no material) |
| `LTRIB` | Legislacao Tributaria, **parte geral**, com a **Lei Kandir** | sempre |
| local | legislacao estadual ou municipal | **so no pos-edital** |

## O padrao de nome do Estrategia e INVERTIDO entre os dois cursos

Quem for extrair a materia do nome do curso precisa das duas regras:

```
Fiscal:    "Concursos da Area Fiscal - Curso Basico de <MATERIA>"
Controle:  "Concursos de Tribunais de Contas (Nivel Superior) <MATERIA> - Curso Regular"
```

No Fiscal a materia vem **no fim**; no Controle vem **no meio**, antes do sufixo. Uma regra so
nao pega os dois.

## `tipo_curso_id = 1` NAO garante que e disciplina

Medido em 22/08/2026: **"Sistema de Questoes 1 Ano - Cartao ate 12 x"** (id 143237) vem como
`tipo_curso_id = 1`, igual a uma disciplina, e e **assinatura**.

Filtrar por tipo nao basta. Conferir o nome e excluir explicitamente o que nao for materia.

---

**Duvida sobre algo que nao esta aqui?** Consulte `../DECISOES.md`.
**Licao aprendida nesta base?** Escreva em `APRENDIZADO.md`, nao aqui.
