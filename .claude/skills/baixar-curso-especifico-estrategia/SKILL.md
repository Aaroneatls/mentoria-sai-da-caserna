---
name: baixar-curso-especifico-estrategia
description: >
  Baixa em lote os livros eletrônicos (PDF) de um curso específico do Estratégia
  Concursos, aula por aula, renomeando e organizando os arquivos numa pasta local.
  Prioriza a versão simplificada do livro; se não houver, usa a versão original.
  Use quando o usuário disser "baixa esse curso do Estratégia", "baixa os livros
  da matéria X", "sincroniza esse curso pra pasta", "atualiza o curso que já
  baixei", ou mandar um link de um curso do estrategiaconcursos.com.br pedindo
  pra organizar os PDFs.
---

# /baixar-curso-especifico-estrategia — Download em lote de livros do Estratégia Concursos

## O que essa skill faz

Usa o Chrome real do usuário (via extensão Claude in Chrome, já logado no Estratégia
Concursos) pra navegar pelas aulas de um curso, e baixa direto no disco — sem passar
pela pasta de Downloads — o livro eletrônico de cada aula, renomeado e organizado
numa pasta local.

## Passo 0: Perguntas obrigatórias no início

**Pasta padrão:** `G:\Meu Drive\Inteligência Artificial\Estrategia`
— é aqui que as pastas novas são criadas por padrão, salvo o usuário indicar
outro local. **Essa pasta vive dentro do Google Drive sincronizado**, então
antes de usar ela (seja pra criar algo novo, seja pra checar uma atualização),
**verificar que ela existe de fato no disco** (`Test-Path` / `ls`). Por ser uma
pasta sincronizada, pode não estar montada/sincronizada no momento — se não
existir, avisar o usuário em vez de simplesmente criar uma pasta nova do zero
sem querer em outro lugar.

Sempre perguntar as coisas abaixo antes de fazer qualquer coisa (não assumir, não pular):

1. **Link do curso** — a URL da página do curso no Estratégia Concursos (a página
   que lista "Aula 00, Aula 01..." — normalmente
   `https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{id}/aulas`).
2. **Pasta:** perguntar se quer usar a **pasta padrão** (acima) ou indicar um
   **novo local**. Se confirmar a pasta padrão, usar ela direto. Se pedir outro
   local, usar o caminho informado.

**Não perguntar aqui se é "novo ou atualização"** — isso é descoberto sozinho no
Passo 3, depois de identificar a matéria (Passo 1-2) e procurar automaticamente
por uma pasta já existente dentro do local informado. Ver Passo 3.

3. **Base de siglas de disciplinas (pergunta temporária):** perguntar se já
   existe alguma planilha/tabela de referência com nome de disciplina → sigla.
   **Hoje essa base ainda não existe** — enquanto não existir, seguir usando o
   nome completo da matéria no nome da pasta (padrão atual do Passo 2). Quando o
   usuário criar essa base no futuro, ele vai indicar — a partir daí, usar a
   sigla da disciplina no lugar do nome completo ao montar o nome da pasta. Até
   lá, essa pergunta serve só de lembrete pro usuário, não bloqueia o fluxo.

Não seguir em frente sem as respostas 1 e 2 acima.

## Passo 1: Abrir o curso e identificar matéria / concurso / cargo

1. Carregar as tools do Chrome (se ainda não carregadas):
   `ToolSearch` com `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__browser_batch`
2. Navegar até o link do curso. Se a extensão pedir aprovação de domínio, é normal
   na primeira vez.
3. Ler o título da página / cabeçalho do curso pra extrair:
   - **Matéria** (ex: Direito Constitucional)
   - **Sigla do concurso** (ex: TCDF) — geralmente já vem entre parênteses no título
   - **Cargo** (ex: Analista Administrativo de Controle Externo)
4. **Sigla do cargo:** se não tiver uma sigla óbvia already no título (tipo "ANACE"),
   pesquisar (na própria página do curso ou na internet) pela sigla oficial do cargo
   pro concurso em questão, e decidir sozinho — não precisa confirmar com o usuário.
5. **Sigla do concurso quando não vem óbvia entre parênteses:** pesquisar no Google
   (cruzando com o próprio site do Estratégia Concursos como referência) pelo nome
   do concurso/edital pra achar a sigla oficial ou a forma abreviada mais usada.
   Manter a sigla como ela realmente é usada — não forçar juntar palavras num
   bloco só se o uso comum mantém espaço (ex: o concurso "ISS Manaus" usa a sigla
   com espaço mesmo, `ISS Manaus`, não `ISSMANAUS`).

