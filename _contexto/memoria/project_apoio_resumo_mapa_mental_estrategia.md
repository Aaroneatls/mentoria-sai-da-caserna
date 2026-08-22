---
name: project-apoio-resumo-mapa-mental-estrategia
description: "Resumo e mapa mental do Estratégia ficam por VÍDEO (não por aula); regras de prioridade, deduplicação e descarte fechadas com o Elvis em 22-08-2026"
metadata:
  node_type: memory
  type: project
---

No Estratégia, **resumo e mapa mental não são da aula: são de cada vídeo dentro dela**. No objeto do vídeo (`/api/aluno/aula/{id}` → `videos[]`) existem os campos `resumo`, `slide` e `mapa_mental`, preenchidos quando existem e `null` quando não. As rotas são `/api/video/{videoId}/download/{resumo|mapa_mental|slideshow}`. A tela mostra o botão **do vídeo aberto**, e é por isso que parece haver um só por aula. Substitui a suposição antiga de que o resumo estaria dentro do livro. Ver [[project-resumos-mapas-mentais-indexacao]].

**Regras fechadas com o Elvis em 22-08-2026:**

1. **Prioridade é sempre a aba Resumos / Mapa Mental** (arquivo já separado), porque o aluno só clica e baixa. Resumo que só existe **dentro do livro** vem depois — e o livro só conta se ele próprio rotular a seção como resumo; trecho de teoria escolhido por nós **não** é resumo.
2. **Resumo e mapa mental não têm hierarquia entre si** — se houver os dois, indicar os dois; eles se complementam.
3. **Se o mesmo conteúdo existir nos dois lugares**, comparar: se um for claramente mais completo (ou o outro incompatível), ficar com o mais completo.
4. **Arquivo idêntico repetido em vários vídeos: baixar uma vez só e indicar uma vez só.** É comum — no piloto, um resumo servia aos vídeos 1, 2, 8 e 13 da mesma aula.
5. **Arquivo sem conteúdo (só capa) é descartado.** Caso real: `apznza-2.pdf`, 1 página, apenas "MAPAS MENTAIS – Direito Constitucional / Material compilado pelo Estratégia".
6. **Deduplicar pelo nome do arquivo no CDN, nunca por hash:** o PDF é marcado por download, então o mesmo arquivo baixado 4 vezes dá 4 hashes diferentes (tamanho varia ~100 bytes). Conferir com páginas + primeira linha do texto.
7. **Registrar o que foi conferido**, porque na atualização do curso é preciso repassar o apoio pra ver o que mudou.

**Dois tipos de resumo**, que precisam de marcação diferente: o **compilado** abre com "APRESENTAÇÃO DO MATERIAL — Queridos alunos!!" e cobre um tema inteiro (4 a 12 páginas); o **pontual** vai direto ao assunto em ~2 páginas.

**Limitação que muda o desenho:** a API **não diz quais páginas do livro o vídeo cobre**. A ligação do apoio com o bloco/Cód Mestre tem de ser por **assunto** (título do vídeo), nunca por página — e acontece na fase de granularidade, não na de download. Ver [[project-taxonomia-codigo-mestre-e-atualizacao]].
