---
name: project-skill-mapeamento-aulas-pendencias
description: "Checklist mestre de tudo que foi decidido/pendente pras 3 skills de mapeamento (Estratégia, Bezerra, TecConcursos) + futura 4ª fonte (edital) — conferir antes de criar as skills de verdade"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T09:24:57.694Z
---

## PENDÊNCIAS FINAIS CONSOLIDADAS (2026-08-19) — ler isso primeiro

> **REGRA PERMANENTE (Elvis, 2026-08-19):** esta lista (A / B / C / sequência final) é a **tabela de referência viva** do projeto. Toda vez que **(a)** uma tarefa dela for cumprida, **(b)** surgir uma tarefa nova, **(c)** uma tarefa for substituída/alterada, ou **(d)** algo for decidido a ponto de sair do bloco A, **atualizar este arquivo E reenviar a lista inteira atualizada pro Elvis no chat**, no formato numerado (um item por linha, nome em negrito + descrição indentada). Não é sob demanda — é automático ao final da tarefa. Ver [[feedback_tabela_referencia_viva_reenviar]].

Levantamento pedido por Elvis pra não esquecer nada que ficou "pra discutir depois" ao longo de toda a conversa. Quatro blocos: **(A) decisões ainda em aberto**, **(B) já decidido mas não implementado** (ações/ajustes que não são, em si, uma skill nova), **(C) skills pendentes de produção** (os artefatos/skills concretos que precisam ser criados ou atualizados), e a **sequência final**.

### (A) Decisões ainda em aberto
1. Investigar de verdade os **26 casos "sem correspondência"** da antiga Compatibilização — só 1 caso (Aula 13) foi checado a fundo até agora.
2. **Texto padrão** pra quando não existe resumo do Bezerra correspondente — texto exato ainda não escrito.
3. Fallback quando falta resumo do Bezerra: usar o **resumo próprio do Estratégia**, ou deixar os dois por padrão — decisão adiada.
4. **Critérios extras de Curva ABC** propostos por Claude (razão peso/página, densidade de questões, clareza no edital, teto de páginas, tendência, confiança da amostra) — ainda não confirmados/priorizados por Elvis.
5. Pequenas lacunas de nomenclatura encontradas no teste TCDF (item 1 e item 2 do edital, "objeto do direito administrativo" não citado explicitamente em nenhuma fonte) — não decidido se é preocupante ou só questão de granularidade de metadado.
6. **Nomenclatura exata das skills** (ver bloco C abaixo) — ainda não confirmada com Elvis.
7. **Célula solta "Nº de Páginas" na aba "Base Estratégia", linha 8 coluna G** — resquício do design inicial da planilha. Perguntado a Elvis se limpa ou é intencional, nunca respondido.
8. **R08 do Bezerra (Contratos Administrativos)** tem "EXTINÇÃO DOS CONTRATOS" duplicado no sumário interno do PDF (aparece duas vezes seguidas) — nunca confirmamos se é erro de diagramação do material do próprio Bezerra ou algo a corrigir do nosso lado.
9a. **Siglas de disciplinas propostas por Claude** — a aba "Siglas de Disciplinas" nasceu com 3 siglas confirmadas (`DADM`, `DCON`, `DTRI`) e 15 propostas (AFO, contabilidade, auditoria, controle externo etc.) marcadas como "Proposta — confirmar". Precisam do aval do Elvis antes de virarem prefixo de Cód Mestre (ver [[project_taxonomia_codigo_mestre_e_atualizacao]]).
9b. **23 tópicos da taxonomia ficaram sem aula do Estratégia** (Lei 8.112/1990 inteira, Bens Públicos, Intervenção na Propriedade, agências reguladoras, consórcios/convênios, Lei 13.460/2017, Lei 13.303/2016 licitações). Elvis precisa decidir, tópico a tópico, o que vira aula própria, o que fica coberto só por questão do Tec e o que sai do escopo.
9e. **Cortes do RISCO do BIZURITO (70% e 50%)** — provisorios, definidos sem amostra. Recalibrar
com base real, provavelmente por quartil da disciplina, e propor numeros ao Elvis.
9f. **Granularidade da folha do BIZURITO** — quantos pontos entram e quando agrupar topicos
vizinhos numa folha so, para nao entregar folha de 4 linhas ao lado de outra com 20.

