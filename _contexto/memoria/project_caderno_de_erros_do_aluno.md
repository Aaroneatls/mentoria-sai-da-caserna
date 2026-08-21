---
name: project-caderno-de-erros-do-aluno
description: "Ideia futura: o aluno envia as questões que errou e recebe caderno novo dos mesmos pontos mais um BIZURITO específico"
metadata:
  type: project
---

Levantado pelo Elvis em 2026-08-20. **Para o futuro, não agora.**

## A ideia

O aluno manda o caderno de erros dele. A partir dos pontos que ele errou, o sistema devolve:

1. um **caderno novo** com outras questões dos mesmos pontos
2. um **BIZURITO específico** só com aqueles pontos

## Avaliação: é factível, e a parte difícil já está sendo construída

Com o fichamento pronto (questão → ponto → Cód Mestre), a geração é quase mecânica:

```
lista de # errados -> nossos pontos -> outras questoes dos mesmos pontos -> caderno
                                   -> mesmos pontos -> BIZURITO so' com eles
```

**O gargalo é a entrada, não a saída.** O histórico de acertos vive na conta do aluno. Os
filtros `REMOVER_AS_QUE_ACERTEI` e `REMOVER_ERRADAS` do Tec só enxergam o usuário logado —
ver [[reference_tec_api_desempenho_e_filtros]].

Dois caminhos:

- **Manual leve:** o aluno filtra "questões que errei" no Tec e cola os números num formulário.
  Funciona hoje, sem sistema nenhum, e já entrega o valor.
- **Automatizado:** o aluno cola o link de um caderno dele. Precisa testar se o Tec expõe
  desempenho de terceiro — provavelmente não, por privacidade. **Não testado.**

## Pré-requisito

O fichamento completo. Sem a ligação questão → ponto, não há como saber o que o erro dele
significa. Ver [[project_banco_fichamento_questoes]] e
[[project_cadernos_cobertura_e_composicao_propria]].

## Desenho fechado em 2026-08-20

O desenho completo (fluxo, achados ao vivo no Tec, janela mensal de pedidos, biblioteca de
cadernos de reforço, alocação por ponto e pedidos pra janela do mapeamento) está em
`_contexto/briefing-sistema-caderno-de-erros.md`. Consultar lá antes de retomar.
Ver também a Camada 6 em [[project_bizurito_validacao_conteudo]].
