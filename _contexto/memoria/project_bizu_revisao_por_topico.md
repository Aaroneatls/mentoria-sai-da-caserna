---
name: project-bizu-revisao-por-topico
description: "BIZURITO: PDF de revisão por chave de taxonomia, dividido em núcleo + blocos por banca, gerado do banco de fichamento e entregue por link fixo do Google Docs que exporta PDF — desenhado e testado em 2026-08-20"
metadata:
  node_type: memory
  type: project
---

Terceiro material entregue ao aluno, ao lado do caderno do Tec e do resumo do Bezerra.
Ideia do Elvis em 2026-08-20.

## O que é

Um por **chave de taxonomia** (Cód Mestre, ex. `DADM-014`). Sintetiza **o que a banca cobra
naquele tópico**, não o que a aula ensina. É derivado do banco de fichamento
(ver [[project_banco_fichamento_questoes]]), não escrito do zero.

**1 linha de bizu = 1 ponto fichado** (`DADM-014.P03`), ordenadas por nº de questões.
Ponto sem questão não vira bizu. Cada linha tem no máximo 2 linhas de texto.

## Anatomia (validada no modelo DADM-014, Poder de Polícia)

1. **Cabeçalho** — Cód Mestre + nome mestre.
2. **Faixa de origem** — Estratégia (aula + páginas reais + recorte de tópico), Bezerra (RNN +
   páginas), código e link do caderno.
3. **BIZU FORTE** — o ponto com mais questões fichadas. É a mesma medição da "questão ouro" dos
   Níveis 6 e 7, vista do outro lado: filtro de redundância e seleção de ouro são a mesma coisa.
4. **O QUE A BANCA COBRA** — lista dos pontos, cada um com etiqueta `Pnn · Nq`. A contagem
   visível é o que diferencia isso de um resumo: diz ao aluno onde gastar o tempo.
5. **PEGADINHA** — as trocas de palavra que derrubam (poderá x deverá, taxativo x
   exemplificativo, prazo/competência trocados). É o que o resumo do Bezerra não dá, porque ele
   resume a matéria e não a prova.
6. **LETRA DA LEI** — excerto com os trechos-chave em negrito.
7. **Rodapé** — versão, data e tamanho da base fichada.

## Tamanho: livre (Elvis, 2026-08-20)

Sem teto de linhas nem de páginas. A régua é **um bizu por ponto fichado**: assunto denso gera
bizu longo e está certo. O que não pode é o bizu virar resumo, senão compete com o Bezerra em
vez de complementar.

## Direito autoral (posição fechada por Elvis, 2026-08-20)

- **Lei, decreto, súmula, ementa:** verbatim à vontade (art. 8º, IV da Lei 9.610, não é obra
  protegida). Quando dá pra usar o texto legal pra deixar mais organizado, **é melhor ainda**.
- **Explicação do professor (Estratégia, Bezerra, resolução no Tec):** pode servir de base.
  **Reescrever sempre**, sem copiar a estrutura/sequência didática. Paráfrase não é citação,
  então **não precisa referenciar o professor** — decisão do Elvis. Crédito só seria devido em
  transcrição literal, e a regra é justamente não transcrever.
- A linha que não se cruza: reproduzir parágrafo inteiro ou a sequência didática, porque aí o
  bizu **substitui** o material em vez de complementar.

## Entrega: Google Docs com link de export em PDF (TESTADO em 2026-08-20)

Elvis não quis PDF solto, porque PDF baixado envelhece na mão do aluno. Solução testada e
funcionando ponta a ponta:

1. Gerar o bizu em **HTML** e subir pro Drive convertendo pra Google Doc
   (`files().create` com `mimeType: application/vnd.google-apps.document` + media HTML).
   Tabelas, cores de fundo, negrito e tamanhos sobrevivem à conversão.
2. Atualizar com `files().update(fileId=..., media_body=HTML)` — **o ID não muda**, logo o
   link não muda. Mesma lógica do link imutável do caderno
   (ver [[project_arquitetura_bases_e_link_imutavel]]).
3. Permissão `role=reader, type=anyone` (link não listado).
4. O link que vai pra Tutory é `https://docs.google.com/document/d/<ID>/export?format=pdf`.

**Medido sem nenhuma credencial (simulando o aluno):** HTTP 200, `Content-Type: application/pdf`,
`Content-Disposition: attachment`, bytes começando em `%PDF-`. Editar o Doc reflete no mesmo
link na hora (teste v1 → v2 confirmado).

**Detalhe importante:** o nome do arquivo que o aluno baixa é o **nome do Google Doc**. O padrão
de nomeação do Doc é o que aparece na pasta de downloads dele.

