---
name: feedback-encurtar-nome-arquivo-padrao
description: "Padrão do workspace: ao salvar qualquer arquivo baixado, encurtar o nome já na gravação — renomear depois, se houver critério de classificação"
metadata:
  node_type: memory
  type: feedback
---

**Vale pra tudo que a gente baixar, em qualquer plataforma e qualquer skill.** Ao salvar um arquivo, **encurtar o nome já na hora da gravação**, sem esperar dar problema. Se depois existir um critério de classificação (código do tópico, nº da aula, sigla da disciplina), renomear em cima — mas o padrão de partida é nome curto. Confirmado pelo Elvis em 22-08-2026.

**Why:** o Windows corta caminho em **260 caracteres**, e os nomes de origem do Estratégia estouram sozinhos. Caso real no piloto de Direito Constitucional: `3-1-direito-constitucional-direitos-e-garantias-fundamentais-direitos-e-deveres-individuais-e-coletivos-parte-1-docx.pdf` — o arquivo baixou, mas **não abria**: `PdfReader` e até `os.path.getsize` davam "caminho não encontrado". Só voltou a funcionar depois de encurtar. O erro engana, porque parece arquivo corrompido e é só o caminho.

**How to apply:** ao gravar, cortar o nome de origem (limite prático ~50-60 caracteres no nome do arquivo) preservando o que identifica o conteúdo. Se precisar renomear com caminho longo, usar o prefixo estendido do Windows (`\?\` + caminho absoluto) — sem ele, o próprio rename falha. Vale junto com [[feedback-nome-arquivo-vem-da-capa-do-pdf]]: a fonte do nome continua sendo o conteúdo, o que muda é o tamanho.

**Como medir o caminho (armadilha real, 22-08-2026):** medir sempre o caminho **absoluto**. `os.path.join(raiz, dirpath, arquivo)` com `dirpath` vindo de `os.walk('.')` no Windows **descarta a raiz** quando o componente começa com barra invertida — o número sai plausível (215 em vez de 263) e passa despercebido, porque parece confortável. Usar `os.path.abspath(os.path.join(dirpath, f))`. Medição correta em 22-08-2026: 1.212 arquivos na pasta do Estratégia, **157 acima de 240 caracteres e 1 já acima de 260**.

**O que devolve espaço é não repetir o pai**, não encurtar sigla: aplicar só a regra 1 do `bases/NOMENCLATURA.md` (pasta da disciplina não repete concurso nem data; arquivo não repete a disciplina) leva os 157 para **zero**, com pior caminho em ~230. O prefixo de sigla (`LTRIB - `) **consome** 8 caracteres — é organização, não espaço.
