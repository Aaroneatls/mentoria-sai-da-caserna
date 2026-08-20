# Padrões de diagramação dos PDFs do Estratégia Concursos

Levantamento feito em 20/08/2026 para dar base à skill de mapeamento de aulas.
O objetivo é conseguir dizer "estude da página X, tópico A, até a página Y, tópico B"
com certeza, sem depender do sumário e sem heurística frágil.

## Base medida

| item | número |
|---|---|
| PDFs varridos (varredura completa) | **1.096** (100% do acervo, 0 erro de leitura) |
| Pacotes | 4 (Regular Controle, Regular Fiscal, ISS Manaus AFTM, Pacotaço TCDF ANACE) |
| Disciplinas distintas | **71** |
| Professores distintos (cabeçalho) | **90** |
| Páginas processadas | ~108.600 |
| Faixas roxas encontradas | **12.495** |

Ferramenta: `pymupdf` 1.28.2 (`get_drawings()` + `get_text()`). **Não usar `pypdf`** para isso.

A varredura foi rodada duas vezes sobre os 1.096 arquivos: a primeira levantou cor, fonte,
rasterização, questões, tabelas e numeração; a segunda repetiu tudo com a lógica de junção
de faixas multilinha corrigida (ver F), que é a que vale para as perguntas **E**, **F** e **K**.
Todos os números abaixo são do acervo inteiro.

---

## A. A cor da faixa é a mesma em todas as disciplinas e professores?

**Sim — e é praticamente a única cor que importa.**

Levantei todas as cores de retângulo preenchido largo em 1.096 PDFs:

| cor (RGB 0-1) | ocorrências | o que é |
|---|---|---|
| `(1.0, 1.0, 1.0)` | 354.874 | branco — fundo de célula/caixa, ignorar |
| `(0.949, 0.949, 0.949)` | 56.979 | cinza claro — fundo de tabela, ignorar |
| **`(0.259, 0.192, 0.643)`** | **20.426** | **faixa de título (roxo Estratégia)** |
| `(0.259, 0.18, 0.643)` | 1.163 | mesma faixa, variação de arredondamento |
| `(0.251, 0.18, 0.643)` | 858 | idem |
| `(0.258, 0.191, 0.645)` | 624 | idem |
| `(0.0, 0.125, 0.376)` | 519 | azul-marinho — **cabeçalho de tabela**, não é título |
| `(1.0, 0.753, 0.0)` / `(1.0, 1.0, 0.0)` | 439 / 332 | amarelo de destaque/marca-texto |

**Nenhuma disciplina usa outra cor de faixa de título.** Só 1 PDF em 1.096 não tem
nenhuma faixa roxa, e é um simulado (ver D).

O roxo tem **4 variações de arredondamento**. Comparar com igualdade exata perde
~3.100 faixas (25% delas).

**Regra prática:** aceitar a cor com tolerância de `±0.06` em cada canal em torno de
`(0.259, 0.192, 0.643)`. Nunca comparar com `==`.

---

## A-bis. Cor não basta: a geometria é que separa título de tabela

Essa foi a descoberta mais importante da investigação. A regra antiga
("retângulo roxo com largura > 400pt") **produz falso positivo em massa**, porque
cabeçalho de tabela e caixa de mapa mental usam exatamente o mesmo roxo.

Medições (página sempre A4, 595×842pt — **100% dos 1.096 PDFs**):

| elemento | altura | x0 (borda esquerda) | largura |
|---|---|---|---|
| **faixa de título** | **24-46pt** (94% entre 27 e 34) | **30-34pt** (margem do texto) | 508-552pt |
| cabeçalho de tabela | 12,0-24,4pt | 37 a 182pt (varia) | 336-521pt |
| caixa de mapa mental | ~20-30pt | 121-250pt | 200-258pt |

Exemplos reais de falso positivo que a largura sozinha não pega:
`DDL (DATA DEFINITION LANGUAGE)` (w=520pt, h=12,1) e `DESCRIÇÃO` (w=452pt, h=12,4)
em Banco de Dados; `EXEMPLOS` (w=333pt) em Português é célula de tabela.

**Regra prática — uma faixa de título é um retângulo que satisfaz TUDO:**
1. preenchimento roxo (tolerância ±0.06);
2. **altura ≥ 24pt** — este é o filtro decisivo;
3. **x0 ≤ 12% da largura da página** (~71pt) — encostado na margem esquerda;
4. largura ≥ 72% da largura da página (~430pt).

Distribuição de alturas das 12.495 faixas: 27pt (1.618), **30pt (6.858)**, 31pt (2.762),
34pt (457) — ou seja, 30-31pt é o padrão dominante.

### Caixa de citação/destaque (não é título)
141 retângulos roxos passam nos 4 critérios mas contêm uma **frase inteira em caixa baixa**
(ex.: *"A administração pode perpetrar fraude, burlando controles..."*, h=54pt).
São caixas de destaque. **Descartar quando o texto tiver mais de 90 caracteres, ou mais
de 45 caracteres com mais de 55% de minúsculas.**