## Passo 2: Definir o nome da pasta do curso

Padrão fixo (sempre seguir esse formato):

```
Matéria (SIGLA_CONCURSO-SIGLA_CARGO)
```

Exemplo: `Direito Constitucional (TCDF-ANACE)`

- Sintetizar o nome da matéria se for muito extenso.
- Sempre entre parênteses: sigla do concurso, traço, sigla do cargo.
- Esse é o padrão definitivo — não trocar sem o usuário pedir explicitamente.
- **Limite de caminho do Windows (260 caracteres):** antes de criar a pasta,
  estimar o tamanho do caminho completo (`pasta raiz + \ + nome da matéria +
  \ + nome de arquivo mais longo esperado`). Está autorizado a sintetizar o
  nome da matéria (e, se precisar, o nome dos arquivos de aula) sempre que
  isso ameaçar estourar o limite — não é preciso perguntar ao usuário toda vez,
  só nos casos ambíguos. Ver orçamento de caracteres sugerido nos "Detalhes
  técnicos e pegadinhas" abaixo.

## Passo 3: Procurar pasta existente antes de criar (detecção automática)

**Escopo da busca: só dentro da pasta informada no Passo 0** (a pasta padrão ou
o outro local que o usuário indicou) — nunca varrer o computador inteiro nem
outras pastas fora dali.

Com o nome definido no Passo 2, procurar dentro dessa pasta por uma subpasta já
existente que corresponda a essa matéria. **Comparação:**
- Ignorar maiúsculas/minúsculas e acentuação (ex: "direito constitucional" bate
  com "Direito Constitucional").
- Ignorar um eventual prefixo `(N-M)` (ex: `(10-20) Direito Constitucional
  (TCDF-ANACE)` bate com `Direito Constitucional (TCDF-ANACE)`).

**Se encontrar exatamente uma pasta correspondente:**

1. Listar o que já tem dentro: quantos `.pdf` já baixados, quantos `.txt`
   placeholder pendentes.
2. Informar o usuário e perguntar como quer proceder, com três opções:
   - **Atualização Parcial** (padrão sugerido) — baixa só as aulas que ainda
     estão faltando (travadas na coleta anterior, agora liberadas). Não mexe
     nos PDFs já baixados. Rápido.
   - **Atualização Completa** — além de baixar o que falta, reconfere **todos**
     os PDFs já baixados contra a versão atual no site e substitui os que
     tiverem sido revisados/atualizados desde a última coleta. Mais lento,
     porque precisa rebaixar cada aula já existente pra comparar.
   - **Criar pasta nova do zero** — mesmo já tendo uma pasta encontrada.
3. **Se optar por Atualização Parcial ou Atualização Completa:** esse vira o
   modo atualização pro resto da skill — usar essa pasta, seguir a lógica de
   "Modo atualização" do Passo 4 em diante, no sub-modo escolhido.
4. **Se optar por criar nova do zero:** perguntar também **se quer que a pasta
   antiga localizada seja apagada** (nunca apagar sem essa confirmação explícita
   — é uma ação destrutiva e irreversível) ou se prefere manter as duas
   coexistindo (nesse caso, a pasta nova precisa de um nome que não conflite,
   ex: sufixo " (nova)" — confirmar com o usuário como diferenciar).

**Se encontrar mais de uma pasta correspondente** (ex: uma pasta solta na raiz
da pasta padrão e outra dentro de algum pacote): **não escolher sozinho** —
listar todas as encontradas (caminho completo de cada uma) e perguntar ao
usuário qual delas é a certa antes de seguir.

**Se não encontrar nenhuma pasta correspondente:** é download novo — criar
`<pasta informada>/<Matéria (SIGLA-SIGLA)>/` com `mkdir -p`. Não tem o que
atualizar, então não precisa perguntar mais nada sobre isso.

## Passo 4: Levantar a lista de aulas

1. Na página `/aulas` do curso, usar `read_page` (filter interactive) pra coletar
   os links de cada aula (padrão `/app/dashboard/cursos/{id}/aulas/{aulaId}`).
   A lista carrega aos poucos — rolar a página (`scroll`) e repetir `read_page`
   até não aparecerem mais aulas novas.
2. Anotar a numeração "Aula 00", "Aula 01"... e o assunto resumido de cada uma
   (aparece embaixo do título, ex: "Direitos sociais.").

