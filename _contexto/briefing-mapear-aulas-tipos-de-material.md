# Handoff completo para a sessão "Mapear Aulas"

> Fechamento da sessão "Tipos de material do Estratégia" — 2026-08-20.
> Fonte detalhada: `_contexto/estrategia-tipos-de-material.md`.
>
> **Este documento é autossuficiente.** A sessão de origem foi encerrada; tudo o que
> importa dela está aqui. Leia inteiro antes de retomar o mapeamento — há decisões que
> mudam o desenho, aprendizados técnicos que evitam retrabalho, e pendências herdadas.
>
> **Companheiro obrigatório:** `_contexto/skills-estrategia-mudancas-2026-08-20.md` —
> prévia completa do que mudou nas duas skills de download e no `AGENTS.md`. Como essas
> mudanças **não estão commitadas**, esse arquivo é o registro independente delas.

---

# PARTE 1 — Decisões do Elvis (não são sugestões)

| # | Decisão | Consequência para o mapeamento |
|---|---|---|
| 1 | **O aluno faz só o Curso Regular** | Nenhum outro material entra no plano por padrão |
| 2 | **O arquivo de referência é o PDF simplificado** | Se o desenho assumia o original como âncora, tem que ser revisto — as paginações são diferentes |
| 3 | **Passo Estratégico fica fora do escopo** | É teoria de verdade, mas só entra em matéria de peso baixo, e raro. **Não construir nada em cima dele agora** |
| 4 | **Estatística do Estratégia está proibida como referência** | Nem para compor peso, nem para conferir. Se alguma conclusão usa esses percentuais, tem que sair |
| 5 | **Índice do Bizu não é insumo** | As referências saem do nosso levantamento, com mais granularidade |
| 6 | **Rodízio de matrícula é livre** | Não precisa pedir autorização; só checar se alguma sessão está usando o produto |

**Gatilho definido para o Passo Estratégico:** a avaliação de como (e se) ele entra fica
para **o primeiro pós-edital que a gente montar e que tenha Passo Estratégico**. Não
antecipar.

---

# PARTE 2 — O que mudou no acervo (já executado)

## 2.1 Todos os PDFs ganharam sufixo `LS` / `LC`

```
Aula 03 - Fundações, empresas públicas e sociedades de economia mista LS (30-07-2026).pdf
Aula 18 - Improbidade administrativa - Lei 8.429-1992 LC (30-07-2026).pdf
```

| Sufixo | Significa |
|---|---|
| `LS` | **Livro Simplificado** |
| `LC` | **Livro Completo** (a versão original) |

O sufixo entra **entre o assunto e a data**. O resto do nome não mudou, então casar por
`Aula NN` continua funcionando. Só o **Curso Regular** leva sufixo — Passo, Bizu, Trilha,
Monitoria e Rodadas têm card único, sem distinção de versão.

**Estado das 4 pastas em `G:\Meu Drive\Inteligência Artificial\Estrategia`:**

| Pasta | PDFs | LS | LC | Validação |
|---|---|---|---|---|
| `Pacotaço TCDF (ANACE) 2026` | 177 | 126 | 51 | 35 amostras, 1 erro corrigido |
| `ISS Manaus (AFTM) 2026` | 227 | 162 | 65 | 68 amostras, 0 erros |
| `Regular Controle` | 211 | 159 | 52 | 100% nas 2 disciplinas de risco + amostra, 19 erros |
| `Regular Fiscal` | 481 | 290 | 191 | 44 amostras, 0 erros |

**1096 PDFs, zero sem sufixo. 201 aulas conferidas, 20 erros corrigidos.** Nenhuma
pendência de validação.