### Fonte das faixas
`Montserrat-Bold` (128.197 caracteres) e `Montserrat,Bold` (104.589) cobrem a quase
totalidade; `Calibri-Bold` (22.298) aparece em alguns professores. Serve como conferência,
mas **não usar como critério primário** — há PDFs com fonte embutida anônima
(`CIDFont+F2`, `___WRD_EMBED_SUB_41`).

---

## B. O corpo do texto é sempre 12,0?

**Não.** Em 1.096 PDFs:

| corpo | PDFs | % |
|---|---|---|
| **12,0** | 928 | **84,7%** |
| 13,0 | 97 | 8,9% |
| 11,0 | 67 | 6,1% |
| 11,9 / 11,2 / 9,0 | 4 | 0,4% |

Disciplinas que fogem do 12,0 (as maiores):

- **13,0** — Administração Pública (Regular Controle, 19), Tecnologia da Informação
  (Regular Fiscal, 18), Análise de Informações (17), Administração Geral e Pública
  (TCDF, 16), Auditoria Governamental (12), Direito Previdenciário/Rubens (8).
- **11,0** — Tecnologia da Informação (Regular Fiscal, 32), Informática (18),
  Análise de Dados/Estatística e IA (4), Banco de Dados e Linguagem SQL (4),
  Governança de Dados e Segurança da Informação (4).

Repare que **Tecnologia da Informação usa 11,0 em 32 aulas e 13,0 em outras 18** — o corpo
varia dentro da mesma disciplina, aula a aula.

O corpo detectado responde por **84,7% dos caracteres na mediana**, mas cai a **29,5%**
no pior caso (aula quase toda de tabela/código).

Tamanhos acima do corpo, por frequência: 15,0 (em todos os 1.096 PDFs), 16,0 (845),
14,0 (711), 13,0 (525), 20,0 (110), 18,0 (86).

**Regra prática:** nunca fixar 12,0. Calcular o histograma de tamanho ponderado por
número de caracteres **em cada PDF** e tomar a moda como corpo. Se a moda ficar abaixo
de 60% dos caracteres, tratar a hierarquia de subtítulo desse PDF como pouco confiável e
cair para as faixas (nível 1) e as linhas roxas (nível 2).

**Confirmado:** não testar negrito. O flag é inconsistente entre aulas.

---

## B-bis. Existe um nível 2 de título, e ele NÃO é retângulo

Descoberta nova. Abaixo da faixa roxa existe um segundo nível hierárquico desenhado como
**um par de linhas horizontais roxas de largura total**, com o texto do subtítulo entre elas.
Não é retângulo preenchido nem retângulo com contorno — são dois traços (`h = 0.0`)
separados por 15-45pt.

Exemplo (Português, Regular Controle, Aula 06, pág. 29 do arquivo): faixa
`USO DO SINAL DE DOIS PONTOS (:)` e, logo abaixo, entre duas linhas roxas,
`Ligar orações ou termos que tenham natureza de "explicação"`.

- **410 dos 1.096 PDFs** usam esse nível 2 (37,4%).
- Disciplinas que mais usam (média de subtítulos por PDF): Língua Portuguesa TCDF **27,4**,
  Português Regular Controle **20,9**, Língua Portuguesa ISS Manaus **19,8**,
  Português Regular Fiscal **16,3**, Direito Penal ISS Manaus **15,5**,
  Direito Constitucional Regular Controle **13,2**, Raciocínio Lógico ISS Manaus **11,7**.
- Cor do traço: `(0.259, 0.192, 0.643)` (20.615 traços) e a variante `(0.278, 0.173, 0.733)` (1.623).

**Regra prática:** juntar traços roxos com largura ≥ 72% da página e x0 na margem;
quando dois deles estiverem a 14-46pt um do outro, o texto entre eles é subtítulo de
nível 2. Descartar se o texto passar de 90 caracteres (aí é linha de tabela — isso
descartou 748 candidatos falsos).

---

## C. Qual a proporção de faixas rasterizadas por disciplina/professor?

Bem menor do que o Direito Administrativo fazia parecer. No acervo inteiro:
**287 de 12.495 faixas (2,3%)** devolvem texto vazio.

- **71 PDFs (6,5%)** têm pelo menos uma faixa rasterizada.
- **57 das 71 disciplinas (80%) têm 0% de rasterização.**
- Apenas **4 PDFs** são 100% rasterizados (com 3+ faixas).

Disciplinas com rasterização relevante:

