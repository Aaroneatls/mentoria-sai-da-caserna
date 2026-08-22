# Aprendizado — Base 1 — Disciplinas

> Este arquivo **cresce**. Toda licao aprendida trabalhando nesta base entra aqui, com a data e
> com o custo que ela teve. Aprendizado nao se arquiva junto com o dado.

## 22/08/2026 · Nome de pasta e dado DERIVADO, e esconde disciplina

O plano original montava os apelidos do Estrategia so pelos nomes das pastas do Drive. Ao pedir
a lista de cursos da plataforma, a conta nao fechou:

```
22 pastas no Drive  x  25 cursos tipo 1 na plataforma
  21 casam 1 pra 1
  +1 "Curso Basico de Discursiva", que ninguem tinha baixado
  +2 Reforma Tributaria, que na plataforma sao TRES cursos e no Drive e UMA pasta
```

Quem criou a pasta ja consolidou na mao. **A camada de pasta perde informacao; a de plataforma e
bruta.** Se a base tivesse nascido so das pastas, tres cursos ficariam invisiveis para sempre.

**Mas o grau de derivacao varia por area:** o Regular Controle casou **12 pra 12**, exato. Nao da
para confiar nem desconfiar da pasta em bloco; confere-se contra a plataforma, area por area.

**Custo se tivesse passado:** a Discursiva e as duas Reformas extras nunca apareceriam, e o aluno
seria mandado para um curso que a base nao sabe que existe.

## 22/08/2026 · A pasta nunca pode ser fonte do `.txt` (achado da sessao de mapear aulas)

Eu propus regenerar `fontes/estrategia.txt` lendo as pastas do Drive depois da renomeacao, para
o modo `atualizar` nao comparar contra nomes velhos. **Era circular**: as pastas vao ganhar o
**nosso** prefixo de sigla, entao a base 1 passaria a "descobrir" na fonte um nome que nos mesmos
inventamos.

A regra que ficou: **o `.txt` guarda o nome como a plataforma mostra, e so muda quando o
Estrategia mudar. O nome da pasta e derivado dele, nunca fonte dele.** Conferir a pasta continua
valendo, mas como *check de coerencia separado* ("a pasta bate com o que o CSV mandou criar?"),
nunca como fonte.

## 22/08/2026 · Nome literal e otimo para localizar e pessimo para casar

A regra do projeto manda gravar `nome_na_fonte` literal, com acento errado e erro de digitacao
preservados (`Direito Tribubario` com dois B). Esta certa: e chave de busca dentro da fonte.

**O efeito colateral apareceu na hora do join.** Quem precisa preencher `Cod Mestre` nas planilhas
so teria o nome para casar, contra um campo mantido sujo de proposito. Solucao: o `id_na_fonte`
deixou de ser exclusivo do Tec e passou a valer para o Estrategia tambem, com o `curso_id`.

**Regra geral:** onde a fonte oferecer id numerico, guardar o id. **Nome literal serve para
achar; id serve para casar.** Os dois convivem, nao competem.

## 22/08/2026 · O Tec junta o que a gente separa, e separa o que a gente junta

O casamento com o Tec e **muitos-para-muitos nos dois sentidos**:

| Materia do Tec | Vira | O que isso significa |
|---|---|---|
| 69 · AFO, Direito Financeiro e Contabilidade Publica | `AFO` **e** `CONTPU` | 1 materia -> 2 disciplinas nossas |
| 37 · Auditoria Governamental e Controle | `AUDIT` **e** `CTREXT` | 1 materia -> 2 disciplinas nossas |
| 4 · Informatica + as 9 `TI - ...` | `TECINF` | 10 materias -> 1 disciplina nossa |

**Consequencia direta para as bases 3 e 5:** filtrar questao **por materia** nao isola disciplina
nossa. Pedir a materia 69 traz AFO misturada com Contabilidade Publica. O corte tem de ser por
**assunto**, um nivel abaixo. Descobrir isso agora custou 1 chamada; descobrir na base 5 custaria
um acervo inteiro contaminado.

## 22/08/2026 · Medir antes de aceitar, mesmo vindo de outra sessao

Duas vezes um dado chegou pronto e a medicao mudou a conclusao:

1. O `renomear-pastas.csv` "casava por string exata". Nao casava: o disco tem o sufixo
   ` (Regular Fiscal) (18-08-2026)` que o nome da fonte nao tem. **0 de 32 por igualdade.**
   Corrigido gravando o nome completo do disco, o que devolve o join para igualdade em vez de
   mandar todo mundo usar `startswith`.