### Modo atualização — o que pular

Antes de baixar qualquer coisa, listar o que já existe na pasta. O comportamento
abaixo depende do sub-modo escolhido no Passo 3 (Atualização Parcial ou Completa):

- Arquivos `Aula NN - ... (DD-MM-AAAA).pdf` já baixados (data entre parênteses —
  ver "Nome do arquivo" no Passo 5):
  - **Atualização Parcial:** **pular essa aula**, já está completa. Não reconfere.
  - **Atualização Completa:** **não pular** — rebaixar essa aula (mesmo processo
    do Passo 5) e comparar a data extraída do PDF novo com a data que já está no
    nome do arquivo local (ver "Comparar e substituir PDF já baixado" no Passo 5).
- Arquivos `Aula NN - ... - DD-MM-AAAA.txt` (placeholder, data com traço — ver
  Passo 6) → em **qualquer** sub-modo, **checar de novo** se o livro já ficou
  disponível. Se sim: baixar o PDF normalmente e **apagar o `.txt` antigo** —
  **passo obrigatório, nunca esquecer:** sempre que um PDF real substitui um
  `.txt` placeholder, o `.txt` correspondente tem que ser apagado da pasta antes
  de seguir pra próxima aula. Se ainda não: deixar o `.txt` como está (pode
  atualizar a data prevista se ela mudou).
- Aulas que não aparecem na pasta nem como `.txt` → baixar normalmente.

**Lembrete de formato:** a data entre **parênteses** `(DD-MM-AAAA)` é a data real
de elaboração/atualização do PDF, extraída da própria primeira página do arquivo.
A data depois de um **traço** `- DD-MM-AAAA.txt` é só a previsão de liberação
informada pelo site pra uma aula ainda travada. Os dois formatos nunca se
confundem visualmente por causa disso.

**Atalho pra não precisar abrir aula por aula:** a própria página `/aulas`
(listagem) já mostra, pra cada aula, se ela está travada com "Disponível em
DD/MM/AAAA" ou liberada (sem essa tag, geralmente "Não estudei" / "baixado").
Usar `get_page_text` na listagem pra comparar com os `.txt` pendentes na pasta
antes de navegar pra qualquer aula individual — só vale a pena abrir a página
de uma aula específica (Passo 5) se ela aparecer sem tag de data (ou seja, já
liberada) e ainda não tiver PDF baixado na pasta.

## Passo 5: Baixar o livro de cada aula (o núcleo do processo)

Para cada aula pendente, repetir:

1. Navegar para `https://www.estrategiaconcursos.com.br/app/dashboard/cursos/{id}/aulas/{aulaId}`
   (ou clicar no título da aula na lista) e esperar ~2s carregar.
2. Localizar os cards de download da aula: "Baixar Livro Eletrônico versão
   simplificada", "versão original", "marcação dos aprovados". **Só interessam
   os dois primeiros.**
3. **Se existir "versão simplificada":** clicar nesse card.
4. **Se não existir simplificada mas existir "versão original":** clicar no card
   de versão original (fallback).
5. **Se nenhuma das duas existir** (aula ainda não liberada pelo curso): ver Passo 6.
6. O clique abre uma **nova aba** com uma URL direta e assinada da CDN
   (`cdn.estrategiaconcursos.com.br/storage/temp/aula/.../simplificado.pdf?Expires=...&Signature=...`).
   Pegar essa URL com `tabs_context_mcp` (pode levar 1-2s pra aba carregar o título/URL).
7. Baixar o PDF **direto pra pasta de destino**, com um **nome temporário** (a
   data só entra no nome final depois de extraída — ver abaixo), via `curl`
   (Bash), sem passar pela pasta de Downloads:
   ```bash
   curl -s -o "<pasta>/Aula NN - Assunto Sintetico.pdf.tmp" "<url capturada>" -w "HTTP:%{http_code} SIZE:%{size_download}\n"
   ```
   Conferir que retornou `HTTP:200` e um `SIZE` não-trivial.
8. Extrair a data da primeira página do PDF (ver "Extrair a data do PDF" abaixo)
   e renomear o `.tmp` pro nome final com a data.
9. Fechar a aba do PDF (`tabs_close_mcp`).
10. Voltar pra lista de aulas e seguir pra próxima.

### Nome do arquivo

```
Aula NN - Assunto Sintético (DD-MM-AAAA).pdf
```