| disciplina | % faixas rasterizadas | faixas |
|---|---|---|
| Direito Administrativo (Regular Controle) | **29,1%** | 59/203 |
| (4-5) Gestão de Contratos (TCDF) | 25,6% | 23/90 |
| Controle Externo (Regular Controle) | 20,7% | 17/82 |
| Direito Administrativo (TCDF) | 16,9% | 40/236 |
| Direito Administrativo (ISS Manaus) | 15,9% | 33/207 |
| Direito Administrativo (Regular Fiscal) | 13,2% | 46/348 |
| Lei Orgânica do TCDF e Regimento Interno | 10,7% | 3/28 |
| Auditoria (Regular Fiscal) | 8,0% | 24/301 |
| Direito Civil - Paulo Sousa (Regular Fiscal) | 7,8% | 20/257 |

O padrão é **do professor, não da disciplina**: Direito Administrativo aparece nos 4 pacotes
sempre entre 13% e 29%. Não existe professor com material 100% rasterizado ao longo de um
curso inteiro — só aulas isoladas (as Aulas 05 e 14 de Direito Administrativo do Regular
Controle são os casos conhecidos).

**Regra prática — folha de contato.** O retângulo é sempre detectável mesmo quando o texto
não é. Para resolver as faixas mudas, montar um PNG único com todas as faixas rasterizadas
do PDF (uma por linha, com o número da página ao lado, via `page.show_pdf_page` com `clip`)
e ler visualmente de uma vez. Validado em 18 faixas de 6 disciplinas diferentes: a leitura
sai limpa e barata. **Nunca inferir o título de uma faixa muda pelo contexto.**

---

## D. Existem aulas SEM faixa roxa nenhuma?

**Praticamente não: 1 PDF em 1.096.**

- `Legislacao Tributaria Estadual (Regular Fiscal) / Aula 05 - Simulado (06-12-2022).pdf`
  — 42 páginas, zero faixa. É um **simulado**, não tem teoria para mapear.

Além dele, **10 PDFs com mais de 25 páginas têm só 1 ou 2 faixas**:
Bibliotecas Python (51 pg), Bibliotecas de Python (51 pg), CPC 06 Arrendamentos (26 pg),
4 aulas de Direito Previdenciário/Adriana Menezes, 3 de Direito Previdenciário/Rubens Maurício,
LINDB (74 pg).

Nesses casos a estrutura vem do **nível 2** (linhas roxas): a Aula 04 de Direito
Previdenciário/Adriana tem 2 faixas mas **8 subtítulos**; a LINDB tem 2 faixas e 3 subtítulos.

**Regra prática:** se o PDF tiver menos de 3 faixas e mais de 25 páginas, montar a estrutura
pelo nível 2. Se também não houver nível 2 (caso das Bibliotecas Python), **marcar a aula
como "sem estrutura detectável" e escalar para o Elvis** — não inventar corte.

---

## E. Aulas com mais de uma zona de teoria

O caso da Aula 11 (PPPs e Consórcios) existe, mas é menos comum do que parecia — e a
contagem só fica correta depois de juntar as faixas multilinha (ver F).

Contagem de zonas de teoria (uma zona = bloco `TEORIA…` que aparece depois de um bloco
`QUESTÕES…`):

| zonas de teoria | PDFs | % |
|---|---|---|
| 1 | 960 | 87,6% |
| 2 | 64 | 5,8% |
| 3 | 7 | 0,6% |
| 4 | 3 | 0,3% |
| 5 | 1 | 0,1% |
| 6 | 1 | 0,1% |
| 0 (nenhuma faixa de teoria) | 60 | 5,5% |

**76 PDFs (6,9%) têm 2 ou mais zonas de teoria.**

Concentração por disciplina: Inglês Instrumental (8), Contabilidade Geral ISS (5),
Auditoria Regular Fiscal (5), Contabilidade Pública Regular Controle (5),
Controle Externo (5), Tecnologia da Informação (5), Contabilidade Geral e Avançada/Gilmar (4),
Contabilidade Geral e Avançada/Cardozo (4), Contabilidade Geral Avançada Regular Controle (4),
AFO (3), Legislação Tributária Municipal (3), AFO Regular Fiscal (3), Auditoria ISS (3),
Direito Previdenciário/Rubens (3).
**É sobretudo fenômeno de Contabilidade e Auditoria**, onde o professor empacota 2-3 CPCs
ou 2-3 normas na mesma aula.

### Como distinguir a segunda zona — duas assinaturas que funcionam

1. **Repetição literal da faixa de abertura.** O professor de Auditoria abre cada
   mini-aula com `MOTIVAÇÃO DA AULA` → `CONTEXTUALIZAÇÃO` → teoria →
   `RESUMO EM MAPAS E ESQUEMAS` → `QUESTÕES…` → `GABARITO` →
   `RESPOSTAS DAS QUESTÕES SUBJETIVAS`, e repete o ciclo inteiro. Na Aula 04 de
   Materialidade/Risco/Fraudes (169 páginas) isso acontece **3 vezes**
   (páginas 2, 74 e 107 do arquivo). Em 31 PDFs a primeira faixa reaparece 2+ vezes.
