---
name: baixar-curso-completo-estrategia
description: >
  Baixa em lote os livros eletrônicos (PDF) de um PACOTE completo do Estratégia
  Concursos (várias matérias/categorias de uma vez — Curso Regular, Passo
  Estratégico, Bizu Estratégico etc), organizando tudo em pastas por categoria
  e por matéria. Diferente da baixar-curso-especifico-estrategia (que baixa só
  UM curso/matéria por vez), essa skill mapeia o pacote inteiro primeiro e
  pergunta quais categorias baixar. Use quando o usuário mandar um link de
  pacote do estrategiaconcursos.com.br (padrão
  `/app/dashboard/pacote/{id}`), ou disser "baixa esse pacote inteiro do
  Estratégia", "baixa o curso completo", "baixa tudo desse concurso no
  Estratégia", "sincroniza o pacote inteiro pra pasta".
---

# /baixar-curso-completo-estrategia — Download em lote de um PACOTE completo do Estratégia Concursos

## O que essa skill faz

Usa o Chrome real do usuário (via extensão Claude in Chrome, já logado no Estratégia
Concursos) pra abrir a página de um **pacote** (não um curso único), mapear todas as
matérias/categorias que existem dentro dele, perguntar ao usuário quais categorias
baixar, e então baixar — direto no disco, sem passar pela pasta de Downloads — o
livro eletrônico de cada aula de cada matéria selecionada, organizado em pastas por
categoria.

Se o link que o usuário mandar for de um curso único (`/app/dashboard/cursos/{id}/aulas`,
não um pacote), avisar e sugerir usar a skill `baixar-curso-especifico-estrategia` em vez
dessa.

## Passo 0: Perguntas obrigatórias no início

**Pasta padrão:** `G:\Meu Drive\Inteligência Artificial\Estrategia`
— é aqui que as pastas novas são criadas por padrão, salvo o usuário indicar
outro local. **Essa pasta vive dentro do Google Drive sincronizado**, então
antes de usar ela **verificar que ela existe de fato no disco** (`Test-Path` /
`ls`). Por ser uma pasta sincronizada, pode não estar montada/sincronizada no
momento — se não existir, avisar o usuário em vez de simplesmente criar uma
pasta nova do zero em outro lugar.

Sempre perguntar antes de fazer qualquer coisa (não assumir, não pular):

1. **Link do pacote** — a URL da página do pacote no Estratégia Concursos (padrão
   `https://www.estrategiaconcursos.com.br/app/dashboard/pacote/{id}`).
2. **Pasta:** perguntar se quer usar a **pasta padrão** (acima) ou indicar um
   **novo local**. Se confirmar a padrão, usar ela direto. Se pedir outro local,
   usar o caminho informado.

**Não perguntar aqui se é "novo ou atualização"** — isso é descoberto sozinho no
Passo 2, depois de identificar o concurso/cargo (Passo 1) e procurar
automaticamente por uma pasta de pacote já existente dentro do local informado.
Ver Passo 2.

3. **Base de siglas de disciplinas (pergunta temporária):** perguntar se já
   existe alguma planilha/tabela de referência com nome de disciplina → sigla.
   **Hoje essa base ainda não existe** — enquanto não existir, seguir usando o
   nome completo da matéria no nome da pasta (padrão atual do Passo 6). Quando o
   usuário criar essa base no futuro, ele vai indicar — a partir daí, usar a
   sigla da disciplina no lugar do nome completo ao montar o nome da pasta. Até
   lá, essa pergunta serve só de lembrete pro usuário, não bloqueia o fluxo.

Não seguir em frente sem as respostas 1 e 2 acima.

## Passo 1: Abrir o pacote e identificar concurso / cargo

1. Carregar as tools do Chrome (se ainda não carregadas):
   `ToolSearch` com `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__browser_batch,mcp__claude-in-chrome__find,mcp__claude-in-chrome__form_input`
2. Navegar até o link do pacote. Se a extensão pedir aprovação de domínio, é normal
   na primeira vez.
