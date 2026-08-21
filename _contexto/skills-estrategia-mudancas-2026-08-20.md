# Prévia das mudanças nas skills do Estratégia — 2026-08-20

> **Por que este arquivo existe.** É o registro legível do que mudou nas skills: se o
> `SKILL.md` for revertido ou alguém precisar entender a mudança sem ler o diff, dá para
> reconstruir tudo a partir daqui.
>
> **Status do git:** commitado e sincronizado em 2026-08-20. As seções descritas abaixo
> estão no repositório.
>
> Arquivos alterados:
> - `.claude/skills/baixar-curso-especifico-estrategia/SKILL.md` — +156 linhas, −9
> - `.claude/skills/baixar-curso-completo-estrategia/SKILL.md` — +159 linhas, −3
> - `AGENTS.md` — +9 linhas, −1

---

## 1. Sufixo `LS` / `LC` no nome do arquivo

**Vale só para o Curso Regular.** Passo, Bizu, Trilha, Monitoria e Rodadas têm card único,
sem distinção de versão — nome sem sufixo.

```
<Rótulo exato da aula> - Assunto Sintético [LS|LC] (DD-MM-AAAA).pdf
```

| Sufixo | Significa | Quando usar |
|---|---|---|
| `LS` | **Livro Simplificado** | baixou o `pdf_simplificado` |
| `LC` | **Livro Completo** (original) | baixou o `pdf` |

Exemplos reais:

```
Aula 03 - Fundações, empresas públicas e sociedades de economia mista LS (30-07-2026).pdf
Aula 18 - Improbidade administrativa - Lei 8.429-1992 LC (30-07-2026).pdf
```

**Motivo:** o mapeamento ancora o aluno por número de página, e as duas versões têm
paginações diferentes. Como a skill prioriza o simplificado e cai pro original quando não
existe, a pasta fica mista — no TCDF-ANACE, 54 de 180 aulas (30%) só têm o completo, e
quatro disciplinas não têm simplificado nenhum.

**O sufixo reflete o que foi REALMENTE baixado, não o que a API oferecia.** Quando a
detecção de stub rebaixa a aula na versão original, o arquivo é `LC` mesmo com
`pdf_simplificado` presente na API.