9c. **Formato alternativo de esquema pro BIZURITO** — Elvis avisou em 2026-08-20 que vai propor
outro desenho visual pra comparar com o atual (núcleo + blocos por banca) e escolher qual fica mais
fácil de entender. O nome do material já está fechado: **BIZURITO**.
9d. **Onde o bizu entra no fluxo do aluno** — proposta do Claude: teoria → caderno → resumo do
Bezerra → bizu (ele é feedback do que caiu, rende mais com a memória fresca do erro). Não confirmado.

9. **Recursos nativos do Tec ainda não avaliados como possível atalho**: o manual completo (ver [[reference_tecconcursos_manual_completo]]) mapeou que existem **"Guias de Estudo"** (já fazem cruzamento edital→matéria→assunto→quantidade nativamente, com cadernos prontos e questões inéditas pros pontos sem questão real) e **"Visualizar como curso"** (trilha sequencial com teoria+vídeo+questões+progresso). Nunca avaliamos se algum desses recursos nativos resolve parte do que estamos construindo manualmente (taxonomia central, cadernos por nível) antes de reinventar do zero.

### (B) Já decidido, mas não implementado (ações/ajustes, não skills novas)
10. **Compatibilização refeita usando a taxonomia central** — ainda não executada (a antiga foi apagada, ver item 22 mais abaixo no arquivo).
11. **Peso por banca específica com piso de confiança** (~15-20 questões) — regra desenhada, não implementada.
12. **Separar as fontes do Tec por banca de forma sistemática** — feito manualmente uma vez (TCDF), não como mecanismo repetível.
13. **Levantamento mais completo de editais por banca** (além dos ~10-13 já feitos) pra alimentar a taxonomia central.
14. **Validação técnica da API interna do Tec** — confirmada como próximo passo, ainda não executada.
14g. ~~**Habilitar a Google Docs API**~~ — **FEITO por Elvis em 2026-08-20** (projeto Cloud id
574156806233). É o que permite A4 e margem mínima; sem ela o importador força Letter com margem
de 1 polegada.

15. **Checkpoint permanente:** antes de qualquer skill ser dada como pronta, percorrer esse checklist inteiro item a item com Elvis (regra já vigente desde 2026-08-18, ver seção final).

14a. **Manuais operacionais das plataformas (pedido por Elvis em 2026-08-19).** O
`_contexto/tecconcursos.md` virou caderno de anotações (levantamento + correções empilhadas).
Elvis quer que ele seja reorganizado como **manual de operação** — regras, bizus, armadilhas,
contratos de API, tudo em ordem de uso — e que exista o **equivalente para o Estratégia
Concursos**. Objetivo: sempre que formos mexer em qualquer das duas plataformas, existir um
documento claro pra consultar antes.

14b. **Triagem de questão por conteúdo, não por assunto do Tec (problema levantado por Elvis
em 2026-08-19 após o teste do Nível 1).** Dois furos no método atual: (i) pegar as N mais
recentes de um assunto traz **questões redundantes** (mesmo ponto, mesma resolução), quando
seria melhor guardar a repetida pra outro nível e trazer uma que cobre ponto novo; (ii) o
assunto do Tec é **mais grosso** que o tópico mestre, então nada garante que a questão seja
**resolvível com o que a aula do Estratégia ou o resumo do Bezerra efetivamente ensinaram**.

14c. **BLOQUEANTE ANTES DE FECHAR A SKILL — reaproveitamento de teoria entre áreas.** Elvis
determinou em 2026-08-20 que **Claude deve trazer isso à discussão no momento de fechar a skill
de taxonomia**, sem esperar ele lembrar. Razão: logo virão bases de outras disciplinas e de
outras áreas (Controle, Legislativa), e a decisão precisa estar tomada antes, não depois.
O mecanismo já está desenhado — mesmo `hash_teoria` = mesmo Cód Mestre e mesmo nome mestre,
teoria agnóstica de área e questões por área/banca (ver
[[project_teoria_compartilhada_entre_areas]]).

14d. **Atualização automática quando o professor mexe no PDF — EXPLICAR EM DETALHE ANTES DE
EXECUTAR.** Elvis pediu em 2026-08-20 que isso fique na lista em linguagem simples, porque a
descrição técnica não ficou clara pra ele. **Claude deve retomar o assunto com explicação
detalhada no momento de executar.**