3. Ler o título da página pra extrair:
   - **Sigla do concurso** (ex: TCDF) — geralmente já vem entre parênteses no título.
   - **Cargo** (ex: Auditor Fiscal de Tributos Municipais).
4. **Sigla do cargo:** se não tiver uma sigla óbvia no título, pesquisar (na própria
   página ou na internet) pela sigla oficial do cargo pro concurso em questão, e
   decidir sozinho — não precisa confirmar com o usuário.
5. **Sigla do concurso quando não vem óbvia entre parênteses:** pesquisar no Google
   (cruzando com o próprio site do Estratégia Concursos como referência) pelo nome
   do concurso/edital pra achar a sigla oficial ou a forma abreviada mais usada.
   Manter a sigla como ela realmente é usada — não forçar juntar palavras num
   bloco só se o uso comum mantém espaço (ex: o concurso "ISS Manaus" usa a sigla
   com espaço mesmo, `ISS Manaus`, não `ISSMANAUS`).

## Passo 2: Procurar pasta de pacote existente antes de criar (detecção automática)

**Escopo da busca: só dentro da pasta informada no Passo 0** (a pasta padrão ou
o outro local que o usuário indicou) — nunca varrer o computador inteiro nem
outras pastas fora dali.

Com a sigla `SIGLA_CONCURSO-SIGLA_CARGO` definida no Passo 1, procurar dentro
dessa pasta por uma pasta de pacote já existente que corresponda a esse
concurso/cargo — o nome raiz do pacote é livre, então o jeito confiável de
identificar é abrir as pastas de primeiro nível encontradas e checar se as
subpastas de categoria/matéria lá dentro usam essa mesma sigla (ex: `Direito
Constitucional (TCDF-ANACE)`). **Comparação:** ignorar maiúsculas/minúsculas,
acentuação, e um eventual prefixo `(N-M)` nas subpastas.

**Se encontrar exatamente uma pasta de pacote correspondente:**

1. Resumir o que já tem: quais categorias existem, quantas matérias em cada uma,
   e quantas já estão completas vs incompletas (olhando o prefixo `(N-M)` de
   cada subpasta — ver Passo 9).
2. Informar o usuário e perguntar como quer proceder, com três opções:
   - **Atualização Parcial** (padrão sugerido) — baixa só as aulas que ainda
     estão faltando em cada matéria (travadas na coleta anterior, agora
     liberadas). Não mexe nos PDFs já baixados. Rápido.
   - **Atualização Completa** — além de baixar o que falta, reconfere **todos**
     os PDFs já baixados do pacote inteiro contra a versão atual no site e
     substitui os que tiverem sido revisados/atualizados desde a última coleta.
     Bem mais lento num pacote grande, porque precisa rebaixar cada aula já
     existente pra comparar.
   - **Criar pasta nova do zero** — mesmo já tendo uma pasta encontrada.
3. **Se optar por Atualização Parcial ou Atualização Completa:** esse vira o
   modo atualização pro resto da skill — usar essa pasta como a pasta do
   pacote, seguir a partir do Passo 4 (mapear o que já existe localmente e
   cruzar com o site), no sub-modo escolhido.
4. **Se optar por criar nova do zero:** perguntar também **se quer que a pasta
   antiga localizada seja apagada** (nunca apagar sem essa confirmação explícita
   — é uma ação destrutiva e irreversível) ou se prefere manter as duas
   coexistindo (nesse caso, a pasta nova precisa de um nome que não conflite —
   confirmar com o usuário como diferenciar, ex: sufixo com a data da coleta).

**Se encontrar mais de uma pasta de pacote correspondente** (ex: mais de um
pacote baixado pro mesmo concurso/cargo): **não escolher sozinho** — listar
todas as encontradas (caminho completo de cada uma) e perguntar ao usuário qual
delas é a certa antes de seguir.

**Se não encontrar nenhuma pasta correspondente:** é download novo — a pasta do
pacote vai ser criada do zero dentro do local informado (ver Passo 6). Não tem
o que atualizar, então não precisa perguntar mais nada sobre isso.