2. **Faixa de categoria TEORIA depois de faixa de categoria QUESTÕES.** É a regra geral
   e cobre os casos em que o título muda (`CPC 27 – ATIVO IMOBILIZADO` … `LISTA DAS
   QUESTÕES` … `CPC 04 - ATIVO INTANGÍVEL`).

**Regra prática:** varrer as faixas em ordem de página, classificar cada uma
(ver K) e abrir uma nova zona de teoria toda vez que uma faixa `TEORIA` aparecer depois de
uma faixa `QUESTÕES`. Cada zona vira um assunto separado no mapeamento, com seu próprio
intervalo de páginas.

### Aulas sem marcador de fim
**39 PDFs (3,6%)** não têm nenhuma faixa de encerramento. Destes, 4 são 100% rasterizados
(resolvem-se pela folha de contato) e 1 é o simulado sem faixa nenhuma. Concentram-se em
Direito Previdenciário/Adriana Menezes (7), Direito Administrativo Regular Controle (5),
Controle Externo (3). Nesses casos **a teoria vai até o fim do arquivo** — o que costuma
estar certo, porque são aulas sem bateria de questões.

---

## F. Faixa que quebra em duas linhas

Confirmado, e **existe caso de 3, 4, 5 e até 6 linhas**.

| linhas na faixa | ocorrências |
|---|---|
| 1 | 11.786 (95,5%) |
| 2 | 525 (4,3%) |
| 3 | 20 |
| 4 | 6 |
| 5 | 1 |
| 6 | 1 |

**25 PDFs** têm alguma faixa de 3+ linhas. O recorde é
`Auditoria (Regular Fiscal) / Aula 11 - Tópicos de Auditoria Fiscal` com uma faixa de
**6 linhas**; e `Contabilidade de Custos / Aula 00 - Noções Iniciais` com uma de 5.

Exemplo de 2 linhas: `EXERCÍCIOS COMENTADOS - APLICAÇÃO DA` + `PENA`
(Direito Penal Regular Fiscal, Aula 06, pág. 64).

**Regra de junção (validada):** duas faixas se juntam quando, **na mesma página**,
o x0 difere menos de 60pt e o espaço vertical entre elas está entre **-8pt e +14pt**
(pode haver sobreposição negativa). Aplicar em cadeia, sem limite de linhas.

Isso importa muito: com a tolerância antiga (`0 ≤ gap < 10`) a Aula 06 de Direito Penal
era lida como **11 zonas de teoria**; com a tolerância corrigida ela é lida como **1 zona**,
que é o certo. A junção errada inflava a contagem de multi-zona de 6,9% para 17,6% — ou seja,
**mais da metade das "aulas com dois assuntos" seriam falso positivo** se a junção fosse
feita com a tolerância errada.

---

## G. Apresentação do professor

Existe, é rara, e **é detectável pelo título da faixa** — não é preciso caçar a frase.

- **184 PDFs (16,8%)** têm uma faixa de abertura que não é teoria.
- Apenas **23 PDFs (2,1%)** têm a frase de auto-apresentação nas 10 primeiras páginas
  (14 em Aula 00, 9 em outras aulas).

Títulos de faixa de abertura, por frequência (acervo inteiro):

| título | PDFs |
|---|---|
| APRESENTAÇÃO DA AULA | 52 |
| APRESENTAÇÃO | 39 |
| CONSIDERAÇÕES INICIAIS | 31 |
| OBSERVAÇÕES SOBRE A AULA | 11 |
| APRESENTAÇÃO DO CURSO | 10 |
| APRESENTAÇÃO DO TÓPICO | 8 |
| APRESENTAÇÃO DO PROFESSOR | 4 |
| APRESENTAÇÃO DO PROFESSOR E DO CURSO | 3 |
| APRESENTAÇÃO E DIVULGAÇÃO / E ORIENTAÇÕES / PESSOAL | 7 |
| CRONOGRAMA | 2 |

Frases reais encontradas (todas na página 1, 2, 3 ou 9 do arquivo):

- *"Bom, antes de começarmos, peço licença para me apresentar. Meu nome é Stefan Fantini"*
  — Administração Geral e Pública (TCDF) e Administração Pública (Regular Controle).
- *"Antes de mais nada, gostaria de me apresentar. Meu nome é He..."* — Controle Externo
  e Lei Orgânica do TCDF.
- *"permita-me fazer uma breve apresentação pessoal: meu nome é Fábio Dutra"* —
  Direito Tributário (ISS Manaus) e Noções de Direito Tributário (TCDF).
- *"Meu nome é Felipe Luccas Rosa"* — Língua Portuguesa (TCDF).
- *"Meu nome é Luciano Rosa"* — Contabilidade de Custos (Regular Fiscal).
- *"Sou o Professor Leandro Signo..."* — Conhecimentos do DF (TCDF).
- *"APRESENTAÇÕES / Saudações! Meu nome é Celso Natale"* — Economia (ISS Manaus).

