# Quais materiais do Estratégia entram no mapeamento por página

> Investigação de 2026-08-20, no pacote **TCDF (Analista Administrativo de Controle
> Externo — Serviços Técnicos Administrativos — ANACE) Pacotaço — Pacote Teórico +
> Pacote Passo Estratégico — 2026 (Pós-Edital) + Sistema de Questões**
> (`/app/dashboard/pacote/393930`, 35 cursos).
>
> Amostra: **48 itens** — 29 PDFs baixados na hora (pasta temporária, apagada depois),
> 17 PDFs do Curso Regular já sincronizados no Drive (um sorteado por disciplina) e
> 2 anexos de videoaula (slide + mapa mental) e 4 Bizus Estratégicos. Nenhum HTTP 429.

---

## Como a amostra foi levantada

A varredura saiu inteira da API interna, sem navegar curso por curso:

- `GET /api/aluno/curso/{id}` — devolve todas as aulas do curso com `pdf`,
  `pdf_simplificado`, `pdf_grifado`, `is_disponivel` e as flags do curso
  (`funcionalidade_mapa_mental`, `funcionalidade_resumo`, `raio_x`, `mapa_da_lei`).
- `GET /api/aluno/aula/{id}` — **é aqui que mora o resto.** Descoberta desta sessão,
  e a mais importante para a skill de download.

**O endpoint de curso é um resumo, e mente por omissão.** Ele devolve `videos: []` e
`pdf_grifado: null` mesmo quando os dois existem. Só o endpoint de **aula** traz:

| Campo | No endpoint de curso | No endpoint de aula |
|---|---|---|
| `videos` (com `slide`, `mapa_mental`, `resumo`, `audio`) | quase sempre vazio | completo |
| `pdf_grifado` | quase sempre nulo | presente |

Medido na Aula 03 de Direito Administrativo do TCDF (`3951051`): pelo curso, zero
vídeos e sem grifado; pela aula, **8 vídeos, 2 slides, 1 mapa mental e o PDF grifado**.

**Isso invalidou uma conclusão intermediária desta própria investigação** — cheguei a
registrar que "PDF grifado e resumo estão ligados na conta e vazios", quando na verdade
eu estava lendo o endpoint errado. Regra pra skill: **nunca concluir ausência de
material a partir do endpoint de curso.**

Detector de título: o tipográfico de
[[project_detector_tipografico_titulos_estrategia]] (faixa roxa `(0.259,0.192,0.643)`
+ histograma de corpo de fonte), rodado com `pymupdf` sobre os 48 arquivos.

**Nenhum dos 48 PDFs tem sumário embutido** (`get_toc()` volta vazio em 48/48),
em nenhum tipo de material. O detector tipográfico não é o caminho preferido: é o
único caminho.

---

## Tabela por tipo de material

