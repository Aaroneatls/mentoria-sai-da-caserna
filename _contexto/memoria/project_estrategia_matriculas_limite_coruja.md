---
name: project-estrategia-matriculas-limite-coruja
description: "Estratégia limita a 3 matrículas simultâneas; matricular e desmatricular exigem digitar CORUJA; qualquer pacote pode entrar no rodízio e a busca no catálogo é sempre por pacote"
metadata:
  node_type: memory
  type: project
---

A assinatura vitalícia do Estratégia (conta da Gisilene, ver [[project-conta-estrategia-compartilhada]]) permite **no máximo 3 produtos matriculados ao mesmo tempo**. Produto que não está em "Produtos matriculados" não abre: a página do pacote vem vazia e a API devolve **HTTP 500** (500 = sem matrícula, não "curso removido"). Aprendido em 19/20-08-2026.

**Fluxo, em `/app/dashboard/assinaturas`:**
1. Se os 3 slots estiverem cheios, clicar `DESMATRICULAR` no produto que vai sair, digitar `CORUJA` e confirmar.
2. Buscar o produto desejado na aba **PACOTES**, clicar `MATRICULAR` e digitar `CORUJA`.
3. Recarregar — ele aparece em "Produtos matriculados" com o `href` `/app/dashboard/pacote/{id}`.

**Três regras confirmadas pelo Elvis em 20-08-2026:**

- **`CORUJA` vale nos dois sentidos**, matrícula e desmatrícula.
- **Qualquer pacote pode entrar ou sair do rodízio, inclusive o da PRF** — não há mais pacote intocável. Fazer isso quando a tarefa pedida exigir, sem perguntar de novo.
- **Procurar sempre por PACOTE**, nunca por curso: o que o Elvis chama de "curso" é um pacote no Estratégia, e as disciplinas dentro têm nomenclatura diferente (o pacote `Curso Regular para Área Fiscal - Pacote Completo` (id 220865) contém `Concursos da Área Fiscal - Curso Básico de Direito Administrativo`). Buscar por curso faz o produto "sumir" do catálogo sem ter sumido.

**How to apply:** na busca da API usar `GET /api/assinatura/curso/search?q=<nome>&type=pacote&size=51&page=N` com o mesmo Bearer das skills. Antes de desmatricular, conferir placeholders `.txt` (aulas ainda não publicadas) da pasta daquele pacote no Drive e avisar o Elvis, porque essas aulas ficam inacessíveis enquanto ele estiver fora.


## Rodízio é livre (Elvis, 2026-08-20)

Matricular e desmatricular **não precisa de autorização prévia**. A regra antiga (checar
placeholders `.txt` e avisar antes) **caiu**.

A única checagem obrigatória: **alguma sessão em andamento está usando, baixando ou
acessando aquele produto?** Se não estiver, pode trocar à vontade pra executar a tarefa.
Placeholder `.txt` só importa se o pacote que vai sair estiver em uso naquele momento.

## Correção: nem tudo se acha na aba PACOTES (2026-08-20)

A regra "buscar sempre por PACOTE" vale pro **pacotão de um concurso**. Material granular
— **Bizu Estratégico, Passo Estratégico, Monitoria, Trilha, Discursiva** — só aparece na
aba **CURSOS**, e buscar por ele em PACOTES devolve zero enganoso.
Ver [[reference_estrategia_busca_catalogo_abas]].
