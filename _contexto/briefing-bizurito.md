# Briefing — BIZURITO (para a sessão "Mapear Aulas")

> **Como usar:** abra a janela do Mapear Aulas e cole a seção **"Prompt para colar"** no fim deste
> arquivo. Este documento é o handoff completo da sessão de 20/08/2026, em que o BIZURITO foi
> desenhado, prototipado e validado. O layout está **fechado**; o que falta é dado real.

---

## 1. O que é o BIZURITO

Terceiro material entregue ao aluno, ao lado do caderno de questões do Tec e do resumo do Bezerra.
É **uma folha A4 por chave de taxonomia** (Cód Mestre, ex. `DADM-014`) que responde a uma pergunta
só: **o que a banca cobra neste tópico**.

Não é resumo de teoria. É leitura de prova. Na plataforma entra como **complemento aos resumos**.

**Regra de origem (dura):** cada linha nasce de **questão fichada**, e a frase deriva da
**resolução do professor no Tec** e do gabarito, nunca de conhecimento próprio do modelo. Cada
linha guarda os `#` das questões que a originaram. Sem rastro, não entra.

---

## 2. Anatomia da folha (fechada, ver modelos publicados)

1. **Cabeçalho preto** — a palavra BIZURITO na fonte da marca (imagem), o Cód Mestre em dourado,
   o nome do tópico, a lista de subtópicos e o tamanho do acervo. Logo Sai da Caserna à direita.
2. **Faixa dourada do edital** (só no pós-edital) — concurso e item do conteúdo programático.
3. **Faixa "ANTES DE LER, TENTE RESPONDER"** — as perguntas de cada ponto, em texto corrido,
   etiquetadas pelo código do ponto. Serve de aquecimento por recuperação ativa.
4. **Tabela** com 4 colunas: `PONTO` · `QUESTÕES` · `RISCO` · `O QUE A BANCA COBRA`.
5. **Blocos**: `OURO GERAL` (cai nas principais bancas) e um `OURO DA <BANCA>` por banca.
6. **Legenda**, **caixa de anotações** e **rodapé**.

### Coluna RISCO (rótulos aprovados)

| Rótulo | Cor tela | Corte | Vira, em cinza |
|---|---|---|---|
| MAIORIA ACERTA | `#EDF6EE` | acerto ≥ 70% | 242 |
| MUITOS ESCORREGAM | `#F8DE9A` | 50% a 69% | 222 |
| ESSA DERRUBA | `#E9A79E` | < 50% | 186 |

**Nunca imprimir o percentual**: expõe a fonte e envelhece. As cores são escalonadas por
luminância de propósito, para sobreviverem à impressão em preto e branco (decisão: **um link só**,
o aluno imprime do navegador). O rótulo é texto, então funciona mesmo sem cor.

**Os cortes 70/50 são provisórios.** Com amostra maior, recalibrar (provavelmente por quartil
dentro da disciplina) e trazer sugestão ao Elvis.

### Regras de conteúdo da coluna QUESTÕES

- É a contagem de questões **daquele acervo** que cobram **aquele ponto**.
- **Os números não se somam** e isso está escrito na legenda: a mesma questão pode cobrar mais de
  um ponto, e as questões da banca também entram no bloco geral.
- **O bloco OURO GERAL não tem total próprio** — o acervo do tópico fica no cabeçalho.
- Blocos de banca dizem "N questões da banca neste tópico".
- **Só entra ponto com mais de uma questão** (decisão do Elvis, 20/08/2026).

---

## 3. Entrega: Google Docs com link fixo (testado ponta a ponta)

1. Gerar HTML → subir ao Drive convertendo em Google Doc.
2. Atualizar com `files().update()`: **o ID não muda**, logo o link não muda.
3. Permissão `reader/anyone`.
4. O link que vai para a Tutory é `.../export?format=pdf`.

**Medido sem credencial nenhuma:** HTTP 200, `application/pdf`, `attachment`, bytes `%PDF-`.
Editar reflete no mesmo link na hora. **O nome do arquivo que o aluno baixa é o nome do Doc.**

