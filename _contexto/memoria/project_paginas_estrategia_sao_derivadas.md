---
name: project-paginas-estrategia-sao-derivadas
description: "Página do PDF do Estratégia é atributo DERIVADO, não identidade: professores repaginam e quebram aulas. Verificado em 19-08-2026: âncora de PROSA (não de título) + hash_teoria (não o hash do arquivo); a plataforma não expõe data de atualização; cadência mensal nos Regulares custa rebaixar tudo"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T21:06:18.983Z
---

Levantado por Elvis em 2026-08-19. Corrige um erro de desenho: a página vinha sendo tratada
como se fosse referência estável.

## O problema

Os professores do Estratégia **atualizam os PDFs**: repaginam, inserem conteúdo, quebram uma
aula em duas, fundem duas em uma. Toda a numeração de página que a taxonomia e o dicionário de
pontos guardam (`Aula 01 [p3-12]`, `Nº de Páginas de Teoria`) envelhece sozinha, em silêncio.

## O princípio

**O ponto é a identidade; a página é atributo derivado.** É a mesma lógica de
[[feedback_codigo_identifica_conteudo_nao_posicao]] — código identifica conteúdo, não posição.
Uma atualização do curso **não invalida a taxonomia**, invalida uma coluna recomputável.

## O mecanismo

1. **Âncora textual por página de teoria:** guardar as **5 linhas de prosa mais longas** da
   página, normalizadas (sem acento, sem espaço, minúsculo). Depois de uma atualização, procura
   esse texto e obtém a página nova. Sobrevive a repaginação, inserção de conteúdo e quebra de
   aula. Desempate entre candidatos pela ordem (o conteúdo não muda de ordem numa revisão).
   **Correção de 19-08-2026, testado:** a versão anterior mandava guardar **o título do
   subtópico** — isso **não funciona**. Busca por título acerta 0 de 5 seções (o título aparece
   na prosa o tempo todo), metade dos cabeçalhos é banner gráfico e não sai no `extract_text()`,
   e os títulos do Índice são gerados por template e não batem com o impresso no corpo. Com
   prosa: 99,5% sob repaginação simulada, 0% de âncora perdida.
2. **Dois hashes, não um.** O hash do arquivo inteiro funciona (testado: dois downloads do mesmo
   PDF saem byte a byte idênticos, não há marca d'água por download), mas é **ruidoso**: o
   Estratégia monta o PDF de um mestre único de teoria e troca só a seção de questões por banca
   — em 16 de 16 pares de aula o `sha256` do arquivo diferia e a teoria era idêntica. Então:
   `sha256_arquivo` pra integridade, e **`hash_teoria`** (texto normalizado só do bloco de
   teoria, boilerplate detectado automaticamente) como gatilho de revalidação. Só o que muda o
   `hash_teoria` entra na fila. Cuidado: a marca d'água é **por conta**, então hash só compara
   dentro da mesma conta (ver [[project_conta_estrategia_compartilhada]]).
   Comparar com [[feedback_download_bezerra_convencoes]]: o esqueleto do Bezerra (baixar pra
   temp + comparar hash) transfere igual, mas o **diff do Sumário** dele não tem equivalente
   aqui — o Índice do Estratégia dá 11,8 páginas de teoria por seção em média, grosso demais.
   O `hash_teoria` ocupa esse lugar.
3. **Respondido em 19-08-2026: a plataforma NÃO expõe data de atualização.** O único campo de
   data da API (`data_publicacao` em `GET /api/aluno/curso/{id}`) é cronograma de liberação
   semanal, não revisão. Os headers do CDN também não servem (o PDF é gerado sob demanda, o
   `Last-Modified` nasce na hora). A data real continua sendo a impressa na capa do PDF, que as
   skills de download já extraem. **Não dá pra saber o que mudou sem baixar.**

## Os quatro casos se repetem

O curso tem o mesmo ciclo de vida da taxonomia: **renomeação** e **substituição** de seção a
automação resolve pela âncora; **desdobramento** (aula vira duas) e **fusão** vão para a **Fila
de Pendências**, porque exigem decisão de quem conhece o conteúdo.

## Cadência (definida por Elvis)

- **Cursos Regulares:** verificação **mensal** — é onde o professor mexe.
- **Cursos pós-edital:** raro ou nunca; basta uma verificação pontual antes de usar.

A cadência é **por tipo de curso**, não global.

**O mensal não é barato como se supunha** (descoberto em 19-08-2026). Como a plataforma não
expõe data de atualização, verificar significa **rebaixar os PDFs**. E existe cota: a resposta
da API traz `aulas_baixadas`, `aulas_baixadas_hoje` e `downloads_restantes` (valia 50 na conta
testada) — olhar esse campo antes de rodar em lote. Um `HEAD` também não é neutro: ele já marca
a aula como baixada. Vale reavaliar se o mensal fica em todos os Regulares ou só nas disciplinas
que o professor mais mexe.

## Escopo do alerta antes de montar caderno

Elvis pediu alerta de "material atualizado recentemente?" antes de criar caderno. Vale, mas com
o escopo correto: **página desatualizada não muda a questão escolhida** — a questão é escolhida
pelo ponto, não pela página. O que ela estraga é a **indicação de onde estudar** que acompanha o
caderno e a checagem de resolvibilidade. O alerta age sobre o material de apoio, não sobre a
composição do caderno.

## Colunas que isso acrescenta

Na taxonomia e no dicionário de pontos: **âncora textual**, **hash/versão do PDF de origem** e
**data da última verificação**, ao lado da página.

**Onde cada coisa mora** (definido em 19-08-2026): os hashes vão pra planilha de metadados da
disciplina — 4 colunas novas depois de `Nº de páginas do PDF`: `SHA-256 (arquivo)`,
`Hash da Teoria`, `Páginas de Teoria` (ex. `3-25`, delimitado pelo Índice) e `Token CDN`.
**A âncora NÃO cabe em planilha** — são 445 KB por disciplina; vai num sidecar
`<Matéria> - ancoras.json` na pasta da disciplina.

## Onde está o detalhe

Investigação completa (medições, endpoints, taxas de acerto, envelope de robustez) em
`_contexto/estrategia-versionamento.md`. Protótipo rodando em `scripts/estrategia_ancora.py`
(`fichar` gera o baseline, `conferir` compara e emite o mapa `p_antiga → p_nova`).

**Ainda sem prova:** se o token de 4 hex do CDN muda quando o professor atualiza a aula — se
mudar, vira detector barato de verdade. Registrar o token desde já pra ter a série histórica.

**Why:** sem isso, daqui a alguns meses metade das indicações de página aponta pro lugar errado
e ninguém percebe, porque nada quebra — o número continua lá, só que apontando pra outra coisa.

**How to apply:** ao mexer nas skills de download do Estratégia ou criar a
`revalidar-paginas-estrategia`, gravar os dois hashes + o sidecar de âncoras; em atualização,
`sha256_arquivo` igual → nada; diferente mas `hash_teoria` igual → só questões, não tocar em
página; `hash_teoria` diferente → relocalizar. Página cuja âncora sumiu vai pra revisão humana
(Fila de Pendências), nunca pra remapeamento automático — é justamente o caso em que a
taxonomia pode ter mudado de verdade.
