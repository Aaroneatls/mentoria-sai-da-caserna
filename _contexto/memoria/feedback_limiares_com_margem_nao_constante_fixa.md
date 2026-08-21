---
name: feedback-limiares-com-margem-nao-constante-fixa
description: "Nas skills de leitura de PDF, todo limiar geométrico ou tipográfico é faixa com verificação no momento, nunca constante fixa — varia por professor e por aula"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T11:02:43.558Z
---

Dito pelo Elvis em 2026-08-20, e comprovado no mesmo dia.

**A regra:** qualquer número usado para identificar elemento no PDF — largura, altura, margem,
corpo de fonte, cor, distância — entra como **faixa de tolerância**, e de preferência **medido
no próprio documento em tempo de execução**. Nunca como constante cravada no código.

**Por quê:** o layout varia por professor e por aula, mesmo dentro do mesmo template e da mesma
disciplina. Não existe "o padrão do Estratégia" — existe uma família de variações.

**A prova:** a varredura dos 1.096 PDFs mediu a margem esquerda das faixas de título entre
**x0 = 28 e 36pt** e recomendou esse intervalo. Aplicado às 18 aulas de Direito Administrativo,
ele **descartaria 57 faixas legítimas** das Aulas 06 e 07, que usam **x0 = 41**. A faixa boa é
`x0 <= 60`.

Outros casos medidos que confirmam:

| O que | Variação real |
|---|---|
| Corpo do texto | 12,0 em 84,7% dos PDFs, mas 13,0 em 97 e 11,0 em 67 |
| Altura da faixa | 27, 30, 31, 34pt — e caixa de mnemônico em 21pt |
| Margem x0 | 30, 34, 36, 41pt |
| Questão dentro da teoria | de 0% a 65% conforme a disciplina |
| Faixa rasterizada | 0% em 57 das 71 disciplinas, 100% em algumas aulas |

**Como implementar:** o detector já faz isso com o corpo da fonte (histograma do próprio
documento define o que é corpo e o que é título). Estender o mesmo princípio ao resto:
medir primeiro, decidir depois. Quando não der para medir, usar faixa larga e **registrar o
que ficou de fora** para conferência, em vez de descartar em silêncio.

Ver [[project_detector_tipografico_titulos_estrategia]] e
[[feedback_qualidade_acima_de_economia_de_tokens]].