- `NN` com dois dígitos, igual aparece no site (Aula 00, Aula 01...).
- Assunto sintetizado a partir do título da aula (não precisa copiar literalmente
  o texto enorme do currículo, resumir pro nome do arquivo ficar legível).
- `(DD-MM-AAAA)` = data de elaboração/atualização do PDF, extraída da primeira
  página do próprio arquivo (ver abaixo) — **entre parênteses**, com traço (nunca
  barra). Se não for possível extrair nenhuma data (ver fallback abaixo), o
  arquivo fica sem esse sufixo mesmo.
- Sem acentos problemáticos ou caracteres especiais que possam dar problema em
  scripts (mas pode manter cedilha/acentuação normal do português nos nomes).

### Extrair a data do PDF

A maioria dos livros eletrônicos do Estratégia traz, na primeira página, a data
de elaboração/atualização daquele material. Depois de baixar o PDF (todo
download, não só em modo atualização), extrair essa data pra usar no nome do
arquivo:

```bash
python -c "
import re, sys
from pypdf import PdfReader
texto = PdfReader(sys.argv[1]).pages[0].extract_text() or ''
m = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)
print(f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else '')
" "<caminho do .tmp>"
```

- Se `pypdf` não estiver instalado no ambiente, instalar com `pip install pypdf`
  antes de seguir.
- Se a página 1 tiver mais de uma data (raro), usar a primeira encontrada.
- **Fallback se não achar nenhuma data** (PDF escaneado sem texto, ou o padrão
  daquele curso for diferente): manter o nome do arquivo sem o sufixo de data
  (`Aula NN - Assunto Sintético.pdf`) e seguir normalmente — não travar o
  download por causa disso. Pode mencionar no resumo final que essa aula não
  teve data identificada.

### Comparar e substituir PDF já baixado (só em Atualização Completa)

Quando o sub-modo escolhido no Passo 3 for **Atualização Completa**, pra cada
aula que já tem PDF local:

1. Rebaixar o PDF normalmente (passos 1-8 acima) pra um arquivo temporário.
2. Extrair a data da primeira página do PDF novo.
3. Comparar com a data que já está no nome do arquivo local (entre parênteses).
4. **Se a data for igual:** apagar o `.tmp` recém-baixado, não mexer no arquivo
   existente.
