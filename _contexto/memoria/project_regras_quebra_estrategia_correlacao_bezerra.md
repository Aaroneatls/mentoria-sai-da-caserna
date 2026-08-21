---
name: project-regras-quebra-estrategia-correlacao-bezerra
description: "Regras de quebra de subtópico do Estratégia (10-20 páginas) e de correlação com os resumos do Bezerra (página real do PDF, disciplina, arquivo) — definidas por Elvis em 2026-08-19"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T17:56:14.007Z
---

Regras detalhadas de negócio definidas por Elvis em 2026-08-19 (ver [[project_skill_mapeamento_aulas_pendencias]] pro checklist geral). Refinam como a skill de mapeamento do Estratégia deve quebrar os PDFs de aula e como correlacionar com os resumos do Bezerra.

## Quebra de subtópicos do Estratégia (páginas de teoria)

- **Referência: 10 a 20 páginas por bloco/parte.** Em casos excepcionais pode extrapolar pra mais de 20 ou ficar abaixo de 10, mas evitar.
- Se um PDF tem, por exemplo, 25 páginas de teoria, o ideal é quebrar em partes de ~12-13 páginas (proporcional), não uma parte de 20 e outra de 5.
- **Prioridade: limite natural do assunto sobre o número redondo de páginas.** Se o assunto é uno (não dá pra quebrar sem cortar o raciocínio no meio), mantém inteiro mesmo que passe de 20. Se a quebra natural entre dois tópicos cai em, por exemplo, 10 + 15 páginas, tudo bem ficar assim mesmo não sendo um meio a meio perfeito.

## "Quantidade de páginas" = só teoria

- Refinamento importante: quando falamos de páginas de uma aula, é **sempre só teoria**, nunca as páginas de questões/comentários.
- **Questão resolvida embutida DENTRO do texto de teoria** (exemplo prático no meio da explicação) **conta como teoria**.
- **Lista de questões separada no final** (seção "Questões Comentadas" ou "Lista de Questões") **não conta** como teoria.
- Isso já bate com o critério já usado (teoria = até onde começa a seção de questões comentadas/lista, ver [[feedback_contagem_questoes_pdf_aulas]]), mas a nuance do exemplo embutido é importante pra não cortar teoria errado em PDFs de formato diferente.

## Correlação com os resumos do Bezerra

- **Página real do leitor de PDF, nunca a numeração impressa na folha.** Página impressa pode divergir do índice real por causa de capa, sumário, etc. — o que vale é a posição real quando abre num leitor de PDF (equivale ao índice que já é extraído via `pypdf`, método que já vem sendo usado).
- Ao indicar a correspondência de uma aula/parte do Estratégia no resumo, registrar: **disciplina do resumo** (pode divergir da esperada), **nome do arquivo**, **página real**.
- **Usar a estrutura do próprio resumo pra ajudar a decidir onde quebrar a aula do Estratégia** — é um alinhamento nos dois sentidos, não só o Estratégia ditando a quebra sozinho. Evita que a quebra do Estratégia fique "solta" sem nenhum ponto de apoio equivalente no resumo.
- **Um resumo pode cobrir mais de uma aula do Estratégia.** Quando um tópico do resumo não bater com a aula "óbvia" que está sendo comparada, **varrer todas as outras aulas da disciplina** antes de concluir que não tem correspondência.
- **Objetivo final da varredura:** identificar tópicos do Bezerra que não aparecem em **nenhuma** aula do Estratégia daquela disciplina.
- **Diferenciar dois casos quando um tópico do resumo não bate exatamente com a aula:**
  - **Complemento correlato** (mesmo tema, resumo mais detalhado que o PDF do Estratégia, ex: adiciona um ponto específico dentro do mesmo assunto) → mantém a indicação de página, é bônus pro aluno estudar também.
  - **Assunto/legislação genuinamente diferente** (não é o mesmo tema, é outra lei/outro tópico que o Estratégia realmente não trata) → não força o link, mas registra como "sem correspondência" (informação legítima, não erro).

## Casos sem resumo de referência

- Quando não houver resumo do Bezerra pra uma aula/parte do Estratégia, definir um **texto padrão** de "sem resumo disponível" pra skill usar (texto exato ainda não definido).
- **Pendência futura:** atualizar as skills de download do Estratégia (`baixar-curso-especifico-estrategia`, `baixar-curso-completo-estrategia`) pra também identificar e baixar o **PDF de resumo próprio do Estratégia** (existe essa opção na plataforma, separada do resumo do Bezerra). Quando não tiver resumo do Bezerra, pode usar o do Estratégia como fallback, ou por padrão deixar os dois disponíveis — **decisão ainda não tomada**, fica pra mais adiante.

**Why:** essas regras garantem que a quebra de subtópico do curso principal (Estratégia) fique didaticamente e estruturalmente compatível com a segunda fonte (Bezerra), em vez de cada fonte ser mapeada isoladamente e depois forçada a bater.

**How to apply:** ao desenhar a skill de mapeamento do Estratégia e a skill de mapeamento do Bezerra, aplicar essas regras desde a primeira extração — não é um ajuste posterior, é como a quebra deve nascer.

## ALVO ATUALIZADO — 21/08/2026

O alvo do bloco desce de **12 para ~10 paginas de teoria**. Pode passar nos casos em que o
material nao oferece titulo onde cortar (ver Auditoria Governamental), mas a mira e 10.

**Por que importa alem do tamanho:** quanto menor o bloco, maior a chance de dois cursos
diferentes caírem no mesmo recorte de conteudo, porque a sequencia do assunto e parecida mesmo
quando a escrita difere. Isso reduz muito os casos em que um curso junta o que o outro separa, e
portanto reduz a necessidade de quebrar topico em grao fino. Ver
[[project_cod_mestre_formato_e_ordem]].

**O corte continua sendo no titulo mais proximo do alvo**, nunca a cada 10 paginas fixas.
