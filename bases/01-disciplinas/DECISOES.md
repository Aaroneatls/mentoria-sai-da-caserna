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

---

**Duvida sobre algo que nao esta aqui?** Consulte `../DECISOES.md`.
**Licao aprendida nesta base?** Escreva em `APRENDIZADO.md`, nao aqui.
