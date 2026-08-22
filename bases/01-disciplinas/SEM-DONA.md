# Fontes sem dona — Base 1

> Gerado pela skill `montar-base-disciplinas`. **Não editar na mão**: é a leitura do
> filtro `status` do `dados/apelidos.csv`. Para mudar algo aqui, muda-se a classificação lá.

Levantado em 22/08/2026, sobre 5 camadas de fonte e 429 apelidos.

| Balde | O que é | Quantas | Pede decisão? |
|---|---|---|---|
| 1 | pode ser disciplina que esquecemos | 11 | **sim, do Elvis** |
| 2 | fora do escopo, outra carreira | 117 | não |
| 3 | legislação/conteúdo local, nasce em pós-edital | 30 | não |
| 4 | não é disciplina (lixo de migração) | 39 | não, vira insumo do A28 |

---

## Balde 1 — precisa do olho do Elvis

São as que **não casaram com nenhuma das 21 e não são obviamente de outra carreira**. Cada
uma pode ser matéria que a gente esqueceu, ou pedaço de uma que já existe.

| Nome na fonte | Fonte | Por que eu duvidei |
|---|---|---|
| Administração Geral | Bezerra | a nossa `ADMPUB` é Administração **Pública**. O Tec junta as duas numa matéria só (id 14), o Bezerra separa. Não existe pasta de Administração Geral em Regular nenhum. |
| Análise das Demonstrações Contábeis | Tec | pode ser tópico dentro de `CONTAB` em vez de disciplina. Aparece no Tec (58) e na Tutory, e não existe no Regular. |
| Legislação Tributária Federal | Tec | a `LTRIB` é a parte **geral**. Federal pode ser ela, ou pode ser específico de Receita Federal. O Elvis já apontou a `LTRIB` para o curso 336350 do Estratégia, então ela não depende disto. |
| Matemática | Tec | o Tec tem `Matemática` (62) separada de `Raciocínio Lógico` (217) e de `Matemática Financeira` (20). A gente só tem as duas últimas. |
| Redação Oficial | Tec | matéria própria no Tec (26). Pode ser parte de `PORT`, ou pode seguir a Discursiva e ficar fora por não ser conteúdo objetivo. |
| Ética no Serviço Público | Tec | cai em quase todo edital e é matéria própria no Tec (193). Não existe no Regular, então pela regra de escopo fica de fora. |
| Administração Geral | Tutory | a nossa `ADMPUB` é Administração **Pública**. O Tec junta as duas numa matéria só (id 14), o Bezerra separa. Não existe pasta de Administração Geral em Regular nenhum. |
| Administração Geral (Fiscal/ Controle) | Tutory | a nossa `ADMPUB` é Administração **Pública**. O Tec junta as duas numa matéria só (id 14), o Bezerra separa. Não existe pasta de Administração Geral em Regular nenhum. |
| Análise das Demonstrações Contábeis (Fiscal/ Controle) | Tutory | pode ser tópico dentro de `CONTAB` em vez de disciplina. Aparece no Tec (58) e na Tutory, e não existe no Regular. |
| Gestão de Contratos (Fiscal/ Controle) | Tutory | aparece só na Tutory. Provavelmente é tópico de `DADM`, não disciplina. |
| Legislação e Ética no Serviço Público | Tutory | cai em quase todo edital e é matéria própria no Tec (193). Não existe no Regular, então pela regra de escopo fica de fora. |

**Não são órfãs, são decisão registrada:** a **Discursiva** (cursos 268932 e 268941) e o
**Sistema de Questões 1 Ano** (143237) ficaram de fora por decisão do Elvis em 22/08/2026,
não por falha de levantamento. Estão em `DECISOES.md` desta pasta.

---

## Balde 2 — fora do escopo (117)

Nenhuma existe em Regular nenhum, e a regra de escopo é clara: o que não está no Curso
Regular não entra. A esmagadora maioria vem do Tec, que cobre **todas** as carreiras.

**Bezerra (6):** RFB - Administração Financeira, RFB - Comércio Internacional, RFB - Direito Previdenciário, RFB - Inglês, RFB - Legislação Tributária Federal, RFB - Legislação aduaneira

**Tec (106):** Administração de Recursos Materiais, Antropologia, Arqueologia, Arquitetura, Arquivologia, Artes e Música, Atualidades e Conhecimentos Gerais, Bancos - Atendimento, Vendas, História, etc., Biblioteconomia, Biologia e Biomedicina, Ciências Atuariais (Atuária), Ciências Políticas, Ciências Sociais, Comunicação Social, ...

**Tutory (5):** DIREITO PROCESSUAL CIVIL, DIREITO PROCESSUAL CIVIL - REVISÃO TEÓRICA, Direito Processual Civil (Fiscal/ Controle), Inglês, Inglês (Fiscal/ Controle)

---

## Balde 3 — local, nasce em pós-edital (30)

Legislação de estado ou município, e conhecimentos locais de um concurso. Viram
`LTRIB-<ente>` ou equivalente quando o edital sair.

**Bezerra (2):** Legislação Tributária Estadual, Legislação Tributária Municipal

**Estrategia Regular Fiscal (4):** Concursos da Área Fiscal (Todos Estados) Curso Básico de Legislação Trib. Estadual, Concursos da Área Fiscal - Curso Básico de Legislação Tributária Municipal, Legislacao Tributaria Estadual, Legislacao Tributaria Municipal

**Tec (8):** Direito Administrativo Estadual e do DF, Direito Administrativo Municipal, Direito Constitucional Estadual e Distrital, Direito Constitucional Municipal, Legislação Geral Estadual e do DF, Legislação Geral Municipal, Legislação Tributária dos Estados e do Distrito Federal, Legislação Tributária dos Municípios

**Tutory (16):** Economia Regional do Pará (Fiscal), História de Campina Grande/PB, História e Aspectos Geoeconômicos do Rio Grande do Norte (Fiscal/ Controle), LEI ORGÂNICA DO TCDF E REGIMENTO INTERNO, Legislação Tribuntária Federal, Legislação Tribuntária Municipal, Legislação Tributária Estadual do Goiás (Fiscal/ Controle), Legislação Tributária Estadual do Rio Grande do Norte (Fiscal/ Controle), Legislação Tributária Municipal de Manaus (Fiscal), Legislação Tributária do Estado de São Paulo (Fiscal), ...

---

## Balde 4 — não é disciplina (39)

Insumo direto do **plano de migração da Tutory (item A28)**. São simulados, revisões,
tópicos virados disciplina e sobras de trabalho antigo.

**Estrategia Regular Fiscal (2):** Concursos da Área Fiscal - Curso Básico de Discursiva (Sem Correção), Sistema de Questões 1 Ano - Cartão até 12 x

**Tutory (37):** Atos Administrativos (Passo Estratégico), Atos Administrativos - Simulado (Passo Estratégico), Control. 1, Control. 3, Dir. Adm 1, Dir. Adm 2, Dir. Adm 3, Dir. Adm 4, Dir. Adm 5, Dir. Cont 1, Dir. Cont 2, Dir. Cont 3, ...