**Confirmado:** no Direito Administrativo do Regular Controle não há nenhuma.

### Detector proposto (duas camadas)

1. **Camada principal — título da faixa.** Normalizar o texto (ver "Armadilhas de texto")
   e descartar a seção inteira quando o título contiver `APRESENTACAO`, `SUMARIO`,
   `INDICE`, `CONSIDERACOESINICIAIS`, `OBSERVACOESSOBREAAULA`, `CRONOGRAMA`,
   `QUEMSOU`, `SOBREOPROFESSOR`, `AVISOIMPORTANTE`, `COMOESTUDAR`.
2. **Camada de segurança — frase.** Dentro das 10 primeiras páginas, procurar
   `me chamo`, `meu nome é`, `sou o professor/a professora`, `peço licença para me
   apresentar`, `gostaria de me apresentar`, `permita-me fazer uma breve apresentação`,
   `quem sou eu`.

**Cuidado com falso positivo:** `APRESENTAÇÃO` também aparece em títulos de conteúdo real —
`CPC 26 – APRESENTAÇÃO DAS DEMONSTRAÇÕES CONTÁBEIS`, `CAPÍTULO 7 – APRESENTAÇÃO E
DIVULGAÇÃO`, `DLPA E DMPL: OBRIGATORIEDADE E APRESENTAÇÃO`. **Só tratar como abertura
quando a palavra estiver no começo do título** (ou o título for exatamente
`APRESENTAÇÃO`/`APRESENTAÇÕES`), nunca quando vier depois de um travessão ou de um
número de capítulo.

A camada 2 pega 7 PDFs que a camada 1 não pegaria; e a página 9 de dois PDFs deu falso
positivo (a frase "meu nome" aparecendo dentro de um texto de prova de Português e de
um exemplo de direito de imagem). Por isso a camada 2 **não deve cortar sozinha** —
serve para sinalizar e conferir.

---

## H. Questões embutidas no meio da teoria

Medi, para cada disciplina, quantas páginas da zona de teoria contêm material de questão
(cabeçalho `(BANCA / ANO)` ou `(BANCA - ANO)`, linha `Comentários:`, linha `Gabarito: Letra X`).

**Global: 12.495 de 42.038 páginas de teoria = 29,7%.**

A variação entre disciplinas é enorme — de 0% a 65%:

| disciplina | % das páginas de teoria com questão | forte* |
|---|---|---|
| Língua Portuguesa (TCDF) | **64,6%** | 3,2% |
| Direito Tributário (Regular Fiscal) | 61,1% | 6,5% |
| Direito Tributário (ISS Manaus) | 57,1% | 7,8% |
| Raciocínio Lógico e Mat. Financeira (TCDF) | 55,9% | 32,1% |
| Raciocínio Lógico (ISS Manaus) | 53,1% | 28,9% |
| Raciocínio Lógico e Analítico (Reg. Controle) | 48,9% | 27,4% |
| Estatística (ISS Manaus) | 46,7% | 33,3% |
| Português (Regular Controle) | 45,5% | 32,5% |
| Direito Administrativo (Regular Controle) | 44,8% | 26,7% |
| AFO/Orçamento (Regular Controle) | 37,7% | 26,3% |
| Contabilidade Geral e Avançada (Gilmar) | 36,2% | 13,7% |
| Direito Constitucional (Regular Controle) | 31,3% | 26,5% |
| Contabilidade Geral (ISS Manaus) | 29,0% | 16,1% |
| Administração Geral e Pública (TCDF) | 12,5% | 7,0% |
| Direito Civil (ISS Manaus) | 10,1% | 6,7% |
| Tecnologia da Informação (Regular Fiscal) | 9,2% | 3,3% |
| Economia (ISS Manaus) | 8,7% | 0,0% |
| Contabilidade Pública (Regular Controle) | 8,5% | 0,5% |
| Análise de Informações (Regular Controle) | 8,2% | 0,1% |
| Direito Empresarial (Regular Fiscal) | 0,2% | 0,0% |
| Informática / Direito Penal / Noções de Direito Civil / Análise de Dados / Direito Penal ISS / Direito Empresarial ISS | **0,0%** | 0,0% |

\* "forte" = a página tem cabeçalho de questão **e** comentário, ou seja, é quase certamente
uma página de questão resolvida, não só uma menção.

**Leitura:** Português, Raciocínio Lógico, Estatística e Direito Tributário são
disciplinas em que **metade da "teoria" é questão comentada**. Contabilidade Pública,
Economia, TI, Direito Penal e Direito Empresarial são teoria quase pura.

**Regra prática para dimensionar o bloco de estudo:** o alvo de 10 páginas (faixa 5-12)
**não pode ser contado em páginas brutas**. Classificar cada página da zona de teoria como
"teoria" ou "questão" e dimensionar o bloco pelo número de páginas de teoria, tratando a
página de questão com peso menor. Como o percentual é estável **por disciplina**, dá para
usar o percentual da disciplina como fator de correção quando não valer a pena classificar
página a página.