## Passo 3: Mapear todas as matérias do pacote e categorizar

1. Usar `get_page_text` na página do pacote pra listar todos os cursos/blocos que
   aparecem (cada linha é um item clicável).
2. **Classificar cada item por padrão de nome:**

   | Padrão no nome | Categoria | Padrão de download |
   |---|---|---|
   | Nome de matéria puro (sem prefixo/sufixo especial) | **Curso Regular** | livro simplificado + original (fallback) |
   | Começa com "Passo Estratégico de " | **Passo Estratégico** | livro único por aula |
   | É exatamente "Bizu Estratégico" (curso único, matérias viram "aulas" dentro dele) | **Bizu Estratégico** | livro único por aula |
   | Começa com "Simulado" | **Simulado** | livro único por aula (simulado + gabarito são aulas separadas) |
   | É "Discursiva Sem Correção" | **Discursiva** | livro único por aula |
   | Contém "Trilha Estratégica" | **Trilha Estratégica** | livro único por aula (numeração "Trilha NN" em vez de "Aula NN") |
   | Qualquer outro padrão não reconhecido | **Outra categoria** — criar uma categoria nova com nome descritivo baseado no padrão observado | testar ao abrir a primeira aula (Passo 6) |

3. **Todas as categorias têm livro eletrônico pra baixar**, inclusive Simulado,
   Discursiva e Trilha Estratégica — confirmado na prática: cada uma delas segue
   o mesmo padrão de card único "Baixar Livro Eletrônico versão original" que o
   Passo Estratégico e o Bizu Estratégico usam (ver Passo 7). Não existe categoria
   "sem livro" por padrão — todas entram como opção de download no Passo 5.
4. Se aparecer algum item cuja categoria não dá pra determinar só pelo nome, abrir
   o curso (Passo 6) rapidamente pra checar o card de "Baixar Livro Eletrônico"
   antes de decidir em qual grupo de padrão de download ele se encaixa.

## Passo 4: Modo atualização — mapear o que já existe localmente e cruzar com o site

**Só se aplica se o Passo 2 resultou em atualização.** Em modo novo, pular direto
pro Passo 5.

1. Listar a pasta do pacote (localizada no Passo 2): quais pastas de categoria
   existem (`Curso Regular`, `Passo Estratégico`, etc), e dentro de cada uma,
   quais subpastas de matéria/bloco já existem.
2. Pra cada subpasta de matéria já existente, ler o nome (extrair o prefixo
   `(N-M)` se tiver — ver Passo 9) e contar os arquivos reais dentro: quantos
   `.pdf` (já baixados, com a data entre parênteses no nome — ver Passo 7) e
   quantos `.txt` (placeholder de aula ainda não disponível na coleta anterior,
   com a data prevista depois de um traço).
3. Pra cada matéria com `.txt` pendente, abrir a listagem `/aulas` dela no site
   (usando o mapeamento do Passo 3 pra achar o link certo) e comparar: quais
   aulas que antes estavam travadas ("Disponível em DD/MM/AAAA") já aparecem
   liberadas agora ("Não estudei"/estudada)? Essas são as aulas **atualizáveis**.
4. Apresentar um resumo pro usuário, por categoria e matéria, por exemplo:

   ```
   O que já existe na pasta informada:
   - Curso Regular
     - (10-20) Direito Administrativo — 3 aulas novas liberadas desde a última coleta
     - (20-20) Direito Constitucional — completo, nada pra atualizar
   - Passo Estratégico
     - (5-19) Economia — 1 aula nova liberada
   ```

5. Perguntar: **"Quer que eu atualize essas pastas?"** — com a opção de
   confirmar todas de uma vez, ou escolher manualmente quais matérias atualizar.
   Não seguir pro download sem essa confirmação.
6. **Se o sub-modo escolhido no Passo 2 for Atualização Parcial:** matérias que
   existem localmente mas não têm nenhuma aula nova liberada não precisam de
   ação — só mencionar no resumo que já estão em dia (ou completas).