| Tipo | O que é | Itens | Tem estrutura de título? | Entra no mapeamento? | Por quê |
|---|---|---|---|---|---|
| **Aula em PDF (Curso Regular)** | Teoria completa, 27-246 pgs | 18 | **Sim.** Faixa roxa + corpo 11-13 com 3-4 níveis acima | **Sim — é o material do aluno** | O aluno faz **só o Curso Regular** por padrão. Método validado em 17 disciplinas deste pacote |
| **PDF Simplificado** | Mesma aula sem os grifos/boxes | 126 de 180 aulas | Sim, mesmo template | **SIM — é o arquivo de referência** | Decisão do Elvis (2026-08-20). É o que a skill de download já prioriza e o que está na pasta. **Mas 30% das aulas não têm** — ver ressalva abaixo |
| **PDF Grifado** | Aula com marcação do professor | 5 aulas checadas | Mesmo template da aula | **Sim, espelhado** | **Existe** — só não aparece no endpoint de curso (ver correção abaixo). Mesma teoria da aula, paginação a conferir |
| **Passo Estratégico** | Teoria condensada por assunto, 3-46 pgs | 8 | **Sim, e bem limpa.** Faixa roxa + 16/14/13 sobre corpo 12 | **Exceção, não regra** | É teoria (não revisão), mas **fora do plano padrão**. Só em matéria de peso baixo, e ainda assim raro. Avaliação completa adiada pro 1º pós-edital |
| **PE — aula "Simulado"** | Questões inéditas + gabarito comentado | 1 | Sim, mas por bloco de questão | **De outra forma** | Âncora é o assunto do simulado, não a página |
| **PE — "Análise Estatística"** | Tabela de % de incidência por assunto | 2 | Faixa única, 3 pgs | **Não** | Decisão do Elvis (2026-08-20): **estatística do Estratégia não vale como referência**, nem para compor nem para conferir. O banco de pesos é nosso. Ver [[project_base_propria_de_pesos_substitui_tec]] |
| **PE — "Caderno de Jurisprudência"** | Julgados por assunto, 16 pgs | 1 | Sim, uma faixa por assunto | **Sim, mas como revisão** | Não traz teoria nova. Mesmo tratamento do `COMPILADO DE JURISPRUDÊNCIA` dentro da aula |
| **PE — "Questionários EXTRAS"** | Perguntas/respostas de revisão, 246 pgs | 1 | Sim, faixa por assunto (29 faixas) | **De outra forma** | Volume enorme, zero teoria nova. Âncora é o assunto |
| **Bizu Estratégico** | Revisão em esquemas, 29-46 pgs, 32 aulas | 4 | Sim (16/14 sobre 12), mas só 3 faixas roxas | **Baixa prioridade** | Quase todo imagem (3.680 numa aula), página não serve. E o Resumo Esquematizado do Bezerra cobre o mesmo papel muito melhor — ver comparação abaixo |
| **Trilha Estratégica** | Plano de estudos semanal do Estratégia | 3 | Sim (22/16/15 sobre 12), 21-23 faixas | **De outra forma — e é referência** | Ver seção própria abaixo |
| **Rodadas Avançadas de Simulados** | Caderno de prova + gabarito + ranking | 3 | Faixa roxa, mas de seção administrativa | **Não** | É prova, não material de estudo. Âncora natural é o número da questão |
| **Discursiva Sem Correção** ("as Cursivas") | Produção textual + rodadas de temas | 3 | Sim, mas **template diferente** | **Sim, com ressalva** | É o que o Elvis chama de "Cursivas". Traz teoria própria (tipologia textual, estrutura do texto) e rodadas de temas. Capitular/versalete despedaçado é severo aqui |
| **Monitoria** | Encontros do Prof. Fábio Dias | 2 | Não | **Não** | O PDF é um stub de 3 páginas que diz, com todas as letras, que **as aulas saem só em vídeo, sem PDF e sem fórum** |
| **Videoaula** | Vídeo por tópico, 8 por aula na amostra | 8 (metadados) | — | **De outra forma** | Âncora é o **título do vídeo**, não a minutagem: os vídeos já vêm picados por tópico |
| **Slide de videoaula** | PDF 720x405, 75 pgs | 1 | Não tem faixa nem hierarquia de corpo | **De outra forma** | Um slide por página. Âncora é o número do slide, mas só existe **no primeiro vídeo de cada bloco** |
| **Mapa mental** | PDF 1386x780, 1 assunto por página | 1 | Não | **De outra forma** | Âncora é o nome do assunto. Também só no primeiro vídeo do bloco |
| **Resumo (por vídeo)** | Campo `resumo` da API | 38 vídeos checados | — | **Raro demais pra contar** | Existe, mas **1 em 38 vídeos** o tem (PRF Português Aula 00). Não dá pra montar índice em cima disso |
| **Legislação / súmulas / Raio-X / Mapa da Lei** | — | — | — | **Não existe aqui** | `raio_x=false` e `mapa_da_lei=false` nos **35** cursos. Legislação aparece **dentro** da aula (faixa `LEGISLAÇÃO`), não como curso |
| **Sistema de Questões** | Banco de questões da plataforma | — | — | **Não (é outra trilha)** | Campo `tec_concursos` veio nulo em todas as aulas do pacote. Nossa correlação com questões passa pelo TecConcursos |

---

## Os três tipos que faltavam — todos resolvidos

