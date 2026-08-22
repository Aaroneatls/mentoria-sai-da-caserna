# Aprendizado — Base 2 — Estrategia Concursos

> Este arquivo **cresce**. Toda licao aprendida trabalhando nesta base entra aqui, com a data e
> com o custo que ela teve. Aprendizado nao se arquiva junto com o dado.

## 21/08/2026 — do teste de aprendizado

- **Titulo e o que tem fonte maior que o corpo.** Nunca testar negrito: o flag e invertido entre
  safras e ha titulos em `Montserrat Medium`, que nao tem "Bold" no nome.
- **A faixa de secao pode vir numerada** (`6. LISTA DE QUESTOES`). Sem remover o prefixo antes de
  casar, a teoria vai ate a ultima pagina do arquivo. Custou uma auditoria inteira errada: 1.224
  paginas de teoria contadas onde havia 552.
- **Titulo numerado e legitimo** (`1 - Conceitos Introdutorios`). Testar `isupper()` no primeiro
  caractere descarta todos: Administracao Publica foi de 65 para 199 titulos depois da correcao.
- **A teoria pode voltar depois das questoes.** Medir por zona, nunca supor que o arquivo e
  teoria e depois questao.
- **Titulo que e imagem nao tem camada de texto.** A hipotese de que "sempre sobra fragmento" era
  falsa. Renderizar e olhar e o unico metodo confiavel, nao o ultimo recurso.
- **Pagina e sempre a do arquivo PDF**, nunca a impressa na folha nem a do sumario.

## 22/08/2026 — a marca d'agua esta na CAMADA DE TEXTO

O PDF do Estrategia carrega, em quase toda pagina, uma linha com **CPF e nome do titular da
conta**:

```
02055447114 - Gisilene Tatianne Santos de Lima
```

Medido: **124 das 125 paginas** de "Aula 00 - Regime Juridico-Administrativo e Principios LS".

**Isso quebra o `hash_teoria` se nao for tratado.** O hash existe para dizer que dois cursos tem a
mesma teoria e portanto compartilham Cod Mestre. Com a marca dentro do texto, o mesmo conteudo
baixado por **contas diferentes** gera hashes diferentes, e a regra falha **em silencio** — o
sistema simplesmente deixa de reconhecer que sao o mesmo topico.

**A regra:** normalizar antes de qualquer processamento de texto — remover a linha de marca
(padrao `<CPF> - <Nome>`) e, em geral, **tudo que varia por conta ou por download**.

Vale para o hash, para as ancoras de prosa e para qualquer extracao. O detector de titulos por
tamanho de fonte nao sofre, porque a marca e pequena, mas as ancoras de prosa sofreriam.

**Nao invalida o hash como conceito**, so exige a normalizacao antes.

### Junto disso: o hash do ARQUIVO nao serve para nada

Descoberto pela sessao das skills de download em 22/08: o PDF vem **marcado por download**. Quatro
downloads do mesmo arquivo deram quatro hashes diferentes, com o tamanho variando ~100 bytes
(90.153 / 90.183 / 90.224 / 90.274).

Entao hash de arquivo daria **falso positivo de mudanca em toda execucao**. A assinatura de
mudanca passa a ser: **nome do arquivo no CDN** (identidade) + numero de paginas + tamanho
aproximado (tolerancia de ~1 KB) + data da capa do PDF.

## 22/08/2026 — a estrutura fixa do PDF, e o hash cross-conta

### O PDF tem moldura fixa

Medido pela sessao das skills de download em 15 aulas, e conferido aqui em 6 PDFs de Direito
Administrativo. Vale em **100%** dos arquivos, simplificado e original:

```
p1       CAPA        titulo da aula, curso, autor, data
p2       INDICE      secoes numeradas com pagina
p3       a TEORIA comeca de fato
ultima   CONTRACAPA  em branco, zero caracteres uteis
```

**O codigo ja comecava em 3** — isso estava certo desde sempre, sem ninguem ter notado.

**Mas ia ate `doc.page_count`** e engolia a contracapa, errando uma pagina no ultimo bloco de cada
aula. Corrigido em 22/08 com `ULTIMA_UTIL = doc.page_count - 1`.

**Consequencia pratica:** um PDF de 84 paginas tem **81 de conteudo**. Sem o desconto, o alvo de
~10 paginas de teoria erra para menos justamente no bloco de abertura, que costuma ser o mais
denso.

### O hash_teoria e estavel dentro da mesma conta

Medida da outra sessao: quatro downloads do MESMO resumo deram quatro hashes de **arquivo**
diferentes, mas o hash do **texto extraido** foi **identico nos quatro** (4.598 caracteres),
sem normalizacao nenhuma. A marca nao quebra porque e constante para a mesma conta.

**Entao o risco e especificamente CROSS-CONTA.** Conta de coleta e conta de producao geram hash
diferente para o mesmo conteudo, e a falha e silenciosa.

Consequencia boa: **o que ja foi colhido numa conta so e internamente consistente.** A
normalizacao e obrigatoria para comparar entre contas, nao para reprocessar o que ja existe.

## 22/08/2026 — `pacote_id` NAO e chave estavel; `curso_id` e

Medido pela sessao das skills de download:

**O "Regular Controle" tem pelo menos DOIS ids de pacote.** A busca do catalogo devolve
**224364** ("Pacote Completo Cursos Regulares"), e esse id da **HTTP 404** na API do aluno. O que
existe e abre e o **365538** ("Pacote Completo Cursos Regulares + Sistema de Questoes").

Mesmo produto na cabeca do usuario, dois ids, e **o que a busca sugere e justamente o que nao
funciona**.

**`curso_id`, ao contrario, nao tem evidencia contra:** os 25 cursos do Fiscal e os 12 do
Controle responderam pelos ids que a API deu, e o `220883` (Direito Administrativo Fiscal)
continua o mesmo desde o levantamento de 18/08.

**A regra:**

| Campo | Serve de chave? |
|---|---|
| `pacote_id` | **nao**, nunca depender dele |
| `curso_id` | **sim**, mas com `nome_na_fonte` ao lado como chave de recuperacao |

**Suspeita em aberto:** o id do pacote do TCDF mudou de `393927` para `393930` no mesmo dia. Se
tiver sido o Estrategia recriando o produto, e nao alguem rematriculando, reforca que id de
pacote e volatil.

## O padrao de nome e INVERTIDO entre os dois cursos

Quem for parsear nome de curso precisa das duas regras:

```
Fiscal:    "Concursos da Area Fiscal - Curso Basico de <MATERIA>"
Controle:  "Concursos de Tribunais de Contas (Nivel Superior) <MATERIA> - Curso Regular"
```

No Fiscal a materia vem **no fim**; no Controle vem **no meio**, antes do sufixo.

## Cuidado ao detectar a contracapa

A ultima pagina e **imagem pura**: zero caractere extraivel, mas com imagens. Quem testar por
"pagina vazia de texto" acerta; quem testar por "pagina sem imagem" **erra**. O nosso corte usa
posicao (`page_count - 1`), que nao depende de nenhum dos dois.