5. **Se a data for diferente (ou o arquivo local não tiver data no nome, de uma
   coleta anterior à criação desse fluxo):** apagar o PDF antigo, renomear o
   `.tmp` pro nome final com a nova data. Vale registrar essa substituição pra
   mencionar no resumo final (ex: "Direito Constitucional, Aula 05: PDF
   atualizado de 12-03-2025 pra 08-07-2026").

## Passo 6: Aula ainda não disponível → placeholder `.txt`

Quando a aula não tiver nem "versão simplificada" nem "versão original" disponível
(o site costuma mostrar uma previsão de liberação no lugar do vídeo/PDF), **não
baixar nada** — criar um arquivo de texto no lugar, seguindo o mesmo padrão de nome
do PDF, só que terminando em mais um traço + a data prevista, extensão `.txt`:

```
Aula NN - Assunto Sintético - DD-MM-AAAA.txt
```

**Data com traço, nunca com barra** (`DD-MM-AAAA`, não `DD/MM/AAAA`) — barra não
é caractere válido em nome de arquivo no Windows e quebra a criação do arquivo.

Conteúdo do `.txt`: uma linha simples informando que o material ainda não estava
disponível na data da coleta e qual a previsão de liberação informada pelo site.

**Isso é um marcador importante:** sempre que encontrar um arquivo `.txt` nesse
formato dentro de uma pasta de curso, isso indica que aquela aula específica ainda
não tinha o livro liberado no momento em que os dados foram coletados — não é um
erro nem um arquivo esquecido.

## Passo 7: Nomear a pasta com indicador de progresso (N-M)

Depois de processar todas as aulas do curso:

1. Contar **M** = total de aulas do curso e **N** = quantas delas realmente têm
   PDF baixado (arquivos `.pdf` de verdade, não os `.txt` placeholder do Passo 6).
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
5. **Sempre renomear a pasta existente com `Rename-Item` (ou equivalente) —
   nunca apagar a pasta e recriar do zero pra aplicar esse prefixo.** Apagar e
   recriar perde a pasta original (e qualquer PDF real já baixado nela) e conta
   como criar uma pasta nova, não atualizar a existente.

Isso deixa visível, só olhando o nome da pasta no Explorer, se o curso ainda tem
aula pendente de liberação pelo site ou já está 100% baixado.

## Passo 8: Verificação final

Depois de processar todas as aulas:

1. Listar os arquivos da pasta (`ls`), já com o nome renomeado no Passo 7.
2. Conferir que a quantidade de PDFs + TXTs bate com o total de aulas do curso.
3. Validar cada PDF com `file` (deve reportar "PDF document", não algo corrompido
   ou HTML de erro).

O resultado final é a pasta em si, já com os arquivos dentro e o nome renomeado
com o progresso `(N-M)` — não precisa gerar nem apresentar uma tabela resumo
pro usuário no final.

## Detalhes técnicos e pegadinhas (aprendidos na prática)

- **Limite de 260 caracteres de caminho no Windows** — orçamento sugerido pra não
  estourar: pasta raiz (~50 caracteres, ex: a pasta padrão já usa isso) + nome da
  pasta da matéria até ~70 caracteres (`(N-M) Matéria (SIGLA-SIGLA)`) + nome do
  arquivo da aula até ~80 caracteres. Se a soma projetada passar de ~240
  caracteres (deixando margem de segurança), sintetizar o nome da matéria e/ou o
  assunto da aula no nome do arquivo até caber — está autorizado a fazer essa
  redução sozinho, sem perguntar ao usuário, priorizando manter a sigla e o
  número da aula intactos (é o que mais identifica o arquivo) e cortando a parte
  descritiva.
- **Truncar nome de arquivo sem perder o que diferencia dois arquivos:** se dois
  arquivos da mesma matéria têm título quase idêntico e só diferem no final,
  truncar o texto genérico pra um tamanho fixo faz os dois ficarem com o mesmo
  nome e um sobrescreve o outro. Colocar o que diferencia **no início** do nome
  do arquivo, antes do texto que vai ser truncado.
- **Nem todo curso começa em "Aula 00"** — alguns começam direto em "Aula 01".
  Não assumir que "Aula 00" sempre existe; usar a primeira aula que realmente
  aparecer na listagem.
- **A primeira aula pode estar travada** (com "Disponível em DD/MM/AAAA") —
  trata-se normalmente como qualquer aula bloqueada: vira placeholder `.txt`
  (Passo 6), não é motivo pra pular pra segunda aula.
- **Nunca clicar às cegas em coordenadas fixas** achando que o layout é idêntico
  entre aulas — sempre esperar carregar (`wait` ~1.5-2s) e, se possível, confirmar
  com `screenshot` ou `read_page` antes de clicar, porque o scroll/posição dos
  cards muda de aula pra aula.
- **Fechar aba + navegar na mesma aba de controle no mesmo `browser_batch`** costuma
  falhar com erro de "tab not in same group" — fazer isso em duas chamadas
  separadas (fechar a aba do PDF numa chamada, navegar na outra).
- O link da CDN é assinado e temporário (parâmetro `Expires`), mas isso só afeta
  o **link de download** — o arquivo já baixado no disco é permanente como
  qualquer PDF.
- O Chrome do usuário precisa ficar aberto (pode minimizado) durante toda a
  execução — a extensão controla o navegador real dele, não existe navegador
  interno alternativo com a sessão logada.
- Ao repetir a lista de aulas depois de baixar uma, a página volta pro topo —
  rolar de novo até a aula desejada antes de clicar nela.
- **Atualização Completa é mais lenta e consome mais banda** — rebaixa todo PDF
  já existente só pra comparar a data. Não é o padrão sugerido; só usar quando o
  usuário pedir explicitamente ou aceitar a opção quando oferecida no Passo 3.
- Extração de data depende de `pypdf` (Python). Se o pacote não estiver
  instalado, instalar com `pip install pypdf` antes de processar a primeira aula.

## Regras gerais

- Não baixar vídeos, resumos, slides, mapas mentais ou cadernos de questões —
  só o livro eletrônico (PDF), simplificado ou original.
- Não pular a pergunta inicial (link + pasta) nem a confirmação do Passo 3
  (pasta existente encontrada → Atualização Parcial, Atualização Completa ou
  criar nova) mesmo que o usuário pareça claramente já ter dado essas
  informações antes — confirmar a cada execução da skill.
- Se o curso tiver dezenas de aulas, processar tudo sem pausar pra pedir confirmação
  a cada aula — só reportar progresso a cada poucas aulas ou no final.