Em português claro, o problema é este: hoje, se o professor do Estratégia mexer numa aula e
mudar a numeração das páginas, todas as indicações de página que a gente guardou passam a
apontar para o lugar errado — **e nada avisa**. O número continua lá, bonito, só que errado.

O que precisa existir: um jeito de (a) perceber sozinho que a aula mudou, (b) reencontrar onde
foi parar cada trecho na versão nova, e (c) atualizar tudo de uma vez, em vez de a gente ir
consertando planilha por planilha. A parte técnica de como fazer isso já está resolvida e
descrita em [[project_paginas_estrategia_sao_derivadas]] — falta implementar.

14e. **Validação obrigatória das páginas indicadas (Elvis, 2026-08-20).** Elvis exige garantia
de que a página indicada trata mesmo do assunto anunciado. Claude reconheceu que **as páginas
dos pontos não eram confiáveis**: vinham de busca livre pelo termo, o que devolve "onde a
palavra aparece" e não "onde o assunto é ensinado" — daí faixas infladas como
`Princípio da legalidade → p6-22`, quando o conteúdo está em 2 páginas.

**Correção:** localizar o ponto pela mesma evidência estrutural do bloco (título ou primeiras
linhas da página), e rodar validação automática com três checagens — a primeira página do bloco
abre o assunto anunciado? o termo aparece com destaque na faixa? as faixas dos pontos cobrem o
bloco sem buraco nem sobreposição? O que não passar vai para revisão, **nunca entra na planilha
com número que parece certo**.

14f. **Indicação de onde começar e onde parar DENTRO da página (Elvis, 2026-08-20).** A quebra
deve cair sempre num título. E quando a página tiver **mais de um tópico**, a referência precisa
dizer o recorte: *"p12, do tópico X ao tópico Y"*. Sem isso o aluno abre a página, encontra três
assuntos e não sabe até onde é a matéria dele.

### (C) Skills pendentes de produção
Nenhuma dessas foi criada de verdade em `.claude/skills/` ainda — tudo até agora é protótipo direto na planilha "teste mapeamento de aulas" (ver [[project_projetos_planilha_mapeamento_aulas]]).

16. **mapear-assuntos-estrategia**
    Mapeamento das aulas do Estratégia (metadados por subtópico, quebra de 10-20 páginas).
17. **mapear-resumos-bezerra**
    Mapeamento dos resumos esquematizados do Bezerra + correlação com o Estratégia.
18. **mapear-assuntos-tecconcursos**
    Mapeamento de assuntos do TecConcursos (filtros, exportação, roteiro de perguntas já desenhado).
19. **criar-taxonomia-central** (nome provisório)
    Cria e atualiza a base de taxonomia central — planilha nova + geração de nomes mestres + atualização automática a cada edital processado (ver [[project_taxonomia_central_nome_mestre]]). Precisa nascer com **3 modos: criar, atualizar (preservando os Cód Mestre já atribuídos) e cascatear** a atualização pras bases dependentes; a chave de tudo é o Cód Mestre `SIGLA-NNN`, não o nome (ver [[project_taxonomia_codigo_mestre_e_atualizacao]]).
20. **gerar-cadernos-tecconcursos** (nome provisório)
    Geração dos 7 níveis de caderno do Tec (ver [[project_niveis_caderno_tec_e_pesos]]) — algoritmo de fatiar por rodada + controle externo de questões já usadas.
21. **Atualização de `baixar-curso-especifico-estrategia` e `baixar-curso-completo-estrategia`** (skills já existentes)
    (O que ajustar: hoje essas skills baixam só o **livro eletrônico** de cada aula. Precisam passar a identificar e baixar também o **PDF de resumo próprio do Estratégia** — que é um material separado, disponível na mesma plataforma, distinto do livro eletrônico e distinto do resumo do Bruno Bezerra. Serve de fallback pra quando o Bezerra não cobrir aquele trecho, ou, por padrão, pra manter os dois disponíveis — essa parte específica ainda não foi decidida, é o item 3 do bloco A.)