- **Bizu Estratégico** — não está no TCDF, mas **está no Curso Regular Área Fiscal e
  no PRF Pacotaço**, os dois já matriculados. Também existe avulso no catálogo, com
  **122 versões por concurso-cargo** (SEFAZ-CE, SEFAZ-RS, ISS Santos-SP, ISS Campina
  Grande-PB, PM-SP, ALECE, TJs, PC-PR…). Examinado — ver seção própria abaixo
- **"Cursivas" = o curso de Discursiva** (Elvis, 2026-08-20). Não era tipo novo: é o
  `Discursiva Sem Correção`, que o TCDF tem (curso `393491`, 8 aulas) e que já estava
  na amostra. Traz teoria de produção textual e **rodadas de temas** (Prof. Márcio
  Damasceno, 3 rodadas)
- **Curso Estratégico** — nenhum produto se chama assim. A busca devolve 3632 itens,
  mas todos são casamento solto de "Curso" com "Estratégico" (`Passo Estratégico ... -
  Curso Regular`). Segue sem existir

### Como achar um tipo de material sem abrir curso por curso

`GET /api/aluno/pacote/{id}` devolve `cursos[]` com um campo **`tipo_curso_id`**, que
é a classificação real do material. Decodificado nesta sessão comparando os três
pacotes matriculados:

| `tipo_curso_id` | Material |
|---|---|
| 1 | Curso Regular / teoria (inclui Discursiva) |
| 3 | Monitoria |
| 5 | Trilha Estratégica |
| 7 | Passo Estratégico |
| 27 | **Bizu Estratégico** |
| 30 | Rodadas Avançadas de Simulados (confirmado nos 3 pacotes) |

Isso é bem mais barato que varrer nome de curso, e é o caminho pra skill descobrir
o que um pacote tem antes de baixar qualquer coisa.

### A busca do catálogo acha, sim — mas só na aba CURSOS

O Bizu **é produto avulso e matriculável**: a aba CURSOS devolve **122 resultados**
para "Bizu". Ele aparece por concurso-cargo, no mesmo padrão dos outros materiais:

- `Prefeitura de Manaus-AM - ISS Manaus (Auditor Fiscal de Tributos Municipais -
  AFTM - Nível I) **Bizu Estratégico** - 2026 (Pós-Edital)`
- `SEFAZ-CE`, `SEFAZ-RS`, `SEFAZ-AC`, `SEFAZ-DF`, `ISS Santos-SP`,
  `ISS Campina Grande-PB`, `PM-SP`, `ALECE`, `TJs`, `PC-PR`… (122 no total)
- `Curso Regular para Área Fiscal - Bizu Estratégico` — o que examinamos

**Armadilha da interface que custou uma conclusão errada:** clicar na aba CURSOS
**por coordenada não troca a aba** — a página continua listando PACOTES, e a busca
volta zero para qualquer coisa que só exista como curso. O clique só pega chamando
`element.click()` direto no `<button>`. Dá pra conferir pela classe: a aba ativa tem
`class="Tab isActive"`. **Sempre verificar a aba ativa antes de confiar num resultado
de busca vazio.**

A busca também é **fuzzy (OR)**: "Bizu Receita Federal" devolve 3772 resultados
casando só "Receita" ou "Federal". Resultado alto não quer dizer que achou; ler os
primeiros itens é obrigatório.

Os dois caminhos servem a coisas diferentes: `tipo_curso_id` diz **o que tem dentro
de um pacote já matriculado**; a aba CURSOS diz **o que existe no catálogo** e pode
ser matriculado avulso.

---

## O simplificado é a referência — e falta em 30% das aulas

Decisão do Elvis (2026-08-20): o mapeamento se faz sobre o **PDF simplificado**. É o que
a skill de download já prioriza, então é o que está na pasta do Drive.

O problema medido no pacote TCDF-ANACE:

| | Aulas |
|---|---|
| Curso Regular do pacote | 180 |
| Com `pdf_simplificado` | **126 (70%)** |
| Só com original | 54 (30%) |

**Quatro disciplinas não têm nenhum simplificado:** Língua Portuguesa, Lei Orgânica do
DF, Lei Orgânica do TCDF e Regime Jurídico dos Servidores. Outras têm parcial — Direito
Administrativo tem 14 de 21.

