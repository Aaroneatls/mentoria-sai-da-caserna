# Padrão de nomes de pasta e arquivo

> **Documento transversal.** Vale para as skills de download, para a base 2 (Estratégia), para a
> base 4 (materiais de parceiros) e para qualquer coisa que grave arquivo no Drive.
>
> Ele existe por um motivo medido: em 22/08/2026 o caminho mais longo do Drive tinha **263
> caracteres**, contra o limite de **260 do Windows**, e **157 arquivos** chegavam a 240. Já
> estava quebrado.
>
> **A regra 1 sozinha resolve.** Medido em duas sessões independentes: aplicando só ela, os 157
> caem para **zero** e o pior caminho vai de 263 para **227**. Sobra folga para a subpasta de
> apoio (82 caracteres) em todas as 71 disciplinas — a pior fica em 229.
>
> Isso importa para a ordem do trabalho: a renomeação **não depende da sigla da base 1**. O
> prefixo de sigla é ganho de organização, e como ele *acrescenta* 8 caracteres, é bom que a
> folga já esteja garantida sem ele.

---

## 1 · O orçamento de caracteres

**A regra que manda é uma só: nenhum caminho real pode chegar a 240.** O Windows corta em 260; os
20 de sobra são para quem mover a pasta ou criar uma subpasta.

Os tetos por nível abaixo são **guarda-corpo**, para um nome fugir do controle e ser pego cedo.
Eles **não somam** o limite, e não deveriam: medido em 22/08, o pior caminho real é **219**,
enquanto a soma dos tetos dá 255. Os níveis não estouram juntos — o arquivo de 92 caracteres mora
numa pasta de nome curto.

| Nível | Teto | Maior real hoje | Exemplo |
|---|---|---|---|
| Raiz (fixa) | 47 | 47 | `G:\Meu Drive\Inteligência Artificial\Estrategia\` |
| Concurso | 28 | 26 | `Pacotaço TCDF (ANACE) 2026\` |
| Tipo de curso | 20 | 17 | `Passo Estratégico\` |
| Disciplina | **64** | 58 | `AFO - Administracao Financeira e Orcamentaria (18-08-2026)\` |
| Arquivo | **92** | 92 | `Aula 16 - Responsabilidades - Sindicância e proc… LC (30-07-2026).pdf` |

Dentro do nível disciplina: **45** para o `<SIGLA> - <Disciplina>`, **13** para a data (regra 9) e
**6** para a marca de pendência (regra 6). 45 + 13 + 6 = 64.

> ### REGRA 10 — quando o caminho passar de 240, quem encurta é o ARQUIVO
>
> Se um caminho real chegar a 240 sem que nenhum nível tenha estourado o seu teto, **encurta-se o
> nome do arquivo**, nunca o da pasta.
>
> A pasta é **identidade** — é por ela que se acha a disciplina, e ela aparece em toda a base. O
> nome do arquivo é **descrição**, e os títulos do Estratégia trazem gordura de sobra
> (`Aula 14 - Funções essenciais à justiça - 9.1 Ministério Público - 9.2 Ad…`). Cortar descrição
> custa pouco; cortar identidade quebra o join.
>
> Encurta-se **pelo fim do tema**, preservando sempre `Aula NN`, a versão (`LS`/`LC`) e a data.

**O `conferir` tem de FALHAR** quando qualquer caminho real chegar a 240 — não avisar. Teto que
ninguém testa não é teto.

**Histórico de um erro deste próprio documento:** até 22/08 a tabela dizia teto 80 para o arquivo,
número que nunca foi medido. O maior real já era 92, e a mediana é 60. Um teto inventado não
segura nada e ainda faz o orçamento parecer apertado onde ele não é.

## 2 · O erro que causou o estouro, e a regra que o impede

O caminho campeão era este:

```
...(ISS Manaus-AFTM) (19-08-2026)\Legislação Tributária (Zona Franca de Manaus) (ISS Manaus-AFTM) - Metadados.gsheet
```

`(ISS Manaus-AFTM)` aparece **duas vezes** e a data também. A pasta filha repetia o que a pasta
pai já dizia.

> ### REGRA 1 — não repetir o que o pai já diz
>
> Concurso, data e tipo de curso aparecem **uma vez só**, no nível onde nascem. A pasta da
> disciplina não repete o concurso; o arquivo não repete a disciplina.

Só essa regra devolve **60 caracteres** de folga.

---

## 3 · A estrutura

```
G:\Meu Drive\Inteligência Artificial\Estrategia\
└── <Concurso> (<Sigla-Concurso>) <Ano> (<DD-MM-AAAA>)\
    └── <Tipo de Curso>\
        └── <SIGLA> - <Disciplina>\
            ├── <Aula NN> - <Tema> <LS|LC> (<DD-MM-AAAA>).pdf
            ├── Apoio - Resumos e Mapas Mentais\
            │   ├── R - <slug>.pdf
            │   └── MM - <slug>.pdf
            └── <SIGLA> - Metadados.gsheet