22. **gerar-bizurito** (nome do material fechado: **BIZURITO**) — **GERADOR JA CONSTRUIDO E
    VALIDADO em 2026-08-20**, em `bizurito/` (gerar_bizurito.py, modo_impressao.py,
    dados_bizurito.py). Briefing completo em `_contexto/briefing-bizurito.md`, com a secao 7
    listando o que a sessao de mapeamento precisa validar antes da execucao real. Falta so a
    origem real do conteudo: hoje o dicionario de entrada e escrito a mao, e passa a sair da
    planilha.
    Renderiza o **BIZURITO** por chave de taxonomia, em núcleo + blocos por banca (Cebraspe, FGV,
    FCC), a partir do banco de fichamento e
    e publica como Google Doc com link fixo de export em PDF. Anatomia, paleta por banca, redação
    do rodapé de IA, camada obrigatória de revisão de português e o teste ponta a ponta do link
    estão em [[project_bizu_revisao_por_topico]].
    **Pré-requisito de desenho (não de execução):** a aba `Pontos` precisa nascer com as colunas
    `Bizu`, `Bizu Forte` e `Letra da Lei`, preenchidas **na mesma passada do fichamento** — senão
    é reabrir ~1.100 questões depois.

23. **gerar-bizu-do-bizu** (material novo, aprovado em 2026-08-20)
    Consolidado da **disciplina inteira** por pos-edital, so com os pontos `ESSA DERRUBA`.
    Material de vespera de prova. Nele vale separar pergunta e resposta.

### Sequência de execução confirmada (linha final, nessa ordem)
1. ~~**Teste específico que Elvis vai passar**~~ — **CONCLUÍDO em 2026-08-19**: era montar a taxonomia de Direito Administrativo como aba de teste. Entregue: aba **"Taxonomia Central (DADM)"** com 137 tópicos mestres cobrindo as 18 aulas do Estratégia + 23 tópicos sinalizados como sem aula do Estratégia, e aba **"Siglas de Disciplinas"**.
2. **Refazer a Compatibilização** usando a taxonomia central como base (agora com o Cód Mestre como chave)
3. **Migrar a taxonomia de teste pra planilha própria** (a decisão original era planilha separada; o teste ficou como aba por ser teste)
4. **Validar tecnicamente a API interna do Tec**
5. Só então desenhar a **skill de cadernos do Tec** (7 níveis)

---

Checklist consolidado em 2026-08-18, a pedido de Elvis, reunindo tudo que foi decidido ao longo de uma sessão longa de prototipagem na planilha "teste mapeamento de aulas" (ver [[project_projetos_planilha_mapeamento_aulas]]). Ele pediu explicitamente que isso ficasse listado pra não se perder antes de formalizar as skills.

## Estrutura geral
1. São **3 skills separadas** (ver [[project_tres_skills_mapeamento]]): mapeamento Estratégia, mapeamento Bezerra, mapeamento TecConcursos — não uma skill só. Uma **quarta fonte, o edital**, entra futuramente como cruzamento adicional (não é uma skill de mapeamento própria, é usada depois — ver item 23).
2. **Objetivo final**: pra cada aula X do Estratégia, ter (a) as páginas do resumo Bezerra correspondente, (b) os filtros do Tec relacionados (pra montar cadernos de questões usando o banco de questões do **próprio TecConcursos**, não as questões nativas do Estratégia), e (c) quais pontos do edital aquela aula alcança e quais não alcança — pra entregar uma compatibilização completa pros alunos.
2a. **Arquitetura em 2 camadas confirmada por Elvis (2026-08-19):**
   - **Camada 1 — construída uma vez por disciplina, reaproveitável em qualquer concurso**: metadados das aulas do Estratégia, biblioteca de resumos do Bezerra, taxonomia de assuntos do Tec (genérica, sem travar em banca). É o que já foi prototipado pra Direito Administrativo (Base Estratégia, Base Resumos, Base Tec Concursos).
   - **Camada 2 — acionada a cada concurso/edital novo, descartável por concurso**: recebe o edital específico → lê banca + conteúdo programático → seleciona o filtro de banca certo no Tec pra gerar o caderno daquela aula, e aponta quais pontos do edital cada aula cobre ou não.
