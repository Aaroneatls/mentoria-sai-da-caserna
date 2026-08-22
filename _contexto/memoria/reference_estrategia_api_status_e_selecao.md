---
name: reference-estrategia-api-status-e-selecao
description: "Estratégia: 404 em pacote e 500 em curso significam a MESMA coisa (não matriculado); e produto se seleciona pelo id do href, nunca por texto do nome"
metadata:
  node_type: memory
  type: reference
---

Dois enganos que custaram tempo em 22-08-2026, os dois medidos:

**1. Status da API não fala de existência, fala de matrícula.**

| Endpoint | Sem matrícula | Com matrícula |
|---|---|---|
| `/api/aluno/pacote/{id}` | **404** | 200 |
| `/api/aluno/curso/{id}` | **500** | 200 |

Provado com produtos que sabidamente existem: PRF 226226 e ISS Manaus 396632 devolvem 404 quando fora da matrícula. **Nunca concluir "o produto foi removido" a partir de 404 ou 500** — foi esse engano que fez o "Regular Fiscal" parecer excluído do catálogo.

**2. Selecionar produto pelo id, nunca por casamento de texto.** Os nomes se contêm uns aos outros: um seletor que procurava "Sistema de Questões" para achar o pacote de Controle pegou o **TCDF**, cujo nome também termina em "+ Sistema de Questões" — e desmatriculou o pacote errado. Ancorar sempre no `href` `/app/dashboard/pacote/{id}` e subir para a linha a partir dele.

**Consequência de desenho:** o mesmo concurso tem **várias embalagens** com ids diferentes e a **mesma lista de disciplinas** (Regular Controle: 224364 = 12 disciplinas + Trilha/Bizu/Monitoria; 365538 = as mesmas 12 + Sistema de Questões). Então `pacote_id` identifica a embalagem, e o conteúdo é a lista de `curso_id`. Ver [[project-estrategia-matriculas-limite-coruja]] e [[reference-estrategia-busca-catalogo-abas]].

**Atenção:** `tipo_curso_id = 1` não garante disciplina — "Sistema de Questões 1 Ano - Cartão até 12 x" (143237) vem como tipo 1 e é assinatura. Filtrar por tipo 1 sem exclusão faz a skill tentar baixar um produto que não tem aula.
