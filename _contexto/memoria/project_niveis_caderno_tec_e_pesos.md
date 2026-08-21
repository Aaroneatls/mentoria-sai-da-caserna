---
name: project-niveis-caderno-tec-e-pesos
description: "Os 7 níveis de caderno de questões do Tec (definição, escopo, tamanho pré/pós-edital), metodologia de amostra/peso por banca e Curva ABC — definidos por Elvis em 2026-08-19"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T19:30:16.853Z
---

Metodologia completa definida por Elvis em 2026-08-19 (sessão de prototipagem da skill de mapeamento, ver [[project_skill_mapeamento_aulas_pendencias]]). Ainda não implementada — são as regras de negócio pra quando a skill de montagem de cadernos do TecConcursos for construída de verdade.

## Os 7 níveis de caderno de questões

Cada nível usa o mecanismo técnico já mapeado (ver item 13a de [[project_skill_mapeamento_aulas_pendencias]]): puxar lista de IDs por assunto via API interna do Tec, fatiar em blocos por rodada, injetar via "Adicionar questões por código", controle externo numa planilha nossa (nunca confiar no Tec pra evitar repetição).

| Nível | Nome | Escopo | Qtd pré-edital | Qtd pós-edital |
|---|---|---|---|---|
| 1 | **Caderno de Fixação por Tópico** | uma parte/subtópico da aula | ~1 questão/página, mín. 10, entre 10-20 | mantém |
| 2 | **Caderno de Fixação por Assunto/Aula** | aula inteira | até 30 | mantém |
| 3 | **Caderno de Simulado por Bloco de Assunto** | bloco de ~4 aulas (flexível) | até 40 | reduz pra até 30 |
| 4 | **Caderno Simulado por Bloco Acumulado** | blocos anteriores somados (sequencial) | até 40 | reduz pra até 30 |
| 5 | **Caderno de Revisão da Matéria** | disciplina inteira, vários cadernos | até 30 por caderno (vários cadernos, total acumulado bom) | varia 10-40 conforme peso da disciplina no edital — **definido a posteriori na skill de pós-edital** |
| 6 | **Caderno Ouro por Aula** | aula | sem mínimo, até ~10 | mantém |
| 7 | **Caderno Ouro por Disciplina** | disciplina inteira | ~10/aula, compensando entre aulas | mantém |

**Regra geral de teto:** nenhum caderno passa de **40 questões**, EXCETO o Ouro por Disciplina (nível 7), que é o único isento desse teto. Se algum cálculo ultrapassar 40, quebra em mais cadernos em vez de estourar.

### REFINAMENTO CRÍTICO DO DIMENSIONAMENTO (Elvis, 2026-08-19) — vale sobre a tabela acima

O tamanho do caderno **não é definido pela contagem de páginas**, e sim pelo **número de
pontos distintos que têm questão disponível**. A página vira referência de esforço de leitura
e teto de sanidade, não meta.

Os dois casos que Elvis usou pra explicar:
- **10 páginas de teoria, mas só 5 questões no banco e todas cobrando o mesmo ponto** → o
  caderno certo tem **1 ou 2 questões**, não 10. Repetir o mesmo ponto não ensina nada.
- **5 páginas de teoria, mas 15 questões abordando aspectos genuinamente distintos** → o
  caderno **pode passar** das 5, porque cada questão agrega conteúdo novo.

**Regra nova:** 1 questão por ponto distinto coberto. O piso de 10 do Nível 1 **deixa de ser
rígido** — caderno com 4 questões que cobrem 4 pontos distintos está correto, não é falha de
banco. Os tetos continuam valendo (20 no Nível 1, 40 geral, Nível 7 isento); quando os pontos
distintos passam do teto, **quebra em mais de um caderno** do mesmo nível.

A granularidade do "ponto distinto" é a mesma já definida na seção de granularidade máxima
(cada princípio do LIMPE é um ponto separado). É ela que determina tudo — sem granularidade
consistente, o dimensionamento não fecha.

**Consequência retroativa:** os cadernos do teste de 2026-08-19 sinalizados como "abaixo do
mínimo" (DADM-003 com 3, DADM-009 com 6) podem estar **corretos** — depende de quantos pontos
distintos essas questões cobrem. A sinalização só pode ser confirmada depois do fichamento.

**Duas métricas novas que caem desse raciocínio:**
- **Densidade de pontos por página** — muitos pontos em poucas páginas = assunto de cobrança
  concentrada, candidato forte a Curva A mesmo com peso bruto baixo (substitui com vantagem o
  critério de "densidade de questões por página" que estava proposto).
- **Página com conteúdo e sem questão** = gap de banco: o aluno estuda e não tem como
  praticar. Mesma família dos gaps da taxonomia, tem que ser sinalizado ao Elvis.

### Questão que serve a mais de um tópico mestre (Elvis, 2026-08-19)