2b. **Banco de taxonomia por banca (tarefa futura, sugerida por Claude e aprovada por Elvis em 2026-08-19)**: as abas Cebraspe/FGV/FCC não devem ficar estáticas nos ~10-13 editais pesquisados hoje — cada edital novo processado pela Camada 2 deve **alimentar de volta** essas abas de referência, fazendo o "dicionário de nomenclatura por banca" crescer e ficar mais preciso a cada concurso processado. Isso ainda não foi implementado, é só a ideia registrada — entra na lista de melhorias a fazer depois do protótipo validado.
2c. **Escopo atual é só Direito Administrativo** (matéria de teste). Elvis confirmou que depois disso vai expandir pra outras matérias, construindo essas mesmas bases de dados (Estratégia/Bezerra/Tec/bancas) pra cada uma. O protótipo de hoje é a prova de conceito antes de escalar.

## Padrão de planilha
3. Cabeçalho sempre na linha 10, dados a partir da linha 11, linhas 1-9 livres pra design (ver [[feedback_planilha_projeto_padrao_cabecalho]]).
4. Coluna de metadados sempre identificada por fonte: "Metadados (Estratégia)", "Metadados (Bezerra)", etc — nunca "Metadados" genérico.
5. Formatação Google Sheets padrão (ver [[feedback_formatacao_padrao_google_sheets]]): alinhamento centralizado, quebra de texto, excesso de linha/coluna aparado com margem, largura de coluna ajustada ao conteúdo.
6. Sempre Google Sheets nativo (ver [[feedback_preferencia_google_sheets_sobre_excel]]), não Excel local solto — exceto uma cópia de backup do export bruto do Tec, que também deve ser salva na pasta local.

## Metadados e compatibilização
6b. **Ser cirúrgico nas faixas de página citadas na compatibilização, não arredondar pra um range largo** (confirmado em 2026-08-19, caso real: item 4 do edital TCDF/Agentes Públicos citou "R15 (p35-61)" quando o subtópico específico de sindicância/PAD é só p58-61 — a faixa larga misturava licenças/afastamentos, que não é o que o item pedia). Regra: quando um item cita um subtópico específico (ex: "sindicância e processo administrativo disciplinar"), citar a faixa de página exata daquele subtópico nos metadados de origem, não um intervalo amplo que "também contém" o trecho certo. Se o item do edital cobrir vários subtópicos da mesma fonte, listar cada faixa separadamente com o rótulo do subtópico (ex: "R15 (p19-21 vacância; p24-32 remuneração; p47-57 regime disciplinar; p58-61 sindicância/PAD)"), em vez de um único range genérico.
6a. **Peso bruto do Tec pode enganar quando a base mistura matéria Municipal/Estadual com Federal** (confirmado em 2026-08-19 checando a Aula 13/Agentes Públicos): quando a seleção de matérias do Tec inclui "Direito Administrativo Municipal" (ou Estadual), os assuntos de maior peso tendem a ser conteúdo de estatutos locais específicos (cada prefeitura/estado tem sua própria lei), que não têm correspondência real com uma aula de curso genérico/federal — mesmo aparecendo com peso alto (ex: 7,40%) só por coincidência de tema genérico ("servidor", "agente público"). Regra: **sempre priorizar a âncora legal batendo com o conteúdo real da aula sobre o peso bruto** — um assunto de 0,16% com "Lei nº 8.112/1990" no nome vale mais como match do que um de 7,40% "(Servidores Municipais)" sem relação nenhuma com a lei federal tratada na aula. Vale considerar, ao configurar uma skill de mapeamento Tec futura, se compensa restringir a matéria só à "(Doutrina e Leis Federais)" quando o curso de referência for federal/genérico, em vez de somar as 3 matérias (Federal+Estadual+Municipal) — depende do objetivo de cada mapeamento.
7. Metadados quebrados por **subtópico real** (não a aula inteira), granularidade "dá pra estudar de uma vez" — nem bloco gigante, nem fatiado artificialmente (ver [[feedback_planilha_metadados_nucleo_secundario]]).
8. Âncora legal (artigo/lei/súmula) sempre como critério de match **forte** entre fontes; nome/tema parecido como critério **fraco**.
9. **Numeração nunca é chave de match** entre fontes — confirmado com exemplos reais (Aula 05 do Estratégia = "Poderes e Deveres", mas R05 do Bezerra = "Atos Administrativos"; a numeração diverge).
10. "Sem correspondência" é informação legítima (gap real de conteúdo entre fontes, ex: Lei 8.112 detalhada só no Bezerra), não é erro de cruzamento — registrar como está, não forçar match.
11. Cada assunto do Tec pertence a **uma única aula** do Estratégia (a de match mais forte) — regra necessária pra poder calcular peso por aula sem duplicar contagem.
12. Calcular o **peso % de cada aula do Estratégia** = soma dos pesos (% do Tec) dos assuntos atribuídos a ela + reportar separadamente o "% sem correspondência no Estratégia" (os pesos por aula não têm por que somar 100%).