---

## I. Estruturas que não podem ser cortadas ao meio

- **27.713 de 108.592 páginas (25,5%)** contêm tabela.
- **5.307 tabelas atravessam a virada de página.**
- **833 dos 1.096 PDFs (76,0%)** têm pelo menos uma travessia.

Ou seja: cortar um bloco de estudo numa virada de página tem chance real de partir uma
tabela ao meio.

**Detector (validado):** numa página, colecionar os traços do `get_drawings()` —
linhas horizontais (`altura < 2,5pt` e `largura > 50pt`) e verticais (`largura < 2,5pt`
e `altura > 20pt`). A página tem tabela quando há **≥ 3 horizontais e ≥ 2 verticais**.
A tabela atravessa a virada quando o traço mais baixo da página *n* fica a menos de 140pt
do rodapé **e** o traço mais alto da página *n+1* está a menos de 160pt do topo.

**Regra prática:** o corte do bloco nunca pode cair numa página marcada como
"tabela atravessa para a próxima". Empurrar o corte para a primeira página seguinte que
não tenha travessia. Como a faixa alvo é 5-12 páginas, quase sempre existe folga.

**Limitação conhecida:** o detector acha *grades*. Fluxograma e mapa mental (que no
Estratégia são desenhados com caixas roxas soltas e setas, não com grade) **não são
pegos**. Não achei um sinal geométrico confiável para eles — ver "Casos que precisam de
decisão do Elvis".

---

## J. Numeração impressa x página do arquivo

**Há divergência, ela não é constante, e por isso a regra do projeto está certa.**

| offset (impresso − índice do arquivo) | PDFs |
|---|---|
| **+1** | 964 (87,9%) |
| **0** | 121 (11,0%) |
| sem número legível | 9 (0,8%) |
| −3 | 2 (0,2%) |

Os dois padrões:

- **offset +1** (maioria): o rodapé traz `N` e o total, e a capa conta como página 1.
  Índice 10 do arquivo imprime "11".
- **offset 0**: numeração começa depois da capa. Índice 20 do arquivo imprime "20".
  Ex.: `Noções de Primeiros Socorros / Aula 01`, `Legislação Tributária Municipal / Aula 00`.

11 PDFs têm detecção fraca (<80% de concordância). Num deles
(Contabilidade Geral e Avançada / Gilmar Possati, Aula 07) o rodapé mostra "44" em toda
página — é o **total**, não a página corrente, e o número corrente não sai no texto.

**Regra prática:** confirmada a regra do projeto — **sempre usar o índice da página no
arquivo PDF** (base 1 na hora de falar com o aluno, se preferir), nunca o número impresso
e nunca o sumário. O desvio típico é de 1 página, mas varia por PDF e não dá para assumir.

---

## K. Gramática de seções (resultado novo)

Classifiquei as 12.339 faixas em 5 categorias, com base na tabela de frequência dos
títulos reais do acervo (e não em palpite):

| categoria | faixas | o que é |
|---|---|---|
| QUESTOES | 7.368 | fecha a zona de teoria |
| TEORIA | 4.270 | conteúdo |
| RASTER | 287 | faixa muda, precisa da folha de contato |
| REVISAO | 219 | RESUMO / PARA REVISAR / RESUMO EM MAPAS E ESQUEMAS |
| ABERTURA | 195 | apresentação, sumário, cronograma |

Repare que **há mais faixa de questão do que de teoria** (7.368 contra 4.270): o professor
fatia a bateria de exercícios por banca e por tópico.

Formas de sequência mais comuns:

| forma | PDFs | % |
|---|---|---|
| TEORIA → QUESTOES | 582 | 53,1% |
| TEORIA → REVISAO → QUESTOES | 112 | 10,2% |
| ABERTURA → TEORIA → QUESTOES | 108 | 9,9% |
| TEORIA → QUESTOES → TEORIA → QUESTOES | 35 | 3,2% |
| só QUESTOES | 31 | 2,8% |
| TEORIA → ABERTURA → TEORIA → QUESTOES | 22 | 2,0% |
| TEORIA → REVISAO → TEORIA → QUESTOES | 19 | 1,7% |
| TEORIA → QUESTOES → REVISAO → QUESTOES | 16 | 1,5% |
| só TEORIA | 16 | 1,5% |

**806 PDFs (73,5%) estão numa das 4 formas canônicas simples.**

### Títulos que fecham a teoria (frequência no acervo)

