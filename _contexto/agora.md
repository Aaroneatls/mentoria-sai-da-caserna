# Agora — contexto vivo

> Este é o contexto que muda toda semana (diferente de `estrategia.md`, que é o foco de fundo).
> O `/iniciar` lê isto no começo da sessão; o `/atualizar` escreve aqui no fim.
> Mantenha curto: o que passou de ~30 dias sai daqui (vai pro histórico ou some).

## Handoff para a sessão "Mapear Aulas" (2026-08-19)

Sessão dedicada a estudar o TecConcursos a fundo. **Tudo que foi levantado está em
[`_contexto/tecconcursos.md`](tecconcursos.md)** — manual autocontido de 13 seções, feito pra ser
lido inteiro antes de qualquer trabalho de mapeamento ou montagem de caderno. As
transcrições dos 51 tutoriais oficiais do canal estão em `_contexto/tecconcursos-transcricoes/`.

**Os quatro achados que mudam o desenho do mapeamento:**

1. **API interna `/api/...`** (cookie de sessão, funciona até no plano grátis) —
   `/api/assuntos?materia={id}&hierarquico=true` devolve a taxonomia inteira com ids e
   códigos de hierarquia; `/api/assuntos/buscar-questoes-por-asssunto-relevancia` devolve
   a lista plana de assuntos com peso numa chamada só. Dispensa clicar na árvore.
   Filtro também funciona por URL: `?formato=OBJETIVA&f[0].tipo=ASSUNTO&f[0].id=333&...`
2. **A árvore de assuntos do Tec é ordenada por lógica de aprendizado, como um livro** —
   serve de espinha dorsal pronta pro plano de estudo, não precisa reordenar.
3. **"Gerar cadernos em série" não serve pra plano de estudo.** Distribui por frequência
   histórica: em Português/Fiscal, um caderno de 20 questões sai com 5 de Interpretação de
   Textos (25%) e 57 dos 73 assuntos zerados — e a composição se repete igual em todos os
   cadernos da série.
4. **O filtro não tem memória.** Dois cadernos manuais com o mesmo filtro saem
   **idênticos**; o "em série" desconta, mas só enquanto a aba fica aberta (recarregou,
   volta ao início). O controle do que já foi usado tem que ser nosso.

**Desenho acordado pra montagem de caderno a partir de edital:** taxonomia + pesos pela
API → cruzar com o edital e definir a quantidade por assunto (decisão nossa, registrada em
planilha) → puxar os `#` das questões → registrar o que foi pra qual caderno →
criar o caderno e injetar por **"Adicionar questões por código"** (Configurações do
caderno) → entregar ao aluno **o link do caderno**.

**Direito autoral:** a entrega é só link de caderno. Nada de PDF de material teórico — o
próprio Tec proíbe comercialização sem autorização.

**Contas:** `bizu.cadastros@gmail.com` (Avançado, zerada, usada nos testes — já limpa) e
`aaroneatsl.int@gmail.com` (Grátis; sobrou lá o caderno de teste
"TESTE CLAUDE - Dir Tributario 10q" pra apagar quando logar).

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
- **PRIORIDADE — retomar com o Elvis (ele pediu pra ser lembrado, 19-08-2026):** como indicar **resumos e mapas mentais** de cada aula (download separado / dentro do simplificado / só no original, sempre com a página REAL do PDF) e **como isso impacta a indexação do "mapear aulas"** — ele vai gerar uma skill por lá que mexe no trabalho daqui. **Não escrever esse passo nas skills `baixar-curso-*-estrategia` antes dessa conversa.**
- Pacote **"Curso Regular para Área Fiscal"** (teórico) sumiu do catálogo da assinatura em 19-08-2026 — não dá pra matricular. Os 21 Curso IDs das disciplinas estão nas planilhas de metadados da pasta; quando o pacote voltar, matricular e conferir pela API.
- Ajustes já escritos nas skills em 19-08-2026 mas **ainda sem commit/push**: Passo 11B (Índice do Pacote na pasta raiz, com as variantes de produto) e o bloco de rodízio de matrícula com a palavra `CORUJA`.
- **Próxima sessão: Elvis vai passar os links de DOIS cursos específicos do Estratégia pra testar as skills atualizadas do zero, numa janela de contexto nova.** Rodar `baixar-curso-especifico-estrategia` normalmente pra cada um — é um teste de validação de tudo que mudou hoje (nomenclatura, validação final, checagem de conteúdo, Curso ID, planilha de metadados).
- Rodar /mapear pra criar mais skills personalizadas pro dia a dia.

## Quente agora
Organização do fluxo de dados: baixar e estruturar material do Estratégia Concursos em pastas locais pra montar planos de estudo.
