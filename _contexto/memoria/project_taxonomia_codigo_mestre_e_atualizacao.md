---
name: project-taxonomia-codigo-mestre-e-atualizacao
description: "Chave da taxonomia central é o Cód Mestre (SIGLA-NNN), não o nome; tabela de siglas de disciplinas com aliases; skill precisa ser atualizável e cascatear pras bases dependentes"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T18:44:03.468Z
---

Definido por Elvis em 2026-08-19, durante a construção do primeiro protótipo de taxonomia (ver [[project_taxonomia_central_nome_mestre]] pro desenho geral).

## 1. A chave é o código, não o nome

A coluna mestre da taxonomia **não é o nome do assunto** — é uma **codificação**:

```
<SIGLA DA DISCIPLINA>-<NNN>
```

Ex.: `DADM-001`, `DADM-047`. A numeração é sequencial **dentro de cada matéria**.

**Por quê:** o nome do tópico vai ser ajustado com o tempo (acento, vírgula, reformulação). Se as bases dependentes apontarem pro nome, qualquer retoque quebra o vínculo. Apontando pro código, o tópico continua sendo o mesmo mesmo depois de renomeado.

**Regra prática:** todas as bases derivadas (compatibilização, cadernos do Tec, planos de estudo, planilhas por edital) referenciam o **Cód Mestre**. O nome é coluna descritiva, livre pra editar.

## 2. Tabela de siglas de disciplinas (com aliases)

A base mestre precisa ter uma **aba própria de siglas de disciplinas**, porque a mesma disciplina aparece com vários nomes diferentes entre editais, Estratégia, Bezerra e Tec ("Direito Administrativo", "Noções de Direito Administrativo", "Direito Administrativo Municipal", "Legislação Administrativa"...).

Colunas: **Sigla | Nome Mestre da Disciplina | Nomes alternativos encontrados nas fontes | Status** (Confirmada / Proposta — confirmar).

Siglas já confirmadas: `DADM` (Direito Administrativo), `DCON` (Direito Constitucional), `DTRI` (Direito Tributário). As demais foram propostas por Claude e aguardam confirmação do Elvis.

Essa aba é o que alimenta o prefixo do Cód Mestre — sigla nova só entra depois de registrada ali.

## 3. A skill de taxonomia tem que ser atualizável, com cascata

A skill de criação da taxonomia (`criar-taxonomia-central`, nome provisório) **não pode ser de mão única**. Precisa nascer com:

1. **Modo criar** — monta a base do zero pra uma disciplina nova.
2. **Modo atualizar** — reprocessa uma disciplina já existente **preservando os Cód Mestre já atribuídos** (tópico que continua existindo mantém o código; tópico novo ganha o próximo número livre; tópico que sumiu é marcado como descontinuado, nunca reaproveita o número).
3. **Cascata de atualização** — depois de atualizar a taxonomia, rodar (ou pelo menos listar, em ordem) a atualização de **todas as bases dependentes** que usam aquela nomenclatura: compatibilizações, planilhas de edital, bases de cadernos do Tec, planos de estudo. A skill tem que entregar essa sequência, não deixar o Elvis descobrir na mão o que ficou desatualizado.

## 4. Layout padrão da aba de taxonomia (definido no protótipo de 2026-08-19)

Cabeçalho na linha 10, dados da 11 em diante, legenda de cores nas linhas 2-7 (área de design). Colunas, nessa ordem:

`Cód Mestre | Nome Mestre do Tópico | Eixo Temático | Estratégia — Aula | Estratégia — Subtópico (páginas de teoria) | Estratégia — Nº de Páginas de Teoria | Bezerra — Resumo, subtópico e páginas | Tec — Assunto(s) | Tec — Qtd. Questões | Tec — % da Matéria | Edital — Item | Âncora Legal Principal | Status de Cobertura | Observações`

A coluna **Nº de Páginas de Teoria** é derivada do intervalo `[pX-Y]` do subtópico e serve pra dimensionar esforço de leitura (entra depois no cálculo de razão peso/página da Curva ABC). **Atenção:** quando vários tópicos mestres apontam pro mesmo bloco do Estratégia, a página aparece repetida em cada linha — a coluna Observações avisa, e qualquer soma tem que deduplicar por (aula + intervalo de páginas), nunca somar a coluna direto.

**Esquema de cores do Status de Cobertura** (pedido por Elvis em 2026-08-19): **roxo** = sem aula do Estratégia; **azul** = sem resumo do Bezerra; **laranja** = sem assunto no Tec; **vermelho** = mais de uma lacuna ao mesmo tempo; **verde** = completo. Além da célula de status, as próprias células da fonte que está faltando ficam pintadas com a cor correspondente, pra bater o olho na linha e ver de onde vem o buraco.

**Why:** a taxonomia é a espinha dorsal de tudo. Se ela mudar e as bases derivadas não acompanharem, o sistema inteiro passa a apontar pra tópico errado — e isso só aparece muito depois, no plano de estudo entregue ao aluno.

**How to apply:** já incluir os três modos no desenho da skill, desde a primeira versão. Ver também [[project_niveis_caderno_tec_e_pesos]] e [[project_regras_quebra_estrategia_correlacao_bezerra]].
