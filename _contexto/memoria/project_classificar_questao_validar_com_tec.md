---
name: project-classificar-questao-validar-com-tec
description: "Classificar questão nunca é só casar palavra-chave: checar a classificação do TecConcursos e a correlação com as questões do próprio PDF, e separar as não resolvíveis pela aula"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T11:09:20.068Z
---

Definido pelo Elvis em 2026-08-20, a partir do caso da Contabilidade.

## O problema: palavra-chave engana

Em **Contabilidade** (e em Auditoria) o mesmo assunto aparece ligado a **outras matérias**, de
forma mais aprofundada. Casar a questão com o tópico por palavra-chave coloca a questão no
lugar errado — e o aluno recebe uma questão que a aula dele não ensina.

Por isso o **Nome Mestre não pode se perder em detalhamento**: quanto mais granular o nome,
mais fácil misturar assuntos de matérias diferentes. O nome tem que segurar a referência do que
aquele bloco realmente é.

## As três checagens, sempre juntas

Ao dizer que uma questão pertence a um tópico:

1. **A minha classificação** — leitura do enunciado e do comentário do professor.
2. **A classificação do TecConcursos** — o Tec já tem taxonomia própria de assuntos. Serve de
   referência independente. Divergência entre as duas é sinal de que preciso olhar de novo.
3. **A correlação com as questões que estão dentro do PDF da aula** — se a questão se parece
   com as que o professor comentou ali, ela é do tema; se destoa de todas, provavelmente não é.

Dá mais trabalho. É intencional: o objetivo é garantir que a questão seja **resolvível com a
aula do Estratégia**.

## As não resolvíveis não são descartadas

Questão que o material não cobre é **marcada como não resolvível** e guardada. Ela vai alimentar
**cadernos específicos numa camada separada** — não some, só não entra no caderno do tópico.

## Ressalva sobre a nomenclatura

Conforme as questões forem sendo delineadas, **as nomenclaturas podem precisar ser
reformuladas**. O nome do tópico não é definitivo antes de a camada de questões existir: se a
prática mostrar que o recorte não bate com o que as bancas cobram, o nome muda.

Ver [[feedback_nome_mestre_sintetiza_referencia_e_literal]], [[project_banco_fichamento_questoes]]
e [[project_taxonomia_codigo_mestre_e_atualizacao]].
