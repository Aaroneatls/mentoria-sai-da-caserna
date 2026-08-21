---
name: project_limite_requisicao_tec_historico
description: historico de bloqueios do Tec fica no localStorage e no repo; objetivo e achar o padrao do limite para coletar sem depender do CAPTCHA do Elvis
metadata:
  type: project
---

**Objetivo (Elvis, 21/08/2026): autonomia.** Cada bloqueio do Tec hoje custa a atencao dele,
porque o desbloqueio vem por CAPTCHA e so ele resolve. Em vez de aceitar isso como fato da vida,
a gente **mede** o comportamento do limite ate achar o padrao, e ajusta ritmo e espera para
nunca mais bater nele.

**Onde fica:** `localStorage['historico']` no tecconcursos.com.br, que sobrevive a reload.
Exportar periodicamente para `mapeamento/historico_tec.json` no repo, porque localStorage pode
ser limpo. Eventos gravados: `arranque`, `bloqueio` (com quantas questoes desde a ultima
liberacao e em que ritmo), `espera`, `liberou_sozinho` (com quantos minutos ficou bloqueado),
`captcha_resolvido_pelo_elvis`, `fim`.

**O evento que mais importa e `liberou_sozinho`.** Se o 429 passar com o tempo, existe janela de
recuperacao e da para esperar em vez de chamar o Elvis. Por isso o coletor agora **espera longo
de proposito** (1, 2, 4, 8 min ate o teto de 30) em vez de desistir no terceiro 429. Marcar a
aba de vermelho avisa ele sem obrigar a agir.

**Medido ate agora (21/08/2026), nao chutado:**
- CAPTCHA resolvido as 21:49 de 20/08. Na manha seguinte, as 06:24, ainda vinha 429.
- CAPTCHA resolvido as 06:35 de 21/08: liberou na hora.
- Colheu **200 questoes (~400 requisicoes) em ~15 minutos** e travou de novo, com ritmo de 1,275s
  entre chamadas. Primeira hipotese a testar: o limite e por volume em janela curta, e 1,2s entre
  requisicoes e agressivo demais.

**Trava de geracao:** o coletor guarda `window.__GEN` e morre sozinho se outro for armado. Sem
isso, dois coletores escrevem o mesmo objeto `base` e um apaga o trabalho do outro. Ja quase
aconteceu ao trocar o formato da linha.

**Rearmar depois do CAPTCHA:** o codigo do coletor fica guardado em
`localStorage['coletor_src']`. Rearmar e `eval(localStorage.getItem('coletor_src'))`, uma linha,
porque o reload mata o script mas nao o localStorage. Ver [[feedback_bloqueio_plataforma_como_agir]].
