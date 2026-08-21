---
name: project-guias-do-tec-uso-e-limites
description: "Guias de Estudo do Tec: usar como fonte de consulta e alerta (nomenclatura de matéria, observações sobre inéditas, conferência de contagem), nunca como fonte de composição de caderno"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T20:28:26.475Z
---

Avaliado em 2026-08-19 a pedido de Elvis, examinando o guia real do **TC DF 2026**
(`/guias/tc-df-2026/analista-administrativo-de-controle-externo-tc-df/...`).

## Veredito: consulta e alerta, nunca composição

### Onde o guia serve

1. **Dicionário de nomenclatura de matéria — o maior valor.** O guia lista as matérias do
   edital já traduzidas para o nome que o Tec usa, agrupadas nos blocos do edital
   (Conhecimentos Básicos / Específicos / Especializados). Resolve o problema de "matéria com
   nome diferente no pós-edital" e alimenta a aba **Siglas de Disciplinas**.
2. **Bloco "Observações"** — diz o que **não será abordado** e **quais assuntos terão apenas
   questões inéditas**. No guia do TCDF: *"Não abordaremos: IDF0"* e *"Abordaremos o seguinte
   assunto por questões inéditas: Resolução nº 296/2016, títulos I, II e III"*.
3. **Conferência do nosso recorte.** O caderno de Direito Administrativo do guia tem **1.136
   questões**; nosso filtro independente (Cebraspe + área Controle + 2017-2026 + sem anuladas e
   desatualizadas) deu **1.111**. Validação cruzada barata.
4. **O caderno de inéditas já vem isolado** (75 questões no TCDF), separado dos demais.

### Onde o guia NÃO serve

- **A composição dos cadernos dele é inaproveitável.** Além do problema de trazer questão fora
  do edital (apontado por Elvis), o caderno dele é **por matéria inteira** — 1.136 questões num
  caderno só. É o oposto do nosso desenho (caderno por ponto, com curadoria de redundância e
  checagem de resolvibilidade). Adotar seria abandonar o método.
- Os "capítulos teóricos" são **teoria do próprio Tec**, não do Estratégia nem do Bezerra. Não
  substituem nossa camada de cobertura.

## O bloco de Observações é MUTÁVEL (Elvis, 2026-08-19)

O Tec **vai atualizando** as observações ao longo do tempo. É ali que ele anuncia quando vai
lançar questões inéditas. **Depois que as inéditas são criadas, o anúncio some** — foi o caso do
guia do TCDF quando examinado.

**Consequência:** ler o guia uma vez só não serve — perde-se a janela em que o anúncio está no
ar. O tratamento é o mesmo dos PDFs do Estratégia
(ver [[project_paginas_estrategia_sao_derivadas]]): **guardar o texto das observações e comparar
a cada consulta**. Qualquer mudança dispara alerta na Fila de Pendências.

Os dois sinais importam:
- **Anúncio aparece** → registrar a data prevista e agendar a rodada de atualização.
- **Anúncio some** → as inéditas foram criadas; é hora de fichar e montar o caderno novo.

## Rotina proposta, quando um edital novo entra

1. Ler a lista de matérias → alimenta o dicionário de nomenclatura.
2. Ler e **arquivar** o bloco de observações → o que fica de fora e o que virá só por inéditas.
3. Comparar a contagem por matéria com a nossa, como sanity check do recorte.
4. Reler periodicamente e **diffar** as observações.

## Filtros de ENUNCIADO do guia — o outro ativo aproveitável

Levantado por Elvis em 2026-08-19. Os guias usam **filtros por enunciado** (busca textual) pra
capturar questões que a classificação por assunto não pega. Os editores do Tec fazem isso na mão
e **já descobriram quais termos funcionam** por matéria — esse conhecimento é o ativo, não o
caderno deles.

**Como extrair:** salvar o caderno do guia na nossa conta e ler os **grupos de filtro** pela API
de configuração do caderno. Evita raspar HTML.

**Status: registrado no fluxo, execução adiada por decisão do Elvis (2026-08-19).** Nada foi
salvo na conta ainda.

### Por que o filtro de enunciado NÃO substitui o fichamento

Teste feito em 2026-08-19, com correção de uma conclusão apressada:

- Assunto `6053` (Regime Jurídico) no recorte Cebraspe/Controle/10 anos: **3 questões**.
- Enunciado `"regime jurídico administrativo"` no mesmo recorte: **50 questões**.
- **Mas** essas 50 se espalham por **17 assuntos diferentes** (poder de polícia, terceiro setor,
  estabilidade, atos, greve…). Numa amostra de 25, só **1** estava mesmo em Regime Jurídico.

O motivo: *"Acerca do regime jurídico administrativo, julgue os itens a seguir"* é **preâmbulo
padrão da Cebraspe**. O filtro pegou a frase de abertura, não o conteúdo. **A escassez do
DADM-003 é provavelmente real.**

**Lição:** o filtro de enunciado é ferramenta de **alcance com muito ruído**. Só presta
**combinado com o fichamento**, que lê a questão e descarta o ruído.

**E o termo escolhido decide tudo:**
- Termo genérico (nome de tópico) → pega preâmbulo. `"regime jurídico administrativo"` = 50, lixo.
- Termo específico (nome de instituto) → pega conteúdo. `"supremacia do interesse público"` = 6;
  `"indisponibilidade do interesse público"` = 8.

## Ressalva técnica

**A página do guia não tem API** — é renderizada no servidor, sem chamada a `/api/`
(confirmado por interceptação de `fetch`/`XHR`). Então é **raspagem de HTML**, mais frágil que
o resto da automação do Tec. A estrutura é simples, mas quebra se mudarem o layout.

URLs: a listagem fica em `/guias/`; cada concurso em `/guias/{slug}`; cada cargo em
`/guias/{slug}/{cargo}/...`.
