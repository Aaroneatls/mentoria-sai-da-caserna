---
name: project-mapeamento-8-disciplinas-resultado
description: "Resultado do teste real de mapear 8 disciplinas do Regular Controle: o que funcionou, os dois modos de falha do detector e onde a granularidade quebra"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T15:50:30.405Z
---

Teste real executado em 2026-08-20, com o Elvis ausente. **395 blocos em 8 disciplinas** do
Curso Regular Controle. Planilha: `Base Curso Regular Controle — Blocos de Estudo
(multidisciplina)`.

## Resultado por disciplina

| Disciplina | Blocos | Fora da faixa 5-12 | Confiança |
|---|---|---|---|
| AFO, Orçamento Público e LRF | 44 | 0 | ALTA |
| Direito Constitucional | 58 | 1 | ALTA |
| Português | 57 | 1 | ALTA |
| Direito Administrativo | 92 | 6 | MÉDIA |
| Controle Externo | 41 | 3 | MÉDIA |
| Contabilidade Pública | 72 | 11 | MÉDIA |
| Administração Pública | 23 | 11 | **BAIXA** |
| Auditoria Governamental | 8 | 3 | **BAIXA** |

## Modo de falha 1 — título e corpo com o MESMO tamanho de fonte

Em **Administração Pública** e **Auditoria Governamental** o corpo do texto é **13,0** e os
títulos também são **13,0**. Diferem só pelo negrito — que é justamente o sinal em que não dá
para confiar, porque o flag é invertido entre safras do template.

Resultado: 1 título a cada 13 a 45 páginas, granularidade insuficiente para blocos de 10.

**A saída é o nível 2 por par de linhas roxas** (presente em 410 dos 1.096 PDFs, segundo a
varredura). Na Aula 11 de Administração Pública são 9 páginas com esse padrão. Precisa ser
implementado **em conjunto** com a tipografia, não como alternativa —
ver [[project_detector_tipografico_titulos_estrategia]].

## Modo de falha 2 — fim da teoria não detectado

Em **Auditoria Governamental**, várias aulas saíram com o arquivo inteiro marcado como teoria
(`p3-193` num arquivo de 193 páginas). A faixa `QUESTÕES` não foi reconhecida ali. Sem o fim da
teoria, a contagem infla (1.224 páginas, implausível) e o corte fica sem sentido.

Em **Controle Externo** o mesmo problema existia e **foi corrigido** lendo visualmente 17 faixas
rasterizadas: a disciplina caiu de 616 para 540 páginas de teoria. As 17 estavam quase todas em
`QUESTÕES COMENTADAS` / `GABARITO` / `REFERÊNCIAS`.

**Lição:** faixa rasterizada não lida não pode ser tratada como inexistente — ela é
frequentemente o marcador de fim de teoria, e ignorá-la corrompe a disciplina inteira. O
mapeador agora registra essas faixas como `pend_faixa` em vez de descartá-las em silêncio.

## Teoria multi-zona é comum, não exceção

Em **Controle Externo, 5 das 9 aulas** têm teoria retomando depois de um bloco de questões.
Confirma o alerta em [[project_zonas_de_teoria_e_questao_no_pdf]].

⚠️ **Bug encontrado e corrigido:** usar o fim da PRIMEIRA zona como limite do último bloco gera
**página final menor que a inicial** quando o bloco começa numa zona posterior. Saíram blocos de
`-130` páginas. O limite tem que ser a última página da ÚLTIMA zona, e vale uma trava que
descarta bloco invertido.

## Densidade de questão por disciplina (medida)

Auditoria Governamental 43% · AFO 40% · Controle Externo 39% · Contabilidade Pública 39% ·
Direito Constitucional 34% · Direito Administrativo 32% · **Administração Pública 6%**.

Medido por página que contém questão. Por área é bem menor — ver
[[project_zonas_de_teoria_e_questao_no_pdf]].

## Custo de processamento

`find_tables()` é o gargalo: 4 disciplinas estouraram 10 minutos numa execução. Rodar
disciplina a disciplina, em segundo plano, e não em laço único.

Ver [[feedback_validar_cache_por_amostragem]] e [[project_base_regular_e_pos_edital_cod_mestre]].
