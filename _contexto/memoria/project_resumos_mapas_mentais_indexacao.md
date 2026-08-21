---
name: project-resumos-mapas-mentais-indexacao
description: "Pendência aberta em 2026-08-19: definir com o Elvis como indicar resumos e mapas mentais das aulas e como isso entra na indexação da skill de mapeamento de aulas"
metadata:
  node_type: memory
  type: project
---

**Lembrar o Elvis disso quando ele voltar.** Em 19-08-2026 ele saiu da sessão deixando este ponto em aberto, e pediu explicitamente pra ser lembrado.

O que ficou pendente de conversa (antes de eu escrever qualquer coisa nas skills):

1. **Como indicar resumo e mapa mental** de cada aula: se existe download separado na aula, se está dentro do livro simplificado, ou se só está no original — sempre com a **página real do PDF** (ver [[feedback-pagina-sempre-do-arquivo-pdf]]; o Índice do livro não serve, os números dele não batem com a página real).
2. **Como isso impacta a indexação do "mapear aulas"** — ele vai pedir uma skill nova por lá que mexe no que a gente faz aqui, então o formato dessas colunas tem que nascer compatível com [[project-skill-mapeamento-aulas-pendencias]] e [[project-taxonomia-codigo-mestre-e-atualizacao]].

**Estado técnico já levantado** (não precisa refazer): a API não expõe resumo/mapa mental; a aba de downloads da aula tem no máximo simplificado, original e grifado; detectar exige abrir o PDF e varrer os cabeçalhos das páginas. Proposta em cima da mesa: 4 colunas novas na aba `Aulas` da planilha de metadados (Resumo / Resumo pág. / Mapa Mental / Mapa Mental pág.) e contagem por matéria no Índice do Pacote (Passo 11B).

**How to apply:** não escrever esse passo nas skills `baixar-curso-*-estrategia` antes de fechar os dois pontos acima com ele.
