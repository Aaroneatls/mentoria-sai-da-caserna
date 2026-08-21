---
name: project-base-propria-de-pesos-substitui-tec
description: "Os percentuais de incidência passam a ser calculados da NOSSA base de fichamento, não da exportação de relevância do Tec; e precisam ser fatiáveis por banca"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-19T20:57:34.398Z
---

Decidido por Elvis em 2026-08-19.

## A decisão

O peso/percentual de incidência passa a ser **calculado da nossa base de fichamento**
(ver [[project_banco_fichamento_questoes]]). A aba **"Base Tec Concursos"**, hoje alimentada
pela exportação de "Relevância (apenas assuntos)", **sai de cena** assim que a nossa base cobrir
a janela de 10 anos daquela disciplina.

**A troca é por disciplina, não de uma vez.** Enquanto o fichamento de uma disciplina não fechar
a janela, o número do Tec continua valendo pra ela. Ao fechar, comparar os dois lado a lado
antes de confiar.

## Por que a nossa é superior

1. **Granularidade.** O Tec dá um número por assunto. Dentro de *um* assunto dele ("Princípios
   Implícitos"), o fichamento de 2026-08-19 achou 8 pontos com distribuição bem desigual:
   supremacia 4, autotutela 3, segurança jurídica 3, continuidade 2, igualdade 2,
   proporcionalidade 1, indisponibilidade 1, verdade material 1.
2. **Peso por aula do Estratégia — só a nossa base produz.** O Tec não conhece o Estratégia; não
   existe caminho pra extrair dele quanto pesa a Aula 06. Só a cadeia ponto → tópico mestre →
   aula dá esse número, que é justamente o que se usa pra montar cronograma.
3. **O peso do Tec carrega erros de classificação.** No teste, **3 das 16** questões do balde do
   DADM-001 pertenciam a outros tópicos, e uma questão do balde de princípios era da Lei 13.460.
4. **Questão que cobre vários pontos.** O Tec conta 1 questão = 1 assunto; nosso modelo conta
   1 questão = N pontos, o que é mais fiel ao que a prova cobra.

**Nada se perde:** a coluna "Assunto no Tec" fica guardada em cada questão fichada, então a
visão do Tec é reproduzível a qualquer momento. Nossa base é superconjunto.

## O peso tem que ser FATIÁVEL POR BANCA (Elvis, 2026-08-19)

No **pós-edital**, o peso que vale é o **da banca do edital**, não o geral — é isso que permite
selecionar questão com a cara daquela banca. Então a banca é **dimensão de cálculo**, não só
coluna descritiva: os mesmos pontos precisam render percentual global (pré-edital) **e**
percentual por banca (pós-edital), a partir da mesma base.

**Consequência prática — o fichamento não pode ser restrito a uma banca.** O teste de
2026-08-19 fichou **só Cebraspe**, então ele não permite fatiar. Para a base valer, é preciso
fichar a janela **cobrindo as bancas de interesse**, com a banca registrada em cada questão.

**Volume (área Controle, matéria 1, 2017-2026):**

| Recorte | Questões |
|---|---|
| Só Cebraspe | 1.111 |
| Cebraspe + FGV | 1.672 |
| Cebraspe + FGV + FCC | 1.778 |
| Todas as bancas | 4.475 |

**Recomendação:** fichar as **três bancas principais** (1.778). Custa ~60% a mais que só a
Cebraspe e destrava o peso por banca; fichar todas custaria 4x por bancas que não interessam ao
público-alvo.

### As duas visões de peso (Elvis, 2026-08-19)

São **duas visões sobre a MESMA base**, não duas bases a manter. O fichamento é um só, com a
banca gravada em cada questão; o que muda é o recorte de leitura.

| Visão | Composição | Quando se usa |
|---|---|---|
| **Composta** | Cebraspe + FGV + FCC, dentro da área | **Pré-edital** |
| **Por banca** | uma banca isolada | **Pós-edital** (a banca do edital) |

### Regra de fallback quando a amostra da banca é pequena

1. Pós-edital usa, por padrão, o peso **da banca do edital**.
2. Se a amostra daquela banca for **pequena demais** naquele ponto, usa o **compilado das três**
   — sempre **marcando** que houve substituição e qual visão foi efetivamente usada.
3. Se nem assim der pra mensurar, usar as **outras bancas como referência**, também marcado.

### ALERTA OBRIGATÓRIO: divergência entre as visões

Quando a amostra da banca for pequena e o número vier do composto, **o percentual pode sair
distorcido** — alto ou baixo demais — porque está carregando o comportamento das outras bancas.

**Nesses casos a skill tem que alertar o Elvis para conferência caso a caso.** Não decide
sozinha, não entrega o número como se fosse da banca. O alerta mostra: o percentual da banca, o
percentual composto, o tamanho da amostra de cada um e a diferença entre eles.

**Cuidado geral com amostra:** fatiar por banca **divide a amostra**, e no nível do ponto ela já
é pequena (supremacia = 4 questões em 10 anos só na Cebraspe). Além do fallback acima, cabe
**subir a agregação** (ponto → tópico → aula), sempre sinalizando qual nível foi usado.

## Duas travas obrigatórias no cálculo

1. **O denominador inclui os não classificados.** Fichar **toda** a janela; o que não couber em
   nenhum ponto vai pra um balde de **não classificados** que **continua entrando na conta**.
   Sem isso o percentual vira "porcentagem do que eu mapeei" e infla pra cima.
2. **Piso de confiança no nível do ponto.** Amostra fina é frágil (supremacia = 4 questões em 10
   anos). Calcular no ponto, **reportar a confiança junto**, e subir a agregação quando magra.
   Ver [[project_niveis_caderno_tec_e_pesos]].

## As estatísticas do Estratégia NÃO entram (Elvis, 2026-08-20)

O material do Estratégia vem com percentual de incidência pronto em pelo menos três lugares:

- **Passo Estratégico**, seção `ANÁLISE ESTATÍSTICA` (por banca e cargo do concurso)
- **Passo Estratégico**, aula avulsa "Análise Estatística da Matéria"
- **Bizu Estratégico**, p3 (junta Cebraspe + FCC + FGV da área inteira)

**Nada disso entra como referência.** Nem para compor, nem para conferir. O banco de pesos é
nosso e sai do fichamento — o número deles fica de fora da conta e não vale como validação
cruzada.

Motivo: são recortes de amostra que não controlamos (janela, banca e área variam de material
para material, e nenhum deles declara o denominador), e a granularidade é de assunto, não de
ponto. Misturar isso com a nossa base contamina o número sem ganho nenhum.

Isso é mais forte que a regra do Tec logo abaixo: **o Tec continua servindo de conferência de
recorte; o Estratégia não serve nem para isso.**

## O que o Tec continua sendo

- **Conferência do recorte:** nosso 1.111 bateu com os 1.136 do guia do TCDF. Divergência grande
  vira sinal de erro no filtro.
- **Árvore de descoberta:** é por ela que se encontram as questões pra fichar.