1. **Regra geral:** a questão vai pro tópico **que faz mais sentido / mais abrangente** —
   aquele cuja teoria realmente sustenta a resolução. Nos demais tópicos ela fica registrada
   como **secundária**, disponível pros níveis de bloco (3 e 4).
2. **Exceção de escassez:** quando a ligação com dois tópicos **não é clara** e um deles tem
   **poucas ou nenhuma questão**, pode **repetir a mesma questão** nos dois cadernos, sem
   problema. Elvis foi explícito: nesse caso a repetição é aceitável.

Isso torna a **injeção por código** ainda mais necessária: a plataforma deduplica sozinha
(ver [[project_tec_gerador_nao_repete_questao]]), então forçar a repetição deliberada
provavelmente só é possível pela rota de "Adicionar questões por código".

Alvos imediatos dessa exceção no teste de 2026-08-19: DADM-003 (3 questões) e DADM-009 (6).

### Detalhe de cada nível

- **Nível 1 (Fixação por Tópico):** pra cada parte da aula (ex: "Princípios" Parte 1 = 10pg, Parte 2 = 15pg), monta caderno só com questões **resolvíveis pelo que foi visto naquela parte específica** — não precisa ser 100% resolvível questão a questão, mas não pode estar fora do escopo. Prioriza cobertura de tópico (uma questão por subtópico) sobre volume. Duas questões do mesmo assunto com resolução/abordagem diferente podem entrar; com resolução idêntica, não.
- **Nível 2 (Fixação por Assunto/Aula):** complementar ao 1, pro aluno fazer alguns dias depois. Pode abranger a aula inteira (várias partes juntas). Evita repetir a mesma questão do Nível 1 — se havia mais de uma opção parecida, usa alternativa; se só existe uma no banco, repete.
- **Nível 3 (Simulado por Bloco):** mistura questões das ~4 aulas do bloco, maximizando cobertura. Mesma lógica de reaproveitamento do nível 2 (repete só se não houver alternativa).
- **Nível 4 (Acumulado):** depois do bloco 2 → acumulado(1+2). Depois do bloco 3 → acumulado(1+2+3). E assim sucessivamente, sempre antes de começar as aulas do próximo bloco. Maximiza cobertura no escopo acumulado; repetição aceita quando inevitável.
- **Nível 5 (Revisão da Matéria):** depois de estudar toda a matéria. Distribuição proporcional por peso (~1 questão por aula, aulas de peso maior ganham 2) — usa exatamente a lógica de peso% × tamanho do caderno já desenhada em [[project_skill_mapeamento_aulas_pendencias]] (seção "Estratégia de peso... geração de cadernos proporcionais").
- **Níveis 6 e 7 (Ouro):** "questão ouro" = questão que (a) representa um padrão/lógica que se repete com frequência no banco, ou (b) é bem completa, revisando vários assuntos numa só questão (principalmente pela resolução). Nível 6 = por aula; Nível 7 = disciplina inteira.

### Regra de granularidade máxima na seleção (vale pra todos os níveis)

Sempre considerar o tópico no **nível mais aprofundado possível**. Exemplo: dentro de "Princípios da Administração" (LIMPE), cada princípio (legalidade, impessoalidade, moralidade, publicidade, eficiência) é um tópico **distinto**, não um bloco só.
- Questão que trata **só de um** princípio isoladamente → cobre só aquele tópico, precisa de outra pra cobrir o próximo.
- Questão que **mistura/trata vários** juntos → conta como cobertura simultânea de todos.

### Registro técnico obrigatório