## Contagem de questões (PDFs de aula do Estratégia)
13. Questão anulada conta normalmente. Questão duplicada (aparece comentada E na lista do mesmo tópico/banca) conta uma vez só. Questão inédita/complementar soma ao total (ver [[feedback_contagem_questoes_pdf_aulas]]).

## Roteiro fixo da skill do TecConcursos
13a. **Manual completo do TecConcursos (levantamento profundo de outra sessão, 2026-08-19)**: ver [[reference_tecconcursos_manual_completo]] (mora em `_contexto/tecconcursos.md`, colável em qualquer projeto) + [[feedback_tec_serie_nao_serve_plano_estudo]] + [[feedback_tec_filtro_sem_memoria]]. Achados que mudam o desenho da skill de cadernos: existe filtro por URL e API interna (`/api/assuntos?materia={id}&hierarquico=true`, dispensa clicar na árvore); "Adicionar questões por código" é a rota certa pra injetar seleção nossa num caderno; "Gerar cadernos em série" **não serve pra plano de estudo** (distribui por frequência histórica do banco, não pelo edital — testado: um assunto come 25% do caderno e a maioria fica zerada); o filtro do Tec **não tem memória** (mesmo filtro + Mais Recentes = sempre as mesmas questões) — o controle de "o que já foi usado em qual caderno" tem que ser nosso, numa planilha externa com os `#` das questões. Ler o manual completo antes de desenhar a skill de montagem de cadernos.
14. Pergunta obrigatória no início, nesta ordem: **disciplina** → **ano** (padrão sugerido: últimos 10 anos) → **banca** (padrão sugerido: todas; alternativa: combo Cebraspe+FCC+FGV) → **área** (padrão sugerido: Fiscal ou Gestão e Controle — avisando que "Gestão e Controle" se subdivide em Tribunais de Contas/Controladorias/Gestão) (ver [[feedback_skill_tec_filtros_padrao]]).
15. Sempre registrar explicitamente a área usada na planilha de saída (a área impacta a base de dados inteira).
16. Sempre remover questões anuladas + desatualizadas, automático, sem perguntar (regra fixa, não filtro opcional).
17. Separar as fontes do Tec por banca ainda é uma pendência a resolver (FGV, FCC, Cebraspe, extensível pra outras).
18. Exportação sempre com **"Organizar por: Relevância (apenas assuntos)"** — nunca "Hierarquia" (ver [[feedback_tec_organizar_por_relevancia]]).
19. Exportação sempre com **"Popular com questões: Mais Recentes"** — nunca "Aleatórias".
20. Bizus de automação do navegador do Tec (ver [[feedback_tec_navegador_bizus]]): recarregar a página se a árvore de seleção bagunçar (não tentar consertar em cima); clicar por `ref` do `read_page`, não por coordenada de pixel; cuidado com `get_page_text` — ele prioriza uma questão de amostra em vez do painel de filtros nessa página.

## Pendências de análise ainda não fechadas
21. Investigar os 26 casos "sem correspondência" da aba "Compatibilização DADM" — confirmar se são todos gaps legítimos (maioria vem do R15/Bezerra, Lei 8.112 detalhada artigo por artigo) ou se algum é falso negativo do cruzamento automático.
23. **Quarta fonte de dados: o edital** (anunciado 2026-08-19, ainda não iniciado). Assim que sair um edital novo, ele vira uma quarta fonte pra cruzar com Estratégia/Bezerra/Tec — pra cada aula do Estratégia, saber quais pontos do conteúdo programático do edital ela cobre e quais não cobre. Antes disso, Elvis vai **adicionar editais de referência de algumas das principais bancas** (com a parte de conteúdo programático) só pra eu entender como cada banca nomeia os tópicos — isso ainda não é o cruzamento real com um edital específico de concurso, é material de referência de nomenclatura por banca. Ainda não foi definido onde esses editais de referência vão ficar salvos nem o formato de extração — só a intenção foi registrada.

