---
name: feedback_ouro_nao_e_dificuldade
description: questao ouro e alto rendimento de revisao, nao dificuldade; questao facil pode ser ouro e o rotulo do Tec nao serve de atalho
metadata:
  type: feedback
---

**Questao ouro nao tem nada a ver com dificuldade.** Uma questao **facil** pode ser ouro. O
rotulo `dificuldade` do Tec (Muito Facil ate Muito Dificil) e enquadramento **deles**, e a gente
nao usa como criterio.

Ouro e questao de **alto rendimento de revisao**, por um destes tres motivos (Elvis, 21/08/2026):

1. **Abrangencia** — toca varios pontos ou assuntos numa questao so.
2. **Qualidade da resolucao** — o comentario e o mais completo entre as do mesmo ponto.
3. **Representatividade** — quando varias questoes repetem o mesmo modelo, escolher a que, ao
   ser resolvida, revisa indiretamente as outras. Desempate: a mais recente, ou a de resolucao
   mais completa.

**Por que isso importa na pratica:** ouro **nao se le da API**. Depende de saber quais pontos
cada questao toca e como e o comentario dela, ou seja, sai do nosso fichamento. Os cadernos de
nivel 6 e 7 nao podem ser montados antes da passada de fichamento.

**Nao confundir com o rotulo de risco do BIZURITO**, que ai sim e percentual de acerto: questao
que muitos erram e a que "escorrega". Os cortes ainda vao ser definidos, e e por isso que o
**percentual exato precisa ser guardado** — ver [[project_censo_por_filtro_x_percentual]].

**Historico do erro:** a definicao certa ja estava registrada em
[[project_niveis_caderno_tec_e_pesos]] desde 20/08, e mesmo assim eu escrevi
`OURO = {'Medio','Dificil','Muito Dificil'}` no `compor_cadernos.py` e repeti o atalho na lista
de tarefas. Atalho por rotulo pronto e tentador justamente porque e barato; nao serve.