**Credenciais:** o token em `credenciais/google-oauth-token.json` já tem escopo `drive` completo,
não precisa re-autorizar. A **Google Docs API foi habilitada** por Elvis em 2026-08-20 no projeto
Cloud id 574156806233 (leva alguns minutos pra propagar depois de habilitar).

## Nome do material: BIZURITO (fechado por Elvis, 2026-08-20)

Nome próprio, evita colisão com o **"Bizu Estratégico"**, que é produto do Estratégia Concursos.

## Divisão por banca dentro da folha (Elvis, 2026-08-20)

A folha tem um bloco **NÚCLEO** (o que cai em qualquer banca) e, abaixo, **um bloco por banca**.
Isso resolve os dois momentos com a mesma base:

- **Pré-edital / Curso Regular** (banca ainda indefinida): sai a folha inteira. O aluno vê o que
  é comum a todas e o que cada uma puxa mais.
- **Pós-edital** (banca conhecida): sai só o **núcleo + o bloco daquela banca**.

Bancas de referência do projeto: **Cebraspe, FGV e FCC**.

### Identidade de cor por banca (fechada)

| Bloco | Cor | Hex |
|---|---|---|
| Núcleo | grafite | `#23303B` |
| Cebraspe | laranja | `#DA6A10` |
| FGV | azul | `#103C7C` |
| FCC | vermelho | `#B32219` |
| Cabeçalho da marca | azul Caserna | `#0F2C4C` |
| Realce do bizu forte | creme | `#FFF3D1` |

O bloco Núcleo é grafite **de propósito**: o azul ficou reservado pra FGV, senão os dois brigam.

**Logo das bancas: decidido NÃO usar.** São marcas registradas de terceiros dentro de material
distribuído a aluno. Cor + nome em caixa alta já dão o reconhecimento imediato.

## Enxugamento do layout (Elvis achou quadros demais, 2026-08-20)

Os quadros separados de "Bizu Forte", "Pegadinha" e "Letra da Lei" foram **dissolvidos dentro
das linhas**: o bizu forte é a linha com fundo creme e estrela, a pegadinha entra na frase do
próprio ponto, e o excerto legal vai em negrito no meio do texto. Lista corrida, não mosaico.

## Caixa de anotação (Elvis, 2026-08-20)

Abaixo de **cada** bloco (núcleo e cada banca), caixa de borda tracejada com folga pra 2 ou 3
linhas de caneta. Elvis orienta os alunos a comentarem o PDF, então o espaço é parte do produto.

## Logo da Sai da Caserna

Versão branca (`marca/Logo Branco.png`) na faixa azul do cabeçalho, composta sobre o azul e
embutida como **data URI base64** no HTML (testado: sobrevive à conversão e aparece no PDF).
Marca d'água atrás do texto foi descartada: briga com a leitura e o Docs não expõe watermark
por API.

## Nota de rodapé (redação final aprovada por Elvis, 2026-08-20)

> Material de apoio elaborado com uso de inteligência artificial, a partir de uma base própria de
> questões de concurso fichadas uma a uma e de uma base robusta de materiais de estudo. A síntese
> pode conter imprecisões: havendo divergência, prevalecem a lei e a jurisprudência. Uso exclusivo
> dos alunos da Mentoria Sai da Caserna.

**Regras de redação do rodapé, ditadas por Elvis:** declarar o uso de IA e a possibilidade de
imprecisão, afirmar a robustez da base, e dizer que o uso é exclusivo dos alunos. **Não** falar
em "distribuição gratuita" nem "sem finalidade comercial", e **não** usar a palavra "curso" (usar
"base robusta de materiais de estudo").

## Camada obrigatória de revisão de português (Elvis, 2026-08-20)

Nasceu de um erro real: passou "impreciçõe s" no rodapé porque a revisão foi feita no **HTML** e
não no PDF renderizado. Entidade de acento mal escrita só aparece depois de renderizar.

**A revisão é sempre sobre o texto extraído do PDF final, nunca sobre o HTML.** Duas camadas:

1. **Checagem automática** (barata, roda sempre): acento/entidade quebrada e caracteres estranhos;
   travessão (proibido pela casa); soma das questões dos blocos batendo com o total do cabeçalho;
   nome de banca padronizado (Cebraspe, não CESPE); citação de lei no formato padrão; linha
   duplicada; texto estourando a célula ou cortado.
2. **Leitura final** do texto extraído, procurando ortografia, concordância, frase truncada e
   construção que soe "de IA".

Nada é publicado sem passar pelas duas. O aluno não pode receber português ruim.

## Configuração de página (Google Docs API)

