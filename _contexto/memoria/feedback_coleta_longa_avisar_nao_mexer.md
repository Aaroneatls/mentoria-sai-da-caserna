---
name: feedback-coleta-longa-avisar-nao-mexer
description: "Antes de iniciar coleta longa no navegador embutido, avisar que ninguém pode navegar na aba — navegar mata o script e a coleta para em silêncio"
metadata:
  type: feedback
---

Definido pelo Elvis em 2026-08-21, depois de duas coletas perdidas.

## A regra

**Antes de começar qualquer coleta longa que rode dentro da página**, avisar explicitamente:

1. **Não navegar na aba do navegador embutido.** Trocar de página apaga o script em execução.
   O dado já salvo em `localStorage` sobrevive, mas a coleta **para em silêncio** — nada avisa,
   e só se descobre ao conferir o progresso.
2. **Não fechar a aba.** Fechar leva o `localStorage` junto e perde tudo.
3. **O Chrome normal do Elvis pode ser usado à vontade** — é outra janela, não interfere.

## O que custou

Na sessão de 2026-08-20 a coleta da base do TecConcursos morreu **duas vezes** por navegação:

- primeira: o app do Tec redirecionou sozinho e zerou o contexto da página
- segunda: durante a noite alguém abriu um caderno na mesma aba; a coleta parou em
  **408 de 5.463 questões (7%)** e ficou parada horas

## Como reduzir o estrago

- **Persistir em `localStorage` a cada lote pequeno** (10 a 15 itens), nunca só no fim. Foi o
  que salvou as 408 já coletadas.
- **Escrever o coletor para ser retomável**: ao religar, ele lê o que já existe e continua de
  onde parou, sem repetir requisição.
- **Conferir o progresso periodicamente** em vez de confiar que está rodando. Coletor morto e
  coletor lento parecem a mesma coisa de fora.

Ver [[feedback_bloqueio_plataforma_como_agir]] e
[[reference_tec_api_desempenho_e_filtros]].
