---
name: project-curso-referencia-e-aulas-faltantes
description: "Qual curso do Estratégia serve de referência por área, mecanismo de referência provisória quando a aula pós-edital ainda não saiu, e a correção de gaps falsos causados por usar o curso errado"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T22:12:21.377Z
---

Definido com Elvis em 2026-08-19.

## 1. Curso de referência por área

Em curso **pós-edital**, o Estratégia **não libera todas as aulas de uma vez**. Enquanto a aula
não sai, usa-se o curso Regular correspondente como **referência provisória**:

- Concurso da área **Fiscal** → `Regular Fiscal`
- Concurso da área **Controle** → `Regular Controle` (Tribunais de Contas, ensino superior)

Ambos já baixados em `G:\Meu Drive\Inteligência Artificial\Estrategia\`.

## 2. O casamento é por CONTEÚDO, nunca por número de aula

Ficou provado na prática: a **Aula 11** é *Controle da Administração* no Regular Fiscal,
*PPPs e Consórcios* no Regular Controle e *Controle da Administração* no TCDF-ANACE. Número de
aula não significa nada entre cursos.

Vale **nome do tópico + âncora legal** — a mesma lógica já usada entre Estratégia e Bezerra
(ver [[project_regras_quebra_estrategia_correlacao_bezerra]]).

## 3. Colunas e rotina

Na taxonomia, duas colunas novas: **origem da referência** (curso do concurso ou substituto) e
**status** (provisório / confirmado). Quando a aula real sair, roda o check e reporta: o que
bateu, o que mudou de página, e o que não existe no curso do concurso ou apareceu a mais.

**O caderno não espera.** Ele é montado pelo ponto, e o ponto não depende de qual curso ensina.
O que fica provisório é só a indicação de onde estudar (mesma distinção de
[[project_paginas_estrategia_sao_derivadas]]).

## 4. Correção importante: gaps falsos por curso errado

A taxonomia de Direito Administrativo de 2026-08-19 foi construída sobre o **Regular Fiscal**
(18 aulas), enquanto os cadernos foram montados na área **Controle**. Isso gerou **gaps falsos**:

- O item **4.8 do edital do TCDF** (sindicância e PAD) foi reportado como "sem aula no
  Estratégia — gap prioritário". **Tem aula**: é a Aula 16 do curso TCDF-ANACE.
- Boa parte dos 11 tópicos de **Lei 8.112/1990** marcados como sem aula está coberta pelas
  Aulas 14, 15 e 16 do TCDF-ANACE (provimento, vacância, estabilidade, remuneração, direitos,
  deveres, responsabilidades).

O curso do TCDF quebra **Agentes Públicos em quatro aulas**, enquanto o Regular Fiscal trata em
uma só (a de 172 páginas).

**Lição:** antes de declarar gap de conteúdo, conferir **qual curso** está servindo de base — o
gap pode ser da fonte escolhida, não do material.

## 4a. ALERTA BLOQUEANTE: mesma disciplina com mais de um professor

Acontece de o mesmo curso trazer **duas pastas da mesma disciplina, com professores
diferentes** — cursos paralelos, não conteúdos diferentes. Casos reais no `Regular Fiscal`
(19-08-2026):

- **Direito Civil** — Cadu Carrilho **x** Paulo Sousa
- **Contabilidade Geral e Avançada** — Gilmar Possati **x** Cardozo Rosa Sande

**Regra (Elvis, 2026-08-19):** a skill **para e pergunta ao Elvis qual usar**. Nunca escolhe
sozinha e **nunca funde** os dois por conta própria. É alerta bloqueante, igual ao dos quatro
casos de mudança de código (ver [[feedback_codigo_identifica_conteudo_nao_posicao]]).

**Tabela de escolhas (manter atualizada conforme Elvis decidir):**

| Disciplina | Curso | Professor escolhido |
|---|---|---|
| Contabilidade Geral e Avançada | Regular Fiscal | **Gilmar Possati** (confirmado por Elvis) |
| Direito Civil | Regular Fiscal | **pendente** — Cadu Carrilho ou Paulo Sousa; Elvis vai conferir |

Escolha feita fica registrada aqui e **não se pergunta de novo** — só se surgir professor novo
ou o Elvis pedir revisão.

## 4b. Escopo de concursos (Elvis, 2026-08-19)

A base cobre, por enquanto, **só as disciplinas que estão nos cursos Regulares**:

- **Regular Fiscal** → Sefaz estaduais (ICMS), ISS municipais e Receita Federal
- **Regular Controle** → Tribunais de Contas e Controladorias

Outras áreas podem entrar depois; hoje o enfoque é esse.

### Método do delta (Elvis, 2026-08-19) — só se levanta o que falta

**A base é construída sobre os cursos Regulares.** Quando chega um pós-edital, carrega-se o
curso específico e **identifica-se apenas as matérias que NÃO existem nos Regulares já
mapeados**. Só essas ganham levantamento próprio; o resto já está pronto.

**Cuidado central:** o nome da disciplina **muda entre cursos, mas as aulas são as mesmas**.
Então a comparação é **por conteúdo das aulas**, nunca pelo nome da matéria. Exemplos do Elvis:
- **Administração Financeira e Orçamentária (AFO)** aparece como **Direito Financeiro**
- **Finanças Públicas** aparece como tópicos dentro de **Economia**
- **Administração Pública** vem junto com **Administração Geral**

**Exemplo real medido em 2026-08-19 — TCDF-ANACE (17 matérias) x Regular Controle (12):**

*Já cobertas pelo Regular Controle (não precisam levantamento):* Direito Administrativo,
Direito Constitucional, AFO, Administração Geral e Pública (≈ "Administração Pública"),
Língua Portuguesa (≈ "Português").

*Caso fronteiriço:* "Raciocínio Lógico e Matemática Financeira" do TCDF corresponde a **duas**
matérias do Regular Controle ("Raciocínio Lógico e Analítico" + "Matemática Financeira") —
fusão de matérias, precisa conferência.

*Só no TCDF (exigem levantamento próprio):* Noções de Primeiros Socorros, Lei Orgânica do TCDF
e Regimento Interno, Gestão de Contratos, Análise de Dados/Estatística/IA, Conhecimentos do DF
e Políticas para Mulheres, Direito Previdenciário, Lei Orgânica do DF, Noções de Direito Civil,
Noções de Direito Tributário, Regime Jurídico dos Servidores do DF.

Ou seja: de 17 matérias, ~5 já estavam prontas e ~10 precisam de trabalho. O delta é o que se
levanta.

*(Nota: o Direito Previdenciário do TCDF vem com **dois professores** — Adriana Menezes e
Rubens Maurício. Cai no alerta bloqueante do item 4a, agora também em curso pós-edital.)*

**Regra: checar por CONTEÚDO, não pelo nome da matéria.** Antes de criar código novo, procurar
os tópicos **no banco inteiro, em todas as disciplinas**. Se já existirem sob outro código,
aponta pra ele; só o que não existe em lugar nenhum gera código novo. A aba **Siglas de
Disciplinas** guarda os nomes alternativos e sustenta essa busca
(ver [[project_taxonomia_codigo_mestre_e_atualizacao]]).

**Matéria ≠ disciplina.** A matéria é o rótulo do pacote em que o conteúdo veio; o conteúdo é o
Cód Mestre. Uma base de matéria misturada (ex.: "AFO, Direito Financeiro e Contabilidade
Pública") tem linhas apontando pra `ACOF-###`, `DFIN-###` e `CPUB-###` ao mesmo tempo — e isso
é normal, não erro.

