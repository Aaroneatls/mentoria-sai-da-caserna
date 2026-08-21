---
name: feedback_bloqueio_plataforma_como_agir
description: o 429 do Tec e da CONTA e vem do proprio Tec, nao da AWS; desacelerar nao ajuda e retentar mantem preso
metadata:
  type: feedback
---

**O 429 do TecConcursos vem do proprio Tec** (nginx, corpo `{"error": "Too Many Requests"}`),
**nao da AWS WAF**. O CAPTCHA da Amazon e um sistema separado, na frente do site. Confundir os
dois leva a pedir CAPTCHA ao Elvis quando o que faltava era so tempo: nas duas vezes de
21/08/2026 passaram-se ~12 minutos entre travar e voltar, e o CAPTCHA no meio provavelmente foi
coincidencia.

**O bloqueio e da CONTA, nao do IP.** Medido em 21/08: mesma conexao e mesmo instante, com o
cookie da conta veio 429, sem cookie nao veio. Consequencia pratica: **uma segunda conta tem
orcamento proprio** e da para dividir os assuntos entre as duas. Antes de fazer isso, conferir
os termos do Tec, e a decisao e do Elvis.

**Desacelerar NAO ajuda** (contraintuitivo, medido): a 1,3s por chamada a conta aguentou 400
chamadas em 15 min; a 4s aguentou **218** em 27 min. Mais devagar travou antes. O bloqueio e
**global**: com a conta de castigo, ate `/api/enums/universos` devolve 429.

**Como agir: silencio TOTAL, e uma unica sondagem no fim.** Quanto tempo, ainda **nao esta
medido**. Em 21/08 as 11:03 o acesso voltou depois de ~19 min de silencio, mas o Elvis acha que
foi ele quem clicou na verificacao, entao **o teste nao vale**. Refazer com ninguem clicando.

**Sondar durante o castigo reinicia o castigo.** O teste de 60 minutos que eu tinha feito de
manha e que "provou" que esperar nao adianta estava **viciado**: eu sondava no meio (08:02,
08:03, 08:04, 09:05). Cada sondagem zerava o relogio. Nao ha escada de retentativa que
funcione; o que funciona e nao chamar.

Consequencia direta: um coletor que checa de 45 em 45 segundos "para perceber rapido quando
liberar" **impede** a liberacao. Descansar 20, 30, 40 minutos em silencio e o certo.

**Cuidado com 200 + HTML:** sem sessao o Tec responde 200 com pagina de login. Conferir o
corpo, nunca so o status. Ver a regra geral de download no AGENTS.md, que nasceu do mesmo erro.

**Historico:** `mapeamento/historico_tec.json` no repo, alimentado tambem por
`localStorage['historico']`. Ver [[project_limite_requisicao_tec_historico]].
