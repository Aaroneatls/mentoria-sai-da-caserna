---
name: project-detector-tipografico-titulos-estrategia
description: "Como achar os títulos de um PDF do Estratégia sem sumário e sem heurística de texto: pelo corpo da fonte, medido por documento"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T11:26:29.997Z
---

Descoberto em 2026-08-20, testado nas Aulas 02, 03, 16 e 17 de Direito Administrativo
(Regular Controle). Substitui todas as tentativas anteriores de detectar título por
expressão regular sobre o texto extraído — aquelas geravam falso positivo em célula de
tabela e caixa de fluxograma, e falso negativo em banner.

## O método

Ler o PDF com `pymupdf` (não `pypdf` — ver abaixo por quê) e usar **duas** fontes:

**Nível 1 — faixa roxa do template.** É um retângulo preenchido com a cor
`(0.259, 0.192, 0.643)`, largura > 400pt, altura entre 18 e 60pt. Achado por
`page.get_drawings()`. O texto sai com `page.get_text('text', clip=rect)`.

**Níveis 2 e 3 — corpo da fonte.** Montar um histograma de tamanho de fonte ponderado por
número de caracteres em todas as páginas de teoria. O tamanho mais frequente é o **corpo do
texto** (sempre 12,0 nas aulas testadas). Todo tamanho **maior que o corpo**, com pelo menos
~60 caracteres no documento inteiro, é um nível de título. Ordenados do maior para o menor:
16,0 = subseção, 14,0 e 13,0 = item.

## Onde a teoria acaba

A faixa **`QUESTÕES PARA FIXAÇÃO`** marca o fim da teoria. Nas aulas que não têm essa, vale a
primeira faixa que casar com `QUESTÕES`, `QUESTÕES COMENTADAS`, `LISTA DE QUESTÕES`, `GABARITO`
ou `REFERÊNCIAS`. Tudo depois é exercício e não entra na conta de páginas.

Isso muda muito o tamanho: as 18 aulas de Direito Administrativo somam **865 páginas de teoria**
dentro de arquivos que têm bem mais que isso (a Aula 16 tem 237 páginas e só 109 de teoria).

`RESUMO` **não** é teoria. `COMPILADO DE JURISPRUDÊNCIA` **é** teoria.

## Boa parte dos títulos é IMAGEM, não texto — medido no curso inteiro

Não é caso isolado. Nas 18 aulas de Direito Administrativo (Regular Controle):

- **61 de 264 faixas de seção (23%)** são imagem rasterizada
- **99 subtítulos** também são imagem
- **Aulas 05 e 14** têm **100%** das faixas rasterizadas; a Aula 14 não tem **nenhum** texto
  acima do corpo na zona de teoria — sem leitura visual ela sai com zero pontos de corte
- Aula 09 tem 34 subtítulos-imagem, Aula 14 tem 17

**Como achar os títulos-imagem:** `page.get_image_info()`, filtrando imagem com largura entre
150 e 545pt e altura entre 14 e 60pt, fora do cabeçalho (y<70) e do rodapé (y>770), e
descartando a faixa decorativa de largura total. Altura ≥21 costuma ser subtítulo em caixa;
menor que isso é item.

**Ao renderizar para ler, recortar a LINHA INTEIRA** (x de 32 a 562), não a caixa da imagem: o
título vem partido em vários pedaços e o recorte pela imagem corta a frase no meio
(`"Criação dos órgãos p"`). Dar folga vertical para títulos de duas linhas.

**Folha de contato** é o jeito eficiente: `page.show_pdf_page(..., clip=rect)` empilhando ~20
títulos por PNG com rótulo `Aula NN pP`. 160 títulos foram lidos em 8 imagens.

Cuidado com o mascote **"ESCLARECENDO!"**, que passa no filtro de imagem e não é título.

## Duas armadilhas que custaram tempo

