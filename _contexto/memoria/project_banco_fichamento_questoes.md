---
name: project-banco-fichamento-questoes
description: "Banco de fichamento de questões do Tec: camada de 'ponto' abaixo do tópico mestre, com 3 abas (Pontos, Questões Fichadas, Questão x Ponto) — desenhado e prototipado em 2026-08-19"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T20:35:28.072Z
---

Desenhado com Elvis em 2026-08-19, depois que o teste do Nível 1 revelou dois furos no método
de montar caderno filtrando por assunto do Tec.

## O problema que originou

1. Pegar as N questões mais recentes de um assunto traz **redundantes** — duas questões
   cobrando o mesmo ponto, com a mesma resolução.
2. O assunto do Tec é **mais grosso** que o tópico mestre, então a questão pode exigir
   conteúdo que a aula do Estratégia e o resumo do Bezerra não ensinam.

Prova concreta: no balde do assunto 497, **3 das 16 questões não pertenciam ao DADM-001**, e
o caderno do DADM-002 tinha **5 das 6 questões de outros tópicos**.

## A solução: a camada de "ponto"

```
Disciplina → Tópico Mestre (DADM-001) → Ponto (DADM-001.P05) → Questões
```

O **ponto** é a unidade indivisível de conteúdo cobrado. É ele, e não o tópico, que define:
- **redundância** = duas questões no mesmo ponto
- **cobertura** = ter questão em cada ponto
- **tamanho do caderno** = nº de pontos com questão disponível

Código do ponto: `<CÓD MESTRE>.P<NN>` (ex.: `DADM-001.P05`). Formato aprovado por Elvis.

## Como se ficha

Puxar da API do Tec **enunciado, alternativas e a resolução do professor**
(`/api/questoes/{id}/comentario`) e extrair: âncoras legais, instituto e a **lista de pontos**
que a questão cobra. Uma questão cobre **vários** pontos — múltipla escolha costuma cobrar um
ponto por alternativa.

## Estrutura (3 abas, na planilha "teste mapeamento de aulas" por decisão de Elvis)

1. **Pontos (DADM)** — dicionário: `Cód do Ponto · Cód Mestre · Nome · Âncora · Onde está no
   Estratégia · Onde está no Bezerra · Nº de Questões · Cobertura pela Teoria`. As duas colunas
   de "onde está" são o que responde se a questão é resolvível com o que foi ensinado.
2. **Questões Fichadas** — uma linha por questão: `# · Ano · Banca · Órgão · Cargo · Tipo ·
   Assunto no Tec · Pontos Testados · Cód Mestre Principal · Secundários · Status · Caderno ·
   Nota`. Status: `usada` / `reserva` / `fora de escopo`.
3. **Questão x Ponto** — uma linha por par. É a que permite contar certo, já que a relação é
   muitos-para-muitos.

## Granularidade da extração dos PDFs e o veredito de cobertura

Discutido com Elvis em 2026-08-19.

**A questão não é "abrir ou não o PDF" — é abrir uma vez por aula em vez de uma vez por
questão.** Com extração rasa (só o nome do subtópico), cada questão exige voltar ao PDF: o
subtópico do DADM-001 tem 16 candidatas, logo 16 leituras do mesmo trecho. Com extração
granular, lê-se uma vez e a checagem de cada questão vira consulta à base.

E o custo marginal é baixo **se for feito na mesma passada** que produz os pontos — o PDF já vai
estar aberto e o texto em mãos pra decidir onde quebrar o subtópico. Adiar significa reabrir tudo.

**O que extrair:** não basta nome de tópico. Guardar as **proposições que a aula ensina** —
prazos, requisitos, exceções, súmulas e artigos citados, números. "Cobre prescrição na
improbidade" não responde se a questão sobre o prazo de 8 anos é resolvível; "ensina que o prazo
é de 8 anos" responde.

**Assimetria de custo:** a aula de Agentes Públicos do Estratégia tem 172 páginas; o resumo
equivalente do Bezerra tem 39. Extrair fundo do Bezerra é barato porque ele já é condensado.
Então: **extração profunda no Bezerra**; no Estratégia, nível de ponto + âncora legal,
aprofundando só onde a checagem der ambígua.

### REGRA DURA: nunca inferir cobertura do Estratégia a partir do Bezerra (Elvis, 2026-08-19)