7. **Se o sub-modo escolhido no Passo 2 for Atualização Completa:** toda matéria
   com PDF já baixado entra na lista de processamento, mesmo as completas — vai
   ser reconferida no Passo 7 (rebaixar e comparar data). No resumo, marcar essas
   como "completa — será reconferida" em vez de "nada pra atualizar".

## Passo 5: Apresentar o mapeamento e perguntar quais categorias baixar

**Modo novo:** mostrar pro usuário um resumo tipo:

```
Categorias encontradas nesse pacote:
- Curso Regular (20 matérias) — livro simplificado + original
- Passo Estratégico (19 matérias) — livro único por aula
- Bizu Estratégico (1 bloco, várias matérias como aulas) — livro único por aula
- Discursiva Sem Correção (1 bloco) — livro único por aula
- Trilha Estratégica (1 bloco) — livro único por aula (numeração "Trilha NN")
- Simulado (1 bloco) — livro único por aula (simulado + gabarito)
```

Perguntar (com uma opção padrão recomendada) quais categorias baixar:

- **Só Curso Regular** (padrão sugerido — é o material principal, com livro
  simplificado)
- **Só Passo Estratégico**
- **Todas as categorias**
- **Escolher manualmente** (usuário lista quais categorias específicas quer)

Não seguir pro download sem essa resposta.

**Modo atualização:** essa pergunta já foi respondida no Passo 4 (quais matérias
atualizar) — não repetir. Seguir direto pro Passo 6 só com as matérias
confirmadas lá. Se o usuário quiser, nesse modo, também baixar matérias/categorias
novas que apareceram no pacote desde a última coleta (e ainda não têm pasta
local), perguntar isso separadamente antes de prosseguir.

## Passo 6: Criar a estrutura de pastas

```
<pasta raiz>/<Nome do Pacote>/
├── Curso Regular/
│   ├── Contabilidade Geral (SIGLA-SIGLA)/
│   ├── Direito Constitucional (SIGLA-SIGLA)/
│   └── ...
├── Passo Estratégico/
│   ├── Contabilidade Geral (SIGLA-SIGLA)/
│   ├── Direito Constitucional (SIGLA-SIGLA)/
│   └── ...
├── Bizu Estratégico/
│   └── Bizu Estratégico (SIGLA-SIGLA)/   ← pasta única, não separa por matéria
├── Discursiva Sem Correção/
│   └── Discursiva Sem Correção (SIGLA-SIGLA)/   ← pasta única, curso já é um bloco só
├── Trilha Estratégica/
│   └── Trilha Estratégica (SIGLA-SIGLA)/        ← pasta única
└── Simulado/
    └── Simulado (SIGLA-SIGLA)/                  ← pasta única
```

- Uma pasta por categoria selecionada no Passo 5.
- Dentro de cada categoria com múltiplas matérias (Curso Regular, Passo
  Estratégico), uma subpasta por matéria, no mesmo padrão de nome da skill
  `baixar-curso-especifico-estrategia`: `Matéria (SIGLA_CONCURSO-SIGLA_CARGO)`.
  Esse é o nome "base" criado antes de baixar qualquer aula — no final (Passo 9),
  a pasta é renomeada (nunca apagada e recriada) pra ganhar o prefixo `(N-M)` na
  frente se o curso ainda não estiver completo.
- **Bizu Estratégico, Discursiva Sem Correção, Trilha Estratégica e Simulado são
  exceção:** cada uma delas já é um curso único no site (não um curso por
  matéria), então vira **uma pasta só** dentro da categoria (ex:
  `Bizu Estratégico (SIGLA-SIGLA)`), com todos os PDFs das aulas daquele bloco
  dentro (ver Passo 7).
- **Modo novo:** criar tudo do zero com `mkdir -p`, dentro da pasta informada no
  Passo 0 (nenhuma pasta de pacote correspondente foi encontrada no Passo 2).
- **Modo atualização:** usar a pasta do pacote localizada no Passo 2; criar só
  as subpastas de categoria/matéria que ainda não existirem (matérias novas no
  pacote), sem recriar as que já existem — sempre atualizar em cima da pasta
  existente, nunca apagar e recriar (ver regra no Passo 9).

