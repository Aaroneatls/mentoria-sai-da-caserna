---
name: reference-tecconcursos-manual-completo
description: "Manual completo do TecConcursos (funcionalidades, planos, limites estruturais, filtro por URL, API interna, guias e visualizar como curso) mora em _contexto/tecconcursos.md do workspace ccos-ratos"
metadata: 
  node_type: memory
  type: reference
  originSessionId: c75d2df2-d078-420b-87c3-77d0347b7996
  modified: 2026-08-19T10:50:12.967Z
---

O manual do TecConcursos fica em `_contexto/tecconcursos.md` (workspace ccos-ratos), e as transcrições dos 29 tutoriais oficiais em `_contexto/tecconcursos-transcricoes/`. Levantado em 18–19/08/2026 navegando a plataforma na conta grátis **e** na conta Plano Avançado, lendo o código da aplicação, o help center e a playlist "Tec Concursos | Tutoriais". É autocontido: dá pra colar inteiro em outro projeto.

Os achados que mudam como trabalhar com o Tec:

1. **Filtro por URL** — `/questoes/filtrar?universo=CONCURSOS&formato=OBJETIVA&f[0].tipo=ASSUNTO&f[0].id=5886&f[1].tipo=ANO&f[1].id=2024`. Dispensa clicar na árvore de assuntos.
2. **API interna `/api/...`** por cookie de sessão. `/api/assuntos?materia={id}&hierarquico=true` devolve a taxonomia inteira; `/api/questoes/contagem/filtros` a contagem; `/api/assuntos/buscar-questoes-por-asssunto-relevancia` a lista plana de assuntos com peso (o "Relevância (apenas assuntos)") numa chamada só. Funciona até no plano grátis.
3. **"Adicionar questões por código"** (Configurações do caderno, plano pago) injeta uma lista arbitrária de ids no caderno — rota mais direta pra montar caderno a partir de seleção feita fora da plataforma. E a **aba Gabarito** lista os `#` de todas as questões do caderno, servindo de extrator.
4. **Guias de Estudo** já entregam o cruzamento edital→matéria→assunto→quantidade, com edital verticalizado, cadernos prontos, questões inéditas pros pontos sem questão real e análise das provas anteriores em %. Guia antigo se reaproveita editando os **grupos de filtro** em Configurações.
5. **"Visualizar como curso"** transforma uma pasta em trilha sequencial (assunto a assunto, com teoria + videoaula + mapa mental + as questões do caderno, "marcar como lido" e progresso Básico→Expert). Só rende com caderno consolidado por matéria.
6. **A árvore de assuntos do Tec é ordenada por lógica de aprendizado, como um livro** — serve de espinha dorsal pronta pra plano de estudo.

Limitações que **não** se resolvem pagando: taxonomia do Tec ≠ nomenclatura do edital; nem toda questão é comentada nem classificada; não dá pra baixar comentário nem teoria e o material teórico proíbe comercialização sem autorização; conta de sessão única (automação derruba o usuário logado); impressão limitada a 1.000 questões/dia; objetivas e discursivas não convivem no mesmo caderno; a `/api` é interna e sem contrato estável.

Relacionados: [[reference_tecconcursos_pagina_filtrar_dinamica]], [[feedback_tec_navegador_bizus]], [[feedback_tec_organizar_por_relevancia]], [[feedback_skill_tec_filtros_padrao]], [[project_tres_skills_mapeamento]].

**Why:** o Elvis pediu explicitamente que esse aprendizado ficasse salvo como texto padrão colável em outras seções, pra que qualquer agente já entre sabendo o potencial e os limites da ferramenta antes de montar caderno de questões a partir de edital.

**How to apply:** antes de construir ou rodar qualquer skill que toque no TecConcursos, ler `_contexto/tecconcursos.md`. Preferir URL/API a clicar na interface, e nunca prometer algo que caia numa das limitações estruturais da seção 8 do documento.
