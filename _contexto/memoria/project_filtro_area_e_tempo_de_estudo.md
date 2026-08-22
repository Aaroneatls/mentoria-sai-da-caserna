---
name: project_filtro_area_e_tempo_de_estudo
description: coleta precisa filtrar por AREA do concurso, senao entra questao de cargo especifico; e o tempo do caderno sai do tempoMedio real do Tec
metadata:
  type: project
---

## Filtrar por area do concurso (Elvis, 22/08/2026)

O criterio de coleta combinado era `assunto + banca + ano`, e ele **nao olha o cargo**. Entra
questao de Contabilidade cobrada em prova de **Contador**, bem mais profunda que a de Auditor
Fiscal, e questao de TI de prova de Analista de TI.

O Tec tem o filtro: `/api/enums/areas` devolve `FISCAL`, `GESTAO_CONTROLE_TRIBUNAIS` e outros.
O criterio passa a ser **`assunto + banca + ano + area`**.

**Medir antes de aplicar:** filtro restritivo demais troca contaminacao por escassez. Ao definir
a janela de anos de cada materia, comparar a contagem **com e sem** o filtro de area. Custa uma
chamada a mais por materia.

## Tempo de estudo do plano

A Tutory pede minutagem por meta. Tres componentes:

| Componente | Fonte |
|---|---|
| Teoria | paginas do bloco x minutos por pagina (**a calibrar**) |
| Questoes | **`tempoMedio` do Tec**, dado real de milhares de alunos |
| Releitura do resumo | paginas do resumo x ritmo mais leve (**a calibrar**) |

`GET /api/questoes/{id}/desempenho` traz `tempoMedio` em segundos (71 na amostra de 21/08). Um
caderno soma o tempo real das questoes que tem dentro.

Para calibrar a teoria, o painel do aluno tem "Tempos de Estudos" e "Horas Liquidas (cronometro)":
se forem acessiveis, o minutos-por-pagina sai do comportamento real dos alunos do Elvis.