2. A secao **A8 estava errada**. Ela afirma que o Regular Controle tem `CONTAB`, `ESTAT` e
   `ECOFIN`. Conferido nos **dois** pacotes do Controle (365538 e 224364, listas de disciplina
   identicas): so o `CONTAB` existe.

## 22/08/2026 · 404 nao quer dizer "nao existe"

Em `/api/aluno/pacote/{id}` do Estrategia, **404 significa nao matriculado**. Produto que existe
e esta fora da matricula devolve 404; o endpoint de **curso** devolve **500** no mesmo caso.
Assimetria da API, nao estado do produto. Tratar 404 como "acabou" faria a skill descartar
material que esta la.

## 22/08/2026 · A marca d'agua e trava de vazamento, nao detalhe de hash

Os PDFs trazem `<CPF> - <Nome do titular>` na camada de texto, em quase toda pagina, capa
inclusive. Descrito primeiro como "hash nao serve", o que e verdade mas e pequeno demais: se a
extracao rodar antes do filtro, **o CPF entra no nome do arquivo** e vira dado pessoal no caminho
da pasta, sincronizado pro Drive e visivel em qualquer print.

Virou a **Regra 8** do `bases/NOMENCLATURA.md`, e virou a **validacao 7** do `conferir.py`, que
falha se achar 11 digitos em qualquer CSV desta base.

**A licao maior:** um achado tecnico pequeno pode ser um risco grande com outro nome. Vale
perguntar sempre "o pior caso disto e so tecnico?".

## 22/08/2026 · Cobertura nao e correcao: validar por amostragem

As 168 entradas da Tutory foram classificadas por regra (regex ordenada), e eu tinha provado que
**zero** ficou sem regra. Isso prova **cobertura**, nao **correcao**: regra casa errado em
silencio.

Aplicada a regra de validacao por amostragem que o projeto ja usa no cache do mapeamento:
**30 entradas sorteadas (18%), semente fixa `20260822`, classificadas a mao antes de olhar o que a
regex deu**. Resultado: **30/30**. Nao e certeza absoluta, mas troca "e o ponto mais fraco da
base" por um teto de erro medido.

**Regra que fica:** ponto fraco que ninguem testa continua fraco para sempre. Se der para medir,
mede-se, mesmo que a medida seja parcial.

## 22/08/2026 · Falha silenciosa com aparencia de sucesso: o caso MATFIN

A pasta `Raciocinio Logico e Matematica` do Regular Fiscal foi marcada `RACLOG`, com observacao de
que o nome mistura `MATFIN`. Parecia inofensivo. Nao era:

```
MATFIN tinha material no Controle  ->  a tabela PARECIA completa
MATFIN nao tinha nada no Fiscal    ->  e ninguem perceberia
```

E o **mesmo** problema das materias 69 e 37 do Tec (uma entrada da fonte para duas disciplinas
nossas), que ja tinha sido resolvido certo com duas linhas. **A solucao existia e nao tinha sido
aplicada por analogia.**

Corrigido: a pasta virou **duas linhas**, `RACLOG` e `MATFIN`, com o vinculo explicito e pendente
de refino. E o `conferir.py` ganhou o **bloco 10**, que confere cobertura por **par (sigla, area)**
em vez de por sigla. Do jeito antigo, `MATFIN` passava no teste.

**Regra que fica:** quando um problema for resolvido, procurar onde mais ele aparece. E teste que
so olha a dimensao errada da tabela aprova o buraco.

## 22/08/2026 · Aviso por prazo e defesa fraca; melhor e nao depender de memoria

Eu propus gravar a data do levantamento no `.txt` e o `conferir.py` avisar quando ficasse velha.
Contraposicao da sessao de mapear aulas, aceita: **aviso por prazo e a categoria de alerta que se
aprende a ignorar em duas semanas**, e ai o furo volta com falsa seguranca por cima.

O encaminhamento melhor e estrutural: **quem ja esta logado reescreve o `.txt` como subproduto**
de cada rodada de download. A data continua sendo gravada, mas como **diagnostico** ("faz 40 dias
que ninguem roda"), nunca como defesa principal.

**Regra que fica:** entre lembrar de fazer e nao precisar lembrar, escolher a segunda.