*(Skill específica: seção "Nome do arquivo". Skill completa: seção "Nome do arquivo —
rótulo exato da aula", mais a linha do Curso Regular.)*

## 2. Modo atualização reconhece o formato antigo

Sem isso, a próxima execução criaria **dois arquivos por aula**.

- **Casar pelo rótulo (`Aula NN`), nunca pelo nome completo.**
- **Atualização Parcial:** não rebaixar; só renomear acrescentando o sufixo. Se
  `pdf_simplificado` não existe na API → `LC`. Se existe, comparar o nº de páginas do
  local com o do original: igual = rebaixe por stub, logo `LC`; diferente = `LS`.
- **Atualização Completa:** o rebaixe resolve — gravar com sufixo e apagar o arquivo
  antigo. Conferir que sobrou só um arquivo por aula.

*(Skill específica: "Modo atualização — o que pular". Skill completa: "Modo atualização —
o que baixar".)*

## 3. Planilha de metadados ganhou campos

| Onde | Campo | Serve pra |
|---|---|---|
| Aba "Aulas" | **`Versão do Livro`** (`LS`/`LC`/`—`) | paginação por aula; disciplina 100% `LC` avisa que não tem simplificado. Vale duas células de resumo com `=COUNTIF()` |
| Subtítulo | **`Tipo de Material`** | `Curso Regular`, `Passo Estratégico`, `Bizu Estratégico`, `Trilha Estratégica`, `Monitoria`, `Rodadas de Simulados`, `Discursiva` |
| Subtítulo | **`Nome do Pacote`** (exato) | é o nome de busca no catálogo |
| Subtítulo | **`Pacote ID`** + link `=HYPERLINK(".../pacote/{id}";"Abrir pacote")` | voltar direto ao produto, e detectar pacote que saiu do ar |

**Vale nos dois modos** — ao criar do zero e ao atualizar. Em planilha antiga sem esses
campos, **acrescentar** sem reescrever o resto.

O `Tipo de Material` sai do `tipo_curso_id` de `GET /api/aluno/pacote/{id}`:
`1`=Curso Regular, `3`=Monitoria, `5`=Trilha, `7`=Passo Estratégico, `27`=Bizu,
`30`=Rodadas de Simulados.

**Por que o pacote importa:** a matrícula é limitada a 3 produtos e o rodízio é constante,
então reencontrar o pacote certo no catálogo já custou tempo. Com nome exato e ID
guardados, vai direto — e se o `pacote/{id}` não abrir mais, o material daquela pasta
virou histórico.

## 4. Nova seção: conferir versão sem baixar o PDF (técnica do `Range`)

O endpoint aceita requisição parcial. `Range: bytes=0-99` devolve `206` com
`Content-Range: bytes 0-99/<TAMANHO TOTAL>` — **100 bytes trazem o tamanho exato do
arquivo remoto**.

```python
UA = {'User-Agent': '<UA de browser>', 'Referer': 'https://www.estrategiaconcursos.com.br/',
      'Range': 'bytes=0-99'}
r = requests.get(url_assinada, headers=UA, timeout=60)
tamanho_remoto = int(r.headers['Content-Range'].split('/')[-1])
```

| Diferença local × remoto | Significa |
|---|---|
| 4 a 30 bytes | mesmo arquivo (variação da marca d'água gerada na hora) |
| megabytes | outra versão |

Limiar: `dif < max(2000, tamanho_local * 0.002)`.

**Identificar o stub por aqui:** o stub tem sempre ~**699 KB**. Se o remoto vier nesse
tamanho e o local for muito maior, o arquivo é `LC`.

**Duas armadilhas:** `HEAD` devolve `404` (só `GET` com `Range`), e **não funciona pelo
`javascript_tool`** — `Content-Range` não é header seguro de CORS e volta `null`. Tem que
ser do shell, com o link assinado.

**Onde usar:** auditar pasta depois de um mutirão, conferir se o PDF local ainda bate com
o do site antes de rebaixar em Atualização Completa, e preencher o sufixo de coleta antiga
sem refazer download.

**Validação do método:** conferiu 56 aulas de Contabilidade do Regular Controle e achou
**exatamente os 19 rebaixes por stub** que a skill já tinha registrado.

*(Seção "Conferir versão/integridade sem baixar o PDF" nas duas skills.)*

## 5. Nova seção: ARMADILHA do assunto terminado em "LC" ou "LS"

Ao decidir se um arquivo **já tem** o sufixo, é tentador testar o fim do nome:

```python
re.search(r' L[SC] \(\d\d-\d\d-\d\d\d\d\)\.pdf$', nome)   # ERRADO
```

Isso casa por acidente com assunto que termina em `LC` — comum em matéria jurídica (Lei
Complementar). Caso real:

```
Aula 12 - Previdência complementar - LC 108-2001 e LC (22-07-2026).pdf
```

O arquivo não tinha sufixo, foi tratado como se tivesse, ficou de fora do lote, e depois
foi lido como `LC` quando era `LS`. Um caso em 1096 PDFs — e sem a conferência por `Range`
passaria batido.

**Como fazer certo:**

1. **Nunca deduzir a versão lendo o nome do arquivo.** A fonte é a API ou o log da coleta.
2. Para saber se o lote já rodou, **conferir a contagem**: nº de PDFs na pasta contra nº
   de linhas no log. Divergência de 1 já é sinal.
3. Se precisar testar pelo nome, comparar com a lista de aulas da API em vez de confiar na
   regex.
4. **Sempre fechar com conferência por amostra.**

*(Seção "ARMADILHA: assunto que termina em 'LC' ou 'LS'" nas duas skills.)*

## 6. Skill completa: armadilhas da busca no catálogo

Acrescentado ao Passo 11B (Índice do pacote):

1. **A aba não troca com clique por coordenada** — continua listando PACOTES e a busca
   volta zero, o que parece resultado legítimo. Trocar com `element.click()` no `<button>`
   e conferir a classe `Tab isActive`.
2. **A busca é fuzzy (OR)** — "Bizu Receita Federal" devolve 3772 itens casando só
   "Receita". Contagem alta não significa acerto.
3. **Material granular (Bizu, Passo, Monitoria, Trilha, Discursiva) não aparece na aba
   PACOTES** — só na aba **CURSOS**, onde é produto avulso matriculável (122 Bizus no
   catálogo, por exemplo).

## 7. `AGENTS.md` — rodízio de matrícula e busca no catálogo

**Rodízio é livre, não precisa pedir autorização** (Elvis, 2026-08-20). A única checagem
obrigatória antes de matricular ou desmatricular: **alguma sessão em andamento está usando,
baixando ou acessando aquele produto?** Se não estiver, trocar à vontade. Caiu a regra
antiga de conferir placeholder `.txt` e avisar antes.

Também entrou a tabela de onde procurar cada coisa no catálogo (PACOTES × CURSOS), a
armadilha da aba e a tabela do `tipo_curso_id`.

---

## Não aplicado — decisão pendente do Elvis

**Trava de caminho longo do Windows (260 caracteres).** Proposta e não implementada.

O sufixo de 3 caracteres estourou o limite em Contabilidade Geral Avançada do Regular
Fiscal, e o `os.rename` falhou no meio do lote. A correção usada no mutirão foi:

- caminho estendido — prefixo `\\?\` no caminho absoluto antes de qualquer operação de
  arquivo;
- loop **retomável**, que pula o que já foi feito;
- log com `flush()` a cada linha, para não perder o progresso se quebrar.

As duas skills **escrevem** arquivos com nomes longos dentro de pastas já longas, e agora
escrevem 3 caracteres a mais. **Essas pastas estão no limite** — vai acontecer de novo.