## Passo 7: Baixar o livro de cada aula de cada matéria selecionada

Para cada matéria dentro de cada categoria selecionada (Passo 5) ou confirmada
pra atualização (Passo 4), repetir o mesmo processo da skill
`baixar-curso-especifico-estrategia` (Passos 4 a 6 dela), com uma diferença por
categoria:

### Curso Regular

- Igual à skill original: preferir "Baixar Livro Eletrônico versão simplificada";
  se não existir, usar "versão original" como fallback.
- Nome do arquivo: `Aula NN - Assunto Sintético (DD-MM-AAAA).pdf`, dentro da
  subpasta da matéria (data extraída da primeira página do PDF — ver "Extrair a
  data do PDF" abaixo).

### Passo Estratégico

- Só existe um card: "Baixar Livro Eletrônico" (sem distinção simplificada/original).
  Clicar nesse card direto.
- Nome do arquivo: `Aula NN - Assunto Sintético (DD-MM-AAAA).pdf`, dentro da
  subpasta da matéria.

### Bizu Estratégico

- Mesma lógica de único card "Baixar Livro Eletrônico" do Passo Estratégico.
- **Diferença:** como todas as aulas desse curso único já são matérias diferentes,
  o nome do arquivo usa o **nome da matéria da aula** em vez de "Aula NN":
  `Nome da Matéria (DD-MM-AAAA).pdf` (ex: `Auditoria (DD-MM-AAAA).pdf`,
  `Língua Portuguesa (DD-MM-AAAA).pdf`), todos dentro da mesma pasta
  `Bizu Estratégico (SIGLA-SIGLA)/`.

### Discursiva Sem Correção

- Mesmo card único "Baixar Livro Eletrônico versão original".
- Curso já é um bloco só (não por matéria) — nome do arquivo:
  `Aula NN - Assunto Sintético (DD-MM-AAAA).pdf`, todos dentro da pasta única
  `Discursiva Sem Correção (SIGLA-SIGLA)/`. Algumas aulas vêm marcadas "(Somente
  PDF)" no título do site — é só uma informação do site, não muda o processo.

### Trilha Estratégica

