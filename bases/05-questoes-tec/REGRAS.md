# Regras de acesso ao TecConcursos

Decididas em 21/08/2026, depois de a plataforma avisar que o acesso estava **"fora dos padrões
de um aluno habitual"**. O objetivo destas regras é um só: continuar eficiente sem nunca mais
provocar esse aviso.

> **Estas regras valem acima de qualquer conveniência de execução.** Se cumprir a regra
> significa demorar mais, demora mais.

## 1. O coletor questão a questão está PROIBIDO

Foi ele que gerou o aviso: ~2.300 requisições em poucas horas, batendo de rota em rota.
A impressão faz o mesmo trabalho com **1% do tráfego**.

Se `localStorage['coletor_src']` ainda existir no navegador, **apagar**, não executar.
Nenhuma sessão futura deve rearmá-lo.

O mesmo vale para os censos por filtro (`censo_src`, `censo_banca_src`): já cumpriram o papel
e não devem ser repetidos enquanto a impressão der conta.

## 2. A impressão é o único canal de volume

É o único lugar onde o Tec **publica o limite e mostra o contador**: 1.000 questões por dia,
blocos de até 200. Usar até o teto e **parar quando o contador zera**.

Nunca tentar passar do teto, nem testar se passa.

## 3. Um caderno-base, não um caderno por lote

O formulário de impressão tem `configuracoes.questaoInicial`. Com um caderno grande dá para
imprimir **fatias** dele (1-200, 201-400, ...) em vez de criar um caderno novo a cada lote.

Isso derruba a criação de cadernos de 28 para 1 por disciplina, e evita encher a pasta do Elvis
de `ZZ-COLETA`.

## 4. Criar caderno em ritmo de gente

Criar caderno é uso normal da plataforma; **criar 8 em dois minutos não é**. Espaçar.
O volume aqui é pequeno de qualquer jeito: ~260 requisições por disciplina inteira.

## 5. Depois de um 429, o dia acabou

Sem retentativa, sem escada de espera, sem sondagem para "ver se já liberou". Foi insistindo
que a conta virou padrão anômalo. Ver [[feedback_bloqueio_plataforma_como_agir]].

## 6. Uma conta só

Duas contas movidas por duas pessoas é uma coisa; uma segunda conta para dobrar um limite é
outra, e é exatamente o padrão que caracteriza burla. Recomendação retirada em 21/08/2026,
a pedido do Elvis, que levantou o risco de banimento.

## 7. A varredura de atualização repete os filtros da base

Uma vez por mês, pedir a lista de ids **com exatamente o mesmo conjunto de filtros que montou a
base**: assunto, anos da janela, as três bancas, e a limpeza (`REMOVER_ANULADAS`,
`REMOVER_DESATUALIZADAS`, `REMOVER_ADAPTADAS_INEDITAS`). Comparar com o banco:

| Comparação | Significado |
|---|---|
| Está no Tec, não está na base | questão nova, imprimir |
| Está nos dois | continua válida |
| Está na base, sumiu do Tec | virou anulada ou desatualizada, trocar nos cadernos |

**Se faltar um filtro, a comparação mente.** Em 21/08/2026 eu rodei sem o filtro de banca e o
Tec devolveu 292 questões onde a base tem 42: teria acusado 250 "novas" que são de bancas que a
gente não usa, e gastado ~600 chamadas para produzir lixo. Conferir a contagem por
`contagem/filtros` (1 chamada, devolve só o número) **antes** de puxar a lista.

**Custo:** com os filtros certos, cabe em ~1 chamada por assunto, ~72 por disciplina.

**Já verificado em 21/08/2026:** a base nasceu limpa. Nos assuntos 497, 503 e 512, a contagem
com limpeza bate exatamente com o que temos (42, 93 e 144). As sujas existem no acervo e ficaram
de fora.

## 8. O clique da verificação é do Elvis

Claude não clica em CAPTCHA, nem em "CONTINUAR", nem em "não sou um robô". Vale mesmo a pedido.

---

## O que isso custa

| | Requisições | Prazo |
|---|---|---|
| Direito Administrativo inteiro | **menos de 100** | 6 dias |
| As 8 disciplinas | ~600 | ~44 dias |

Contra ~11.000 requisições do caminho antigo. E cada disciplina pode ir ao ar assim que ficar
pronta, sem esperar o resto.
