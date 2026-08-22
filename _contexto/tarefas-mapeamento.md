# Lista viva de tarefas

> Reorganizada em 21/08/2026, depois que o Bloco 1 de decisões fechou e o projeto passou a viver
> em `bases/`. As decisões fechadas estão em **`bases/DECISOES.md`** — leia lá antes de começar
> qualquer base. Aqui fica só o que **falta**.

Última atualização: 21/08/2026.

---

## A — Decisões pendentes

### A.1 — Nenhuma trava o começo

**O Bloco 1 fechou por inteiro.** `A8` `A12` `A14` `A15` `A24` `A25` estão em `bases/DECISOES.md`.

O único item externo é a **conta nova do Tec**, que o Elvis vai criar. Ela trava só a coleta.

### A.2 — Vão apertar durante a execução

| # | Decisão | Quando aperta |
|---|---|---|
| A27 | As 3 melhorias de composição de caderno (ver B38, B39, B40) | ao montar o primeiro caderno |
| A26 | Quais editais entram | ao começar a base 6 |
| A34 | Quais parceiros entram como fonte além do Bezerra | ao montar a base 4 |
| A28 | Migração dos nomes de disciplina na Tutory, e a saída da Reforma de dentro de `DTRIB` | antes do primeiro plano novo |
| A5 | Nomenclatura final das skills | ao empacotar |

### A.3 — Futuro, com gatilho para voltar

| # | Item | Volta quando |
|---|---|---|
| A33 | Abrir a **área Legislativa** | terminar o mapeamento de Fiscal e Controle |
| A18 | Cortes de risco do BIZURITO | o BIZURITO voltar ao caminho crítico |
| A21 | Amostra mínima antes do rótulo de RISCO | idem |
| A22 | Escada do N8 | houver leitura de desempenho do aluno |
| A23 | Forma do caderno de erros: PDF ou link | o primeiro aluno for usar |
| A10 | A Tutory informa se o aluno começou o caderno? | houver acesso de leitura |
| A17 | Caderno personalizado por aluno na Tutory | idem |
| A19 | Ordem do Passo Estratégico | no primeiro pós-edital com Passo |
| A20 | Slide e mapa mental por bloco de vídeo | material complementar entrar no plano |
| A4 | Critérios extras da Curva ABC | a base de pesos estiver cheia |
| A30 | "Técnica de Estudos" é do plano ou do tópico? | na skill da Tutory |
| A35 | **Minutos por página** da teoria: estimar ou calibrar com os dados dos alunos? | ao montar o 1º plano |
| A29 | Hospedagem da página de orientação | a base alimentar a página |

---

## B — Execução, por base

### Base 1 · Disciplinas

| # | Item | Bloqueia? |
|---|---|---|
| B8 | Montar a tabela: 21 disciplinas, sigla, apelidos de cada fonte, contador de código | **é o próximo passo** |
| B46 | Área como **lista**, não coluna, para aceitar a Legislativa depois | junto |

### Base 2 · Estratégia Concursos

| # | Item | Bloqueia? |
|---|---|---|
| **A39** | **Estratégia: download e curso** — discutido em outra sessão, trazer as conclusões | **trava a base 2** |
| B47 | Mapear Direito Administrativo com o alvo de **~10 páginas** | sim, é o piloto |
| B13 | As 4 colunas de hash e o arquivo de âncoras de prosa | sim |
| B48 | Tabela de pares **bloco × tópico** (muitos para muitos) | sim |
| B49 | Coluna `depende de` (pré-requisito), padrão **livre** | sim |
| B7 | Comparação **bloco a bloco** entre pacotes, nunca aula a aula | não |
| B9 | Cruzamento Fiscal × Controle: quais tópicos são compartilhados | não |
| B12 | Reaproveitamento de teoria entre áreas | não |
| B14 | Cadência de revalidação de páginas | não |
| B23 | Materiais complementares do Estratégia (resumos e mapas mentais) — **sessão própria** | não |
| B25 | Os 7 pontos de decisão de `estrategia-padroes-pdf.md` | não |
| ~~B24~~ | ~~Trava de caminho longo~~ **resolvido 22/08**: orçamento por nível em `bases/NOMENCLATURA.md` | — |
| B63 | **Renomear os 146 arquivos que já passam de 240 caracteres** | sim, antes de novo download |
| B64 | **As duas** skills de download (específico e completo) ganham os 3 modos: `baixar`, `atualizar`, `conferir`. **Continuam separadas** — Elvis vetou fundir em 22/08 | mandado à sessão de download |
| B65 | `hash_conteudo`: sha256 do texto **sem a marca d'água**, já que hash de arquivo muda a cada download | sim, sustenta o `atualizar` |
| B66 | `_manifesto.csv` na pasta da disciplina: é o que a base 2 lê; a planilha é a vista do Elvis | sim |
| B67 | Aba **`Apoio`** na planilha, com `Aulas` aceitando mais de um valor | junto do download dos apoios |
| B68 | Gatilho de impacto no fim do `atualizar`: escrever em `IMPACTOS.md` e perguntar se roda a base 2 | não |

### Base 3 · Taxonomia do Tec

| # | Item | Bloqueia? |
|---|---|---|
| B50 | Puxar a árvore por matéria (~1 chamada cada) e ligar ao Cód Mestre | não |
| B22 | Diff dos guias do Tec, perfil de acervo, checkpoint permanente | não |
| B19 | Reorganizar os manuais | não |

### Base 4 · Materiais de parceiros

| # | Item | Bloqueia? |
|---|---|---|
| B51 | Mapear os resumos do Bezerra, guardando **a matéria de origem dele** | não |
| B52 | Estrutura de fonte que aceite parceiro novo sem mexer na base | não |