Como a skill cai pro original quando não há simplificado, **a pasta é mista e o nome do
arquivo não diz qual versão é**. Antes de mapear é preciso saber qual versão está em
mãos: as paginações são diferentes e a âncora de página só vale pro arquivo que o aluno
tem. Duas saídas possíveis, e nenhuma foi decidida:

1. Gravar a versão no nome do arquivo (ou numa planilha de metadados) no momento do
   download.
2. Detectar a versão pelo próprio PDF (o simplificado tem menos páginas e menos boxes
   para a mesma aula) — só funciona se os dois estiverem à mão para comparar.

Confirmei que `pdf_simplificado` **é confiável no endpoint de curso**, ao contrário de
`pdf_grifado` e `videos`. A ausência é real, não artefato de leitura.

---

## Estrutura fixa do Passo Estratégico

Todos os 8 PE examinados seguem a mesma espinha, o que faz dele o tipo **mais
previsível de todos** — mais até que a aula em PDF:

```
p2   Índice
p3   ANÁLISE ESTATÍSTICA · "O que é mais cobrado dentro do assunto?"
p4   ROTEIRO DE REVISÃO E PONTOS DO ASSUNTO QUE MERECEM DESTAQUE   <- a teoria
...  (16 = seção · 14 = item · 13 = subitem)
p29  APOSTA ESTRATÉGICA
p31  QUESTÕES ESTRATÉGICAS
p37  QUESTIONÁRIO DE REVISÃO E APERFEIÇOAMENTO
p42  REFERÊNCIAS BIBLIOGRÁFICAS
```

A **teoria do PE** vai de `ROTEIRO DE REVISÃO...` até antes de `APOSTA ESTRATÉGICA`.
Tudo depois é exercício. Vale a mesma regra de fim de teoria da aula em PDF, só que
com faixas de nome diferente — a lista de faixas terminais da skill precisa crescer.

**Armadilha nova: capitular (drop cap).** No PE o template usa letra inicial maior
que o resto do título, e o `pymupdf` devolve os dois pedaços separados:

```
"TOS" + "DMINISTRATIVOS"   ->  ATOS ADMINISTRATIVOS
"OTEIRO DE REVISÃO..."     ->  ROTEIRO DE REVISÃO...
"POSTA" + "STRATÉGICA"     ->  APOSTA ESTRATÉGICA
```

É primo do versalete despedaçado que já está na memória, mas o defeito é outro: ali
faltava juntar letra solta, aqui a **primeira letra some do span**. Quem recompõe é
a faixa roxa (`page.get_text(clip=rect)` devolve a frase inteira). Regra prática:
**quando o span de título começa no meio de uma palavra, cair pro texto da faixa.**

---

## Bizu Estratégico — examinado no Curso Regular Área Fiscal (curso `356047`)

4 itens examinados (Aula 00 "Explicações", Português, Direito Administrativo,
Auditoria). O curso tem **32 aulas, uma por disciplina, todas disponíveis**.

**Não se ancora por página — ancora-se pelo número do bizu.** Cada aula é uma lista
de itens numerados `1)`, `2)`, `3)`… sob o nome do assunto, e a própria aula traz na
p4 um índice que já faz a correlação:

| Assunto | Bizus | Caderno de Questões |
|---|---|---|
| Atos Administrativos | 1 a 11 | `questo.es/6q3bqm` |
| Licitações | 12 a 22 | `questo.es/tddouo` |
| Lei de Acesso à Informação | 23 a 26 | `questo.es/csdtl2` |

Ou seja: o Estratégia já entrega **assunto → intervalo de bizus → link de caderno
pronto**. É a mesma correlação que estamos construindo, só que dentro da casa deles
e com o Sistema de Questões deles em vez do Tec.

Três coisas medidas:

- **É quase todo imagem.** O Bizu de Direito Administrativo tem 46 páginas e **3.680
  imagens**; o de Português, 555; o de Auditoria, 986. O conteúdo é esquema e
  fluxograma, não prosa. O detector tipográfico acha os títulos, mas o *conteúdo* não
  sai por extração de texto — o que sai vem quebrado (`"Presungaode leg[timidade"`).
