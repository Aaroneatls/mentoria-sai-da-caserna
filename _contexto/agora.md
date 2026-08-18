# Agora — contexto vivo

> Este é o contexto que muda toda semana (diferente de `estrategia.md`, que é o foco de fundo).
> O `/iniciar` lê isto no começo da sessão; o `/atualizar` escreve aqui no fim.
> Mantenha curto: o que passou de ~30 dias sai daqui (vai pro histórico ou some).

## Onde paramos
Sessão longa em 2026-08-18: baixei o pacote inteiro "Regular Fiscal" (22 disciplinas, ~415 aulas) e, na validação, achei e corrigi vários bugs reais de nomenclatura/conteúdo. Isso motivou uma bateria grande de melhorias nas skills `baixar-curso-especifico-estrategia` e `baixar-curso-completo-estrategia` (ambas já sincronizadas no GitHub) — ver lista em "Decisões recentes". Também criei planilha de metadados (Google Sheets) pra cada uma das 22 disciplinas, salva na respectiva pasta no Drive.

## Decisões recentes
- 2026-08-18 — Navegador embutido é o padrão pras duas skills; Chrome real só com autorização pedida a cada vez.
- 2026-08-18 — Rótulo do arquivo (Aula NN) tem que ser cópia exata do site, nunca sequencial próprio — corrige bug real de deslocamento de numeração. Tags de mídia/equipe ("Somente PDF" etc) não entram no rótulo.
- 2026-08-18 — Toda pasta (pacote e cada disciplina) leva sufixo de data `(DD-MM-AAAA)` da última atualização — controle independente por disciplina.
- 2026-08-18 — Checagem de conteúdo por palavra-chave (grátis, local, sem gastar token) durante o download, comparando o PDF com o assunto esperado — sinaliza aula suspeita sem travar.
- 2026-08-18 — Validação final (cruzar rótulo do site x arquivo local) virou passo obrigatório nas duas skills, só por nome, sem reabrir PDF.
- 2026-08-18 — Curso ID do Estratégia é registrado e conferido a cada atualização — se mudar, avisar o usuário com contexto em vez de decidir sozinho (o site às vezes reatribui ID mantendo o mesmo conteúdo).
- 2026-08-18 — Planilha de metadados (Google Sheets nativo, nunca Excel local) é saída obrigatória de toda disciplina baixada/atualizada — abas Aulas + Legenda, formatação padrão salva na memória.

## Pendências
- **Próxima sessão: Elvis vai passar os links de DOIS cursos específicos do Estratégia pra testar as skills atualizadas do zero, numa janela de contexto nova.** Rodar `baixar-curso-especifico-estrategia` normalmente pra cada um — é um teste de validação de tudo que mudou hoje (nomenclatura, validação final, checagem de conteúdo, Curso ID, planilha de metadados).
- Rodar /mapear pra criar mais skills personalizadas pro dia a dia.

## Quente agora
Organização do fluxo de dados: baixar e estruturar material do Estratégia Concursos em pastas locais pra montar planos de estudo.