### Base 5 · Questões do Tec

| # | Item | Bloqueia? |
|---|---|---|
| B42 | **Gabarito junto de cada questão** na impressão (`JUNTO_QUESTAO`) | **sim** |
| B45 | Apagar os `ZZ-COLETA` e limpar `coletor_src` do navegador | sim, higiene |
| B27 | Apagar o caderno `101395596` (banca ESAF) pela lixeira | sim, higiene |
| B53 | Definir a janela de anos **por matéria**, mirando ~2.500 questões e teto de 10 anos | antes de cada coleta |
| B55 | Filtro **Área (Carreira)**: Controladorias + Tribunais de Contas, sem Gestão Governamental | **antes da 1ª coleta** |
| B62 | Filtro de **escolaridade**: só nível superior | **antes da 1ª coleta** |
| B60 | Aba de **concursos**, montada a partir do cabeçalho impresso, com a marca de área especializada | junto da coleta |
| B61 | Busca externa sobre os concursos duvidosos, para o Elvis marcar | junto |
| ~~B58~~ | ~~Corte por órgão~~ **resolvido**: o filtro de Área tem subníveis | — |
| B59 | Repuxar a lista completa de filtros do Tec: pode haver um de área especializada | 1 chamada |
| ~~B56~~ | ~~Coletar `tempoMedio`~~ **descartado**: custa 1 requisição por questão | — |
| B44 | Caderno-base com fatias por `questaoInicial`, em vez de um temporário por lote | não |
| B43 | Testar criar caderno vazio: cairia de 5 para 3 requisições | não |
| B5 | Camada de **ponto**: ler o enunciado e ligar ao tópico | sim, sustenta os cadernos |
| B38 | Tamanho de caderno proporcional ao nº de pontos, não fixo em 15 | depende de A27 |
| B39 | Ordem didática dentro do caderno | depende de A27 |
| B40 | Cobertura manda em N1-N2, peso real manda em N3-N5 | depende de A27 |
| B32 | Cadernos **separados** para questão inédita, que exige plano avançado do aluno | não |
| B37 | Biblioteca de cadernos por ponto, criados sob demanda e reaproveitados | não |
| B33 | Seguir alimentando o histórico do limite do Tec | não |
| B35 | Na skill final, trocar o censo pelo **percentual real** questão a questão | não |
| B21 | Pasta parametrizada e ponto de retomada nas skills | não |

### Base 6 · Editais

| # | Item | Bloqueia? |
|---|---|---|
| B17 | Levantamento de editais e vínculo item → Cód Mestre | não |
| B54 | Alerta de nomenclatura quando o edital chamar diferente da gente | não |

### Futuro

| # | Item |
|---|---|
| B28 | BIZURITO passada 2: comentário dos pontos que viram folha |
| B29 | Teste controlado: 2 tópicos com passada completa |
| B26 | Seção 7 do BIZURITO: granularidade, onde os Docs ficam, Bizu do Bizu |
| B30 | Implementar o N8 |
| B31 | Dossiê por aluno |
| B36 | Leitor do caderno de erros do aluno, **inclusive questão fora do nosso banco** |
| B57 | **Revisão de 15 minutos** na grade do plano: como entra, o que revisa, com que cadência |
| B16 | Peso com piso de confiança |

---

## C — Skills a criar

Uma por base, com três modos: **`criar`**, **`atualizar`** e **`conferir`**.

`montar-base-disciplinas` · `mapear-blocos-estrategia` · `mapear-taxonomia-tec` ·
`mapear-materiais-parceiros` · `coletar-questoes-tec` · `mapear-editais` ·
`fichar-questoes` · `gerar-cadernos` · `publicar-plano-tutory`

E atualizar as 2 skills de download do Estratégia.

---

## D — Como a gente trabalha

**Reconhecimento antes de construir.** Ao entrar material novo, primeiro uma passada barata que
só **caracteriza**: tamanhos de fonte, vocabulário das faixas, taxa de rasterização, onde a
teoria começa e acaba. O maior custo de 20/08 não foi decisão errada, foi retrabalho.

**Aproveitar o aprendizado, não recomeçar do zero.** O que se refaz é o **dado**, não o método.
Código validado, regras e transcrições feitas à mão continuam valendo.

**O que só existe na memória do Claude não existe.** A fonte de verdade é o repositório, porque é
o que qualquer assistente lê. Ver `AGENTS.md`.

**Toda base reporta o impacto nas outras.** Ao terminar, escrever em `bases/IMPACTOS.md` o que
mudou e qual base isso afeta; ao começar, ler de lá. Se uma base já pronta precisar de ajuste,
ajustar na hora. Base desatualizada contamina tudo que vem em cima dela.

**Quando não entender, perguntar.** O Elvis escreve por ditado; frase truncada é erro de
transcrição, não de raciocínio.

---

## E — Estado em 21/08/2026

| | |
|---|---|
| Decisões do Bloco 1 | **todas fechadas** |
| Estrutura | 6 bases em `bases/`, cada uma com README, aprendizado e skill |
| Memória | 91 arquivos copiados para `_contexto/memoria/`, versionados |
| Base antiga | arquivada em `_arquivo/2026-08-21-aprendizado/`, serve de conferência |
| Próximo passo | **base 1**, e depois o piloto da base 2 em Direito Administrativo |

O que a sessão de aprendizado produziu, e que fica de conferência: 1.224 questões colhidas,
5.423 classificadas por dificuldade e banca, 199 fichadas em 38 pontos, 8 cadernos publicados.
