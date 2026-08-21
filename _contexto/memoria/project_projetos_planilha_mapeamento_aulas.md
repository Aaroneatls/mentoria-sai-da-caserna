---
name: project-projetos-planilha-mapeamento-aulas
description: "Planilha \"teste mapeamento de aulas\" no Drive — base pra futura skill de mapeamento de aulas a partir de PDFs"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-17T15:09:42.456Z
---

Existe uma planilha do Google Sheets chamada "teste mapeamento de aulas" em `Inteligência Artificial/Projetos/` no Drive (URL: https://docs.google.com/spreadsheets/d/1pkppkmt9zdMLUUwL49-b84XROhQpipLcCBaM2xM4c88/edit), criada como protótipo pra uma skill nova que Elvis quer construir: mapear um conjunto de PDFs de aulas (baixados pelas skills `baixar-curso-especifico-estrategia` / `baixar-curso-completo-estrategia`) numa base estruturada.

Abas:
- **Base Geral**: cabeçalho na linha 10 (ver [[feedback_planilha_projeto_padrao_cabecalho]]), colunas Cód, Assunto, Tópicos da Aula, Metadados (ver [[feedback_planilha_metadados_nucleo_secundario]]), Nº da Aula, Nº Pags Teoria, Nº de Questões, Nº Total de Páginas.
- **Parâmetros**: tabela Disciplina → Sigla (DADM, DCON, CONGA, DTRI são as 4 disciplinas de teste, baseadas no pacote "ISS Manaus (AFTM) 2026" em `G:\Meu Drive\Inteligência Artificial\Estrategia`).

**Why:** é uma planilha de teste/protótipo — os dados nela vieram de 4 disciplinas com 2 aulas cada (dataset reduzido pra validar formato antes de rodar em escala).

**How to apply:** quando a skill de mapeamento de aulas for formalizada, usar essa planilha e essa estrutura como referência de formato validado (cabeçalho linha 10, metadados núcleo/secundário). Perguntar se o objetivo final é replicar esse mesmo formato pra outros concursos/disciplinas ou se a estrutura ainda vai mudar.
