# Autorizações do Elvis

> Recado de sessão é **aviso**; decisão se confere **aqui**. Um agente que recebeu autorização por
> mensagem de outro agente pode verificar neste arquivo antes de executar — é o que o
> `agentes/README.md` manda, e é o certo.
>
> Só o coordenador escreve aqui, e só o que o Elvis disse de fato.
>
> ### Decisão refinada exige linha nova, na hora
>
> Em 22/08 este arquivo ficou **apontando para uma versão descartada** do esquema de siglas por
> algumas horas: a autorização original foi registrada, o esquema foi refinado depois, e a linha
> não acompanhou. O `ESP-TAXONOMIA` percebeu e avisou — se não tivesse, uma sessão nova poderia ler
> daqui, criar um ente pela regra velha e **congelar a sigla errada**.
>
> **Registro desatualizado é pior que registro ausente**, porque ele é consultado com confiança.
> Refinou, escreve na hora; e a linha antiga fica, apontando para a nova.
>
> **Quando a aprovação for geral** (*"de acordo com o que você decidiu"*), registrar assim, com a
> frase literal e o que estava em cima da mesa naquele momento — nunca como se ele tivesse
> aprovado ponto a ponto.

| Data | O que ele autorizou | A quem |
|---|---|---|
| 22/08/2026 | **Reescrever os Passos 2/6, 7/9 e 9/11** das duas skills de download, eliminando as instruções antigas de nome de pasta em vez de conviver com elas. Palavras dele: *"Perfeito! Pode fazer os ajustes. Concordo com os dois pontos aí."* | `ESP-ACERVO` |
| 22/08/2026 | **A data desce para o nível da disciplina** e sai do nível do concurso (REGRA 9). Mesma mensagem. | todos |
| 22/08/2026 | **Rodízio de matrícula é livre**, sem pedir autorização; só registrar as trocas. A única checagem é se alguma sessão está usando o produto naquele momento. | `ESP-ACERVO` |
| 22/08/2026 | **`atualizar` em vez de reconstrução** nos dois Regulares, Controle primeiro e validado antes do Fiscal. | `ESP-ACERVO` |

| 22/08/2026 | **Matricular e desmatricular à vontade** no Estratégia, em qualquer curso. Ele confirmou que foi ele mesmo que tirou o Regular Fiscal e pôs o PRF. Palavras dele: *"pode mudar à vontade. Pode desmatricular e matricular lá em curso. Tem problema não."* | `ESP-ACERVO` |

| 22/08/2026 | **Desmembrar a `LTRIB`** em `LTEST`, `LTMUN` e `LTFED`, mais família por ente. Palavras dele: *"Pra mim tá show."* **O esquema de siglas foi refinado depois — ver a linha seguinte, que é a que vale.** | `ESP-TAXONOMIA` |
| 22/08/2026 | **Esquema de siglas por ente, versão final.** Estado `LT`+UF · município capital `LTM`+UF · município não-capital `LTM`+UF+inicial · **Distrito Federal `LTDF` e só** (não existe `LTMDF`) · empate resolvido pelo `nomes-congelados.csv`, nunca pela fórmula. Aprovação **geral**, nas palavras dele: *"em relação ao OK e às decisões que você tomou, sou de acordo"* — dita logo após o coordenador apresentar este esquema. | `ESP-TAXONOMIA` |

| 22/08/2026 | **Renomeação aprovada e execução liberada.** `<SIGLA> - <Disciplina> (DD-MM-AAAA)` nas pastas e `<SIGLA> - Metadados` nas planilhas. Palavras dele: *"Em relação à renomeação, tá ok"* e *"pode dar sequência aí"*. | `ESP-ACERVO` |
| 22/08/2026 | **Escopo: só os dois Regulares.** `Pacotaço TCDF` e `ISS Manaus` **não** são atualizados agora, e ele **vai excluí-los depois** — então não gastar trabalho neles. Palavras dele: *"esses cursos depois eu vou excluir o ISS Manaus e o do TCDF"*. **A exclusão é dele, não de agente.** | `ESP-ACERVO` |

| 22/08/2026 | **Autonomia plena de matrícula, reafirmada.** O especialista matricula e desmatricula sem perguntar. Palavras dele: *"você tem livre autonomia pra matricular ou desmatricular os cursos ali... eu deixo isso já como uma regra geral pra você não precisar perguntar pra mim"*. **A única checagem: alguma sessão NOSSA está usando aquele produto neste momento?** Não estando, roda. | `ESP-ACERVO` |

---

## O que NUNCA é autorizado

**COMPRA DE QUALQUER ESPÉCIE.** Dito pelo Elvis em 22/08, junto com a liberação do rodízio:
*"Só não pode fazer nenhum tipo de compra."*

Nenhum agente compra curso, pacote, assinatura, plano ou upgrade — em nenhuma plataforma, com nenhum
meio de pagamento, ainda que já cadastrado, e ainda que a tarefa fique bloqueada sem aquilo. Curso
que exige compra vira **pendência para o Elvis**, nunca decisão de agente.

Vale igual para o Estratégia, o TecConcursos (inclusive o plano avançado que libera questão inédita)
e a Tutory.

---

**Condição que vale para as quatro primeiras:** nada é executado antes de o Elvis ler o **diff dos passos
tocados** e liberar. A autorização é para *reescrever a skill*, não para *rodar*.
