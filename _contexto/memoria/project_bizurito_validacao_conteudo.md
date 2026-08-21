---
name: project-bizurito-validacao-conteudo
description: "Arquitetura de validação do conteúdo do BIZURITO em 6 camadas, incluindo a auditoria obrigatória de 'olhar de fora' e o registro de vícios que aprende a cada execução"
metadata:
  node_type: memory
  type: project
---

Nasceu de um teste real em 2026-08-20: Elvis mandou auditar o BIZURITO de Poder de Polícia como
se eu fosse um especialista em resolver questões. **Três das treze linhas estavam com problema**,
num conteúdo que eu tinha escrito com cuidado. Em escala de centenas de folhas, isso não se
sustenta sem trava. Ver [[project_bizu_revisao_por_topico]].

## Os três erros achados (viraram o catálogo de vícios)

1. **Lista parcial apresentada como completa.** Escrevi "São os do caput" e listei 5 dos **8**
   bens tutelados do art. 78 do CTN (faltaram atividades dependentes de concessão/autorização,
   tranquilidade pública e respeito à propriedade). **É o pior erro possível:** o aluno decora a
   lista como fechada e erra a questão *por causa do nosso material*.
2. **Requisito omitido de tese jurisprudencial.** Na tese do Tema 532 faltaram "exclusivamente"
   e "de atuação própria do Estado". Como a banca cobra trocando um requisito, omitir requisito
   entrega o aluno.
3. **Regra absoluta demais.** "O item que contiver essa expressão está errado" é o mesmo vício
   que a própria folha manda o aluno desconfiar.

## Camada 0 — Origem: o bizu sai da resolução do professor (REGRA, Elvis 2026-08-20)

A frase do bizu **deriva da resolução do professor no Tec e do gabarito**, nunca do meu
conhecimento próprio. Foi escrever de cabeça que produziu os três erros acima.
Cada linha guarda os **# das questões que a originaram**: sem rastro, não entra.
Consequência: erro possível deixa de ser invenção e passa a ser, no máximo, síntese ruim,
que é muito mais fácil de detectar.

## Camada 1 — Checagem mecânica (automática, roda sempre)

Sobre o **PDF renderizado**, nunca sobre o HTML: acento e entidade quebrada, travessão
(proibido), **informalidade** (pra, pro, a gente, cara, beleza...), soma das questões dos blocos
batendo com o total do cabeçalho, percentual na coluna RISCO, e uma página.

## Camada 2 — Conferência de âncora contra fonte oficial (automática)

Toda citação de **artigo, lei, súmula ou tema de repercussão geral** é extraída do texto e
conferida contra a fonte oficial (Planalto, STF, STJ). Dois testes:
- os termos citados aparecem mesmo no dispositivo?
- **teste de completude:** se a frase usa "são", "os do caput", "apenas", "somente",
  "exclusivamente", "os requisitos são", a lista precisa ser **conferida item a item** contra o
  dispositivo. Foi exatamente aqui que o art. 78 passou.

## Camada 3 — Olhar de fora (obrigatória, pedido de Elvis 2026-08-20)

Uma passada **independente**, lendo **só a folha final**, sem o contexto de como ela foi montada,
no papel de quem chega de fora e desconfia: *"peraí, deixa eu ver se isso está certo mesmo"*.

Perguntas fixas para **cada linha**:
- O que precisaria ser verdade para essa afirmação ser **falsa**?
- Falta algum **requisito** da tese, do conceito ou da regra?
- A lista está **completa** ou parece completa sem ser?
- Tem palavra **absoluta** (sempre, nunca, todo, apenas) que a fonte não sustenta?
- Dois termos **próximos** foram tratados como sinônimos? (valor de mercado x VRL, aplicar x
  cobrar, nominal x efetiva)
- O **sujeito** da frase está certo? (quem aplica, quem cobra, quem delega)

## Camada 4 — Contraprova pela questão (o teste definitivo)

Pegar uma questão real já fichada que cobre o ponto e perguntar: **lendo apenas este bizu, o
aluno acerta?** Se não acerta, o bizu está incompleto, por mais correto que esteja.
É barato porque a questão já está na base.

## Camada 5 — Aprendizado acumulado (pedido de Elvis 2026-08-20)

**Ao final de cada BIZURITO gerado**, rodar a avaliação, registrar o que apareceu e **atualizar
este arquivo**. Cada erro novo vira uma pergunta fixa da Camada 3, de modo que a auditoria fica
mais afiada a cada execução em vez de recomeçar do zero. É o mesmo espírito da regra de sugestão
de melhoria ao fim das skills (ver [[feedback_sugestao_melhoria_final_execucao]]).

## Camada 6 — Erro agregado dos alunos (Elvis aprovou em 2026-08-20)

O caderno de erros dos alunos retroalimenta o BIZURITO: **se muitos alunos erram o mesmo ponto,
a suspeita recai sobre o nosso material, não sobre eles**. Vira insumo de prioridade de qual
folha reescrever. Ver [[project_caderno_de_erros_do_aluno]].

**Não usar o percentual cru.** A amostra é pequena (100 alunos, e a minoria manda o export), e
percentual baixo pode ser só questão difícil. O sinal é o **delta contra o índice de acerto da
comunidade**, que a API do Tec já entrega em `/api/questoes/{id}/desempenho`:

- comunidade 70%, nossos alunos 30% -> **o material falhou**, prioridade de reescrita
- comunidade 30%, nossos alunos 30% -> questão difícil, o material está ok

Isso normaliza a dificuldade e por isso funciona mesmo com N baixo. Ainda assim, exigir um
**mínimo de alunos no mesmo ponto** antes de agir, pra não reescrever folha por causa de 3 casos.

**Só vale para dentro.** Devolver ao aluno o percentual dele comparado à turma foi **descartado
por Elvis**: a amostra é pequena e o Tec já oferece "COMPARE-SE COM A COMUNIDADE", com base
muito maior. Comparar com a turma seria uma versão pior do que ele já tem de graça.

## Limite honesto

Nenhuma camada zera o risco. Por isso continuam existindo: a ressalva de imprecisão no rodapé, o
**código de reporte** na mão do aluno (última rede) e a possibilidade de corrigir no mesmo link
sem trocar o endereço.

**Why:** material de estudo errado é pior que material nenhum, porque o aluno confia e não
confere.

**How to apply:** as camadas 0 a 2 são pré-requisito de publicação. A 3 e a 4 são obrigatórias
antes de qualquer folha ir para aluno. A 5 roda sempre, ao final.