Logs reversíveis (8 CSVs) em
`G:\Meu Drive\Inteligência Artificial\Estrategia\_logs-renomeacao-LS-LC (20-08-2026)\`.
Dá para desfazer tudo a partir deles.

## 2.2 Por que o sufixo era necessário

O simplificado **não existe em toda aula**. No pacote TCDF: 126 de 180 aulas (70%) têm;
54 (30%) só têm o completo. Quatro disciplinas não têm **nenhum** simplificado (Língua
Portuguesa, Lei Orgânica do DF, Lei Orgânica do TCDF, Regime Jurídico dos Servidores);
Direito Administrativo tem 14 de 21.

Como a skill de download cai pro original quando não há simplificado, a pasta ficava
mista e uma âncora de página podia apontar pro arquivo errado sem ninguém perceber.

## 2.3 As planilhas de metadados também mudaram

As skills de download passam a gravar:

| Onde | Campo | Serve pra |
|---|---|---|
| Aba "Aulas" | **`Versão do Livro`** (`LS`/`LC`/`—`) | saber a paginação por aula; disciplina 100% `LC` avisa que não tem simplificado |
| Subtítulo | **`Tipo de Material`** | `Curso Regular`, `Passo Estratégico`, `Bizu`, `Trilha`, `Monitoria`, `Rodadas`, `Discursiva` |
| Subtítulo | **`Nome do Pacote`** + **`Pacote ID`** + link | voltar direto ao produto no catálogo, e detectar pacote que saiu do ar |

**Impacto:** se o Mapear Aulas *lê* essas planilhas, ganhou colunas. Se *escreve*, precisa
preservar os campos novos.

---

# PARTE 3 — Aprendizados técnicos (economizam retrabalho)

## 3.1 O endpoint de curso mente por omissão

```
GET /api/aluno/curso/{id}    → resumo, OMITE campos
GET /api/aluno/aula/{id}     → completo
```

| Campo | Endpoint de curso | Endpoint de aula |
|---|---|---|
| `pdf`, `pdf_simplificado` | confiável | confiável |
| `pdf_grifado` | **quase sempre nulo** | presente |
| `videos` (+ `slide`, `mapa_mental`, `resumo`, `audio`) | **quase sempre vazio** | completo |

Medido na Aula 03 de Direito Administrativo do TCDF (`3951051`): pelo curso, zero vídeos
e sem grifado; pela aula, **8 vídeos, 2 slides, 1 mapa mental e o grifado presente**.

**Regra: nunca concluir ausência de material pelo endpoint de curso.** Isso invalidou uma
conclusão intermediária da própria investigação.

## 3.2 Conferir versão sem baixar o PDF — técnica do `Range`

O endpoint aceita requisição parcial:

```python
UA = {'User-Agent': '<UA de browser>', 'Referer': 'https://www.estrategiaconcursos.com.br/',
      'Range': 'bytes=0-99'}