```

### Nível 1 — Concurso

| | |
|---|---|
| Formato | `<Nome> (<Sigla>) <Ano>` |
| Exemplos | `Pacotaço TCDF (ANACE) 2026` · `Regular Controle` |
| A data | **não vem aqui** — ver a regra 9 |

Curso Regular não tem concurso nem ano: fica `Regular Controle` e `Regular Fiscal`.

### Nível 2 — Tipo de curso

Valores fixos: `Curso Regular` · `Passo Estratégico` · `Bizu Estratégico` · `Monitoria` ·
`Trilha` · `Rodadas Avançadas`.

Existe mesmo quando só há um tipo, porque a estrutura tem de ser previsível para a skill que lê.

### Nível 3 — Disciplina

| | |
|---|---|
| Formato | `<SIGLA> - <Nome que a fonte usa> (<DD-MM-AAAA>)` |
| Exemplo | `DADM - Direito Administrativo (18-08-2026)` |

> ### REGRA 9 — a data mora onde a atualização acontece
>
> A data fica **na disciplina**, não no concurso. Decidido pelo Elvis em 22/08/2026.
>
> Ele já tinha fixado em 18/08 que queria ver, só olhando o Drive, quando cada matéria foi mexida.
> Esse motivo **ficou mais forte** com o modo `atualizar`: antes o curso vinha inteiro de uma vez e
> a data do concurso dizia a verdade sobre tudo dentro dele; agora a atualização é **por
> disciplina**, e uma data no nível do concurso passa a **mentir** assim que uma única matéria for
> atualizada.
>
> Custo: **zero**. Saem 13 caracteres de um nível e entram 13 no outro — o caminho medido fica em
> ~219, o mesmo do cenário sem data nenhuma.
>
> Não duplicar: data em dois níveis são duas versões da mesma verdade, e elas divergem.

> ### REGRA 2 — a sigla é nossa, o nome é da fonte
>
> O prefixo é o nosso Cód Mestre de disciplina; o resto é **o nome que o Estratégia usa**,
> sintetizado se passar de 45 caracteres, mas **nunca traduzido**.
>
> Traduzir quebra a busca: quem abre a plataforma procurando `TECINF` não acha nada. E o prefixo
> agrupa a listagem por disciplina, que com 21 pastas por curso faz diferença.

**Nunca repetir o concurso aqui.** Ele já está no nível 1.

**Nunca levar numeração de aula.** Sobras como `(41-42)` são posição, não identidade, e a pasta
identifica conteúdo. Fora.

**Sufixo de professor entra quando DISTINGUE.** Só há um caso hoje — as duas Contabilidades do
Regular Fiscal, que sem o sobrenome viram o mesmo nome e perdem a distinção de que o A8 depende:

| | |
|---|---|
| `CONTAB - Contab Geral e Avancada (Possati)` | 42 |
| `CONTAB - Contab Geral e Avancada (Cardozo)` | 42 |

Note o tipo de síntese: encurtou-se **uma palavra** (`Contabilidade` → `Contab`), não um conceito.
`Geral`, `Avancada` e o professor sobrevivem inteiros. **Síntese tira caracteres, nunca informação.**

**Medido em 22/08:** dos 29 pares `<SIGLA> - <Disciplina>` das fontes, **27 cabem** nos 45. Os dois
que estouram são esses. E a sigla não é a culpada — o par mais apertado que ainda cabe é
`AFO - Administracao Financeira e Orcamentaria`, com **45 exatos** e a menor sigla do conjunto.
Encurtar sigla não compra folga onde a folga falta; quem come o orçamento é o nome da fonte.

### Nível 4 — Arquivo de aula

| | |
|---|---|
| Formato | `Aula NN - <Tema> <LS\|LC> (<DD-MM-AAAA>).pdf` |
| A data | é a **da capa do PDF**, não a do download |
| `LS` / `LC` | livro simplificado ou completo. **O simplificado é o padrão**; o completo entra quando não existe simplificado |
| O tema | vem **da capa do PDF**, não do rótulo do site, quando os dois divergirem |

### Nível 4b — Apoio (resumo e mapa mental)

Subpasta `Apoio - Resumos e Mapas Mentais`, **única por disciplina, sem subpasta por aula**.

| Prefixo | O que é |
|---|---|
| `R - ` | resumo |
| `MM - ` | mapa mental |

```
DADM - Direito Administrativo/
└── Apoio - Resumos e Mapas Mentais/
    ├── MM - Atos Administrativos.pdf
    ├── MM - Improbidade Administrativa.pdf
    ├── MM - Licitações e Contratos.pdf
    ├── R - Atos Administrativos.pdf
    ├── R - Improbidade Administrativa.pdf
    └── R - Poderes Administrativos.pdf
