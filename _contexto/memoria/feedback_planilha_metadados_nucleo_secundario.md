---
name: feedback-planilha-metadados-nucleo-secundario
description: "Formato de metadados pra comparar teoria entre PDFs de aula — coluna \"Metadados\" quebrada por subtópico com página e âncora legal (v2)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-18T10:38:20.829Z
---

Pra planilhas de mapeamento de aulas (como a "teste mapeamento de aulas", ver [[project_projetos_planilha_mapeamento_aulas]] e [[feedback_planilha_projeto_padrao_cabecalho]]), a coluna "Metadados" guarda um fingerprint da teoria de cada aula.

**Formato atual (v2, desde 2026-08-18), por subtópico:**

```
[pP-Q] Nome do Subtópico (do índice interno do PDF): âncora legal se houver (art. X da Lei Y/AAAA, Súmula Z); institutos/conceitos específicos desse subtópico
[pP-Q] Próximo Subtópico: ...
```

Cada subtópico é um item do índice interno do PDF (com sua própria faixa de página), um por linha dentro da célula — não mais um bloco único pra aula inteira. Âncoras legais (artigo, número de lei, súmula) vêm ANTES dos termos de tema livre, porque são o critério de match mais forte e inequívoco entre fontes diferentes (um "art. 9º da Lei 8.429/1992" não tem sinônimo; um nome de tema como "Poder Disciplinar" pode aparecer com nomes diferentes em fontes diferentes).

**Por que mudou do formato v1 (núcleo/secundário em bloco único por aula):** ao planejar cruzar essas aulas com a lista de assuntos do TecConcursos (ver [[project_skill_mapeamento_aulas_pendencias]]), ficou claro que o Tec quebra o conteúdo em assuntos bem mais granulares que uma aula inteira — ex: uma aula sobre "Atos Administrativos" corresponde a pelo menos 4 assuntos separados do Tec (Espécies/Classificação, Desfazimento, Atributos, Elementos/Requisitos). Um metadado no nível da aula inteira não permite dizer qual PARTE da aula bate com qual assunto do Tec.

**Regra de granularidade (atualizada em 2026-08-18):** o índice interno do PDF é o ponto de partida, mas não é o limite — sempre que um item do índice for grande demais pra ser um "assunto de estudo" só (referência prática: a maioria dos subtópicos de uma aula fica entre 5 e 20 páginas; acima de ~30-40 páginas cobrindo temas claramente diferentes, considerar grande demais), quebrar mais fundo em subtemas reais do conteúdo (procurando subtítulos/cabeçalhos internos do próprio texto, não só o índice da página 2). O critério é pensar em quem vai estudar aquele pedaço: cada subtópico deve corresponder a um "assunto" que faz sentido estudar de uma vez, nem fatiado demais (granularidade artificial por parágrafo) nem grande demais (bloco de 100+ páginas misturando vários temas). Caso real: a Aula 13 (Agentes Públicos) tinha um bloco único de 140+ páginas ("Agentes Públicos Parte 2", p24-168) que foi quebrado em subtemas menores nesse ajuste.

- Fica numa célula (coluna D), não em arquivo separado — decisão consciente pra manter tudo alinhado à linha da aula e fácil de comparar por script/planilha.

**Nomenclatura da coluna (desde 2026-08-18):** sempre que houver mais de uma fonte de metadados na mesma planilha/projeto (Estratégia, resumos do Bruno Bezerra, TecConcursos, edital, etc.), nomear a coluna como `Metadados (Nome da Fonte)` — ex: `Metadados (Estratégia)`, `Metadados (Bezerra)` — nunca deixar só "Metadados" genérico quando pode haver ambiguidade sobre de qual fonte é.

**Why:** o objetivo é, dado um PDF novo, conseguir dizer se ele cobre a mesma teoria de uma aula já catalogada — mesmo vindo de curso/concurso diferente (testado com sucesso comparando TCDF-ANACE com a base ISS Manaus-AFTM: índice + amostra de texto bastaram pra confirmar match, e um PDF de assunto diferente corretamente não bateu).

**How to apply:** ao criar ou expandir uma planilha desse tipo (mapeamento de aulas a partir de PDFs do Estratégia/TecConcursos), seguir esse formato de metadados por padrão — perguntar antes de mudar a estrutura se for uma planilha diferente/com objetivo diferente.
