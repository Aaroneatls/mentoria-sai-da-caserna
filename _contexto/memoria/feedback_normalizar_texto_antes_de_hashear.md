---
name: feedback_normalizar_texto_antes_de_hashear
description: o PDF do Estrategia tem CPF e nome do titular na camada de texto; hashear sem remover quebra a comparacao entre contas
metadata:
  type: feedback
---

**O PDF do Estrategia carrega CPF e nome do titular da conta na CAMADA DE TEXTO**, em quase toda
pagina: `02055447114 - Gisilene Tatianne Santos de Lima`. Medido em 22/08/2026: **124 de 125
paginas**.

**Consequencia:** hashear o texto sem remover isso faz o mesmo conteudo, baixado por **contas
diferentes**, gerar hashes diferentes. A regra de "mesma teoria = mesmo Cod Mestre" falha **em
silencio**: o sistema deixa de reconhecer que sao o mesmo topico e ninguem percebe.

**A regra geral:** antes de hashear ou ancorar, **remover tudo que varia por conta ou por
download**. Vale para `hash_teoria`, para ancoras de prosa e para qualquer extracao comparativa.

O detector de titulos por tamanho de fonte nao sofre, porque a marca e pequena. As ancoras de
prosa sofreriam.

**E o hash do ARQUIVO nao serve para nada:** o PDF vem marcado por download. Quatro downloads do
mesmo arquivo deram quatro hashes e quatro tamanhos (90.153 / 90.183 / 90.224 / 90.274 bytes).
Assinatura de mudanca correta: **nome do arquivo no CDN** (identidade) + paginas + tamanho
aproximado com ~1 KB de tolerancia + data da capa do PDF.

Ver [[project_paginas_estrategia_sao_derivadas]] e [[feedback_validar_cache_por_amostragem]].