| título | ocorrências | em N PDFs |
|---|---|---|
| GABARITO | 1.228 | 595 (82,5%) |
| QUESTÕES COMENTADAS | 1.080 | 513 |
| LISTA DE QUESTÕES | 1.003 | 446 |
| REFERÊNCIAS | 119 | 78 |
| LISTA DAS QUESTÕES | 84 | 75 |
| QUESTÕES PARA FIXAÇÃO | 82 | 56 |
| QUESTÕES COMENTADAS NA AULA | 77 | 52 |
| QUESTÕES RESOLVIDAS E COMENTADAS | 67 | 26 |
| LISTA DAS QUESTÕES COMENTADAS | 43 | 35 |
| RESPOSTAS DAS QUESTÕES SUBJETIVAS | 41 | 29 |
| QUESTÕES COMPLEMENTARES COMENTADAS | 30 | 30 |
| GABARITO DAS QUESTÕES COMPLEMENTARES | 30 | 30 |
| BIBLIOGRAFIA | 15 | 15 |
| EXERCÍCIOS COMENTADOS / PARA PRATICAR | 22 | 17 |

São **81 variantes distintas** contendo "QUESTÃO/QUESTÕES" e **10 variantes** de "GABARITO".
Listar títulos exatos não funciona.

**Regra prática:** normalizar o título e marcar como fim de teoria quando o texto
normalizado contiver `GABARITO`, `REFERENCIA`, `BIBLIOGRAFIA`, `EXERCICIO` ou `QUEST`.
Exceção: títulos que só *mencionam* questões e são conteúdo —
`TABELA DE APOIO PARA COMPREENSÃO DAS QUESTÕES COMENTADAS` e
`MOTIVAÇÃO DA AULA (QUESTÕES SUBJETIVAS)` (4 ocorrências no total).

A última faixa do PDF é `GABARITO` em 470 casos e `REFERÊNCIAS` em 74.

---

## L. Armadilhas de texto (obrigatório tratar)

Achadas na varredura, todas capazes de quebrar comparação de string:

1. **Versalete falso.** A fonte de título renderiza a capitular num tamanho e o resto
   noutro, e o extrator devolve `Q UESTÕES C OMENTADAS`, `L ISTA DE Q UESTÕES`,
   `G ABARITO`, `R EFERÊNCIAS`. Ocorre em 9-11 PDFs por variante.
2. **Caracteres invisíveis.** Zero-width space `U+200B` no começo do título
   (`​ EXERCÍCIOS COMENTADOS`) e marcas direcionais `U+202D/U+202C` no meio
   (`‭L‬‭ISTA‬‭DE‬‭Q‬‭UESTÕES‬`).
3. **Marca d'água antipirataria dentro do texto.** `GABARITO ==37DF0==` — um código
   por usuário injetado no meio do título, em 5 PDFs.
4. **Caixa desenhada duas vezes (sombra).** O mesmo rótulo sai duplicado:
   `DESCRIÇÃO DESCRIÇÃO`, `DDL (DATA DEFINITION LANGUAGE) DDL (DATA DEFINITION LANGUAGE)`.
5. **Glifo espúrio.** `CAUSAS DE EXTINÇÃO DA PUNIBILIDADE Ã DIVERSAS DA PRESCRIÇÃO`.
6. **Texto branco.** `color == 0xFFFFFF` é rótulo de fluxograma, não conteúdo.
7. **Texto vertical na lateral.** A tarja lateral vira letras soltas no topo da página
   (`N Õ I P Ã`) e polui o cabeçalho.

