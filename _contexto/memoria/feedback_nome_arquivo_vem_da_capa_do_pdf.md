---
name: feedback_nome_arquivo_vem_da_capa_do_pdf
description: "Nos downloads de material, o nome do arquivo vem do título impresso na capa do PDF quando ele diverge do rótulo da plataforma"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 466c375d-4133-4017-9632-14e291096412
  modified: 2026-08-19T00:07:49.481Z
---

Ao baixar material de plataforma (Resumos Esquematizados do Bruno Bezerra, e por padrão qualquer download em massa), **sempre conferir o rótulo da aula no site contra o título impresso no próprio PDF** (capa da 1ª página / 1º tópico do Sumário). Havendo divergência, **vale o nome que está dentro do PDF** — mantendo o código da aula (R00, R01...) e o nome da matéria, trocando só o assunto. O rótulo antigo do site fica registrado na planilha de metadados (coluna "Rótulo na plataforma (quando diferente)") pra ainda dar pra achar a aula no site.

Exceção: quando a capa lista vários assuntos em vez de um título único (mais de 4 linhas úteis ou ~90+ caracteres), manter o rótulo da plataforma, que nesse caso é o guarda-chuva correto.

**Why:** confirmado pelo Elvis em 2026-08-18, depois do download do combo completo — o professor às vezes deixa no site um rótulo que não corresponde ao conteúdo do PDF (ex: "Atos Lícitos e Ilícitos" num PDF de "Defeitos e Invalidade dos Negócios Jurídicos"). O nome do PDF é a fonte confiável.

**How to apply:** já está documentado no Passo 5.1 da [[skill baixar-resumo-especifico]] e referenciado na baixar-resumo-combo-completo. Ao criar skill nova de download em massa, incluir essa checagem desde o começo. Relacionado a [[feedback_download_bezerra_convencoes]].
