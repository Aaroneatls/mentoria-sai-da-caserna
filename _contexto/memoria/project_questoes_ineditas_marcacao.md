---
name: project_questoes_ineditas_marcacao
description: questao inedita do Tec fica marcada no banco desde a coleta, mas nao separa caderno ainda; separar so quando aparecer materia majoritariamente inedita
metadata:
  type: project
---

O Tec tem questoes **ineditas** (escritas por ele, nao vindas de prova real) alem das de
concurso. Elas exigem plano especifico do aluno, entao um caderno que as misture pode simplesmente
nao abrir para quem nao tem o plano.

**Decisao (Elvis, 21/08/2026):** marcar desde a coleta, nao separar ainda. Gerar caderno sem
distinguir por enquanto. Quando aparecer uma materia majoritariamente inedita, ai sim desenhar
a separacao, ja com o dado na mao.

**Como esta implementado:** a resposta de `/api/questoes/{id}/deslogado` traz
`questaoAdaptadaOuInedita`, `anulada` e `desatualizada`. A linha do banco passou de 12 para 15
campos, com esses tres no fim. O coletor faz duas coisas na mesma fila: colhe o que falta e
**completa** as linhas antigas de 12 campos, gastando 1 requisicao em vez de 2 nessas (o
desempenho ja estava guardado). Ver [[project_banco_fichamento_questoes]].

Na amostra de Direito Administrativo nao apareceu nenhuma inedita: o filtro que montou a lista
das 5.463 ja trouxe so prova real. Guardar o campo mesmo assim custa zero e evita recoleta
quando entrar materia onde elas existem.

A conta do Elvis tem plano avancado (`assinanteAvancado: true`). Isso diz o que **nos** podemos
ver, e nao o que o **aluno** consegue abrir, que continua sendo o item A11 em aberto.