**Não testar negrito.** O flag é inconsistente entre safras do template: nas Aulas 02/03/17
os títulos são não-negrito, e na Aula 16 o **corpo inteiro** vem marcado como negrito. Filtrar
por `'Bold' in font` derruba 3 das 4 aulas. **Só o tamanho vale.**

**Nem toda faixa tem texto.** Na Aula 02 p3 o título "Organização Administrativa" é **imagem
rasterizada** — não sai nem no pypdf nem no pymupdf. A faixa é detectável geometricamente, mas
volta vazia. Nesse caso: renderizar e ler visualmente. Ver
[[feedback_validacao_autonoma_e_corte_de_tabela]].

## Correções vindas da varredura dos 1.096 PDFs

Uma sessão paralela varreu os 4 pacotes (71 disciplinas, 90 professores) em 2026-08-20 e o
relatório está em `_contexto/estrategia-padroes-pdf.md`. O que mudou aqui:

**Faixa não se identifica por largura.** `largura > 400pt` deixa passar cabeçalho de tabela e
caixa de mnemônico, que usam o mesmo roxo. O discriminador é a **altura ≥ 24pt** mais estar na
margem esquerda. Caso real pego por isso: a caixa `(JoVeM, SEMPRE LICITE Com Planejamento…)`
da Aula 07, que tem h=21.

⚠️ A faixa de x0 **28-36pt** do relatório é estreita demais: em Direito Administrativo as Aulas
06 e 07 usam **x0=41** e seriam perdidas — 57 faixas legítimas. Usar `x0 <= 60`.

**Existe um nível 2 que não é retângulo:** um **par de linhas horizontais roxas finas** com o
subtítulo entre elas, presente em **410 dos 1.096 PDFs**. Importa porque a distância entre
faixas tem mediana de 5 páginas mas **p90 = 24 páginas** — em 10% dos trechos a faixa sozinha
não sustenta um bloco de 10 páginas.

⚠️ **Mas o par de linhas sozinho não identifica subtítulo.** Testado nas 18 aulas de Direito
Administrativo: 245 candidatos, **202 já cobertos pela tipografia** e os **43 restantes são
falso positivo** — caixa de destaque com marcadores (`▪ Igualdade: sem favorecimentos; ▪
Competitividade…`) e até a marca d'água `==37df0==`. **Exigir os dois sinais juntos**: par de
linhas **e** corpo de fonte maior que o do texto. Em Direito Administrativo a tipografia
resolve sozinha e o par de linhas não acrescenta nada.

**Rasterização é de professor, não de plataforma:** 2,3% global, **57 das 71 disciplinas têm
zero**. Direito Administrativo fica entre 13% e 29% — é caso ruim, não típico.

**Junção de faixa multilinha:** mesma página, x0 ±60pt, gap vertical entre **−8pt e +14pt** (o
gap pode ser negativo). Há faixas de 3, 4, 5 e 6 linhas. Tolerância errada inflava a contagem
de aulas multi-zona de 6,9% para 17,6%.

**Limpeza de texto obrigatória** antes de comparar qualquer string: marca d'água antipirataria
injetada no título (`GABARITO ==37DF0==`), zero-width space, marcas direcionais Unicode, caixa
desenhada em duplicata (`DESCRIÇÃO DESCRIÇÃO`) e versalete falso (`G ABARITO`).

**Questão dentro da teoria varia de 0% a 65%** (média 29,7%). O Elvis decidiu em 2026-08-20 que
**página com questão no meio da teoria conta normalmente** no tamanho do bloco — o aluno lê e
pensa, leva tempo.

⚠️ **Contar questão pelo cabeçalho `(BANCA - ANO)` erra feio nos dois sentidos.** Exigir o ano
colado no fecho do parêntese perde `(TCE RN / 2026)` e `(Cebraspe – EBSERH/2018)`; afrouxar
passa a contar citação de lei e de doutrina (`(Di Pietro, 2020)`, `(Lei 8.987/1995)`).

