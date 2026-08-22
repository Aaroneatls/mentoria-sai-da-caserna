# Impactos entre bases

> **Toda base, ao terminar, escreve aqui o que ela mexeu nas outras.** E toda base, ao comecar,
> le este arquivo para saber se alguma anterior mudou algo que ela ja usava.
>
> As seis bases se conversam. Sem este registro, a base 2 muda uma regra, a base 1 fica
> desatualizada, e ninguem percebe ate o material chegar torto na mao do aluno.

## Como usar

**Ao terminar uma base**, acrescentar uma secao com:

- o que foi construido
- **o que mudou** em relacao ao que estava decidido
- **qual base isso afeta**, e o que precisa ser ajustado la
- o que ficou pendente

**Ao comecar uma base**, ler daqui para baixo e verificar se ha ajuste pendente que a afete.

**Se uma base ja pronta precisar de ajuste**, fazer o ajuste e registrar aqui tambem. Nao deixar
para depois: base desatualizada contamina tudo que vem em cima dela.

---

## Estado das bases

| Base | Estado | Ultima revisao |
|---|---|---|
| 1 · Disciplinas | **construida, aguardando revisao do Elvis** | 22/08/2026 |
| 2 · Estrategia Concursos | nao iniciada | — |
| 3 · Taxonomia do Tec | nao iniciada | — |
| 4 · Materiais de parceiros | nao iniciada | — |
| 5 · Questoes do Tec | nao iniciada | — |
| 6 · Editais | nao iniciada | — |

---

## Registro

### 22/08/2026 · Sessao das skills de download do Estrategia (pre-base 2)

**O que foi construido:** piloto de levantamento do APOIO do Estrategia (resumo e mapa mental) na
disciplina Direito Constitucional do Regular Fiscal (curso 220880). 42 links, **32 arquivos
distintos** (12 resumos, 20 mapas mentais), 28 MB, presentes em 14 das 22 aulas.

**O que mudou em relacao ao que estava decidido:** descobrimos que resumo e mapa mental **nao sao
da aula, sao de cada VIDEO** dentro dela (campos `resumo` / `mapa_mental` em `videos[]`; rota
`/api/video/{videoId}/download/{tipo}`). A suposicao anterior era que estariam dentro do livro.
Desenho completo em `DECISOES.md`, secao "Apoio do Estrategia: resumo e mapa mental".

**Edicao no arquivo central:** esta sessao escreveu a secao "Apoio do Estrategia" no topo do
`bases/DECISOES.md` em 22/08/2026. Registrado aqui porque duas sessoes escrevendo no arquivo
central ao mesmo tempo perdem decisao.

**Qual base isso afeta:**

- **Base 2 (Estrategia)** — o apoio e tabela secundaria dela. A coleta acontece na fase de
  download; a correlacao apoio -> Cod Mestre fica para a fase de granularidade. Destrava o item
  A39, que estava marcado como bloqueante.
- **Base 1 (Disciplinas)** — o download vai criar, dentro de cada pasta de disciplina, uma
  subpasta de apoio. **Nenhuma pasta de disciplina existente sera renomeada, e o acento nao sera
  normalizado** (os nomes do Regular Fiscal continuam sem acento e os do Controle com acento,
  literal como estao). Se algum nome de pasta mudar em execucao futura, o diff contra
  `bases/01-disciplinas/fontes/estrategia.txt` sera registrado aqui.
- **Base 4 (Parceiros)** — a indicacao de resumo do Bezerra tem **prioridade** sobre a do
  Estrategia, e e a unica que pode ser indicada independentemente do curso de origem do bloco.

**Correcao tecnica para quem for implementar:** **hash de arquivo nao serve** nem para deduplicar
nem para detectar mudanca. O PDF do Estrategia e **marcado por download**: o mesmo arquivo baixado
4 vezes deu 4 hashes diferentes, com tamanho variando ~100 bytes. A identidade e o **nome do
arquivo no CDN**; a assinatura de mudanca deve ser **nome no CDN + n de paginas + tamanho
aproximado + data da capa do PDF**.

**Pendente:**

- confirmar o limite de caracteres da Tutory (o texto de indicacao para o aluno depende dele);
- fechar com o Elvis a convencao de pasta e o destino dos arquivos de apoio;
- estender o levantamento as demais disciplinas (~800 MB estimados no pacote inteiro).


---

### 22/08/2026 · Base 1 — Disciplinas (construida, NAO declarada fechada)

**O que foi construido:** `dados/disciplinas.csv` (21), `dados/apelidos.csv` (429),
`dados/areas.csv` (30), `dados/renomear-pastas.csv` (34), `fontes/tec.txt` (146 materias,
1 chamada), `SEM-DONA.md`, `conferir.py` (8 blocos) e a skill `montar-base-disciplinas`.
Vista publicada em 4 abas. **O gatilho de execucao e do Elvis: nada roda antes do ok dele.**

**O que mudou em relacao ao decidido:**

1. **A secao A8 estava errada.** Ela afirma que o Regular Controle tem `CONTAB`, `ESTAT` e
   `ECOFIN`. Conferido nos dois pacotes do Controle (365538 e 224364, listas identicas): so o
   `CONTAB` existe. **Correcao autorizada pelo Elvis em 22/08/2026.**
