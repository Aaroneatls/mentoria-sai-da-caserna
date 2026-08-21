---
name: project-taxonomia-central-nome-mestre
description: "Proposta de tabela central de nomenclatura própria (\"nome mestre\" por tópico) ligando Estratégia, Bezerra, Tec e Edital numa única linha — proposta por Elvis em 2026-08-19"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T18:02:45.510Z
---

Proposta de Elvis em 2026-08-19 (ver [[project_skill_mapeamento_aulas_pendencias]] pro checklist geral), ainda não implementada.

## A ideia

Em vez de só cruzar as fontes par a par (Estratégia↔Bezerra, Estratégia↔Tec, etc., como vinha sendo feito até aqui), criar uma **tabela central de nomenclatura própria** — um "nome mestre" por tópico, que funciona como chave de ligação entre TODAS as fontes ao mesmo tempo.

Exemplo dado por Elvis: o tópico mestre **"Inexigibilidade e Dispensa de Licitação"** teria, numa linha só:
- **Tec:** o assunto que cita a lei/artigo correspondente (ex: "Contratação Direta, Inexigibilidade e Dispensa - arts. 72 a 75 da Lei 14.133/2021")
- **Estratégia:** "Parte 2 da Aula de Licitações e Contratos" (ou o nome/página real do subtópico mapeado)
- **Bezerra:** o subtópico do resumo que trata do mesmo assunto (nome + página)
- **Edital:** o item/subitem correspondente do conteúdo programático

Ou seja, essa base de nomes próprios vira o **vocabulário oficial** usado pra nomear os tópicos de estudo — cada fonte só "aponta" pra esse nome central, em vez de a gente ficar traduzindo nomenclatura toda vez que cruza duas fontes diretamente.

## Por que isso muda o desenho atual

Até 2026-08-19, o cruzamento era feito como tabelas de compatibilização par a par (ex: aba "Compatibilização" ligando Estratégia→Bezerra→Tec→bancas numa linha por aula, e aba "Compatibilização TCDF 2026" ligando edital→Estratégia→Bezerra numa linha por item de edital). A proposta do nome mestre sugere uma **camada acima dessas**: um dicionário central onde CADA linha é um tópico único e todas as fontes apontam pra ele, em vez de múltiplas tabelas de cruzamento bilateral se sobrepondo.

## Decisões (confirmadas por Elvis em 2026-08-19)

1. **Quem cria os nomes mestres:** Claude cria autonomamente, **sem precisar de aprovação prévia** a cada nome — Elvis vai revisar ao final, mas não é um loop de aprovação item a item.
2. **Critério de nomeação:** buscar um nome próximo ao que já é usado tanto no **Tec** quanto no **Estratégia** — mas no Estratégia, usar os **tópicos que aparecem ao longo do corpo da aula** (os subtítulos internos do PDF, que é basicamente o que já vira o "Metadados (Estratégia)" por subtópico), **não o tópico do sumário/índice geral** (que é mais genérico/alto nível).
3. **Onde vive:** uma **planilha nova, separada**, dedicada só à taxonomia central — não é uma aba dentro da planilha de protótipo. Ela é a **base geral/mestra**, alimentada pelas outras bases (Estratégia, Bezerra, Tec, editais), mas funciona de forma independente: mesmo que Elvis carregue um curso específico (de um concurso) ou o curso genérico "Regular", ambos devem **puxar dessa mesma base de taxonomia central**, não criar taxonomia própria isolada.
3a. **Relação com as tabelas de compatibilização existentes:** a taxonomia central é o **dicionário central**; as abas de compatibilização (ex: "Compatibilização", "Compatibilização TCDF 2026") passam a ser **relatórios derivados dela**, não bases independentes. Confirmado por Elvis em 2026-08-19.
4. **Atualização contínua:** toda vez que uma skill rodar a inclusão/processamento de um **pós-edital** (edital real de um concurso), essa execução deve **alimentar de volta a base de taxonomia central** com os tópicos novos identificados. Isso é uma regra permanente de qualquer skill futura que processe edital — **guardar isso como requisito de design, não só como nota**.

## Sequência de execução confirmada (2026-08-19)

Elvis confirmou a ordem proposta por Claude: (1) fechar o desenho da taxonomia central, (2) refazer a Compatibilização usando esse formato novo, (3) só então desenhar a skill de cadernos do Tec com os 7 níveis. **Escopo confirmado: só Direito Administrativo por enquanto.** **Validação técnica da API interna do Tec confirmada: pode ser feita.** Antes de seguir com essa sequência, porém, Elvis vai passar **um teste específico pra executar primeiro** — aguardando o teste chegar (ainda não descrito em 2026-08-19).

## Nova tarefa registrada (2026-08-19)

Criar a **base de taxonomia central** (planilha nova) e a **skill de criar/atualizar essa base** entram formalmente na lista de tarefas do projeto. Parte dessa tarefa envolve fazer um **levantamento mais completo de editais** do que o já feito até agora (que foi só uma amostra de ~10-13 editais por banca, ver abas Cebraspe/FGV/FCC da planilha "teste mapeamento de aulas") — a base de taxonomia precisa de uma cobertura maior de editais pra ficar robusta.

**Why:** o objetivo é ter um vocabulário único de referência que sirva de espinha dorsal pra montar os tópicos de aula/estudo que vão ser usados de fato — em vez de nomenclatura fragmentada por fonte, e reaproveitável entre qualquer curso (específico ou genérico) que Elvis carregar.

**How to apply:** ao formalizar as skills, incluir a criação/atualização da base de taxonomia central como uma delas (ou uma sub-rotina chamada pelas outras). Toda skill que processa edital deve terminar alimentando essa base de volta. Ver também [[project_niveis_caderno_tec_e_pesos]] pra entender como os cadernos de questão vão consumir esses tópicos, e o ponto de "sinalização de gaps" abaixo.

## Sinalização de gaps (relacionado, mesma mensagem de Elvis)

Vai existir situação em que **não existe aula do Estratégia nem resumo do Bezerra** pra um assunto do edital, mas **existem questões do Tec** tratando dele. Nesses casos, usar as questões do Tec mesmo assim — mas isso precisa ficar **visualmente apontado pro Elvis**, pra ele identificar esse buraco de conteúdo e decidir criar uma aula específica pra cobrir ele. Isso é uma consequência direta de ter a taxonomia central: ela é o lugar natural pra essa sinalização aparecer (uma linha de tópico mestre com Tec preenchido mas Estratégia/Bezerra vazios = gap de conteúdo pra Elvis avaliar).