**Normalização recomendada antes de qualquer comparação:** remover invisíveis, subir
para maiúscula, remover acento, remover tudo que não for `A-Z0-9` (isso mata espaço,
pontuação e a marca d'água vira sufixo inofensivo), e desduplicar a repetição literal
`X X → X`. Depois comparar por **substring**, nunca por igualdade.

---

## Regras para a skill de mapeamento

Consolidado e acionável.

### 1. Abrir o PDF
- `pymupdf`, lendo o arquivo inteiro em memória primeiro
  (`open(path,'rb').read()` + `pymupdf.open(stream=...)`). Na pasta do Google Drive isso
  derrubou o tempo de 10s para 1,2s por PDF, porque evita acesso aleatório em arquivo
  transmitido.
- Confirmar A4 595×842pt (100% do acervo).

### 2. Achar as faixas de título (nível 1)
Retângulo preenchido que satisfaça **os quatro** critérios:
- cor roxa `(0.259, 0.192, 0.643)` com tolerância ±0.06;
- **altura ≥ 24pt**;
- x0 ≤ 12% da largura da página;
- largura ≥ 72% da largura da página.

Depois:
- **descartar sombra**: mesma página, mesmo y (±6pt) e mesmo x0 (±12pt) → é cópia;
- **juntar multilinha**: mesma página, x0 ±60pt, gap vertical entre −8pt e +14pt, em cadeia;
- **descartar caixa de citação**: texto > 90 caracteres, ou > 45 caracteres com > 55% minúsculas.

### 3. Achar os subtítulos (nível 2)
Pares de traços roxos de largura total separados por 14-46pt; o texto entre eles é o
subtítulo. Descartar se passar de 90 caracteres. Usar como estrutura principal quando o
PDF tiver menos de 3 faixas.

### 4. Achar os subtítulos de corpo (nível 3)
Histograma de tamanho de fonte ponderado por caracteres, **calculado por PDF**. A moda é o
corpo (12,0 em 84,7%, mas 13,0 e 11,0 acontecem). Tamanho acima do corpo = título.
**Não testar negrito.**

### 5. Resolver as faixas mudas
Se alguma faixa vier com texto vazio (2,3% delas, 6,5% dos PDFs), montar a folha de contato
e ler visualmente. **Não seguir sem resolver** — uma faixa muda pode ser justamente o
`QUESTÕES COMENTADAS` que fecha a teoria.

### 6. Classificar cada faixa
Normalizar (seção L) e classificar em ABERTURA / TEORIA / REVISAO / QUESTOES pelas
regras da seção K.

### 7. Recortar as zonas de teoria
Percorrer as faixas em ordem de página. Abrir zona ao encontrar `TEORIA`; fechar ao
encontrar `QUESTOES`; reabrir se aparecer `TEORIA` de novo. Cada zona é um assunto,
com início na página da faixa e fim na página da faixa seguinte menos 1.
- Se não houver faixa de encerramento (3,9%), a teoria vai até o fim do arquivo.
- Descartar as zonas `ABERTURA`.

### 8. Dimensionar o bloco de estudo
- Contar páginas **do arquivo**, nunca o número impresso (J).
- Classificar cada página como teoria ou questão (H) e dimensionar pelo conteúdo de teoria.
- Nunca cortar numa página em que uma tabela atravessa para a próxima (I).
- Preferir cortar exatamente numa faixa ou num subtítulo de nível 2 — assim o "até a
  página Y, tópico B" cai num limite real do documento.

### 9. Números de referência para calibragem
- Páginas por PDF: mediana **82**, média 99, mínimo 3, máximo 861.
- Páginas de teoria por PDF: mediana **28**, média 36, máximo 353.
- Faixas por PDF: mediana **8**.
- Distância entre faixas consecutivas: mediana **5 páginas**, média 9,4, p90 **24**, máximo 151.

Esse último número é o alerta: em 10% dos casos a distância entre duas faixas passa de
24 páginas, ou seja, **a faixa sozinha não dá granularidade suficiente para o bloco de
10 páginas**. Nesses trechos é obrigatório descer para o nível 2 (linhas roxas) ou o
nível 3 (tamanho de fonte).

---

## Casos que precisam de decisão do Elvis

1. **Fluxograma e mapa mental não são detectáveis com segurança.** O detector de tabela
   pega grade; os diagramas do Estratégia são caixas roxas soltas com setas e não têm
   assinatura geométrica confiável. Risco de cortar um diagrama ao meio. Opções: (a) aceitar
   o risco; (b) tratar como "não cortável" qualquer página com 3+ caixas roxas pequenas;
   (c) revisão visual só nos pontos de corte. Precisa de decisão.

2. **`RESUMO` conta como teoria?** 147 faixas são de revisão (`RESUMO`, `RESUMO ESTRATÉGICO`,
   `RESUMO EM MAPAS E ESQUEMAS`, `PARA REVISAR...`). Não é teoria nova, mas é material de
   estudo. Entra no bloco, vira bloco próprio, ou fica de fora do mapeamento?

3. **Disciplinas em que metade da "teoria" é questão comentada.** Em Língua Portuguesa
   (TCDF) 64,6% e em Direito Tributário 61% das páginas de teoria são questão. Um bloco de
   10 páginas ali entrega ~4 páginas de teoria nova. Manter 10 páginas fixas ou ajustar o
   alvo por disciplina?

4. **As 10 aulas longas com 1-2 faixas** (Bibliotecas Python 51 pg, LINDB 74 pg,
   Direito Previdenciário/Rubens Aula 04 com 110 pg). Algumas se resolvem pelo nível 2,
   outras não têm estrutura nenhuma. Mapear na mão, pular, ou cortar por página bruta?

5. **O simulado sem faixa** (`Legislacao Tributaria Estadual / Aula 05 - Simulado`).
   Provavelmente deve ficar fora do mapeamento de teoria — confirmar.

6. **Aulas com 2-3 assuntos empacotados** (6,9% dos PDFs = 76 aulas, concentradas em
   Contabilidade e Auditoria). Cada zona vira uma linha separada na planilha de mapeamento,
   ou a aula continua sendo uma linha só com os assuntos listados juntos?

7. **Percentual de questão por disciplina como fator fixo.** Dá para calcular uma vez e
   guardar na planilha, em vez de classificar página a página em toda execução. Vale a pena?

---

## Anexo — arquivos de trabalho

Os scripts e os dados brutos ficaram no scratchpad da sessão
(`scan3.py` varredura, `agg3.py` agregação, `titles.py` tabela de títulos,
`contact.py` folha de contato, `rec4.jsonl` um registro por PDF).
Nenhum PDF foi alterado; o trabalho foi só de leitura.