O Bezerra pode trazer **conteúdo a mais** que o Estratégia não tem, e pode **deixar de fora**
coisa que o Estratégia ensina. São materiais **independentes**.

Portanto o **veredito de cobertura é apurado em cada fonte separadamente**, e as colunas "Onde
está no Estratégia" e "Onde está no Bezerra" nunca se deduzem uma da outra. O Bezerra serve pra
**priorizar o esforço de extração**, jamais pra concluir que o Estratégia cobre algo.

É isso que sustenta os três destinos da questão: coberto pelo Estratégia → caderno normal;
coberto **só** pelo Bezerra → caderno complementar; nenhum dos dois → fora, e sinaliza gap.

### O metadado atual CONFIRMA cobertura, mas não serve pra NEGAR

Descoberto ao aplicar o método nas 16 questões do DADM-001 (2026-08-19).

O formato atual (`[p3-12] Nome do subtópico: âncoras legais; institutos`) é um **resumo**.
Quando o instituto está listado, a confirmação é confiável. Quando **não está**, não dá pra
concluir nada — ausência num resumo não é ausência no PDF.

**Consequência real:** duas questões foram removidas do caderno DADM-001 com base numa
ausência — a de *escolas de conceituação* e a de *objeto do direito administrativo*.
**Precisam ser reavaliadas** quando a taxonomia for refeita com metadado exaustivo.

**Correção a aplicar na refação da taxonomia (curso de Controle), na mesma passada:**
1. **Campo de exaustividade** por subtópico: a lista de institutos é **completa** ou
   **ilustrativa**? Um campo só, e resolve a assimetria — se completa, ausência = não coberto;
   se ilustrativa, ausência = indeterminado, e a questão entra como **parcial** em vez de ser
   descartada.
2. **Lista completa de institutos** onde a extração for exaustiva, no lugar da amostra atual.

Não fazer isso "conforme a necessidade": se toda negativa exigir reabrir o PDF, a checagem
deixa de ser consulta e vira leitura — exatamente o que o fichamento existe pra evitar.

### Caso residual

Quando o ponto está coberto mas a afirmação específica não aparece no que foi extraído: vale a
regra do Nível 1 — a questão **não precisa ser 100% resolvível**, só não pode estar fora do
escopo. Marca como **parcial** e entra. Reabrir o PDF só quando Elvis contestar um caso concreto.

## Etapa de repescagem por enunciado (parte do fluxo, ainda não executada)

O fichamento lê tudo que está **no balde do assunto** — e é **cego pro que está fora dele**:
questão mal classificada, sem classificação, ou num assunto que o tópico mestre não mapeia.

**Regra:** para **pontos abaixo do mínimo de questões**, antes de declarar escassez, rodar uma
**busca por enunciado usando o nome do INSTITUTO** (não o nome do tópico) e mandar os candidatos
pro fichamento, que decide o que presta. Só nos pontos escassos, pra não multiplicar trabalho.

Termo genérico não serve — pega preâmbulo de prova e devolve lixo. O detalhe do teste e os
números estão em [[project_guias_do_tec_uso_e_limites]].

## Regras de uso

- **Ficha uma vez por disciplina.** Os 7 níveis depois só consultam.
- **Redundante não é lixo:** vai pra `reserva`, etiquetada pelo ponto, e alimenta os níveis 2 a 4.
- **O grupo de questões maior num ponto identifica o padrão mais cobrado** — é exatamente a
  definição de "questão ouro" dos níveis 6 e 7. Filtro de redundância e seleção de ouro são a
  mesma medição vista de dois lados.
- **Questão que não cabe em nenhum ponto** é gap de conteúdo e alimenta a taxonomia de volta,
  igual à regra do processamento de edital (ver [[project_taxonomia_central_nome_mestre]]).
- **A ficha envelhece:** quando o Tec marcar a questão como desatualizada, a ficha entra em
  refichamento e os cadernos que a usaram são sinalizados.

**Why:** sem essa camada, "redundância", "cobertura" e "tamanho certo do caderno" não são
mensuráveis — e o caderno vira sorteio das mais recentes.

**How to apply:** ver [[project_niveis_caderno_tec_e_pesos]] pro dimensionamento por pontos e
[[project_tec_gerador_nao_repete_questao]] pras armadilhas da plataforma. Os endpoints de
edição cirúrgica de caderno estão no manual em `_contexto/tecconcursos.md`.
