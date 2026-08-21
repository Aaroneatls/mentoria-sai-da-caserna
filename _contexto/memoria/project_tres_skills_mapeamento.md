---
name: project-tres-skills-mapeamento
description: "Decisão de dividir o mapeamento de assuntos em 3 skills separadas (Estratégia, Bezerra, TecConcursos)"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-18T13:03:17.395Z
---

Elvis decidiu (2026-08-18) que o trabalho de mapeamento de assuntos (ver [[project_projetos_planilha_mapeamento_aulas]]) vai virar **3 skills separadas**, não uma só:

1. **Mapeamento de assuntos da área fiscal a partir das aulas do Estratégia Concursos** — extrai metadados (núcleo/secundário por subtópico, ver [[feedback_planilha_metadados_nucleo_secundario]]) dos PDFs de aula.
2. **Mapeamento dos resumos esquematizados do Bruno Bezerra** — mesmo processo de extração de metadados, aplicado aos PDFs de resumo.
3. **Mapeamento do TecConcursos** — extrai a taxonomia oficial de assuntos do Tec (via filtro `/questoes/filtrar` + "Editar quantidades" + exportar planilha) para uma matéria, cruzando com Área (Carreira) e outros filtros relevantes.

**Why:** cada fonte tem processo de extração bem diferente (PDF vs navegação/filtro no site), então faz mais sentido como skills independentes que depois alimentam a mesma base de compatibilização, em vez de uma skill monolítica.

**How to apply:** ao formalizar essas skills em `.claude/skills/`, criar uma pasta por skill (nomes sugeridos: `mapear-assuntos-estrategia`, `mapear-resumos-bezerra`, `mapear-assuntos-tecconcursos` — confirmar nomenclatura exata com Elvis antes de criar). Ainda não foi criada nenhuma skill formal até 2026-08-18 — tudo prototipado direto na planilha "teste mapeamento de aulas".