- **Só 3 faixas roxas por aula.** A hierarquia real é por corpo de fonte (16/14 sobre
  12) e pela numeração. Faixa roxa aqui não serve de ponto de corte.
- **Tem Análise Estatística própria** (p3), com % de cobrança por assunto para
  Cebraspe/FCC/FGV juntas — outra fonte pro banco de pesos, com recorte diferente da
  do Passo Estratégico (que é por banca e cargo específicos).

### Bizu x Resumo Esquematizado do Bezerra — o Bezerra ganha

O Elvis mandou comparar os dois, e os números dão razão a ele. Mesma disciplina,
Direito Administrativo:

| | Bizu Estratégico | Resumos Bezerra |
|---|---|---|
| Cobertura da disciplina | 1 PDF, 46 pgs | **18 PDFs, 468 pgs** |
| Densidade de texto | 1.361 chars/pg | **2.056 chars/pg** |
| Imagens por página | **80** | 1 |
| Sumário com página | não | **sim, em todo PDF** |
| Um arquivo por tópico | não (tudo junto) | **sim** (`R05 - Atos Administrativos`) |

O Bizu de Atos Administrativos são os **bizus 1 a 11** dentro de um arquivo que cobre
a disciplina inteira. O Bezerra dá **26 páginas só de Atos Administrativos**, em
arquivo próprio, com sumário. Para indexar e para mandar o aluno a um ponto, não há
comparação: 80 imagens por página significa que o Bizu **não tem texto extraível** —
o pouco que sai vem quebrado (`"Presungaode leg[timidade"`).

**Veredito: baixa prioridade.** O Bizu não acrescenta nada que o Bezerra não dê melhor,
e custa muito mais pra indexar. Fica registrado como material existente, fora da fila.

**O índice do Bizu também não vale a pena** (Elvis, 2026-08-20). Ele entrega
assunto → intervalo de bizus → caderno pronto, mas as referências nós mesmos já
estamos levantando, e com mais granularidade. Não é insumo.

---

## A Trilha Estratégica é o nosso concorrente direto (e a prova do problema)

A Trilha é o plano de estudos que o próprio Estratégia entrega. Vale ler o que ela
manda o aluno fazer:

> TAREFA 1 — Administração Geral e Pública
> "Revisão/Estudo da teoria da Aula 02 (Pdf simplificado)."
> Link: .../cursos/393270/aulas

A granularidade da Trilha é **a aula inteira**. Nunca um intervalo de páginas, nunca
um tópico. A Trilha 01 tem 17 tarefas, e todas são "estude a Aula NN" ou "resolva N
questões". É exatamente o buraco que o nosso mapeamento preenche: quem tem a Aula 06
de Português com **185 páginas** não recebe da Trilha nenhuma pista de onde parar.

Mas ela é **insumo bom**: já diz a ordem de estudo, qual PDF usar (original x
simplificado) e quantas questões resolver por aula. Serve de referência de sequência
e de conferência, não de composição — mesmo tratamento que demos aos Guias do Tec
em [[project_guias_do_tec_uso_e_limites]].

---

## Como ancorar cada tipo

| Tipo | Âncora que vamos dar ao aluno |
|---|---|
| Aula em PDF | `De "<título>" (p13) até antes de "<título>" (p20)` — padrão já definido, página do arquivo PDF |
| PDF Simplificado | Mesma frase de tópico, **página recalculada no arquivo simplificado**. Nunca reaproveitar a página do original |
| Passo Estratégico | Mesma frase, dentro do `ROTEIRO DE REVISÃO`. Fora do roteiro, não ancorar por página |
| Caderno de Jurisprudência | Nome do assunto (uma faixa por assunto) |
| Análise Estatística | Não se ancora — vira linha de peso na base |
| Simulado / Questionário Extra / Rodadas | **Número da questão**, no mesmo padrão do Tec ([[feedback_numero_questao_tec]]) |
| Discursiva | Nome do tópico + página, mas conferir o template antes (é outro) |
| Videoaula | **Título do vídeo** (`Aula 03 · vídeo 4 "EP e SEM - Licitações"`). Minutagem não serve: os vídeos já vêm picados por tópico, e o título é estável |
| Slide | Número do slide dentro do bloco. Só existe no 1º vídeo do bloco |
| Mapa mental | Nome do assunto (1 assunto por página) |
| Bizu Estratégico | **Número do bizu** (`Bizus 12 a 22 — Licitações`). O índice da p4 já dá o intervalo por assunto |
| Trilha Estratégica | Número da tarefa (`Trilha 01, tarefa 4`) |

