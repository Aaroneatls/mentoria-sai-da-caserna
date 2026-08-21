---
name: reference-estrategia-busca-catalogo-abas
description: "Buscar produto no catálogo do Estratégia: a aba não troca com clique por coordenada, e a busca é OR — resultado vazio ou gigante engana"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 72f48c50-c074-40da-aadd-30e541792bed
  modified: 2026-08-20T12:04:36.876Z
---

Descoberto em 2026-08-20 procurando "Bizu Estratégico". Concluí que o Bizu **não existia
como produto** porque a busca voltava zero. Estava errado: existem **122** cursos Bizu no
catálogo. O zero era artefato da interface.

## As duas armadilhas

**1. Clicar na aba por coordenada não troca a aba.** Em `/app/dashboard/assinaturas`, as
abas `PACOTES / CURSOS / PROFESSORES / MATÉRIAS` não reagem ao clique sintético por pixel
— a listagem continua em PACOTES. Só funciona chamando `element.click()` direto no
`<button>`:

```js
[...document.querySelectorAll('button')]
  .find(b => /^Cursos$/i.test(b.textContent.trim())).click()
```

Conferir depois, sempre: a aba ativa tem `class="Tab isActive"`.

```js
[...document.querySelectorAll('button')].filter(b => /isActive/.test(b.className))
                                        .map(b => b.textContent.trim())
```

**Nunca acreditar em busca vazia sem antes checar qual aba está ativa.** Material que só
existe como curso (Bizu, Passo Estratégico, Monitoria, Trilha) devolve zero na aba
PACOTES, e o zero parece legítimo.

**2. A busca é fuzzy (OR), não AND.** "Bizu Receita Federal" devolve 3772 resultados
casando só "Receita" ou "Federal", e os primeiros nem são Bizu. Contagem alta não
significa que achou — ler os primeiros itens é obrigatório. Idem "Curso Estratégico":
3632 resultados, nenhum produto com esse nome, só casamento solto das duas palavras.

## Para escrever no campo

O React não enxerga `type` do navegador nem `Enter` (que ainda limpa o campo). Setar pelo
setter nativo e disparar `input`:

```js
const i = document.querySelector('input[placeholder="Pesquisar..."]');
Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(i,'Bizu');
i.dispatchEvent(new Event('input',{bubbles:true}));
```

Dá uns 3-4s de debounce antes de ler o resultado.

## Qual caminho usar

| Pergunta | Caminho |
|---|---|
| O que tem dentro de um pacote **já matriculado**? | `GET /api/aluno/pacote/{id}` → campo `tipo_curso_id` (1=Regular, 3=Monitoria, 5=Trilha, 7=Passo, 27=Bizu) |
| O que **existe no catálogo** e pode ser matriculado avulso? | Aba **CURSOS** da tela de assinaturas |

Buscar por PACOTE continua valendo pra achar o pacotão de um concurso
([[project_estrategia_matriculas_limite_coruja]]) — o que muda é que material granular
(Bizu, Passo, Monitoria) **só aparece na aba CURSOS**.

Ver [[project_estrategia_matriculas_limite_coruja]] e
[[project_detector_tipografico_titulos_estrategia]].