Ao selecionar questão do Tec, guardar **número (#) + ano** (não só o #) — pra sempre identificar a questão e conseguir priorizar as mais recentes.

## Metodologia de amostra e peso por banca/área

**Meta de referência:** ~1.000 questões por disciplina (estimativa, pode variar — se muito discrepante, perguntar na hora de executar).

**Algoritmo de coleta — REVISADO por Elvis em 2026-08-19 (substitui a regra anterior):**

Fichar **todas** as questões da janela de **10 anos**, sempre. A janela é fixa; a meta de
~1.000 deixa de ser critério de parada e passa a ser **piso de suficiência**:

- Se os 10 anos renderem **1.000 ou mais**, ficha tudo e para por aí — não interessa passar
  muito da meta, o que interessa é a janela estar fechada.
- Se renderem **menos de 1.000**, aí sim entram os critérios de expansão (outras bancas na
  ordem da área e, em último caso e só com confirmação do Elvis, área correlata).

Na **montagem do caderno**, sempre priorizar as **mais recentes** dentro do que foi fichado.

*(Regra anterior, agora descartada: regredir ano a ano parando assim que atingisse 1.000.
Problema dela: parava no meio de um ano, deixando a janela com um ano parcial e enviesando
qualquer estatística de peso calculada em cima. E, como o fichamento é base permanente
reutilizada pelos 7 níveis, fichar a janela inteira é feito uma vez e serve pra tudo.)*

**Escopo de banca:**
- **Pré-edital:** conjunto das bancas (FCC+Cebraspe+FGV), dentro da **área específica** (Fiscal ou Controle), até 10 anos.
- **Pós-edital:** primeiro só a **banca específica** do edital, até 10 anos. Insuficiente → complementa com as outras bancas (mesma área). Ainda insuficiente → pode cruzar pra área correlata (Fiscal ↔ Controle/Tribunais de Contas/Controladorias), **mas só confirmando com Elvis na hora de executar**, nunca automático.

**Peculiaridade Cebraspe:** ao complementar com Cebraspe, priorizar primeiro as questões **Certo/Errado**; só se insuficiente, entra com **múltipla escolha** da própria Cebraspe; só depois disso entra outra banca.

**Ênfase por área (peso de referência quando não há banca específica ainda definida):**
- Área **Fiscal** → maior ênfase em **FCC e Cebraspe**.
- Área **Controle** (Tribunais de Contas) → maior ênfase em **Cebraspe e FGV**.

**Ordem de fallback de banca no PÓS-EDITAL (acrescentado por Elvis em 2026-08-19 — detalha o "complementa com as outras bancas" do item acima, não substitui nada):**

Parte da banca do edital. Se ela não fechar o parâmetro (~1.000 questões em até 10 anos), complementa na ordem abaixo, conforme a área. Quando a banca do edital é a **Cebraspe**:

- Área **Controle** (Controladorias e Tribunais de Contas): **Cebraspe → FGV → FCC**
- Área **Fiscal**: **Cebraspe → FCC → FGV**

Ou seja: quem entra depois da Cebraspe é o que muda entre as duas áreas. No Controle o segundo é a FGV; no Fiscal o segundo é a FCC.

**Nota sobre a área no Tec:** o que o Tec chama de "Gestão e Controle" é mais amplo do que a área de Controle que interessa aqui. Dentro dela, selecionar especificamente **Controladorias e Tribunais de Contas**.

**Aceite final:** vai ter assunto que nunca vai ter boa estatística — usa o que tem e sinaliza isso explicitamente na hora da execução.

## Classificação Curva ABC

- **Curva A** = partes/subtópicos que juntos somam **~80%** do peso acumulado.
- **Curva B** = de **81% a 90%** do peso acumulado.
- **Curva C** = os **10% finais** (91-100%).

**Refinamento crítico:** a classificação **NÃO é feita no nível da aula inteira** — uma aula de peso alto mas muito extensa (ex: Licitações e Contratos) não vira Curva A por inteiro só por isso. A classificação é feita **por parte/subtópico** (mesma quebra granular de 10-20 páginas já estabelecida) — dentro de uma mesma aula extensa, algumas partes podem cair em A, outras em B ou C.

**Critérios além do peso% puro** (peso puro pode enganar quando a aula é muito grande — baixo custo-benefício — ou quando é bem curta com peso pequeno mas questões suficientes — vira A mesmo com peso baixo):
- **Razão peso/página** — peso% dividido pelas páginas de teoria do subtópico (custo-benefício formalizado).
- **Densidade de questões por página** — questões do Tec disponíveis / páginas (mede material de prática disponível por esforço de leitura).
- **Clareza no edital** — assunto citado explicitamente no edital vs. correspondência frágil/inferida (correspondência fraca reduz a confiança, deveria puxar pra baixo mesmo com peso ok).
- **Teto de páginas pra Curva A** — mesmo com peso e razão boas, subtópico enorme pode não caber no tempo do aluno.
- **Tendência recente** — assunto subindo ou caindo nos últimos 2-3 anos, não só peso histórico total.
- **Confiança da amostra** — amostra pequena marca incerteza separada, não necessariamente rebaixa a curva.

Esses critérios extras foram propostos por Claude a pedido de Elvis ("pense em outros critérios") — ainda não confirmados/priorizados por ele, ficam como sugestão registrada.

**Ordem de estudo (pré-edital):** prioriza peso/curva, mas respeita **pré-requisito didático/lógico** sobre a ordem que o Estratégia usa (ex: não estuda equação de 2º grau antes da de 1º grau, mesmo que a aula-base tenha peso baixo) — não necessariamente segue a ordem do curso original.

**Why:** Elvis está desenhando isso com muito detalhe porque o objetivo final é gerar planos de estudo pré e pós-edital de verdade pros alunos, usando o banco de questões do Tec de forma dirigida (não aleatória, não "em série") — precisão nessas regras de negócio é o que diferencia um plano de estudo bem feito de um genérico.

**How to apply:** ao desenhar a skill de montagem de cadernos do TecConcursos, seguir essa tabela e essas regras à risca. Nada disso foi implementado ainda em 2026-08-19 — é specification pra quando Elvis sinalizar que quer rodar de verdade.