---

## Decisões — o que foi resolvido nesta sessão

| # | Questão | Resolução |
|---|---|---|
| 1 | Qual material o aluno faz? | **Só o Curso Regular**, pelo **PDF simplificado**. O Passo é teoria, mas fica de fora do padrão — só em matéria de peso baixo, e raro. A avaliação de incluir o Passo fica pro **1º pós-edital que tiver Passo Estratégico** |
| 2 | Estatística do Estratégia entra na base de pesos? | **Não.** Nem para compor, nem para conferir. O banco de pesos é nosso |
| 3 | O índice do Bizu serve de insumo? | **Não.** As referências já saem do nosso levantamento, com mais granularidade |
| 4 | O que são "Cursivas"? | O curso de **Discursiva**. Já estava na amostra |
| 5 | "Curso Estratégico" existe? | **Não**, nenhum produto com esse nome |
| 6 | `pdf_grifado` e `resumo` existem? | **Grifado sim**, era erro de endpoint. **Resumo é raro** (1 em 38 vídeos) |
| 7 | `tipo_curso_id=30` é o quê? | **Rodadas Avançadas de Simulados** |
| 8 | Bizu do ISS Manaus / área fiscal | Existe o do ISS Manaus. Na área fiscal, só ele — fechado, sem pendência |

## O que ainda está em aberto

1. **Slide e mapa mental só existem no primeiro vídeo de cada bloco.** Na Aula 03 de
   Direito Administrativo, 8 vídeos, só 2 têm slide e só 1 tem mapa mental. Ou
   indexamos por **bloco de vídeo** (não por aula), ou o índice fica cheio de buraco.
   Isso fecha a pendência de [[project_resumos_mapas_mentais_indexacao]] no
   diagnóstico, mas a decisão de formato ainda é do Elvis.

2. ~~**Como saber qual versão está na pasta.**~~ **RESOLVIDO em 2026-08-20.** As 4
   pastas foram renomeadas com sufixo `LS`/`LC` (1096 PDFs, zero sem sufixo) e as skills
   de download passaram a gravar o sufixo na origem. Validação por `Range` conferiu 166
   aulas e corrigiu 19 rótulos errados. Falta só validar o TCDF, que precisa do pacote
   `393930` rematriculado.

3. **PDF grifado é uma terceira paginação.** Existe em boa parte das aulas (inclusive
   em disciplinas sem simplificado, como Língua Portuguesa e Regime Jurídico). Não foi
   examinado. Pode ser a saída para as 4 disciplinas sem simplificado — ou só mais
   confusão.

4. **A segmentação em blocos ainda não foi testada no Passo Estratégico.** Provei que
   a estrutura de títulos existe e é limpa; não rodei a quebra em blocos de 10-20
   páginas em cima dela.

5. **Rodadas Avançadas: 25 de 32 itens ainda não publicados.** O curso enche ao longo
   do pós-edital. Se entrar no plano, entra como agenda com data.

6. **Monitoria fica de fora por decisão da plataforma.** O PDF diz que só sai vídeo.
   Única âncora possível seria "assista ao encontro N".

## Nota de matrícula

Não foi preciso desmatricular nada: a conta tinha **2 dos 3 slots** ocupados (PRF
Pacotaço e Curso Regular Área Fiscal). O TCDF-ANACE Pós-Edital ocupou o terceiro e
**continua matriculado**.

**Regra nova (Elvis, 2026-08-20):** o rodízio é livre e não precisa de autorização.
A única checagem antes de trocar é se **alguma sessão em andamento está usando ou
baixando aquele produto**. Se não estiver, pode desmatricular e matricular à vontade.
Registrado no `AGENTS.md` e em [[project_estrategia_matriculas_limite_coruja]].