**O marcador confiável é `Comentários:`** no início da linha — é o que o professor escreve
depois do enunciado. Com ele, Direito Administrativo (Regular Controle) dá **32%**, não os 10%
que o padrão errado indicava. Bate com a média global de 29,7% da varredura.

## Descartar célula de tabela com `page.find_tables()`

Filtro heurístico não dá conta. `find_tables()` acerta: valores como `R$ 392.952,63`,
`Empresa A / Empresa B` e fragmentos como `IV, “c”)` caem todos dentro do bbox da tabela
detectada. Excluir candidato cujo canto superior esquerdo caia num desses bbox.

Somar a isso: rejeitar linha que comece com marcador (`▪ • ● →`), que tenha mais de 30% de
dígitos, que contenha `R$`, ou com mais `)` do que `(`.

## Não confundir prosa com título

Quando o tamanho de título coincide com o de uma caixa de destaque, prosa do corpo entra como
título. Aconteceu na Aula 00 (`"Até 2021, não existia uma 'lei geral' vedando..."`). Filtros que
resolvem: começa em maiúscula, **não** termina em `.,;:`, não contém `. ` seguido de maiúscula
(duas frases = prosa), no máximo 14 palavras, não começa com `art.`/`§`, não casa com o padrão
de enunciado de questão `(BANCA - ANO)`.

Atenção: **título curto é normal** neste material — `Introdução`, `Conceito`, `Patrimônio`,
`Falência`, `Motivo`, `Objeto`, `Licença` são todos legítimos. Não filtrar por tamanho mínimo.

## Nível 2: par de linhas roxas — resolve onde a tipografia falha

Descoberto em 2026-08-20, testado em Administração Pública (Regular Controle).

Quando **corpo e título têm o mesmo tamanho de fonte**, a tipografia sozinha não separa. O
sinal que resta é o **par de linhas roxas finas** (altura ≤ 2pt, largura > 400pt) com o
subtítulo entre elas, gap de 18 a 46pt.

**Exigir DOIS sinais:** o par de linhas **e** (fonte maior que o corpo **ou** família
tipográfica de destaque). O par sozinho gera 43 falso positivo em 245 candidatos — caixa de
destaque com marcadores e até a marca d'água.

Resultado: Administração Pública saiu de **65 para 199 títulos** (1 a cada 3,8 páginas, contra
11,7 antes), e de 23 para 46 blocos.

### ⚠️ Repeti duas armadilhas já conhecidas. Não repetir de novo:

**1. Testei negrito.** O título ali é `Montserrat Medium` — não tem "Bold" no nome e era
descartado. A regra "nunca testar negrito" já estava escrita nesta mesma memória. Aceitar
`Bold`, `Medium`, `Semibold` ou, melhor, só o tamanho.

**2. Rejeitei título numerado.** `"1".isupper()` é falso, então `1 - Conceitos Introdutórios`
caía no filtro de "começa em maiúscula". Tirar o prefixo `\d+[-–—.)]` antes de testar.

## ⚠️ A faixa de fim da teoria pode vir NUMERADA

Erro que inflou três disciplinas inteiras. Em Auditoria Governamental e Contabilidade Pública
as faixas são numeradas:

```
6. LISTA DE QUESTÕES        7. GABARITO
2 – QUESTÕES PARA FIXAÇÃO   5 – GABARITO
```

O padrão `^(questões|gabarito|…)` não casa com o número na frente, então a teoria ia até a
última página do arquivo — Auditoria contava 1.224 páginas de teoria, o que é absurdo.

**Remover o prefixo numérico antes de casar.** Vale também para a apresentação do professor:
`APRESENTAÇÃO E ORIENTAÇÕES` e `MOTIVAÇÃO DA AULA` existem em Contabilidade e Auditoria — é a
apresentação que o Elvis dizia existir e que não aparece em Direito Administrativo.

