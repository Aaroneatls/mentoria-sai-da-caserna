# O que esta base precisa saber

> Extrato de `../DECISOES.md`, so com o que afeta esta base. O arquivo central continua sendo a
> referencia completa; aqui esta o essencial, para a sessao nao gastar contexto com decisao de
> outra base.

## O alvo do bloco: 10 paginas

O que decide e o **Pomodoro**: o bloco de 30 min da Tutory sao **25 de estudo e 5 de intervalo**.
Uma tarefa de 90 min tem **75 minutos efetivos**.

| Paginas | Teoria | Pomodoros | Sobra para questoes |
|---|---|---|---|
| 5 | 25 min | **1 exato** | 50 min |
| **10** | **50 min** | **2 exatos** | **25 min = 1 Pomodoro** |
| 12 | 60 min | 2,4 (quebra) | ~5 questoes |
| 15 | 75 min | 3 exatos | **zero** |

| | |
|---|---|
| Alvo | **10 paginas** |
| Faixa | 5 a 12 |
| Quem manda | **o titulo**, sempre. O alvo so escolhe entre dois titulos possiveis |

Teoria a **5 minutos por pagina**.

## Nome Mestre identifica, INICIE EM localiza

O **Nome Mestre** e nosso e pode sintetizar. O **INICIE EM / TERMINE EM** e **literal do PDF**,
inclusive a caixa alta, porque existe para o aluno achar a pagina.

**Pagina e sempre a do arquivo PDF**, nunca a impressa na folha nem a do sumario.

## Um codigo, varios enderecos

O topico e o mesmo; o endereco depende do curso. E **o link se escolhe pela AREA do aluno**:

```
DADM-0018 compartilhado
  Aluno de Controle  ->  Regular Controle, aula 06, p. 17-29
  Aluno de Fiscal    ->  Regular Fiscal,   aula 07, p. 22-35
```

## O Curso Regular e a espinha

1. O **Regular manda sempre**
2. Nao existe no Regular -> vai para o **especifico**, como suplemento
3. Pos-edital com a aula ja liberada no especifico -> usa a do especifico

**Nao e "o mais novo ganha".** A data vem da **capa do PDF**; o Estrategia nao publica atualizacao.

## Bloco x Topico e muitos para muitos

`Topico` e conteudo; `bloco` e trecho de paginas **de um curso**. Montar a tabela de pares desde
ja, mesmo com 95% das linhas 1 para 1. Um curso pode juntar o que o outro separa.

## Pre-requisito: padrao LIVRE

Preencher `depende de` por duas fontes baratas: a ordem do curso e as **referencias cruzadas no
texto** ("conforme estudamos na aula anterior"). **So marcar com evidencia** — marcar sem
evidencia acorrenta a disciplina numa fila e mata a ordenacao por peso.

## Professor de referencia

| Disciplina | Referencia |
|---|---|
| Contabilidade Geral e Avancada | **Gilmar Possati** |
| Direito Civil | **Paulo Sousa** |

Quando os professores diferem entre areas, **o sistema para e pergunta**. E a escolha resolve a
identidade, nao a localizacao: um codigo, dois enderecos.

## Aula listada mas nao liberada

Chutar o vinculo pelo nome, marcando `provisorio`, com o nome literal da plataforma e uma fila de
conferencia. **Registrar o erro, nao so a correcao.** O texto para o aluno **afirma**, nao duvida.

---

## Download: pasta, produto e unidade — FECHADO em 22/08/2026

- **A pasta leva o nome do Estrategia**, sintetizado, nunca traduzido para a nossa taxonomia.
  Por isso o download **nao depende da base 1**.
- **So o Curso Regular**, nunca o pacotaco: o Passo esta fora do escopo e a vaga de matricula e a
  mesma. Vale tambem para o TCDF.
- **Organizar por CURSO**, nao pela nossa disciplina. A reagrupacao acontece no mapeamento.
- A marca com CPF e da titular da conta (esposa do Elvis). Nunca pode sair em material do aluno.

## Historico — o que estava pendente (resolvido)

**Ha um ponto em aberto que impacta diretamente esta base**, e o Elvis foi discuti-lo em outra
sessao (22/08/2026): a **estrategia de download e de escolha de curso** no Estrategia Concursos.

**Nao comecar o mapeamento antes de trazer as conclusoes de la.** O que se decidir sobre quais
cursos baixar, quais versoes do livro usar e como manter isso atualizado muda o que esta base
recebe de entrada.

O que ja se sabe e que continua valendo ate ser contrariado:

- **material padrao e o livro simplificado** do Curso Regular; so 70% das aulas o tem, e o
  restante usa o completo
- a versao aparece no nome do arquivo como `LS` (simplificado) ou `LC` (completo)
- **limite de 3 produtos matriculados por vez**, com rodizio livre pela palavra `CORUJA`
- pasta padrao: `G:\Meu Drive\Inteligencia Artificial\Estrategia`

## ANTES DE QUALQUER EXTRACAO: normalizar o texto

O PDF do Estrategia traz **CPF e nome do titular da conta na camada de texto**, em quase toda
pagina (`02055447114 - Gisilene Tatianne Santos de Lima`, medido em 124 de 125 paginas).

**Remover essa linha antes de hashear ou ancorar.** Sem isso, o mesmo conteudo baixado por contas
diferentes gera `hash_teoria` diferente, e a regra de "mesma teoria = mesmo Cod Mestre" falha em
silencio.

**E o hash do ARQUIVO nao serve:** o PDF vem marcado por download, e quatro downloads do mesmo
arquivo deram quatro hashes diferentes. A assinatura de mudanca e **nome no CDN + paginas +
tamanho aproximado (~1 KB de tolerancia) + data da capa**.

## Ao mexer no Estrategia: dois cuidados que ja custaram caro

**404 no pacote = NAO MATRICULADO**, nao "nao existe". Se receber 404 em
`/api/aluno/pacote/{id}`, o produto existe e o que falta e matricular. O endpoint de **curso**,
no mesmo caso, devolve **500**.

**Selecionar produto pelo ID no href, nunca pelo texto do nome.** Os nomes se contem uns aos
outros: o TCDF foi desmatriculado por engano porque o seletor casava por "Sistema de Questoes",
que aparece tanto no nome dele quanto no do Controle.

## `tipo_curso_id = 1` NAO garante que e disciplina

Medido em 22/08/2026: **"Sistema de Questoes 1 Ano - Cartao ate 12 x"** (id 143237) vem como
`tipo_curso_id = 1`, igual a uma disciplina, e e **assinatura**.

Filtrar por tipo nao basta. Conferir o nome e excluir explicitamente o que nao for materia.

---

**Duvida sobre algo que nao esta aqui?** Consulte `../DECISOES.md`.
**Licao aprendida nesta base?** Escreva em `APRENDIZADO.md`, nao aqui.
