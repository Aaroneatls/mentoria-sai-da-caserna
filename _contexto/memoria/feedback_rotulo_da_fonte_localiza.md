---
name: feedback_rotulo_da_fonte_localiza
description: toda base de fonte guarda o nome que AQUELA fonte usa; o nosso nome identifica, o da fonte localiza
metadata:
  type: feedback
---

**O nosso nome identifica; o nome da fonte localiza.** E a mesma regra do
[[feedback_nome_mestre_sintetiza_referencia_e_literal]], estendida para todas as fontes.

Toda base carrega uma coluna com **o nome que aquela fonte usa**: a materia do Bezerra, o assunto
do Tec, o nome do curso do Estrategia, o item do edital. Nunca substituir pelo nosso nome ao
guardar.

**O caso que motivou** (Elvis, 21/08/2026): o aluno esta em `Tecnologia da Informacao` no plano,
mas o resumo do Bezerra esta arquivado na materia **Informatica** dele. Sem o rotulo de origem,
o aluno procura, nao acha, e conclui que o material esta errado. Vale nos dois sentidos: pode
estar em Informatica no plano e em Tecnologia no resumo.

A referencia do aluno mostra os dois:

```
Estudo de Tecnologia da Informacao
TECINF-0203
Referencia: Banco de Dados: Normalizacao
            Estrategia - Aula 07, paginas 12 a 24
            Bezerra    - resumo "Modelagem de Dados", na materia INFORMATICA
            (!) No edital do TCDF isso aparece como "Analise de Dados"
```