Somar ao padrão de fim: `bibliografia`, `respostas das questões subjetivas`,
`resumo em mapas e esquemas`.

## Exclusões necessárias

- texto branco (`color == 0xFFFFFF`) — é rótulo dentro de caixa de fluxograma
- texto cujo canto superior esquerdo cai dentro de uma forma preenchida estreita (< 420pt) —
  também é caixa de diagrama
- rodapé/cabeçalho (`Herbert Almeida`, `Equipe Direito`, `Aula NN`, número solto)
- juntar linhas seguidas do mesmo nível a menos de 26pt de distância: é título que quebrou
  em duas linhas
- versalete despedaçado: `R ESUMO` → `RESUMO`. A regex **não** pode juntar quando a letra
  solta é palavra real (`E`, `A`, `O`, `À`), senão vira `EMPRESAS PÚBLICAS ESOCIEDADES`

## Resultado medido

| Aula | Páginas de teoria | Títulos achados |
|---|---|---|
| 02 | 27 | 21 |
| 03 | 18 | 29 |
| 16 | 109 | 79 |
| 17 | 20 | 12 |

Zero falso positivo na conferência. Com esses pontos de corte, a segmentação em blocos por
programação dinâmica (alvo 10 páginas, faixa 5-12) devolveu **18 blocos, todos entre 7 e 11
páginas**. Antes, só a Improbidade tinha 5 blocos estourando o limite.

## Corte em ponto de título, com fronteira simétrica (regra do Elvis, 2026-08-20)

O bloco **não** é uma faixa de páginas — é o trecho entre **dois pontos de título**. Quando dois
blocos dividem a mesma página, ela entra **nos dois**, e cada um diz o seu recorte. O formato da
referência nomeia o tópico de início e o de fim, **com a página entre parênteses**:

```
De "Administração Pública" (p13) até antes de "Regime jurídico das autarquias" (p20)
De "Regime jurídico das autarquias" (p20) até o fim da aula (p29)
```

O motivo é o aluno: quem parou no meio da p20 precisa saber **de onde retomar**. Só marcar
"até antes de X" no bloco anterior deixa o bloco seguinte sem ponto de partida.

## Apresentação do professor não é conteúdo teórico

Trecho em que o professor se apresenta ("eu sou o professor fulano, isso e aquilo") **fica de
fora** da contagem de páginas de teoria. A teoria começa quando a matéria começa. Isso reduz o
número de páginas do início da aula.

Nas 18 aulas de Direito Administrativo (Regular Controle) **não há nenhuma** — a varredura só
achou a palavra "apresentação" no sentido de "apresentação das propostas" em licitação. Mas a
regra vale para outros cursos, onde o Elvis já viu o caso. Saudação curta antes do primeiro
título (Aula 17: "Olá pessoal, tudo bem?… Aos estudos, aproveitem!") também fica fora, por
consequência natural do corte começar no título.

## Cuidado ao nomear o bloco

O guarda-chuva do Nome Mestre é **o assunto da aula**, não a última faixa roxa vista. A faixa
"SUJEITO ATIVO DO ATO DE IMPROBIDADE" (Aula 16 p29) é subordinada ao tema da aula e não o
substitui — carregá-la adiante produzia nomes errados como "Sujeito Ativo do Ato de
Improbidade: penalidades".

Também: só minusculizar a inicial do complemento se ele **não** estiver em Title Case, senão
sai `Organização Administrativa: administração Pública`.

## Resumo e Compilado de Jurisprudência

As faixas `RESUMO` e `COMPILADO DE JURISPRUDÊNCIA` (Aula 16, p101 em diante) marcam **material
de revisão, não teoria nova**. Bloco a partir dali é sinalizado à parte, não entra como estudo
de conteúdo novo.

Ver [[feedback_pagina_sempre_do_arquivo_pdf]], [[project_regras_quebra_estrategia_correlacao_bezerra]]
e [[project_taxonomia_central_nome_mestre]].