**Armadilha crítica:** o importador do Docs **ignora a largura declarada no HTML** e congela as
colunas em 468pt (Letter com margem de 1"). Depois de aplicar A4, é obrigatório reescrever as
larguras coluna a coluna via `updateTableColumnProperties`, senão sobram ~99pt em branco à
direita. O gerador já faz isso.

Outras armadilhas do importador: `@page` é ignorado; o Docs insere um **parágrafo entre tabelas
vizinhas** (13 tabelas custavam ~5cm de altura, por isso o corpo é uma tabela só); tabela
aninhada no cabeçalho estoura a altura da página.

---

## 4. Validação (6 camadas) — ver `project_bizurito_validacao_conteudo`

Nasceu de um teste real: numa auditoria, **3 das 13 linhas** estavam com problema, mais 1 erro de
coerência numérica achado depois. Catálogo de vícios já identificados:

1. **Lista parcial apresentada como completa** (listei 5 dos 8 bens do art. 78 do CTN).
2. **Requisito omitido de tese** (faltaram "exclusivamente" e "de atuação própria do Estado" no
   Tema 532).
3. **Regra absoluta** ("o item que contiver isso está errado").
4. **Dois acervos diferentes na mesma folha sem aviso** (cabeçalho dizia 19, bloco somava 35).

Camadas: **0** origem na resolução do professor · **1** checagem mecânica · **2** conferência de
âncora contra fonte oficial, com **teste de completude** quando a frase usa "são/apenas/os do
caput" · **3** **olhar de fora obrigatório** (ler só a folha final e desconfiar de cada linha) ·
**4** contraprova pela questão ("lendo só este bizu, o aluno acerta?") · **5** registrar o
aprendizado ao fim de **cada** BIZURITO gerado.

### Trava dura dos números (bloqueia a publicação)

`conferir_numeros()` roda **antes** de publicar e levanta erro: linhas de um bloco somando mais
que o total declarado; bloco declarando mais que o acervo; linha maior que o acervo em bloco sem
total; soma das bancas acima do acervo; contagem zerada; ponto repetido no bloco.

---

## 5. Linguagem

**Português formal simples**, sem coloquialismo. O tom informal com gíria é do Instagram, não do
material de estudo. O detector de informalidade roda no PDF renderizado.
Sem travessão. **Texto justificado** (padrão de qualquer documento, ver
`feedback_textos_sempre_justificados`).

**Direito autoral:** lei, súmula e ementa verbatim à vontade. Explicação de professor sempre
**reescrita**, sem copiar estrutura, e **sem necessidade de crédito** porque paráfrase não é
citação (decisão do Elvis).

---

## 6. O código já existe e funciona

Em `bizurito/`:
- `gerar_bizurito.py` — monta o HTML, publica no Drive, aplica A4 e margens, corrige as larguras,
  roda `conferir_numeros()` e `revisar()`.
- `modo_impressao.py` — variante sem fundo chapado (mantida como opção; a decisão atual é link
  único).
- `dados_bizurito.py` — os 3 conteúdos de exemplo (DADM, MAFI, DCON) no formato de entrada.

Formato de entrada: `{codigo, nome, topicos[], total, edital?, blocos[{titulo, sub, cor, claro,
pontos[{ponto, cai, risco, texto, pergunta?, estrela?}]}]}`.

**Na execução real, o que muda é só a origem desse dicionário: sai da planilha, não escrito à mão.**

### Modelos publicados (números fictícios, só layout)

- DADM-014 geral: `https://docs.google.com/document/d/1fLRGWiL37BBS1DbYbDMsdpxJrM46Y7fCBW-57xs7wZ4/export?format=pdf`
- DADM-014 pós-edital TCDF: `https://docs.google.com/document/d/130s2PR4awpNd_2WtEX8Y2ptDrzQxKiSzpcfGg7Ftmfo/export?format=pdf`
- MAFI-004: `https://docs.google.com/document/d/1QfT2lyaOzUfamNgC9MlH8OiH2guAWZG8fJ8j7f6wxHE/export?format=pdf`
- DCON-021: `https://docs.google.com/document/d/1b3FxqYOiDYkKwvBhDAeemNgWL_0K6eSEAUrat4dRkow/export?format=pdf`

---

## 7. O QUE A SESSÃO "MAPEAR AULAS" PRECISA VALIDAR E DECIDIR

Esta é a parte que interfere no trabalho de lá. **Analisar item a item antes da execução real.**

1. **Colunas novas na aba `Pontos`, criadas ANTES da passada de fichamento:**
   `Bizu` (a frase) · `Pergunta` · `Bizu Forte` (calculado) · `Letra da Lei` ·
   `Normas citadas` (índice para atualização legislativa) · `Verificado em` (data).
   **Se não existirem quando o fichamento rodar, é reabrir ~1.100 questões depois.**
2. **Índice de acerto do Tec:** confirmar se vem na API na mesma chamada do fichamento. Se não
   vier, **raspar da tela no momento** (decisão do Elvis) e registrar que precisará ser
   atualizado depois.
3. **Calibrar os cortes de risco** com amostra maior e propor números ao Elvis.
4. **Definir a granularidade da folha**: quantos pontos entram, e quando agrupar tópicos vizinhos
   numa folha só (tópico com banco pobre gerando folha de 4 linhas ao lado de outra com 20 passa
   impressão de descuido).
5. **Onde os Docs ficam no Drive** e o padrão de nome do Doc (é o nome do arquivo que o aluno
   baixa).
6. **Pós-edital:** sai só `OURO GERAL` + o bloco da banca do edital. Quando a banca tiver banco
   pequeno, o geral vira a referência e o bloco da banca é marcado como amostra pequena.
7. **Bizu do Bizu** (material novo, aprovado): consolidado da **disciplina inteira** por
   pós-edital, só com os pontos `ESSA DERRUBA`. Material de véspera. Nele vale separar pergunta e
   resposta, porque na véspera o aluno quer se testar, não ler.
8. **Impressão:** decisão atual é **link único**, com a paleta preparada para preto e branco.
   `modo_impressao.py` fica disponível se a decisão mudar.

---

## 8. Depois do teste real

**Reavaliar tudo com base nos dados reais e trazer sugestões ao Elvis** (compromisso assumido):
tamanho médio da folha, distribuição dos rótulos de risco, se os cortes precisam mudar, se a
granularidade está boa, e o que a Camada 5 registrou de vícios novos.

---

## 9. Salvamento e sincronização (pendente, delegado a esta sessão)

Elvis determinou em 20/08/2026 que **a sessão do Mapear Aulas faz o commit e o push** de tudo,
inclusive do que veio da sessão do BIZURITO. Nada foi commitado por lá de propósito, para não
misturar com trabalho de outra janela.

**O que está aguardando commit no momento do handoff:**

Criado pela sessão do BIZURITO:
- `bizurito/` — o gerador (`gerar_bizurito.py`, `modo_impressao.py`, `dados_bizurito.py`)
- `_contexto/briefing-bizurito.md` — este arquivo
- `marca/Logo BIZURITO preto.png`, `marca/Logo BIZURITO branco.png` e a variante
  `marca/Logo BIZURITO preto (serifada).png` (descartada, mantida como registro)
- `_contexto/preferencias.md` — linha nova do padrão de texto justificado

Já estava pendente, de outras janelas (**conferir antes de commitar, não é trabalho do BIZURITO**):
- `.claude/skills/baixar-curso-completo-estrategia/SKILL.md` e
  `.claude/skills/baixar-curso-especifico-estrategia/SKILL.md` (modificados)
- `AGENTS.md` (modificado)
- `_contexto/briefing-mapear-aulas-tipos-de-material.md`,
  `_contexto/briefing-sessao-tipos-de-material.md`,
  `_contexto/estrategia-padroes-pdf.md`, `_contexto/estrategia-tipos-de-material.md`

**Antes do push**, rodar o checklist de encerramento do `AGENTS.md`: git limpo e sincronizado com
`origin/main`, e **ressincronizar a ponte `.agents/skills`**, que no Windows é cópia e fica
desatualizada a cada skill editada.

> A fonte `dados/Checkpoint Charlie.ttf` (usada na logo) já está versionada. Vale avaliar movê-la
> para `marca/`, junto das logos, para não se perder de novo — foi difícil de localizar.


---

## Prompt para colar na sessão nova

```
Leia _contexto/briefing-bizurito.md deste workspace. Ele traz o desenho completo do BIZURITO,
o novo material que vai junto com os cadernos do Tec e os resumos, e o gerador já pronto em
bizurito/.

Antes de qualquer execução, faça a seção 7 (o que precisa ser validado e decidido): analise item
a item o que isso muda no trabalho de mapeamento e fichamento que você está conduzindo, em
especial as colunas novas da aba Pontos, que precisam existir ANTES da passada de fichamento,
e o índice de acerto do Tec. Me diga o que conflita, o que falta e o que você mudaria.

Depois disso, vamos fazer a execução real com a base de dados de verdade.

Por último: a seção 9 lista o que está aguardando commit, incluindo o que veio da sessão do
BIZURITO. Faça o salvamento e a sincronização com o GitHub por aqui, conferindo antes o que é de
outras janelas, e rode o checklist de encerramento do AGENTS.md.
```
