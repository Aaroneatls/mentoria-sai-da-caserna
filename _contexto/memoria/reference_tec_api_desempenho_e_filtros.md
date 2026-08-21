---
name: reference-tec-api-desempenho-e-filtros
description: "Correções ao manual do Tec: o índice de acerto VEM na API (/desempenho), o tipo de filtro de opção é FILTRO_QUESTAO, e a API só responde do navegador logado"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T23:10:50.674Z
---

Verificado ao vivo em 2026-08-20, com o Elvis logado.

## O índice de acerto VEM na API

O briefing do BIZURITO supunha que talvez não viesse e que seria preciso raspar da tela.
**Não é preciso.**

```
GET /api/questoes/{id}/desempenho
```

```json
{"desempenho": {
  "desempenhoGeral": {"acertos": 10865, "erros": 191, "tempoMedio": 39,
                      "alternativa1": 10865, "alternativa2": 190, ...},
  "desempenhoAluno": {...},
  "alternativaCorreta": 1,
  "dificuldade": "Muito Fácil"}}
```

Traz **mais** do que a tela mostra: `tempoMedio`, a distribuição por alternativa e o rótulo
`dificuldade` do próprio Tec. O índice de acerto é `acertos / (acertos + erros)`.

**Não vem** em `/api/questoes/{id}` nem em `/api/questoes/{id}/deslogado` — são 50 campos e
nenhum de desempenho. Precisa da chamada separada.

**Custo medido:** 100 questões em 26 segundos com pausa de 120ms, zero erro e zero 429.
Mil questões ≈ 4,5 minutos.

## A dificuldade do Tec calibra o nosso RISCO

Medido em 100 questões de um tópico:

| Rótulo do Tec | Acerto médio | Faixa |
|---|---|---|
| Muito Fácil | 94,3% | 80,9 a 100 |
| Fácil | 74,5% | 65,3 a 79,5 |
| Médio | 53,0% | 42,3 a 84 |

O corte de 70% do BIZURITO cai quase exatamente na fronteira Fácil / Muito Fácil. Serve de
conferência independente — ver [[project_bizurito_fontes_e_validacao]].

## ⚠️ Questão recente tem amostra pequena

Questões do TCDF 2023 tinham **4 respostas** cada; um índice de 75% ali é ruído. Já as questões
antigas do mesmo tópico tinham mediana de **281** respostas.

Isso **colide com a regra de recência**: as mais recentes são justamente as de índice menos
confiável, e é esse índice que vira rótulo de RISCO na folha do aluno. Precisa de **amostra
mínima** antes de atribuir rótulo. Ver [[project_recencia_na_selecao_de_questoes]].

## Correções ao manual (`_contexto/tecconcursos.md`)

**O tipo de filtro de opção é `FILTRO_QUESTAO`, não `OPCAO`.** `OPCAO` e `CARACTERISTICA` dão
HTTP 500. Tipos que funcionam: `ASSUNTO`, `BANCA`, `ANO` (singular — `ANOS` dá 500),
`FILTRO_QUESTAO`.

```
filtros[i].tipo=FILTRO_QUESTAO & filtros[i].id=REMOVER_ANULADAS
```
Efeito medido: 4.778 → 4.699 questões (79 anuladas fora).

**Ids de banca** (o chute custou um caderno errado): Cebraspe **4**, FCC **3**, FGV **5**,
VUNESP 6. **`id=2` é ESAF**, banca extinta. São 574 bancas — sempre buscar o id em
`/api/bancas?universo=&formato=OBJETIVA`, nunca supor.

**Não achei endpoint de exclusão de caderno.** `DELETE /api/cadernos/{id}` dá 405;
`/excluir` dá 404. Caderno criado errado precisa ser apagado pela tela.

**`/api/pastas-cadernos`** devolve `{pastas:[...]}`; nesta conta só existe
`Sem classificação` (id **7460777**).

## A API só responde do navegador logado

Chamada do shell dá **HTTP 401** — não há cookie de sessão ali. Do `javascript_tool` no
navegador embutido, com o Elvis logado, funciona. Erro de diagnóstico já cometido: concluir
"o Tec está bloqueado" quando o bloqueio era só do shell.

Ver [[reference_tecconcursos_manual_completo]] e [[project_tec_gerador_nao_repete_questao]].