2. **`areas.csv` deixou de nascer vazio.** A decisao original mandava deixar em branco para nao
   chutar. O Elvis fechou em 22/08 que so vale o que existe **de fato** no Curso Regular, o que
   transforma a lista de matricula dos dois pacotes em evidencia dura. Cada linha carrega a
   evidencia.
3. **Entrou a coluna `camada` (`drive` / `plataforma`)** em `apelidos.csv`, porque as duas tem
   granularidade diferente: 22 pastas para 25 cursos no Regular Fiscal.
4. **O `id_na_fonte` vale para Estrategia e Tec**, nao so para o Tec. Nome literal serve para
   achar; id serve para casar.
5. **`LTRIB` ganhou endereco:** curso 336350 (Legislacao Tributaria sobre o Consumo, a parte da
   Lei Kandir). Decisao do Elvis, 22/08/2026.

**Qual base isso afeta:**

- **Base 2 (Estrategia)** — recebe `renomear-pastas.csv`, com o **nome exato no disco** e o nome
  novo ja conferido contra os 45 caracteres: 31 prontas, **3 pendentes de decisao do Elvis**.
  Recebe tambem o `curso_id` como chave de join para a coluna `Cod Mestre`.
- **Base 3 (Taxonomia do Tec)** — **corrigir o `ROTEIRO.md`**: a pergunta em aberto "puxar as 146
  materias ou so as 21?" partia de premissa errada. As 146 custam **1 chamada**, nao 146; o que
  custa 1 por materia e a arvore de **assuntos**. Materia e apelido e mora na base 1; assunto e
  taxonomia e mora na base 3. O `id_na_fonte` ja esta guardado.
  **Alerta novo:** o Tec junta `AFO` com `CONTPU` (materia 69) e `AUDIT` com `CTREXT` (materia
  37). **Filtrar por materia nao isola disciplina nossa.**
- **Base 4 (Parceiros)** — os 29 apelidos do Bezerra estao mapeados. Ele **nao cobre `CTREXT`,
  `LTRIB` nem `REFTRI`**: registrar como "nao cobre", nao como pendencia. Regra nova do Elvis:
  **toda vez que entrar aula nova, passar o olho no resumo do Bezerra** procurando materia ou
  conteudo sem correspondencia.
- **Base 5 (Questoes do Tec)** — herda o alerta da base 3, e o impacto foi **localizado** com a
  sessao de mapear aulas em 22/08/2026:

  | | Contamina? |
  |---|---|
  | O **corte** da coleta | **nao.** Os filtros ja cortam por assunto; o piloto usou os assuntos 497, 503 e 512 |
  | O **dimensionamento** | **sim.** A decisao A32 e a tarefa B53 dizem "janela de anos **por materia**, mirando ~2.500 questoes" |

  Se a materia 69 e `AFO` + `CONTPU`, entao "2.500 questoes de AFO" medido na materia 69 esta
  **inflado por questoes de outra disciplina nossa**, e a janela de anos sairia **curta demais**,
  jogando fora anos de AFO de verdade.

  **O tamanho tem de ser medido pela soma dos assuntos da disciplina, nunca pela materia.**
- **Base 6 (Editais)** — nao e afetada agora. Entra como **fonte nova** (linha, nao coluna) em
  `apelidos.csv` quando existir.

**Regra nova, registrada a pedido do Elvis (22/08/2026):** pos-edital da area Fiscal que precisar
de materia que so existe no Regular **Controle**, e que ainda nao saiu no curso especifico, manda
o aluno para o material do Controle **e sem ressalva no texto**. So e seguro porque o Cod Mestre e
o mesmo nos dois lados; se a mesma teoria receber codigos diferentes por area, a regra passa a
mandar o aluno para um lugar que a base nao sabe que e equivalente.

**Pendente, e depende do Elvis:**

1. **A pasta `Reforma Tributaria` guarda `LTRIB` (336350) e `REFTRI` (371461, 389109) juntas.**
   Chegou a ser dado como "se resolve sozinho quando reorganizarem as pastas", e **isso foi
   retirado em 22/08/2026**: valia quando o plano era reconstruir do zero, porque baixar por curso
   criaria tres pastas naturalmente. Com o plano em modo `atualizar`, **a pasta existente fica como
   esta**, e separar virou trabalho explicito. Decisao do Elvis, porque mexe na pasta dele.
   Registrado como **B69**.
2. ~~Contradicao entre a A8 e os cursos 220891/220896~~ **resolvida sem precisar do Elvis**: os
   dois cursos sao **genericos** (o 220891 diz "(Todos Estados)"; o 220896 nao nomeia municipio),
   entao **nao sao o `local` de que a A8 fala**, que e `LTRIB-<ente>` e nasce em pos-edital.
   Sobra so a pergunta estreita: sendo genericos, sao **`LTRIB`** tambem? Registrado como **B70**,
   a confirmar pela ementa quando a sessao de download voltar a plataforma.
3. As 8 entradas do balde 1 do `SEM-DONA.md`.