- Mesmo card único "Baixar Livro Eletrônico versão original".
- **Diferença de nomenclatura:** o site numera como "Trilha NN" em vez de "Aula
  NN" — usar esse mesmo padrão no nome do arquivo: `Trilha NN - Assunto
  Sintético (DD-MM-AAAA).pdf`, dentro da pasta única `Trilha Estratégica
  (SIGLA-SIGLA)/`. Tem também um item inicial "Como utilizar a Trilha
  Estratégica" sem número — tratar como uma aula normal, nomeando o arquivo pelo
  próprio título (`Como Utilizar a Trilha Estratégica (DD-MM-AAAA).pdf`).

### Simulado

- Mesmo card único "Baixar Livro Eletrônico versão original".
- Cada simulado do bloco tem normalmente **duas aulas associadas**: o simulado
  em si e o "Gabarito" correspondente — são duas aulas separadas na listagem,
  cada uma com seu próprio card de download. Baixar as duas.
- Nome do arquivo baseado no título da aula (geralmente já traz a data do
  simulado em si) + a data extraída do PDF entre parênteses no final, dentro da
  pasta única `Simulado (SIGLA-SIGLA)/`. Ex: `Simulado Especial -
  23-08-2026 (DD-MM-AAAA).pdf` e `Simulado Especial - 23-08-2026 - Gabarito
  (DD-MM-AAAA).pdf` (barra da data do título trocada por traço, mesma regra do
  Passo 8; a data entre parênteses no final é a de elaboração do PDF, pode ser
  diferente da data do simulado no título).

### Extrair a data do PDF (nome do arquivo)

Depois de baixar cada PDF (todo download, não só em modo atualização), extrair
a data de elaboração/atualização que aparece na primeira página, pra usar no
nome do arquivo (mesmo processo da skill `baixar-curso-especifico-estrategia`):

```bash
python -c "
import re, sys
from pypdf import PdfReader
texto = PdfReader(sys.argv[1]).pages[0].extract_text() or ''
m = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
print(f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else '')
" "<caminho do PDF baixado com nome temporário>"
```

- Baixar sempre com nome temporário (`.tmp`), extrair a data, e só então renomear
  pro nome final com a data.
- Se `pypdf` não estiver instalado, instalar com `pip install pypdf` antes de
  processar a primeira aula.
- **Fallback se não achar data:** manter o nome do arquivo sem o sufixo
  `(DD-MM-AAAA)` e seguir normalmente — não travar o download. Mencionar no
  resumo final quais aulas ficaram sem data identificada.

### Mecânica de download (igual em todas as categorias)

1. Navegar para `https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{id}/aulas/{aulaId}`
   (ou clicar no título da aula na lista) e esperar ~2s carregar.
2. Clicar no card de livro correspondente à categoria (ver acima).
3. O clique abre uma **nova aba** com uma URL direta e assinada da CDN
   (`cdn.estrategiaconcursos.com.br/storage/temp/aula/.../....pdf?Expires=...&Signature=...`).
   Pegar essa URL com `tabs_context_mcp` (pode levar 1-2s pra aba carregar o título/URL).
4. Baixar o PDF **direto pra pasta de destino**, com nome temporário, via `curl`
   (Bash), sem passar pela pasta de Downloads:
   ```bash
   curl -s -o "<pasta>/<nome do arquivo>.pdf.tmp" "<url capturada>" -w "HTTP:%{http_code} SIZE:%{size_download}\n"
   ```
   Conferir que retornou `HTTP:200` e um `SIZE` não-trivial.
5. Extrair a data (ver acima) e renomear o `.tmp` pro nome final.
6. Fechar a aba do PDF (`tabs_close_mcp`).
7. Voltar pra lista de aulas da matéria e seguir pra próxima aula. Depois de
   esgotar as aulas da matéria, voltar pra página do pacote e ir pra próxima
   matéria/categoria.

### Modo atualização — o que baixar

O Passo 4 já identificou, por matéria, quais aulas estão atualizáveis (antes
travadas, agora liberadas). O que fazer com o resto depende do sub-modo
escolhido no Passo 2:

- Arquivos `.txt` placeholder cuja aula agora está liberada (identificado no
  Passo 4) → em **qualquer** sub-modo, baixar o PDF normalmente e **apagar o
  `.txt` antigo** — **passo obrigatório, nunca esquecer:** sempre que um PDF
  real substitui um `.txt` placeholder, o `.txt` correspondente tem que ser
  apagado da pasta antes de seguir pra próxima aula/matéria.
- Arquivos `.txt` placeholder cuja aula continua travada → deixar como está (pode
  atualizar a data prevista se ela mudou no site).
- Arquivos já baixados (`.pdf` com data entre parênteses no nome):
  - **Atualização Parcial:** **pular** — não reconfere.
  - **Atualização Completa:** **não pular** — rebaixar (mesmo processo da
    "Mecânica de download" acima), extrair a data do PDF novo e comparar com a
    data no nome do arquivo local:
    - Data igual → apagar o `.tmp`, não mexer no arquivo existente.
    - Data diferente (ou arquivo antigo sem data no nome, de coleta anterior a
      esse fluxo) → apagar o PDF antigo, renomear o `.tmp` pro nome final com a
      data nova. Registrar essa substituição pra citar no resumo final.

## Passo 8: Aula ainda não disponível → placeholder `.txt`

Mesma regra da skill original: quando a aula não tiver livro disponível ainda,
não baixar nada — criar um `.txt` no lugar, mesmo nome do PDF que seria criado,
terminando em `- DD-MM-AAAA.txt` (data com traço, nunca com barra — barra quebra
nome de arquivo no Windows).

```
Aula NN - Assunto Sintético - DD-MM-AAAA.txt      (Curso Regular / Passo Estratégico)
Nome da Matéria - DD-MM-AAAA.txt                   (Bizu Estratégico)
```

Conteúdo do `.txt`: uma linha simples informando que o material ainda não estava
disponível na data da coleta e qual a previsão de liberação informada pelo site.

**Lembrete de formato:** a data entre **parênteses** `(DD-MM-AAAA)` num `.pdf` é
a data real de elaboração/atualização do arquivo, extraída da própria primeira
página (ver Passo 7). A data depois de um **traço** `- DD-MM-AAAA.txt` é só a
previsão de liberação informada pelo site pra uma aula ainda travada. Os dois
formatos nunca se confundem visualmente por causa disso.

## Passo 9: Nomear a pasta com indicador de progresso (N-M)

Depois de terminar todas as aulas de uma matéria/bloco (pasta de Curso Regular,
Passo Estratégico, ou a pasta única de Bizu/Discursiva/Trilha/Simulado):

1. Contar **M** = total de aulas do curso (linhas na listagem `/aulas`) e **N** =
   quantas delas realmente têm PDF baixado (arquivos `.pdf` de verdade, não os
   `.txt` placeholder do Passo 8).
2. **Se N < M** (curso incompleto): renomear a pasta pra começar com `(N-M) `,
   ex: `(10-20) Direito Administrativo (SIGLA-SIGLA)` (10 aulas com PDF já
   disponível, de um total de 20 aulas no curso). O indicador fica **entre
   parênteses, colado direto no nome da matéria** — sem traço separando os dois,
   só um espaço. **Usar traço dentro do parênteses (`N-M`), nunca barra
   (`N/M`)** — barra é separador de caminho no Windows e quebra o `Rename-Item`
   (confirmado na prática: tentar renomear com `/` lança erro "representa um
   caminho ou nome de dispositivo").
3. **Se N == M** (curso completo): a pasta fica sem prefixo, só
   `Direito Administrativo (SIGLA-SIGLA)`.
4. **Modo atualização:** antes de recalcular, remover qualquer prefixo `(N-M) `
   que a pasta já tenha (de uma execução anterior) pra não acumular prefixos
   antigos — sempre recalcular do zero e renomear com os números atuais.
5. **Sempre renomear a pasta existente com `Rename-Item` (ou equivalente) — nunca
   apagar a pasta (ou a árvore inteira) e recriar do zero pra aplicar esse
   prefixo.** Apagar e recriar perde a pasta original (e qualquer PDF real já
   baixado nela) e conta como criar uma pasta nova, não atualizar a existente —
   o que vale tanto pra corrigir o prefixo quanto pra qualquer outro ajuste feito
   em modo atualização.

Isso deixa visível, só olhando o nome da pasta no Explorer, quais matérias ainda
têm aula pendente de liberação pelo site e quais já estão 100% baixadas.

## Passo 10: Verificação final

Depois de processar todas as categorias/matérias selecionadas:

1. Listar a árvore de pastas criada (`ls` recursivo por categoria), já com os
   prefixos `(N-M)` renomeados.
2. Conferir que a quantidade de PDFs + TXTs de cada matéria bate com o total de
   aulas dela.
3. Validar cada PDF com `file` (deve reportar "PDF document", não algo corrompido
   ou HTML de erro).

O resultado final é a estrutura de pastas em si, já com os arquivos dentro e
cada matéria/bloco renomeado com o progresso `(N-M)` — não precisa gerar nem
apresentar uma tabela resumo pro usuário no final. As duas skills terminam no
mesmo formato: pastas criadas, arquivos dentro, sem relatório à parte.

## Detalhes técnicos e pegadinhas (aprendidos testando esse pacote)

- **Limite de 260 caracteres de caminho no Windows** — orçamento sugerido pra não
  estourar: pasta raiz (~50 caracteres, ex: a pasta padrão já usa isso) + nome
  do pacote até ~40 caracteres + nome da categoria (curto e fixo, não precisa
  cortar) + nome da pasta da matéria até ~70 caracteres (`(N-M) Matéria
  (SIGLA-SIGLA)`) + nome do arquivo da aula até ~80 caracteres. O nome do
  pacote inteiro costuma ser gigante no site (título completo do concurso) —
  **está autorizado a sintetizar esse nome sozinho, sem perguntar ao usuário**,
  usando algo curto e descritivo (ex: `Pacotaço ISS Manaus (AFTM) 2026`) em vez
  do título completo copiado do site. O mesmo vale pra nome de matéria e assunto
  da aula: se a soma projetada do caminho passar de ~240 caracteres (margem de
  segurança), sintetizar o que for preciso — priorizando manter sigla, categoria
  e número da aula intactos, cortando a parte descritiva.
- **Truncar nome de arquivo sem perder o que diferencia dois arquivos:** se dois
  arquivos da mesma matéria têm título quase idêntico e só diferem no final (ex:
  "Simulado Especial ... (23/08/2026)" vs "... (23/08/2026) Gabarito"), truncar
  o texto genérico pra um tamanho fixo faz os dois ficarem com o mesmo nome e um
  sobrescreve o outro. Colocar o que diferencia (`Gabarito`, número da parte,
  etc) **no início do nome do arquivo**, antes do texto que vai ser truncado.
- **Nem todo curso começa em "Aula 00"** — alguns (ex: Direito Processual Penal
  nesse pacote) começam direto em "Aula 01". Não assumir que "Aula 00" sempre
  existe; usar a primeira aula que realmente aparecer na listagem.
- **"Primeira aula que aparece" pode estar travada** (com "Disponível em
  DD/MM/AAAA") — trata-se normalmente como qualquer aula bloqueada: vira
  placeholder `.txt` (Passo 8), não é motivo pra pular pra segunda aula.

## Detalhes técnicos e pegadinhas (herdados da baixar-curso-especifico-estrategia)

- **Nunca clicar às cegas em coordenadas fixas** — sempre esperar carregar
  (`wait` ~1.5-2s) e confirmar com `screenshot` ou `read_page`/`find` antes de
  clicar, porque o layout muda de aula pra aula e de categoria pra categoria.
- **Fechar aba + navegar na mesma aba de controle no mesmo `browser_batch`**
  costuma falhar — fazer em chamadas separadas.
- O campo de busca da página do pacote (`Pesquisar por curso...`) filtra a lista
  em tempo real — útil pra localizar rápido um curso específico dentro do
  pacote, mas usar `find` + `form_input` pra digitar nele (o `type` direto às
  vezes não funciona se o campo perdeu o foco).
- O link da CDN é assinado e temporário (parâmetro `Expires`), mas isso só afeta
  o **link de download** — o arquivo já baixado no disco é permanente.
- O Chrome do usuário precisa ficar aberto (pode minimizado) durante toda a
  execução.
- Um pacote pode ter 40+ itens — processar tudo sem pausar pra confirmação a
  cada matéria, só reportar progresso a cada poucas matérias ou ao trocar de
  categoria.
- **Atualização Completa é bem mais lenta num pacote grande** — rebaixa todo PDF
  já existente do pacote inteiro só pra comparar a data. Não é o padrão sugerido;
  só usar quando o usuário pedir explicitamente ou aceitar a opção quando
  oferecida no Passo 2.
- Extração de data depende de `pypdf` (Python). Se o pacote não estiver
  instalado, instalar com `pip install pypdf` antes de processar a primeira aula.

## Regras gerais

- Não baixar vídeos, resumos, slides, mapas mentais ou cadernos de questões —
  só o livro eletrônico (PDF), em qualquer categoria.
- Não pular as perguntas do Passo 0 (link + pasta), do Passo 2 (pasta de pacote
  existente encontrada → Atualização Parcial, Atualização Completa ou criar
  nova), do Passo 4 (modo atualização — confirmar quais matérias atualizar) e
  do Passo 5 (modo novo — quais categorias baixar), mesmo que o usuário pareça
  já ter dado essas informações antes — confirmar a cada execução da skill.
- Se o link mandado for de um curso único (não um pacote), avisar e sugerir a
  skill `baixar-curso-especifico-estrategia`.