## 4c. Bezerra: base única; Estratégia: uma base por matéria

Decidido por Elvis em 2026-08-19.

- **Bezerra → base única.** Acervo estável, sem versão por concurso, e com conteúdo que migra
  entre matérias (o exemplo dele: coisas de TI aparecem em Informática). Funciona porque as
  linhas apontam pro Cód Mestre, e o prefixo da disciplina faz o roteamento sozinho.
- **Estratégia → uma base por matéria.** Aqui existe uma versão do curso por concurso, então a
  mesma disciplina tem vários recortes vivos ao mesmo tempo.

## 4d. Tarefa registrada: comparar curso Regular x curso específico (Elvis, 2026-08-19)

Quando um **curso específico de concurso** for adicionado, é preciso rodar a **comparação entre
ele e o curso Regular da área** pra gerar **novos índices de assunto** e alimentar a base. Não é
só conferir o que falta — é extrair da diferença os tópicos e pontos que o curso específico traz
e o Regular não tem (e vice-versa).

Base empírica disponível: `Regular Controle` (18 aulas) x `TCDF-ANACE` (21 aulas), ambos em
disco. O TCDF quebra Agentes Públicos em 4 aulas e tem LGPD e Processo Administrativo; o Regular
Controle tem PPPs, Consórcios e Convênios que o TCDF não tem.

**Descoberta que barateia isso (2026-08-19):** pra as aulas que existem nos dois cursos, a
**teoria é idêntica, com a mesma paginação** — o Estratégia monta o PDF de um mestre único de
teoria e troca só a seção de questões. Verificado: Aula 00 do Regular Controle tem 125 páginas
no PDF mas teoria em `p3-25`, exatamente igual à do Regular Fiscal, com os mesmos cortes de
subtópico. Então a comparação entre cursos é sobre **quais aulas existem**, não sobre reler a
teoria.

## 5. Decisão (Elvis, 2026-08-19)

**Parar de usar o `Regular Fiscal`** nesta linha de trabalho. A taxonomia do DADM será refeita,
e isso vai servir de teste do mecanismo de atualização.

**Estado dos cursos baixados em 19-08-2026:** `TCDF-ANACE` com 21 aulas (completo, nenhuma
faltando), `Regular Controle` com 18, `Regular Fiscal` com 18.