r = requests.get(url_assinada, headers=UA, timeout=60)
tamanho_remoto = int(r.headers['Content-Range'].split('/')[-1])   # status 206
```

**100 bytes trazem o tamanho exato do arquivo remoto.** Comparando com
`os.path.getsize()` do local:

| Diferença | Significa |
|---|---|
| 4 a 30 bytes | é o mesmo arquivo (variação da marca d'água gerada na hora) |
| megabytes | é outra versão |

Limiar usado: `dif < max(2000, tamanho_local * 0.002)`.

**Duas armadilhas:** `HEAD` devolve 404 (só `GET` com `Range`), e **não funciona pelo
`javascript_tool`** — `Content-Range` não é header seguro de CORS e volta `null` no
navegador. Tem que ser do shell, com o link assinado.

## 3.3 O "simplificado" pode ser um stub de 3 páginas

Em algumas aulas o `pdf_simplificado` existe na API mas entrega um aviso de 3 páginas
("esta aula não possui PDF simplificado"), e a skill rebaixa pro original. **O arquivo é
`LC` mesmo com `pdf_simplificado` presente.**

O stub tem sempre **~699 KB**. Foram 19 casos, todos em Contabilidade Geral Avançada (14)
e Contabilidade Pública (5) do Regular Controle. **Quem confia só na API erra essas.**

## 3.4 ARMADILHA: assunto que termina em "LC" ou "LS"

Custou um rótulo errado silencioso:

```
Aula 12 - Previdência complementar - LC 108-2001 e LC (22-07-2026).pdf
```

O arquivo **não tinha sufixo**, mas o teste de "já renomeado" casou com o "LC" do assunto
(Lei Complementar), pulou o arquivo, e depois ele foi lido como `LC` quando era `LS`.

**Nunca deduzir a versão lendo o fim do nome do arquivo.** A fonte é a API ou a coluna
`Versão do Livro` da planilha. O nome é rótulo para humano, não campo de dado. Para saber
se um lote já rodou, conferir contagem de arquivos contra linhas do log — divergência de
1 já é sinal.

## 3.5 Busca no catálogo: duas armadilhas

1. **A aba não troca com clique por coordenada.** Continua listando PACOTES e a busca
   volta zero, o que parece resultado legítimo. Trocar com `element.click()` no `<button>`
   e conferir a classe `Tab isActive`.
2. **A busca é fuzzy (OR).** "Bizu Receita Federal" devolve 3772 itens casando só
   "Receita". Contagem alta não significa acerto.

**Material granular (Bizu, Passo, Monitoria, Trilha, Discursiva) não aparece na aba
PACOTES** — só na aba **CURSOS**, como produto avulso matriculável.

Dentro de um pacote matriculado, `GET /api/aluno/pacote/{id}` traz `tipo_curso_id`:
`1`=Curso Regular, `3`=Monitoria, `5`=Trilha, `7`=Passo Estratégico, `27`=Bizu,
`30`=Rodadas de Simulados.

## 3.6 O apelido da pasta não é o nome do produto

| Pasta no Drive | Produto no catálogo | Pacote ID |
|---|---|---|
| `Regular Controle` | **Concursos de Tribunais de Contas (Nível Superior) Pacote Completo Cursos Regulares** | `224364` |
| `Regular Fiscal` | Curso Regular para Área Fiscal - Pacote Completo | `220865` |
| `Pacotaço TCDF (ANACE) 2026` | TCDF (Analista Adm. de Controle Externo - Serviços Técnicos Administrativos - ANACE) Pacotaço … 2026 (Pós-Edital) + Sistema de Questões | `393930` |
| `ISS Manaus (AFTM) 2026` | Prefeitura de Manaus-AM - ISS Manaus (Auditor Fiscal de Tributos Municipais - AFTM - Nível I) Pacotaço … 2026 (Pós-Edital) + Sistema de Questões | `396635` |

**Cuidado com variantes homônimas:** existe um `TCDF (Analista Administrativo de Controle
Externo) Pacotaço` que é `366996` — a variante **Cebraspe pré-edital**, com 19 cursos e
aulas diferentes. Não é o mesmo produto do `393930`. Validar com o pacote errado produz
rótulos errados.

## 3.7 Caminho longo do Windows (260 caracteres)

O sufixo de 3 caracteres estourou o limite em Contabilidade Geral Avançada do Regular
Fiscal, e o `os.rename` falhou no meio do lote. Resolvido com caminho estendido
(prefixo `\\?\` no caminho absoluto), mais loop retomável e log com `flush()`, para não
perder o que já foi feito.

**Essas pastas estão no limite** — qualquer nome mais longo no futuro vai esbarrar de novo.

## 3.8 Detector tipográfico: armadilha nova (capitular)

No Passo Estratégico e no Bizu, o template usa letra capitular e o `pymupdf` devolve o
título **sem a primeira letra**:

```
"TOS" + "DMINISTRATIVOS"   →  ATOS ADMINISTRATIVOS
"POSTA" + "STRATÉGICA"     →  APOSTA ESTRATÉGICA
```

Quem recompõe é o texto da faixa roxa (`page.get_text(clip=rect)`). É diferente do
versalete já conhecido, onde a letra sobrava solta em vez de sumir.

---

# PARTE 4 — Conclusões sobre os tipos de material

O método do detector tipográfico foi testado em **17 disciplinas** de um pacote novo
(TCDF-ANACE), não só em Direito Administrativo. Segurou em todas.

**Nenhum dos 48 PDFs examinados tem sumário embutido** (`get_toc()` vazio em 48/48), em
nenhum tipo de material. O detector tipográfico não é a melhor opção: é a única.

| Tipo | Entra no mapeamento? | Âncora |
|---|---|---|
| **Aula em PDF (Curso Regular)** | **Sim — é o material do aluno** | `De "<título>" (p13) até antes de "<título>" (p20)`, no **simplificado** |
| **Passo Estratégico** | Exceção, fora do padrão | mesma frase de tópico, dentro do `ROTEIRO DE REVISÃO` |
| **Discursiva** ("as Cursivas") | Sim, com ressalva | nome do tópico + página; template diferente |
| **Caderno de Jurisprudência** | Sim, como revisão | nome do assunto |
| **Bizu Estratégico** | Baixa prioridade | número do bizu |
| **Trilha Estratégica** | De outra forma | número da tarefa |
| **Videoaula** | De outra forma | **título do vídeo** (não minutagem) |
| **Slide / Mapa mental** | De outra forma | número do slide / nome do assunto |
| **Simulados, Rodadas, Questionários** | Não / de outra forma | número da questão |
| **Monitoria** | **Não** | só sai em vídeo, sem PDF |
| **Análise Estatística (PE e Bizu)** | **Não** | proibida como referência (decisão 4) |

**"Cursivas" era o curso de Discursiva** — não era tipo novo. **"Curso Estratégico" não
existe** como produto.

**Bizu perde feio para o Bezerra.** Mesma disciplina (Direito Administrativo): Bizu = 1
PDF de 46 páginas com 80 imagens por página e quase nenhum texto extraível; Bezerra = 18
PDFs, 468 páginas, 1 imagem por página, sumário em todo arquivo, um arquivo por tópico.

---

# PARTE 5 — Pendências herdadas

## 5.1 Precisa de decisão do Elvis

1. **Passo Estratégico como teoria: falta definir a ordem.** Ele condensa a mesma matéria
   da aula. O aluno faz aula **e** PE do mesmo assunto? Ou o PE substitui a aula em
   disciplina de peso baixo? (Gatilho: 1º pós-edital com Passo.)
2. **Slide e mapa mental só existem no primeiro vídeo de cada bloco.** Na Aula 03 de
   Direito Administrativo, 8 vídeos, só 2 têm slide e 1 tem mapa mental. Ou indexamos por
   **bloco de vídeos** (não por aula), ou o índice fica cheio de buraco. Isso fecha o
   diagnóstico de `project_resumos_mapas_mentais_indexacao`, mas a decisão de formato é
   dele.
3. **Trava de caminho longo (3.7) nas skills de download** — proposta e **não aplicada**,
   estava esperando o ok do Elvis. O que seria implementado está descrito em
   `_contexto/skills-estrategia-mudancas-2026-08-20.md`, seção "Não aplicado".
4. **Git — risco real de perda.** `AGENTS.md` e as duas skills de download estão
   modificados e **não commitados** (+156 e +159 linhas nas skills, +9 no `AGENTS.md`).
   Nada foi para o GitHub nesta sessão. A prévia em
   `_contexto/skills-estrategia-mudancas-2026-08-20.md` permite reconstruir tudo se as
   skills se perderem, mas **rodar `/syncar` continua sendo o certo a fazer**.

## 5.2 Técnicas, sem bloquear

5. **PDF grifado é uma terceira paginação, não examinada.** Existe inclusive em
   disciplinas sem simplificado (Língua Portuguesa, Regime Jurídico). Pode ser a saída
   para essas quatro — ou só mais confusão.
6. **Resumo por vídeo é raro demais** (1 em 38 vídeos checados). Não dá para montar índice
   em cima disso.
7. **Rodadas Avançadas: 25 de 32 itens ainda não publicados.** O curso enche ao longo do
   pós-edital. Se entrar no plano, entra como agenda com data.

---

# PARTE 6 — O que verificar ao retomar

- O desenho do mapeamento estava assumindo o **PDF original** como âncora? (Decisão 2)
- Havia algo apoiado nos **percentuais do Estratégia**? (Decisão 4)
- Existe código, planilha ou caminho que dependa do **nome do arquivo**? Ele mudou.
- Existe código que **deduza a versão pelo nome**? Não pode — ver 3.4.

---

# PARTE 7 — O que mudou nas skills de download

Resumo; o detalhe está em `_contexto/skills-estrategia-mudancas-2026-08-20.md`.

| # | Mudança | Onde |
|---|---|---|
| 1 | Sufixo `LS`/`LC` no nome do arquivo (só Curso Regular) | as duas skills |
| 2 | Modo atualização reconhece o formato antigo e **renomeia em vez de duplicar** | as duas skills |
| 3 | Planilha ganhou `Versão do Livro`, `Tipo de Material`, `Nome do Pacote`, `Pacote ID` e link | as duas skills |
| 4 | Nova seção: conferir versão sem baixar (técnica do `Range`) | as duas skills |
| 5 | Nova seção: ARMADILHA do assunto terminado em "LC"/"LS" | as duas skills |
| 6 | Armadilhas da busca no catálogo (aba não troca, busca é OR, granular só em CURSOS) | skill completa + `AGENTS.md` |
| 7 | Rodízio de matrícula livre, sem pedir autorização | `AGENTS.md` |
| — | **Trava de caminho longo do Windows** | **proposta, NÃO aplicada** |

**Se for baixar ou atualizar qualquer curso do Estratégia a partir daqui**, as skills já
gravam o sufixo e os campos novos de planilha na origem — não precisa refazer nada à mão.

---

## Memórias relacionadas

`project_material_padrao_simplificado_e_passo` · `project_base_propria_de_pesos_substitui_tec` ·
`reference_estrategia_busca_catalogo_abas` · `reference_estrategia_pastas_x_pacotes` ·
`project_estrategia_matriculas_limite_coruja` · `project_detector_tipografico_titulos_estrategia` ·
`project_resumos_mapas_mentais_indexacao`
