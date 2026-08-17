# Agora — contexto vivo

> Este é o contexto que muda toda semana (diferente de `estrategia.md`, que é o foco de fundo).
> O `/iniciar` lê isto no começo da sessão; o `/atualizar` escreve aqui no fim.
> Mantenha curto: o que passou de ~30 dias sai daqui (vai pro histórico ou some).

## Onde paramos
Criei e testei a skill /baixar-curso-especifico-estrategia — baixa em lote os livros eletrônicos (PDF) de um curso do Estratégia Concursos, organizados numa pasta local. Testada com sucesso no curso de Direito Constitucional (TCDF-ANACE), 15 aulas baixadas.

## Decisões recentes
- 2026-08-17 — Padrão de nome de pasta de curso: `Matéria (SIGLA_CONCURSO-SIGLA_CARGO)`, ex: `Direito Constitucional (TCDF-ANACE)`.
- 2026-08-17 — Padrão de nome de arquivo: `Aula NN - Assunto Sintético.pdf`. Livro simplificado é prioridade; se não existir, usa a versão original como fallback.
- 2026-08-17 — Quando uma aula ainda não tem material liberado, criar um `.txt` no lugar do PDF (mesmo padrão de nome + data prevista) como marcador — não é erro, é aula pendente de liberação.

## Pendências
- Rodar /mapear pra criar mais skills personalizadas pro dia a dia.

## Quente agora
Organização do fluxo de dados: baixar e estruturar material do Estratégia Concursos em pastas locais pra montar planos de estudo.
