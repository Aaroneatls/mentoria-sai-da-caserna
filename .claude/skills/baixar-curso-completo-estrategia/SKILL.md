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

3. **Base de siglas de disciplinas (pergunta temporária, perguntar sempre que
   a skill for carregada):** perguntar se já existe alguma planilha/tabela de
   referência com nome de disciplina → sigla. **Hoje essa base ainda não
   existe** — enquanto não existir, seguir usando o nome completo da matéria
   no nome da pasta (padrão atual do Passo 6). Quando o usuário criar essa
   base no futuro, ele vai indicar — a partir daí, usar a sigla da disciplina
   no lugar do nome completo ao montar o nome da pasta. Até lá, essa pergunta
   serve só de lembrete pro usuário, não bloqueia o fluxo. **Por que isso
   importa:** confirmado pelo Elvis em 2026-08-18, depois de um caso real em
   que somar o sufixo de data (Passo 6) ao nome já grande da matéria estourou
   o limite de 260 caracteres do Windows num arquivo — usar sigla no lugar do
   nome completo da matéria é a forma mais eficaz de ganhar margem de caminho
   de forma permanente, em vez de só sintetizar nome de arquivo caso a caso.

Não seguir em frente sem as respostas 1 e 2 acima.

**Reduzir o tamanho do caminho é uma preocupação constante, não só nos casos
óbvios** — confirmado pelo Elvis em 2026-08-18. Sempre que for nomear pasta ou
arquivo (pacote, categoria, matéria ou aula), já pensar no caminho completo
resultante (ver orçamento de caracteres nos "Detalhes técnicos" mais abaixo) e
preferir a versão mais curta que ainda deixe a aula identificável — não
esperar bater no limite pra só então cortar.

## Passo 1: Escolher o navegador, abrir o pacote e identificar concurso / cargo

1. **Escolher qual navegador controlar, antes de carregar qualquer tool:**
   - **Navegador embutido (Browser pane, `mcp__Claude_Browser__*`) é o padrão**
     — confirmado pelo Elvis em 2026-08-18. Usar esse por padrão sempre que o
     usuário não pedir explicitamente o Chrome. Essas tools já vêm carregadas
     por padrão, **não precisa de `ToolSearch`** — só confirmar o estado atual
     com `tabs_context` antes de navegar. Se a sessão estiver deslogada
     (redirecionar pra tela de login), avisar o usuário e esperar ele logar —
     nunca tentar digitar credenciais.
   - **Claude in Chrome (`mcp__claude-in-chrome__*`)** — **só usar com
     autorização prévia do usuário na própria conversa**, pedida a cada vez que
     for considerar essa alternativa (não vale autorização de uma sessão
     anterior). Se em algum momento parecer que vale a pena trocar pro Chrome
     (ex: navegador embutido indisponível ou deslogado), **perguntar antes de
     tentar** — nunca trocar de navegador sozinho no meio do processo sem
     avisar. Quando autorizado, carregar via `ToolSearch` com
     `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__browser_batch,mcp__claude-in-chrome__find,mcp__claude-in-chrome__form_input,mcp__claude-in-chrome__javascript_tool`
   - Se ficar ambíguo qual dos dois usar (nenhum sinal claro na mensagem do
     usuário), perguntar antes de prosseguir — evita carregar/tentar navegar
     no navegador errado.
   - **Tabela de equivalência** (os passos daqui pra frente na skill usam os
     nomes genéricos da esquerda — trocar pela tool real do navegador
     escolhido):

     | Ação genérica | Claude in Chrome | Navegador embutido |
     |---|---|---|
     | Navegar pra URL | `navigate` | `navigate` |
     | Rodar JS na página | `javascript_tool` | `javascript_tool` |
     | Ler texto da página | `get_page_text` | `get_page_text` |
     | Screenshot / clique | `computer` | `computer` |
     | Contexto de abas | `tabs_context_mcp` | `tabs_context` |
     | Buscar elemento | `find` | `find` |

   - **Mecânica de download é a mesma nos dois navegadores** (ver Passo 7) —
     a diferença é só qual conjunto de tools chamar. Não depende de clicar em
     card nem abrir aba, então a instabilidade de clique em coordenadas
     observada no navegador embutido não afeta esse fluxo.
