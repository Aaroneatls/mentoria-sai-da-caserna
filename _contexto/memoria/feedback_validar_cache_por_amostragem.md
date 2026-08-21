---
name: feedback-validar-cache-por-amostragem
description: Todo valor guardado em cache tem que ser reconferido por amostra a cada execução — hash sozinho não pega detector que mudou nem detector que sempre esteve errado
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T12:52:05.384Z
---

Pedido pelo Elvis em 2026-08-20, quando aprovou guardar em cache o percentual de questão por
disciplina em vez de recalcular sempre.

## A regra — dois níveis

**Durante o trabalho: amostra de 20%** (mínimo 2), sorteada **de novo a cada execução**,
reprocessando do zero e comparando com o guardado. Ao longo do tempo tudo acaba coberto. Se
qualquer item divergir, o cache da disciplina inteira é invalidado e o Elvis é avisado.

**Ao fechar uma base: verificação COMPLETA, sempre, sem perguntar.** Vale para cada base nova
(Regular Fiscal, Regular Controle, pacotes de concurso). O resultado vai registrado na planilha
com a data.

Guardar junto uma **versão do detector**. Se a regra de detecção mudar, o cache cai sozinho,
sem depender da sorte do sorteio.

## Custo medido, não estimado (2026-08-20, 18 aulas de Direito Administrativo)

| | Tempo | Linhas lidas |
|---|---|---|
| Amostra 20% | 8 segundos | 4 |
| Completa 100% | 26 segundos | 18 |

Diferença de ~500 tokens. O trabalho roda em Python; só o resumo de uma linha por aula entra no
contexto. Projetado para um pacote inteiro (211 PDFs): ~5 minutos e ~6 mil tokens.

O Elvis perguntou se a completa ficaria cara. **Não fica** — por isso ela virou obrigatória no
fechamento, não opcional.

**Exceção:** a **leitura visual de títulos rasterizados** (160 imagens só em Direito
Administrativo) é cara de verdade e **não** se refaz a cada fechamento. Para ela vale o hash:
título em imagem só muda se o PDF mudar, então a releitura é feita apenas nas aulas afetadas.

## Por que o hash não basta

O hash responde só uma pergunta: *"o arquivo mudou?"*. Existem dois jeitos de o cache apodrecer
com o arquivo intacto:

1. **O detector muda.** Aconteceu três vezes num único dia (filtro de tabela, marcador de
   questão, altura da faixa).
2. **O detector sempre esteve errado.** O número entrou errado no cache e vira verdade.

## Isso já pagou, na primeira execução

Ao corrigir a contagem de questão para o marcador `Comentários:`, o valor novo foi gravado no
cache mas o **script que gera o cache não foi corrigido junto**. Na execução seguinte ele
sobrescreveu os números bons pelos velhos. A amostra pegou na hora:

```
Aula 11  pag_questao  guardado=0  recalculado=7
Aula 03  pag_questao  guardado=8  recalculado=11
>>> CACHE INVÁLIDO
```

Sem a amostragem, a base teria ficado com dado errado e ninguém notaria.

**Lição que vale além do cache:** ao corrigir um valor, corrigir **a origem que o produz**, não
só o valor gravado.

Ver [[feedback_limiares_com_margem_nao_constante_fixa]] e
[[feedback_qualidade_acima_de_economia_de_tokens]].
