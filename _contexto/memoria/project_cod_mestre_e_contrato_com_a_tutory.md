---
name: project_cod_mestre_e_contrato_com_a_tutory
description: a Tutory casa "ja estudou" pelo nome do assunto + materia, entao o Cod Mestre vira identificador publicado e nao pode mudar nunca
metadata:
  type: project
---

**Descoberta que muda o peso do Cod Mestre** (Elvis, 21/08/2026): a Tutory identifica que o
aluno **ja estudou** uma aula comparando **nome do assunto + materia** entre planos de estudo
diferentes. Se o aluno migra de um plano para outro e os dois nomes batem, ela considera a mesma
aula e nao manda ele refazer.

**Consequencia:** o Cod Mestre nao e so chave interna, e o **contrato com a plataforma**. O que
for publicado naquele campo vira identificador e **nao pode mudar nunca**.

E exatamente por isso que se usa o codigo e nao o nome descritivo: o nome a gente vai querer
melhorar com o tempo, e melhorar quebraria o casamento, fazendo a Tutory tratar a mesma aula como
nova. Ver [[project_cod_mestre_formato_e_ordem]].

**O que pode mudar livremente:** a **ordenacao** do plano. O Elvis confirmou que renumerar nao da
problema, porque a plataforma reordena e continua reconhecendo o que o aluno ja fez pelo nome.
Logo, o passo de 10 em 10 e conforto, nao necessidade.

**O que NAO pode mudar:** o nome da disciplina e o nome do assunto definidos na tabela mestra.

**Em aberto, e precisa ser resolvido antes da primeira publicacao:**

1. **Quantos digitos** no codigo. Ficou `SIGLA-NNN` (3 digitos), mas o Elvis escreveu
   `DADM-0102` (4). Trocar depois da primeira publicacao quebra o casamento de todos os alunos.
2. **O que vai no campo de assunto**: so o codigo (feio, a prova de bala) ou codigo + nome
   (legivel, mas **congela o nome para sempre**). Se a Tutory tiver campo de descricao separado
   do campo que ela usa para casar, da para ter os dois.

**A etapa da Tutory tem skill propria**, separada da geracao do plano.