2. Navegar até o link do pacote. Se o navegador pedir aprovação de domínio (ou
   login, no caso do navegador embutido), é normal na primeira vez.
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
6. **Pacote "Regular" sem concurso específico:** alguns pacotes não são de um
   concurso/edital específico — são pacotes genéricos por área, cobrindo
   matérias comuns a vários concursos daquela área. **O sinal pra reconhecer
   esse caso é a própria palavra "Regular" no nome do pacote** (ex: título
   "Curso Regular para Área Fiscal - Pacote Completo" → é o pacote "Regular
   Fiscal"; existe também "Regular Controle"), não a ausência de sigla de
   edital. Ao identificar esse padrão, usar `(Regular <Área>)` no lugar de
   `(SIGLA_CONCURSO-SIGLA_CARGO)` em todo nome de pasta (ex: `Direito
   Administrativo (Regular Fiscal)`). Não precisa perguntar ao usuário quando
   reconhecer esse padrão — só confirmar se o próprio nome da área ficar
   ambíguo.
7. **"Reforma Tributária" conta como disciplina própria, e pode aparecer mais
   de uma vez no mesmo pacote** — confirmado pelo Elvis em 2026-08-17. Não é
   pra descartar nem tratar como "extra". Quando o nome "Reforma Tributária"
   aparecer em mais de um item do pacote (ex: "Legislação Tributária sobre o
   Consumo (LTC) - Reforma Tributária...", "Reforma Tributária - Lei
   Complementar nº 227/2026...", "Reforma Tributária (LC nº 227/2026)" — cada
   um cobrindo uma frente diferente da reforma, não duplicados), tratar como
   **uma matéria "Reforma Tributária" com uma subpasta por curso**:
   `Curso Regular/Reforma Tributária (Regular <Área>)/<nome curto do curso
   específico>/` — o nome de cada subpasta sintetizado a partir do que
   diferencia aquele curso dos outros (diploma legal e/ou professor), já que
   os títulos completos tendem a ser grandes e parecidos entre si. Reconhecer
   esse padrão sozinho, sem precisar perguntar ao usuário.

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
acentuação, um eventual prefixo `(N-M)` nas subpastas, e o sufixo de data
`(DD-MM-AAAA)` no final tanto da pasta do pacote quanto de cada subpasta de
matéria.

**A varredura tem que descer até os arquivos, não parar no primeiro nível** —
confirmado em 2026-08-18, depois de um erro real: uma matéria pode ter
**subpastas** (a própria skill cria isso pra Reforma Tributária, ver Passo 1.7),
então os PDFs podem estar dois níveis abaixo da pasta de matéria. Numa execução
a pasta `Reforma Tributária (Regular Fiscal)` foi dada como vazia quando na
verdade tinha 33 PDFs em 3 subpastas — porque a listagem parou num nível acima.
Usar varredura recursiva (`os.walk` / `find`) ao contar o que já existe, nunca
só `ls` do primeiro nível. Vale também pro Passo 4 e pro `(N-M)` do Passo 9:
numa matéria com subpastas, **N e M são a soma de todas elas**, e o prefixo e a
data vão na pasta da matéria (a mãe), não em cada subpasta.

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
   | Começa com "Monitoria" | **Monitoria** | livro único por aula (**tem** livro eletrônico — confirmado em 2026-08-18) |
   | Qualquer outro padrão não reconhecido | **Outra categoria** — criar uma categoria nova com nome descritivo baseado no padrão observado | testar ao abrir a primeira aula (Passo 6) |

   **Monitoria** é curso único, com poucas aulas (5 no pacote Regular
   Controle), sobre ciclo de estudos, análise estatística de banca e
   estratégia de revisão — não é matéria de conteúdo. Vira **uma pasta só**
   dentro da categoria, igual Bizu/Trilha/Simulado (ver Passo 6).

3. **Todas as categorias têm livro eletrônico pra baixar**, inclusive Simulado,
   Discursiva e Trilha Estratégica — confirmado na prática: cada uma delas segue
   o mesmo padrão de card único "Baixar Livro Eletrônico versão original" que o
   Passo Estratégico e o Bizu Estratégico usam (ver Passo 7). Não existe categoria
   "sem livro" por padrão — todas entram como opção de download no Passo 5.
4. Se aparecer algum item cuja categoria não dá pra determinar só pelo nome, abrir
   o curso (Passo 6) rapidamente pra checar o card de "Baixar Livro Eletrônico"
   antes de decidir em qual grupo de padrão de download ele se encaixa.
5. **Dois itens com o nome exatamente igual e Curso IDs diferentes → perguntar,
   não escolher sozinho.** Confirmado na prática em 2026-08-18: o pacote Regular
   Controle trazia duas "Trilha Estratégica" com título idêntico, IDs `226812` e
   `369916` — uma com as aulas descritas como "(Pré-Edital)" e outra com
   numeração limpa, ou seja, edições diferentes do mesmo material. **O ID maior
   costuma ser o mais recente, mas isso não é garantia** e o usuário pode querer
   as duas. Abrir a listagem de cada uma pra descrever a diferença (quantas
   aulas, como as aulas estão descritas) e perguntar: só a mais nova, só a
   antiga, ou as duas. Se ele pedir as duas, criar **uma subpasta por edição**
   dentro da pasta da categoria, pra não misturar arquivos de mesmo rótulo.

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
4. **Conferir o Curso ID de cada matéria antes de tratar como atualização —
   crítico, confirmado pelo Elvis em 2026-08-18.** Mesma lógica da skill
   `baixar-curso-especifico-estrategia` (ver "Conferir o Curso ID do
   Estratégia" no Passo 3 dela, incluindo a comparação do assunto da Aula 00
   antiga vs. nova pra dar contexto no aviso): se a matéria já tem planilha
   de metadados (Passo 11 abaixo), comparar o Curso ID registrado nela com o
   ID da URL atual daquela matéria. Se diferente, **avisar o usuário logo no
   início** em vez de decidir sozinho — a Estratégia às vezes atribui ID novo
   a um curso mantendo o mesmo conteúdo, então ID diferente não é prova de
   curso diferente; o critério real é comparar disciplinas/aulas. Fazer essa
   checagem matéria por matéria, não só uma vez pro pacote inteiro.
5. Apresentar um resumo pro usuário, por categoria e matéria, por exemplo:

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
<pasta raiz>/<Nome do Pacote> (DD-MM-AAAA)/
├── Curso Regular/
│   ├── Contabilidade Geral (SIGLA-SIGLA) (DD-MM-AAAA)/
│   ├── Direito Constitucional (SIGLA-SIGLA) (DD-MM-AAAA)/
│   └── ...
├── Passo Estratégico/
│   ├── Contabilidade Geral (SIGLA-SIGLA) (DD-MM-AAAA)/
│   ├── Direito Constitucional (SIGLA-SIGLA) (DD-MM-AAAA)/
│   └── ...
├── Bizu Estratégico/
│   └── Bizu Estratégico (SIGLA-SIGLA) (DD-MM-AAAA)/   ← pasta única, não separa por matéria
├── Discursiva Sem Correção/
│   └── Discursiva Sem Correção (SIGLA-SIGLA) (DD-MM-AAAA)/   ← pasta única, curso já é um bloco só
├── Trilha Estratégica/
│   └── Trilha Estratégica (SIGLA-SIGLA) (DD-MM-AAAA)/        ← pasta única
└── Simulado/
    └── Simulado (SIGLA-SIGLA) (DD-MM-AAAA)/                  ← pasta única
```

- Uma pasta por categoria selecionada no Passo 5.
- Dentro de cada categoria com múltiplas matérias (Curso Regular, Passo
  Estratégico), uma subpasta por matéria, no mesmo padrão de nome da skill
  `baixar-curso-especifico-estrategia`: `Matéria (SIGLA_CONCURSO-SIGLA_CARGO)`.
  Esse é o nome "base" criado antes de baixar qualquer aula — no final (Passo 9),
  a pasta é renomeada (nunca apagada e recriada) pra ganhar o prefixo `(N-M)` na
  frente se o curso ainda não estiver completo, e o sufixo de data no final.
- **Bizu Estratégico, Discursiva Sem Correção, Trilha Estratégica e Simulado são
  exceção:** cada uma delas já é um curso único no site (não um curso por
  matéria), então vira **uma pasta só** dentro da categoria (ex:
  `Bizu Estratégico (SIGLA-SIGLA)`), com todos os PDFs das aulas daquele bloco
  dentro (ver Passo 7).
- **`(DD-MM-AAAA)` no nome do pacote e de cada matéria** — confirmado pelo
  Elvis em 2026-08-18: a pasta do pacote (nível mais alto) leva um sufixo de
  data indicando a última vez que **qualquer coisa** dentro dela foi
  baixada/atualizada; cada pasta de matéria leva o **seu próprio** sufixo de
  data, indicando a última vez que **aquela matéria específica** foi
  baixada/atualizada. São controles independentes — é comum atualizar só uma
  matéria do pacote sem tocar nas outras, e a data de cada pasta reflete isso
  individualmente. Na criação (download novo), a data em ambos os níveis é a
  de hoje. Ver Passo 9 pra como a data da matéria é recalculada, e Passo 10
  pra como a data do pacote é recalculada no final.
- **Modo novo:** criar tudo do zero com `mkdir -p`, dentro da pasta informada no
  Passo 0 (nenhuma pasta de pacote correspondente foi encontrada no Passo 2).
- **Modo atualização:** usar a pasta do pacote localizada no Passo 2; criar só
  as subpastas de categoria/matéria que ainda não existirem (matérias novas no
  pacote), sem recriar as que já existem — sempre atualizar em cima da pasta
  existente, nunca apagar e recriar (ver regra no Passo 9).

## Verificação pendente (pedido do Elvis em 2026-08-18): dá pra baixar tudo por `fetch`?

**Fazer essa checagem no começo da próxima execução desta skill e reportar o
resultado ao Elvis no relatório final.** Não travar o download por causa dela:
se a resposta for "não dá" ou ficar duvidoso, seguir normalmente com o método
atual desta skill.

Contexto: nas skills do Bruno Bezerra (`baixar-resumo-especifico` /
`baixar-resumo-combo-completo`) o download inteiro passou a ser feito por
`fetch` de mesma origem, a partir de **uma única página aberta**, sem navegar
aula por aula — o que eliminou travamento da SPA, esperas longas de
renderização e throttling de timer, e derrubou o tempo do combo inteiro (336
aulas) pra ~40 minutos. O Elvis pediu pra conferir se o mesmo vale aqui.

O que checar no Estratégia (`estrategiaconcursos.com.br`), com o curso já
aberto e logado:

1. **Lista de aulas** — esta skill já usa a API interna (ver "Atalho
   recomendado: pegar todas as aulas de uma vez pela API interna"). Confirmar
   se ela continua respondendo e se cobre tudo que a barra lateral mostra.
2. **Link do PDF de cada aula sem abrir a aula** — procurar o endpoint que a
   página chama pra montar o botão de download do livro eletrônico (olhar
   `read_network_requests` filtrando por `api`, e o payload embutido na
   página). Se existir, é o equivalente ao "server action de materiais" do
   Bezerra.
3. **Download direto por `curl`** — testar se a URL final do PDF funciona fora
   do navegador (como no Bezerra, onde `/api/student/pdf?token=...` responde
   sem cookie de sessão) ou se depende de cookie/sessão, o que obriga a manter
   o download dentro do navegador.

**Se os três passarem:** reescrever o passo de download desta skill no mesmo
molde do Passo 4/5 da `baixar-resumo-especifico` — mas só **depois de
apresentar a proposta ao Elvis e ter o aval dele** (regra do passo de sugestão
de melhoria, que vale igual aqui).

**Se algum falhar:** registrar no relatório final o que falhou e por quê, pra
não ficar refazendo a mesma investigação em toda execução.

## Passo 7: Baixar o livro de cada aula de cada matéria selecionada

Para cada matéria dentro de cada categoria selecionada (Passo 5) ou confirmada
pra atualização (Passo 4), repetir o mesmo processo da skill
`baixar-curso-especifico-estrategia` (Passos 4 a 6 dela), com uma diferença por
categoria:

### Nome do arquivo — rótulo exato da aula (regra geral, vale pra todas as categorias)

**O rótulo da aula (a parte "Aula NN" nos exemplos abaixo) tem que ser copiado
exatamente como aparece na listagem do site, nunca um contador sequencial
próprio dado por quem baixou** — confirmado pelo Elvis em 2026-08-18. Exemplos
reais observados: `Aula 00`, `Aula 01`, `Aula 01 - Parte II` (quando o site
quebra uma aula em mais de uma parte — manter "Parte II" tal como está, não
virar "Aula 02"), `Aula Extra` (aula bônus fora da numeração principal), ou até
títulos sem número tipo `RESUMO - Parte Geral do CC` — usar o próprio título
da aula como rótulo nesse caso. Nunca substituir o rótulo real dado no site
pela numeração sequencial da ordem de download.

**Exceção: anotações de formato/equipe não entram no rótulo** — confirmado
pelo Elvis em 2026-08-18. Tags que descrevem o *tipo de mídia* ou a *equipe*
responsável pela aula, não o *assunto* tratado nela, ficam de fora do nome do
arquivo. Exemplos que **não** entram: `(Somente PDF)`, `(Somente em PDF)`,
`(Aula em PDF)`, `(Equipe de Legislação)`, `(Somente Vídeo)`. Ex: `Aula 20
(Somente PDF)` no site vira só `Aula 20` no arquivo.

**Exceção: nome de professor também não entra no rótulo** — confirmado pelo
Elvis em 2026-08-18. Alguns cursos do pacote rotulam a aula com o autor (ex:
`Aula 00 - Prof. Diego Carvalho e Emannuelle Gouveia`, em Análise de
Informações; `Aula 00 - Prof. Leonardo Mathias`, na Monitoria). O professor é
metadado de autoria, não assunto — o arquivo fica `Aula 00 - <assunto
sintético>`, e a autoria já está registrada na primeira página do próprio PDF.
Num pacote isso costuma valer pra **todas** as aulas da mesma matéria, não só
uma. **Se aparecer algum outro tipo de anotação
parecida que não se encaixe claramente como "tipo de mídia/equipe" nem como
parte do conteúdo, perguntar ao usuário antes de decidir** — não adivinhar
sozinho pra esse caso novo.

**A anotação nem sempre vem entre parênteses.** Visto na prática:
`Aula 16- Somente em PDF`, `Aula 15 - Somente em PDF`, `Aula Extra (Somente
pdf)`. Tratar todas do mesmo jeito, com ou sem parênteses, com ou sem espaço
antes do traço.

**Exceção: créditos de professor também não entram no rótulo** — confirmado em
2026-08-18. O curso de Tecnologia da Informação nomeia as aulas como
`Aula 00 - Prof. Diego Carvalho e Renato da Costa`. Nome de professor descreve
*quem deu* a aula, não o *assunto* dela, então sai do rótulo pela mesma lógica
das anotações de formato: `Aula 00 - Prof. Diego Carvalho e Renato da Costa`
vira só `Aula 00`. Regra prática: cortar tudo a partir de ` - Prof.` /
` - Profa.` até o fim do rótulo (isso já leva junto um eventual `(Somente em
PDF)` no final). Cuidado pra não confundir com `Aula 01 - Parte II`, que **é**
parte do rótulo e fica.

**Rótulos repetidos na mesma matéria: desempatar pelo conteúdo.** Existem cursos
com duas aulas de nome idêntico — em Administração Financeira e Orçamentária há
**duas** `Aula Extra - Somente em PDF`, uma de "Questões Extras FGV" e outra de
"Questões Extras CEBRASPE". Casando só pelo rótulo, os dois arquivos trocam de
lugar (e ficam com o assunto errado no nome) ou um sobrescreve o outro. Quando
o rótulo limpo aparecer mais de uma vez no mesmo curso:

1. comparar o `conteudo` da aula (vem da API) com o nome do arquivo local e
   parear o que tiver mais palavras em comum;
2. **se nenhum arquivo bater, não parear** — deixar aquela aula de fora e citar
   na Validação Final, em vez de arriscar sobrescrever o arquivo errado.

**Exceção: limite de caminho do Windows.** Se o caminho completo do arquivo
estiver perto do limite de 260 caracteres (ver "Limite de 260 caracteres de
caminho no Windows" nos Detalhes técnicos), é permitido sintetizar/abreviar o
rótulo — abreviar o assunto primeiro, e só mexer no rótulo como último
recurso, mantendo pelo menos o número/palavra que identifica a aula (ex:
`Aula 01 - Parte II` pode virar `Aula 01-PII` se for realmente necessário, mas
não virar `Aula 02`). Fora desse cenário de limite de caminho, o rótulo nunca
é sintetizado nem abreviado.

### Curso Regular

- Igual à skill original: preferir "Baixar Livro Eletrônico versão simplificada";
  se não existir, usar "versão original" como fallback.
- **CRÍTICO — o "simplificado" pode ser só um aviso, não a aula.** Confirmado
  na prática em 2026-08-18 (pacote Regular Controle: 19 aulas afetadas, 14 em
  Contabilidade Geral Avançada e 5 em Contabilidade Pública). Em algumas aulas
  o card "versão simplificada" existe e baixa normalmente, mas o PDF tem só
  ~3 páginas e diz que *aquela aula não possui PDF simplificado devido às suas
  características*. A presença do card não garante conteúdo — e o arquivo é um
  PDF válido, então passa em qualquer checagem de formato. Depois de baixar a
  simplificada, antes de renomear: se o PDF tiver **8 páginas ou menos** e o
  texto das 4 primeiras páginas contiver ao mesmo tempo `possui` e
  `simplificado`, descartar o `.tmp` e **rebaixar aquela aula na versão
  original**, sem perguntar ao usuário. Citar as trocas no resumo final. Ver o
  trecho de código na `baixar-curso-especifico-estrategia` (Passo 5, item 6.1).
  **Num pacote isso tende a se concentrar em disciplinas inteiras** (as de
  norma comentada/esquematizada), então não é um caso isolado: se aparecer numa
  aula, esperar mais na mesma matéria.
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

### Extrair a data do PDF (e checar o conteúdo contra o assunto esperado)

Depois de baixar cada PDF (todo download, não só em modo atualização), extrair
a data de elaboração/atualização que aparece na primeira página, pra usar no
nome do arquivo — **e aproveitar essa mesma abertura pra checar, de graça, se
o conteúdo bate com o assunto esperado da tabela** (mesmo script e mesma
lógica da skill `baixar-curso-especifico-estrategia`, ver "Extrair a data do
PDF" lá pra explicação completa da checagem — confirmado pelo Elvis em
2026-08-18):

```bash
python -c "
import re, sys, unicodedata
from pypdf import PdfReader

MESES = {'janeiro':1,'fevereiro':2,'marco':3,'abril':4,'maio':5,'junho':6,
         'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}
STOPWORDS = {'para','como','entre','sobre','pela','pelo','pelas','pelos','com',
             'sem','das','dos','que','uma','um','os','as','de','do','da','em',
             'na','no','por','seu','sua','ao','aos'}

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
def norm(s):
    return strip_accents(s).lower()

reader = PdfReader(sys.argv[1])
texto = reader.pages[0].extract_text() or ''

m = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
if m:
    data = f'{m.group(1)}-{m.group(2)}-{m.group(3)}'
else:
    m2 = re.search(r'(\d{1,2}) de ([A-Za-zçÇéÉ]+) de (\d{4})', texto)
    if m2:
        dia, mes_nome, ano = m2.groups()
        mes_num = MESES.get(strip_accents(mes_nome.lower()))
        data = f'{int(dia):02d}-{mes_num:02d}-{ano}' if mes_num else ''
    else:
        data = ''
print(data)

assunto = sys.argv[2] if len(sys.argv) > 2 else ''
if assunto:
    palavras = [w for w in re.findall(r'[A-Za-zÀ-ÿ0-9]+', assunto)
                if len(strip_accents(w)) >= 4 and norm(w) not in STOPWORDS]
    n_pages = min(6, len(reader.pages))
    texto_conteudo = ' '.join((reader.pages[i].extract_text() or '') for i in range(n_pages))
    texto_norm = norm(texto_conteudo)
    hits = sum(1 for w in palavras if norm(w) in texto_norm)
    print(f'MATCH:{hits}/{len(palavras)}' if palavras else 'MATCH:sem_palavras_chave')
else:
    print('MATCH:sem_assunto')
" "<caminho do PDF baixado com nome temporário>" "<assunto esperado>"
```

- **Duas formas de data já observadas na prática:** numérica `DD/MM/AAAA` e
  escrita por extenso em português `DD de Mês de AAAA` (ex: "31 de Julho de
  2026" — confirmado testando no curso de Direito Administrativo, pacote
  Regular Fiscal). O script acima cobre os dois, tentando o numérico primeiro.
- **Segunda linha de saída (`MATCH:hits/total`):** `hits` igual a 0 com
  `total` maior que 0 → possível conteúdo errado — não travar o download,
  só registrar essa aula como suspeita pra citar na Validação Final (Passo 10).
  **`total` igual a 1 ou 2 é sinal de confiança baixa mesmo com `hits` 0** —
  confirmado numa checagem em lote real em 2026-08-18 contra ~480 aulas já
  confirmadas corretas: os poucos `0/total` encontrados eram todos assunto
  curto (1-3 palavras) com variação de fraseado no PDF, não conteúdo errado.
  Tratar como aviso fraco nesse caso, não como erro confirmado.
- **Checagem de conteúdo olha as primeiras 6 páginas, não só a primeira** —
  confirmado pelo Elvis em 2026-08-18: a página 1 costuma ser só capa (título,
  autor, data), o conteúdo real da aula só aparece depois do índice/apresentação
  do curso. A extração de **data** continua só na página 1 (sempre funcionou
  bem); é a checagem de **conteúdo** que precisa olhar mais páginas.
- **Se der 0 acertos nas 6 primeiras páginas, ampliar pra ~25 antes de marcar
  como suspeita** — confirmado na prática em 2026-08-18 (pacote Regular
  Controle): das 211 aulas, 5 caíram como suspeitas e **todas as 5 eram falso
  positivo** — aulas cujo índice ocupa várias páginas, então em 6 páginas só
  tem capa e sumário. Ampliando a janela o conteúdo aparece com folga (a aula
  de SQL tinha 57 ocorrências de "sql" nas 25 primeiras páginas e 0 nas 6
  primeiras). A segunda passada só roda pras aulas que deram `0/total`, então
  custa quase nada — e num pacote isso é o que separa um relatório final limpo
  de uma lista de suspeitas que o usuário vai ter que conferir na mão.
- Baixar sempre com nome temporário (`.tmp`), extrair a data, e só então renomear
  pro nome final com a data.
- Se `pypdf` não estiver instalado, instalar com `pip install pypdf` antes de
  processar a primeira aula.
- **Fallback se não achar data:** manter o nome do arquivo sem o sufixo
  `(DD-MM-AAAA)` e seguir normalmente — não travar o download. Mencionar no
  resumo final quais aulas ficaram sem data identificada.

### Atalho recomendado: pegar todas as aulas de uma vez pela API interna

**Confirmado em 2026-08-18.** Em vez de abrir a listagem e depois cada aula pra
extrair o `a.LessonButton`, dá pra buscar **o curso inteiro numa única chamada**:

```
GET https://api.estrategiaconcursos.com.br/api/aluno/curso/{cursoId}
Authorization: Bearer <token de GET /oauth/token/>
```

A resposta traz, para **cada** aula: `id`, `nome` (o rótulo exato), `conteudo`
(o assunto), `is_disponivel`, `data_publicacao`, `pdf` e `pdf_simplificado`
(links já assinados). Num pacote de 24 cursos / ~480 aulas isso troca centenas
de navegações por 24 chamadas — a diferença entre horas e minutos.

Como usar sem violar a regra de credenciais:

- O `Bearer` **fica dentro do navegador**. Rodar o `fetch` via `javascript_tool`
  e trazer de volta **apenas os links assinados** (e os metadados das aulas).
  Nunca extrair o token pro shell — além de desnecessário, o classificador do
  Claude Code bloqueia isso, e com razão.
- A assinatura é **por aula**, mas a mesma serve tanto para `/pdf/download/{id}`
  quanto para `/pdfSimplificado/download/{id}`.
- **Os links duram pouco: ~20-30 minutos.** O campo `expiration` da URL vem com
  o relógio do servidor (umas 2h à frente do local) e **engana** — não usar ele
  como referência. Trabalhar em blocos de 2-3 cursos, gerando as assinaturas
  imediatamente antes de cada bloco. Link vencido devolve HTTP 200 com a home
  em HTML, exatamente igual ao erro de User-Agent.
- Aula ainda não liberada vem com `pdf` nulo — tratar como travada (Passo 8).
- Uma forma compacta de trazer os dados sem inflar o contexto: pedir ao
  navegador só `id:assinatura` por aula e casar com a tabela de rótulos que já
  foi montada no Passo 3.

Se a API falhar ou mudar, o caminho antigo (navegar aula por aula e ler o
`a.LessonButton`) continua válido como fallback — está logo abaixo.

### Mecânica de download (igual em todas as categorias)

1. Navegar para `https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{id}/aulas/{aulaId}`
   (ou clicar no título da aula na lista) e esperar ~2s carregar. **Conferir o
   título da aba depois de navegar** — se voltar genérico ("Área do Aluno", ou
   o mesmo título de antes) em vez do título real da aula/curso, a navegação
   falhou silenciosamente (transiente, observado várias vezes na prática) —
   **renavegar uma vez pra mesma URL antes de seguir**, em vez de extrair o
   `LessonButton` de uma página errada.
2. **Não precisa clicar no card nem abrir aba nova.** O link de download já
   está no HTML da própria página, num `<a class="LessonButton">`. Extrair
   direto via JavaScript (`javascript_tool`):
   ```js
   const links = Array.from(document.querySelectorAll('a.LessonButton'))
     .map(a => ({ texto: a.textContent.replace(/\s+/g, ' ').trim(), href: a.href }));
   JSON.stringify(links);
   ```
   Isso retorna um link pra cada card presente na aula — escolher o que
   corresponde à categoria (ver acima).

   **Sempre filtrar os botões pelo ID da aula antes de usar o link** —
   confirmado na prática em 2026-08-18. O `href` de download termina em
   `/download/{aulaId}`; se o link capturado apontar pra outro ID, é o botão
   da aula **anterior**, que ainda não saiu do DOM (a troca de página é
   assíncrona). Isso já gerou um download de 188 bytes sem erro aparente:
   ```js
   const links = Array.from(document.querySelectorAll('a.LessonButton'))
     .filter(a => a.href.includes('/download/' + aulaId));
   ```
   O mesmo filtro serve pra saber que a página da aula certa já carregou.

2.1. **Coleta em lote pela própria SPA (recomendado num pacote).** A área do
   aluno é um SPA React: clicar no `<a>` da aula troca a página sem reload e
   `history.back()` volta pra listagem — então dá pra colher os links de
   **várias aulas num único `javascript_tool`**, em vez de um `navigate` por
   aula. Num pacote de 211 aulas isso trocou ~240 navegações por ~40 chamadas
   (confirmado em 2026-08-18). O script completo está na
   `baixar-curso-especifico-estrategia`, seção "Fallback rápido: percorrer as
   aulas dentro da própria SPA". Regras que valem sempre:
   - **No máximo 7 aulas por chamada** — cada aula leva ~2,5-3s e o executor
     de JS corta em 30s; lote maior estoura e perde a chamada inteira.
   - **Devolver só `expiration` e `signature`** de cada aula, não a URL
     inteira: o resto é template fixo, remontável no shell. Num pacote grande
     isso economiza muito contexto.
   - Alguns `href` vêm como `{aulaId}/videos/{videoId}` — extrair o ID com
     `.split('/')[0]`.
   - Consumir o lote logo depois de coletar: **os links assinados vencem em
     poucos minutos**. Link vencido devolve HTML/arquivo minúsculo no lugar do
     PDF — nesse caso, recoletar a assinatura daquela aula e repetir.
3. Baixar o PDF **direto pra pasta de destino**, com nome temporário, via `curl`
   (Bash) com `-L` (o link redireciona pra CDN assinada
   `cdn.estrategiaconcursos.com.br/.../....pdf?Expires=...&Signature=...`), sem
   passar pela pasta de Downloads:
   ```bash
   curl -sL -o "<pasta>/<nome do arquivo>.pdf.tmp" "<href capturado>" \
     -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36" \
     -H "Referer: https://www.estrategiaconcursos.com.br/" \
     -w "HTTP:%{http_code} SIZE:%{size_download}\n"
   ```

   **O `User-Agent` de browser é obrigatório** — confirmado na prática em
   2026-08-18: com o User-Agent padrão de `curl`/`python-requests` o servidor
   responde **HTTP 200 devolvendo a home do site em HTML (~238 KB)** no lugar
   do PDF. O `Referer` acompanha pelo mesmo motivo.

   **CRÍTICO — nunca validar o download só pelo tamanho.** Como a home em HTML
   tem ~238 KB, qualquer teste do tipo "HTTP 200 e SIZE não-trivial" aceita
   lixo como se fosse PDF. Isso já destruiu 27 PDFs bons numa execução real
   (eles foram apagados e substituídos pelo HTML). Antes de considerar o
   download válido, conferir **as três coisas**:

   1. `HTTP:200`;
   2. os **5 primeiros bytes do arquivo são `%PDF-`** (se o arquivo começa com
      `<`, é HTML: descartar o `.tmp` e repetir a tentativa);
   3. o `pypdf` abre o arquivo e retorna **número de páginas > 0**.

   ```bash
   head -c 5 "<arquivo>.tmp" | grep -q '%PDF-' && echo PDF_OK || echo RECUSADO
   ```

   **Só apagar/substituir o PDF antigo depois que os três testes passarem.**
   Enquanto não passarem, o arquivo que já estava na pasta continua intocado.

   **Bloqueio por volume:** depois de algumas centenas de downloads seguidos na
   mesma conta (~600 numa execução real), a plataforma passa a responder
   **HTTP 302 → HTML** para qualquer PDF — inclusive quando o download é feito
   de dentro do próprio navegador logado. Não é User-Agent nem assinatura
   vencida: é limite da conta. Quando isso acontecer, **parar os downloads,
   avisar o usuário e retomar as matérias que faltaram noutro momento** — nunca
   insistir em laço, e nunca deixar o `.tmp` recusado substituir arquivo bom.
4. Extrair a data (ver acima) e renomear o `.tmp` pro nome final.
5. Voltar pra lista de aulas da matéria e seguir pra próxima aula. Depois de
   esgotar as aulas da matéria, voltar pra página do pacote e ir pra próxima
   matéria/categoria.

**Nota sobre cliques no navegador embutido (Browser pane):** clicar em
coordenadas de tela em itens de listagem (cursos, cards) nem sempre navega de
forma confiável nesse navegador — prefira sempre extrair o `href` real via
`javascript_tool` e navegar direto pela URL, em vez de clicar às cegas.

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

## Passo 9: Nomear a pasta com indicador de progresso (N-M) e data de atualização

Depois de terminar todas as aulas de uma matéria/bloco (pasta de Curso Regular,
Passo Estratégico, ou a pasta única de Bizu/Discursiva/Trilha/Simulado):

1. Contar **M** = total de aulas do curso (linhas na listagem `/aulas`) e **N** =
   quantas delas realmente têm PDF baixado (arquivos `.pdf` de verdade, não os
   `.txt` placeholder do Passo 8).
2. **Se N < M** (curso incompleto): renomear a pasta pra começar com `(N-M) `,
   ex: `(10-20) Direito Administrativo (SIGLA-SIGLA) (18-08-2026)` (10 aulas
   com PDF já disponível, de um total de 20 aulas no curso). O indicador fica
   **entre parênteses, colado direto no nome da matéria** — sem traço
   separando os dois, só um espaço. **Usar traço dentro do parênteses (`N-M`),
   nunca barra (`N/M`)** — barra é separador de caminho no Windows e quebra o
   `Rename-Item` (confirmado na prática: tentar renomear com `/` lança erro
   "representa um caminho ou nome de dispositivo").
3. **Se N == M** (curso completo): a pasta fica sem o prefixo `(N-M)`, só
   `Direito Administrativo (SIGLA-SIGLA) (18-08-2026)`.
4. **Atualizar também o sufixo de data no final do nome pra data de hoje**
   (ver regra no Passo 6) — nessa mesma operação de renomear, sempre, pra
   registrar quando essa matéria específica foi mexida pela última vez. Isso
   vale mesmo que só essa matéria tenha sido tocada nessa execução, sem mexer
   nas outras do pacote.
5. **Modo atualização:** antes de recalcular, remover qualquer prefixo `(N-M) `
   e qualquer sufixo de data antigo que a pasta já tenha (de uma execução
   anterior) pra não acumular — sempre recalcular do zero e renomear com os
   números e a data atuais.
6. **Sempre renomear a pasta existente com `Rename-Item` (ou equivalente) — nunca
   apagar a pasta (ou a árvore inteira) e recriar do zero pra aplicar esse
   prefixo/data.** Apagar e recriar perde a pasta original (e qualquer PDF real já
   baixado nela) e conta como criar uma pasta nova, não atualizar a existente —
   o que vale tanto pra corrigir o prefixo quanto pra qualquer outro ajuste feito
   em modo atualização.

Isso deixa visível, só olhando o nome da pasta no Explorer, quais matérias ainda
têm aula pendente de liberação pelo site, quais já estão 100% baixadas, e quando
cada uma foi mexida pela última vez.

**Data da pasta do pacote (nível acima):** depois de processar **qualquer**
matéria/bloco (mesmo só uma, mesmo em modo atualização tocando uma matéria só),
atualizar também o sufixo de data da pasta do pacote (raiz, ver Passo 6) pra
data de hoje — ela reflete a atividade mais recente em qualquer parte do
pacote, não só quando o pacote inteiro é rebaixado. Fazer essa renomeação uma
vez só, depois de processar todas as matérias da execução atual (não a cada
matéria individual) — evita renomear a pasta-raiz repetidamente à toa.

## Passo 10: Validação final (obrigatória — sempre rodar antes de dar o pacote como concluído)

**Confirmado pelo Elvis em 2026-08-18: essa validação é parte obrigatória da
skill, não um extra — nunca reportar o pacote (ou uma matéria dele) como
concluído sem rodar esse passo.**

**Validação é só por nomenclatura, nunca reabrindo o conteúdo dos PDFs aqui** —
confirmado pelo Elvis em 2026-08-18: não vale a pena gastar tokens
abrindo/lendo cada PDF de novo nessa etapa. A checagem de conteúdo já
aconteceu uma vez, de graça, durante o download (ver "Extrair a data do PDF"
no Passo 7, saída `MATCH:hits/total`) — aqui só se **reporta** o que ela
sinalizou, sem reabrir nada. O cruzamento desse passo é puramente comparação
de texto: rótulo da listagem do site vs. nome do arquivo local.

Depois de processar todas as categorias/matérias selecionadas:

1. Listar a árvore de pastas criada (`ls` recursivo por categoria), já com os
   prefixos `(N-M)` renomeados.
2. **Pra cada matéria/bloco processado, conseguir a lista de rótulos atual.**
   Se essa matéria acabou de ser baixada nessa mesma execução (sem intervalo
   relevante de tempo), **reaproveitar a tabela salva no Passo 4/5** em vez de
   gastar uma nova consulta ao site. Só **re-consultar a listagem `/aulas` do
   site de novo** quando fizer sentido desconfiar que o estado mudou desde a
   coleta original (retomando de uma sessão anterior, ou intervalo longo) —
   nesse caso, só o `get_page_text` da listagem, sem abrir aula por aula. Em
   qualquer um dos dois casos, cruzar item a item com os arquivos locais dessa
   matéria/bloco, só pelo nome:
   - Cada rótulo de aula da listagem deve corresponder a exatamente um arquivo
     local (`.pdf` ou `.txt`) cujo nome começa com esse mesmo rótulo.
   - Rótulo sem arquivo correspondente → aula não baixada, investigar antes de
     considerar aquela matéria concluída.
   - Arquivo local sem rótulo correspondente → rótulo digitado errado ou aula
     que saiu da grade — investigar e, se for rótulo errado, renomear o
     arquivo pro rótulo certo (sem reabrir o PDF, só `mv`/`Rename-Item`).
3. Conferir que **N** (quantidade de `.pdf` reais) e **M** (total de itens na
   listagem do site) batem com o prefixo `(N-M)` aplicado no Passo 9 de cada
   matéria/bloco.
4. **Listar as aulas sinalizadas como suspeitas pelo `MATCH:hits/total`**
   durante o download (ver Passo 7) — as que deram `0/total` mesmo depois da
   janela ampliada de páginas. Não precisa reabrir PDF nenhum aqui, só trazer
   a lista consolidada pro resumo. **Se sobrarem poucas (até ~5 num pacote),
   vale abrir só essas na hora e conferir** — na prática elas costumam ser
   falso positivo, e conferir ali evita entregar pro usuário uma lista de
   pendências que não é pendência. As que forem conferidas e estiverem certas
   entram na planilha como `Baixado (conferido)` (ver Passo 11).
5. Reportar o resultado dessa validação pro usuário — matéria por matéria, se
   bateu 100% por nome, se sobrou algo em algum lado, e se alguma aula ficou
   marcada como suspeita de conteúdo (item 4) — mesmo a skill normalmente não
   gerando relatório à parte, essa validação final é sempre resumida em texto.

O resultado final é a estrutura de pastas em si, já com os arquivos dentro,
cada matéria/bloco renomeado com o progresso `(N-M)`, mais a confirmação de
que o cruzamento bateu em cada uma.

## Passo 11: Planilha de metadados de cada disciplina (obrigatória, Google Sheets)

**Confirmado pelo Elvis em 2026-08-18: toda matéria/bloco processado ganha uma
planilha de metadados própria, na mesma pasta dela** — mesmo processo e mesmo
formato validado na skill `baixar-curso-especifico-estrategia` (ver "Planilha
de metadados da disciplina" no Passo 9 dela — Google Sheets nativo via
`gspread` como preferência permanente, nunca `.xlsx` local; se a autenticação
falhar, parar e pedir ao usuário pra fazer login/reautorizar na hora em vez
de cair pro Excel silenciosamente; abas "Aulas" + "Legenda"; Curso ID no
subtítulo; fórmulas com `;` por causa do locale `pt_BR`; ler de volta pra
conferir que não deu `#ERROR!`/`#REF!`/`#NAME?`, já que não há `recalc.py`
funcionando nesse ambiente).

**Quota do Google Sheets:** a API permite **60 requisições de escrita por
minuto por usuário**, e montar uma planilha (update + formatações + freeze +
aba Legenda) gasta ~10 delas — ou seja, o teto é de ~6 planilhas por minuto.
Num pacote com 20+ matérias isso estoura e vem `APIError [429] Quota exceeded`
(aconteceu em 2026-08-18: 8 planilhas passaram, 14 falharam). Espaçar as
planilhas (~11s entre uma e outra) e, ao pegar um 429, **esperar ~65s e tentar
de novo** em vez de dar a planilha como perdida. Cuidado também com o padrão
"tenta abrir a aba, se falhar cria": se o erro for de quota e não de aba
inexistente, isso tenta criar uma aba que já existe e devolve
`400 Já existe uma página chamada "Legenda"`. Checar a existência da aba pela
lista de abas do arquivo, e só então limpar.

**Rodar sempre DEPOIS do Passo 9 (renomear).** A planilha grava o nome da pasta
no subtítulo (`Pasta: ...`), então se rodar antes da renomeação o subtítulo
nasce desatualizado.

**Diferença de escala:** num pacote inteiro, repetir esse passo pra **cada
matéria/bloco processado nessa execução**, uma planilha por pasta de
disciplina (não uma planilha única pro pacote inteiro) — mantém a
granularidade de "atualizar só uma matéria sem mexer nas outras" (mesma lógica
do sufixo de data por pasta, Passo 9). Bizu/Discursiva/Trilha/Simulado (pastas
únicas, sem separação por matéria) também ganham sua própria planilha, na
pasta única deles.

**Escopo da atualização da planilha = escopo da execução, confirmado pelo
Elvis em 2026-08-18:**
- Se o usuário pedir pra atualizar **só uma disciplina específica** dentro do
  pacote, só a planilha dessa disciplina é atualizada — as outras matérias do
  mesmo pacote ficam intocadas.
- Se o usuário pedir pra atualizar **o curso/pacote inteiro** (ou uma
  categoria inteira), **todas** as planilhas das disciplinas efetivamente
  processadas nessa execução são atualizadas — uma por matéria tocada.
- Em nenhum caso atualizar a planilha de uma matéria que não foi processada
  nessa execução, mesmo que esteja no mesmo pacote.

**Limite de escrita do Sheets — atenção redobrada num pacote.** Confirmado na
prática em 2026-08-18: a cota é de **60 requisições de escrita por minuto por
usuário**, e cada planilha consome várias (criar, `update` das duas abas,
`resize`, `batch_update` de formatação). Com 12 disciplinas de uma vez o erro
**HTTP 429** aparece por volta da sétima planilha e derruba a execução no meio.
Montar o script assim desde o começo:

- Retry por planilha, com espera de ~65s e até ~6 tentativas, só pra erro 429.
- Pausa de ~12s entre planilhas.
- **Idempotência obrigatória:** antes de criar, procurar pelo nome do arquivo
  dentro da pasta de destino no Drive e reaproveitar a planilha existente —
  senão, ao retomar depois do 429, as primeiras disciplinas ganham planilhas
  duplicadas.
- Como o processo é longo, imprimir o progresso planilha a planilha
  (`flush=True`) pra dar pra retomar sabendo onde parou.

## Passo 12: Sugestões de melhoria pra skill (obrigatória ao final de toda execução)

**Confirmado pelo Elvis em 2026-08-18: ao final de todo download/atualização
de pacote, refletir se algo observado nessa execução sugere um ajuste na
própria skill, e apresentar pro usuário aprovar** — não é opcional, é parte do
encerramento normal do processo. É a regra geral do workspace pra skills de
download em massa e de cadernos de questões (ver `AGENTS.md`), e vale igual na
`baixar-curso-especifico-estrategia` (Passo 10 dela).

Depois do relatório final (Passo 10) e das planilhas (Passo 11), avaliar se
algo aprendido nessa execução sugere um ajuste: bug novo, comportamento
inesperado do site, passo lento/repetitivo, oportunidade de deixar algo mais
robusto.

- Sugestão tem que ser **concreta e ligada a algo que realmente aconteceu**
  nessa execução — não inventar sugestão genérica só pra preencher esse passo.
- **Se identificar algo:** apresentar ao Elvis de forma objetiva (o que
  aconteceu, o que mudaria na skill), perguntar se aprova, e só então editar o
  `SKILL.md` (dessa skill e/ou da `baixar-curso-especifico-estrategia`, se
  aplicável às duas) e rodar `/syncar`.
- **Se nada de novo surgiu:** dizer isso de forma curta e objetiva — não
  forçar uma sugestão fraca só pra ter o que falar.
- Apresentar junto do resto do resumo final (validação + planilhas), não como
  pergunta solta separada.
- **Nunca editar a skill nem sincronizar sem aprovação prévia.**

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