Elvis habilitou a **Google Docs API** no projeto Cloud em 2026-08-20. Com ela, `updateDocumentStyle`
define **A4 (595.3 x 841.9 pt)** e margens mínimas (topo 20pt, base 16pt, laterais 22pt, header e
footer 0). **Sem ela o importador força papel Letter e margem de 1 polegada**, e ignora `@page` do
HTML (testado nas duas formas, inclusive o padrão `@page WordSection1` do Word: ignorado).

## Dependência e sequência

O bizu **depende do fichamento** — antes dele, qualquer bizu é chute sobre o que a banca cobra.
Mas o desenho tem que entrar **antes** da passada de fichamento, porque a aba `Pontos` ganha três
colunas novas: `Bizu` (a frase), `Bizu Forte` (calculado pela contagem) e `Letra da Lei`.
Preenchidas lendo a resolução do professor em `/api/questoes/{id}/comentario`, que já vai ser
puxada. Adiar = reabrir as ~1.100 questões de novo.

Ganho de graça: a mesma cascata incremental que sinaliza caderno afetado por questão
desatualizada sinaliza o **bizu afetado**.

## O BIZURITO sai 100% do banco de questões (Elvis, 2026-08-20) — REGRA DURA

Elvis **removeu a linha "NOVO"** (ponto sem questão, incluído por tendência de lei/jurisprudência).
Razão dele: sem questão sustentando, **a gente pode errar e confundir o aluno**. O ganho de
antecipar não paga o risco de ensinar errado.

Consequências:
1. **Toda linha do BIZURITO nasce de questão fichada.** Nada de proposição vinda só de doutrina,
   de comentário de professor ou de leitura minha de tendência.
2. **Só questão atualizada.** O filtro do mapeamento já remove anuladas e desatualizadas; o
   BIZURITO herda esse filtro. E quando o Tec marcar como desatualizada uma questão já fichada, o
   ponto entra em revisão e a folha que o usa é sinalizada.
3. **Ponto sem questão não some do sistema, some da folha.** Ele continua registrado como gap na
   taxonomia central, pro Elvis decidir se vira aula (ver [[project_taxonomia_central_nome_mestre]]).
   É informação de gestão, não material de aluno.

Isso reverte o "remédio pro viés de retrovisor" que estava desenhado em
[[project_bizurito_fontes_e_validacao]]: a lacuna de novidade **continua existindo e é conhecida**,
mas a decisão do Elvis é conviver com ela em vez de preencher com aposta.

## Estado em 2026-08-20: layout FECHADO, gerador PRONTO

Codigo em `bizurito/` e handoff completo em `_contexto/briefing-bizurito.md` (ler esse arquivo
antes de mexer em qualquer coisa do BIZURITO). O que falta e so a origem real do conteudo.

Decisoes finais da sessao, alem das ja registradas acima:
- Coluna **QUESTOES** (era "CAI") e coluna **RISCO** com rotulos **MAIORIA ACERTA / MUITOS
  ESCORREGAM / ESSA DERRUBA**. Percentual nunca aparece.
- Blocos chamam-se **OURO GERAL** (cai nas principais bancas, sem total proprio) e
  **OURO DA <BANCA>** (N questoes da banca neste topico).
- Faixa **"ANTES DE LER, TENTE RESPONDER"** no topo, com uma pergunta por ponto.
- Rodape traz **data de verificacao** das fontes e aviso de que norma pode mudar.
- **Um link so**: a paleta foi escalonada por luminancia para sobreviver a impressao em preto e
  branco (242 / 222 / 186). `modo_impressao.py` fica de reserva.
- **Trava dura de numeros** aborta a publicacao se algum somatorio nao fechar.
- So entra ponto com **mais de uma questao**.

## Em aberto

- **Ordem no fluxo do aluno.** Proposta do Claude: teoria → caderno → resumo Bezerra → BIZURITO,
  porque ele é feedback do que caiu e rende mais com a memória fresca do erro.
- **Formato alternativo de esquema.** Elvis avisou em 2026-08-20 que vai propor outro desenho de
  esquema visual pra comparar com este e escolher o melhor.

**Why:** é o único dos três materiais que fala do *padrão de cobrança*, e não do conteúdo.
Sem ele, o aluno tem teoria e questão, mas não tem a leitura de prova.

**How to apply:** entra como skill própria de renderização (`gerar-bizu`), separada da skill de
fichamento — gerar PDF é outra tecnologia, e assim dá pra regerar tudo depois de qualquer
atualização sem tocar no fichamento. Ver o checklist mestre em
[[project_skill_mapeamento_aulas_pendencias]].