## Estratégia de peso por banca + geração de cadernos proporcionais em rodadas (proposta em 2026-08-19, aprovada por Elvis, ainda a amadurecer)

**Problema 1 — peso por assunto quando a banca específica tem poucas/nenhuma questão:**
- O peso calculado hoje (ex: aba "Compatibilização") usa o Tec **geral** (todas as bancas, área Fiscal) — não é o ideal pra montar caderno de um concurso real, porque quem escreve a prova é a banca específica daquele edital.
- Regra híbrida proposta: se o assunto tiver volume mínimo de questões daquela banca (piso sugerido: ~15-20 questões pra confiar no %), usa o **peso específico da banca**. Abaixo do piso ou zerado, cai pro peso geral da área como estimativa, **marcado explicitamente como "peso estimado (poucas questões da banca)"** — nunca disfarçar de número sólido.
- Assunto do edital com zero questões daquela banca **não é motivo pra excluir do caderno** — é informação (tópico que ainda não caiu, ou banca realmente não cobra). Garantir ao menos 1 questão de reserva (outra banca, com aviso) em vez de fingir que o assunto não existe.

**Problema 2 — gerar cadernos proporcionais ao peso, em várias rodadas sem repetir questão:**
- Limitação de base já confirmada (ver [[feedback_tec_filtro_sem_memoria]], [[feedback_tec_serie_nao_serve_plano_estudo]]): o filtro do Tec não tem memória (mesmo filtro + Mais Recentes = sempre as mesmas questões), e "Gerar cadernos em série" distribui por frequência histórica do banco, não pelo peso que a gente quer.
- Algoritmo proposto:
  1. Pra cada assunto do Tec ligado à aula, puxar a lista completa de IDs de questão (via API interna, ordenado por Mais Recentes).
  2. Calcular quantas questões por rodada cada assunto tem direito: peso% × tamanho do caderno, arredondado, com **piso 1** (nenhum assunto zera).
  3. **Fatiar** a lista de IDs de cada assunto em blocos do tamanho calculado — bloco 1 vai pro caderno/rodada 1, bloco 2 pra rodada 2, etc. Isso evita repetição naturalmente.
  4. Montar cada caderno via **"Adicionar questões por código"** (não via filtro clicado na hora — é a rota que sobrevive a fechar o navegador).
  5. Guardar o controle numa planilha própria (aula → assunto → quais IDs já foram usados em qual rodada).
  6. O número máximo de rodadas possíveis é limitado pelo assunto **mais escasso** (esgota primeiro) — quando ele acabar, ou aceita ficar sem esse assunto nas rodadas seguintes, ou reduz o tamanho do caderno pra esticar mais rodadas.

**Status:** ideia aprovada por Elvis em 2026-08-19, ainda não implementada — ele vai continuar acrescentando/amadurecendo essa estratégia nas próximas mensagens antes de qualquer execução. Não implementar até ele sinalizar que quer rodar de verdade.

## Último item (deixado por último a pedido do Elvis)
22. **Avaliar/executar a estratégia de compatibilização 3 vias (Estratégia ↔ Tec ↔ Bezerra) + cálculo de peso por aula** — combinada em 2026-08-18 mas ainda não executada: montar de novo uma tabela de compatibilização (match por âncora legal, com atribuição única de cada assunto do Tec à aula de match mais forte) e gerar uma tabela/aba de "Peso por Aula" (soma dos pesos do Tec por aula + % sem correspondência). **Atenção:** a aba "Compatibilização DADM" (que já tinha o cruzamento Estratégia↔Bezerra pronto, 155 linhas) foi apagada em 2026-08-19 a pedido do Elvis pra simplificar a planilha em 3 abas (Base Estratégia, Base Resumos, Base Tec Concursos) — esse cruzamento precisa ser refeito do zero quando for a hora de executar este item.

**Why:** sessão longa com muitas decisões incrementais — sem esse checklist consolidado, é fácil esquecer algum critério na hora de formalizar as 3 skills de verdade.

**How to apply:** ao retomar a conversa sobre a skill de mapeamento de aulas, e especialmente quando Elvis pedir pra criar a(s) skill(s) de verdade, percorrer esse checklist item por item e confirmar com ele que cada ponto foi endereçado antes de considerar a skill pronta. Ir riscando/atualizando os itens conforme forem resolvidos.