```

> ### REGRA 7 — o nome do apoio leva o ASSUNTO, nunca a aula
>
> **Por que sem subpasta por aula:** o mesmo arquivo serve vários vídeos e às vezes aulas
> diferentes. Subpasta obrigaria a duplicar (e as cópias divergem) ou a esconder o arquivo das
> outras aulas.
>
> **Por que o nome não leva a aula:** se o arquivo serve as aulas 6, 7 e 9, chamá-lo de
> `R - A06 - ...` **mente** para as outras duas. Aula é circunstância, não identidade — vira
> **coluna** na base, e pode ter mais de um valor.
>
> **Por que o assunto:** é como um humano procura ("o resumo de Improbidade", não "o resumo da
> aula 16"), e é como a correlação funciona — a API não diz que páginas do livro o vídeo cobre,
> então o vínculo com o bloco é **por assunto**. O nome já carrega o que vai ser usado.

**O slug vem da capa do PDF**, não do título do vídeo, quando os dois divergirem (regra 5). Se a
capa não tiver título utilizável, cai para o título do vídeo, e a base registra qual fonte foi
usada. Até 40 caracteres.

> ### REGRA 8 — filtrar a marca d'água ANTES de gerar o slug
>
> Os PDFs do Estratégia trazem `<CPF> - <Nome do titular>` na camada de texto, em quase toda
> página, **capa inclusive**. Se a extração do título acontecer antes do filtro
> `^\s*\d{11}\s*-\s*.+$`, o CPF entra no **nome do arquivo**.
>
> Aí ele deixa de ser um dado no texto e vira **dado pessoal no caminho da pasta**, sincronizado
> pro Drive e visível em qualquer print de tela. O filtro roda antes do slug, não só antes do
> hash.
>
> Vale para todo nome derivado de conteúdo de PDF, não só o do apoio.

**Volume esperado:** o piloto de Direito Constitucional deu 12 resumos e 20 mapas mentais, 32
arquivos. O prefixo já agrupa por tipo e o resto ordena por assunto, então não precisa subdividir.
**Se alguma disciplina passar de ~60 arquivos**, aí sim reavaliar.

---

## 4 · Regras que valem em todos os níveis

> ### REGRA 3 — primeira letra maiúscula
> Vale para toda pasta criada.

> ### REGRA 4 — nunca apagar e recriar
> Atualizar renomeia **em cima** da pasta existente. Apagar e recriar perde o histórico e, se o
> download falhar no meio, perde o material.

> ### REGRA 5 — o nome do arquivo vem da capa do PDF
> Quando o rótulo do site divergir do título impresso na capa, **vale o da capa**. É o que o aluno
> vê quando abre.

> ### REGRA 6 — pendência entra no FIM do nome, nunca no começo
> Se sobrou material por baixar, a pasta ganha `(N-M)` **no fim**: quantos de quantos vieram. Sem
> pendência, sem marca.
>
> ```
> LTRIB - Legislacao Tributaria Municipal (3-14)     certo
> (3-14) Legislacao Tributaria Municipal             errado
> ```
>
> **Por que no fim:** no começo, o parêntese ordena antes de qualquer letra, então **todas** as
> pastas com pendência sobem juntas para o topo da listagem, agrupadas por defeito em vez de por
> disciplina. Isso briga de frente com o prefixo de sigla, que existe justamente para agrupar.
> Corrigido em 22/08, a partir da leitura da sessão de download.

---

## 5 · Como as outras bases leem isto

O caminho é **estruturado**, então dá para extrair sem depender de tabela:

```
.../Regular Controle (18-08-2026)/Curso Regular/DADM - Direito Administrativo/Aula 06 - Atos Administrativos LS (12-05-2026).pdf
     └──── concurso ─────┘ └─data─┘  └─── tipo ───┘  └sigla┘ └── nome na fonte ──┘ └aula┘ └─ tema ─┘ └v┘ └─capa─┘
```

| Campo | De onde sai |
|---|---|
| `concurso`, `data_download` | nível 1 |
| `tipo_curso` | nível 2 |
| `sigla`, `nome_na_fonte` | nível 3, separados pelo primeiro ` - ` |
| `aula`, `tema`, `versao`, `data_capa` | nível 4 |

**Mas o caminho é conveniência, não fonte.** A fonte é a base 2. Se um dia alguém renomear uma
pasta na mão, a base continua certa e o caminho é que fica errado — e o modo `conferir` da skill
tem de pegar isso.

---

## 6 · O que este padrão NÃO resolve

**Nome de arquivo curto perde informação.** `DADM-0018.pdf` cabe em qualquer lugar e não diz nada
para quem abre a pasta. Por isso o nome continua legível, e a identidade fica na base.

**Disciplina que a fonte divide em duas** (o caso de Informática e Tecnologia da Informação no
mesmo curso) vira **duas pastas com a mesma sigla**. Isso é esperado, e a tabela de pares
bloco × tópico resolve. Não force numa pasta só.

**Concurso com vários produtos** (Regular, Passo, pacotaço, sistema de questões) não vira várias
pastas: baixa-se **só o Curso Regular**, então existe uma pasta por concurso.
