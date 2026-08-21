---
name: project_dossie_do_aluno
description: dossie por aluno e viavel e barato de modelar, mas so escala se o dado de desempenho chegar sem passar pela mao do Elvis
metadata:
  type: project
---

Pergunta do Elvis em 21/08/2026: da para montar um dossie de cada aluno?

**Da, e o modelo e pequeno.** O dossie nao e planilha nova, e uma quarta camada encaixada no
que ja existe: disciplina, topico mestre (Cod Mestre), ponto (fichamento), questao. O dossie e
a mesma chave com o aluno na frente, `aluno x ponto -> acertou / errou / quando`. Com isso, o
"botar mais questoes daquele ponto" que ele descreveu sai de graca: e o mesmo
`compor_cadernos.py`, so que a fila de prioridade passa a ser ordenada pelo erro DAQUELE aluno
em vez da dificuldade geral.

**O que decide nao e a modelagem, e a origem do dado.** O dossie so escala se o desempenho
chegar sozinho. Se o Elvis tiver que digitar aluno por aluno, morre na terceira semana, e ele
mesmo levantou isso ("vai me tomar tempo, vai me tomar energia"). Tres origens possiveis, da
melhor para a pior:

1. **TecConcursos** tem desempenho por caderno e por assunto. Depende de como o aluno consome
   o caderno: na nossa conta da para ler, na conta dele nao da acesso direto. Pergunta aberta.
2. **Tutory**, se registrar conclusao e desempenho e tiver exportacao. O Elvis ja falou em dar
   acesso; e o item A10/A17 da lista.
3. **O proprio aluno manda** o caderno de erros. Integracao custa zero, mas depende da
   disciplina dele. Ver [[project_caderno_de_erros_do_aluno]].

**Portanto:** nao projetar o dossie agora. Resolver primeiro de onde vem o dado. Depois disso
o dossie e uma tarde de trabalho. Antes disso e desenho no vazio.
