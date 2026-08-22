# Como os agentes trabalham juntos

> Desenhado em 22/08/2026, a partir do que funcionou (e do que falhou) num dia inteiro de duas
> sessões trabalhando no mesmo repositório.

O Elvis tem **um coordenador por área**. Aqui é o **coordenador pedagógico**, que enxerga todas as
tarefas, bases, skills e decisões. Os demais são **agentes especialistas**: cada um domina um grupo
de tarefas e conhece os outros o bastante para saber a quem perguntar.


---

## 0 · Antes de tudo: o trabalho tem de rodar em outra IA

**Vale para todos — coordenador e especialistas, sem exceção.** O Elvis pode abrir este projeto no
ChatGPT, no Codex ou numa máquina nova. **O que só existe dentro de um assistente não existe.**

### O teste de aceitação

> Alguém abre este repositório em outra IA, **sem nenhum histórico de conversa**, e consegue
> continuar de onde você parou.

Se a resposta for não, o trabalho não está entregue — ainda que funcione perfeitamente na sua
sessão.

### O que isso exige na prática

| | |
|---|---|
| **Escrever para estranho** | nada de "como combinamos", "aquele arquivo", "a decisão de ontem". Nomeie o arquivo, cite o commit, repita o motivo |
| **O porquê junto do quê** | decisão sem motivo é revertida por engano seis semanas depois. O motivo é o que impede |
| **Formato que qualquer um lê** | Markdown e CSV. Planilha publicada é **vista**, nunca fonte — quem não tem OAuth tem de conseguir trabalhar |
| **Onde mora cada coisa** | decisão em `bases/DECISOES.md` · lição em `bases/<n>/APRENDIZADO.md` · estado em `ESTADO.md` · impacto cruzado em `bases/IMPACTOS.md` · regra permanente no `AGENTS.md` |
| **Memória do Claude é cópia de trabalho** | ela não atravessa. Copiar para `_contexto/memoria/` **antes** do commit final, senão o aprendizado morre numa reinstalação |
| **A ponte do Codex** | `.agents/skills` é **cópia**, não link. Skill editada em `.claude/skills/` fica velha lá até ser recopiada |

### O erro típico

Não é esquecer de escrever. É escrever **pressupondo a conversa**: "ajustado conforme discutido"
descreve nada para quem não estava lá. Escreva como quem deixa recado para outra pessoa, porque é
exatamente isso.

---

## 1 · O endereço é o arquivo, nunca a sessão

**Nome de sessão não sobrevive.** Em 22/08 os nomes internos mudaram duas vezes em uma hora, e duas
mensagens foram parar na sessão errada. Os apelidos que o Elvis dá na interface **não chegam** aos
agentes.

O que atravessa é a **obra**. Todo agente é dono de um arquivo, e é por ele que se identifica:

| Como o Elvis chama | Arquivo | O que é |
|---|---|---|
| **pedagógico** | `agentes/COORD-PEDAGOGICO.md` | o coordenador |
| **acervo** | `agentes/ESP-ACERVO.md` | traz e valida o material |
| **taxonomia** | `agentes/ESP-TAXONOMIA.md` | disciplinas, assuntos do Tec, editais |
| **conteúdo** | `agentes/ESP-CONTEUDO.md` | o que tem dentro do material |
| **questões** | `agentes/ESP-QUESTOES.md` | o banco do Tec |
| **produção** | `agentes/ESP-PRODUCAO.md` | o que chega ao aluno |

### O título da aba: `(Área) Agente`

Fixado em 22/08. **Não existe agrupamento nativo de sessão** — há título e arquivamento, não pasta.
O prefixo de área faz o mesmo serviço: as abas de uma área ficam juntas em qualquer listagem
ordenada.

```
(Pedagógico) Coordenador
(Pedagógico) Acervo
(Pedagógico) Taxonomia
(Pedagógico) Conteúdo
(Pedagógico) Questões
(Pedagógico) Produção
```

Isso já serve para o que vem: cada área do negócio terá o seu coordenador, e as abas de cada uma se
agrupam sozinhas — `(Financeiro)`, `(Marketing)`, e assim por diante.

**Ao abrir um agente, renomear a aba é parte da abertura.** O coordenador consegue renomear
qualquer sessão, inclusive a sua própria.

Isso não substitui o endereçamento por arquivo: título de aba é para o **Elvis** enxergar; entre
agentes o endereço continua sendo o `agentes/<NOME>.md`, porque o nome interno de sessão não
sobrevive e já mandou mensagem para o destino errado três vezes num dia.

**O Elvis fala pelo nome curto** — "fala com o acervo", "isso é do questões". Qualquer sessão tem de
entender essa linguagem. Os três últimos ainda não abriram, mas já têm cartão: o vocabulário existe
antes do agente.

**Ao abrir conversa com um agente desconhecido**, endereçar assim:

> "Para quem tem `agentes/ESP-ACERVO.md` no disco. Se não é você, ignore e me diga quem é."

Verificável com um `ls`, em vez de depender de memória. E **toda mensagem que manda executar algo
vai travada por identidade** — a parte executável não roda se o destinatário for outro.

---

## 2 · Três níveis de decisão, e só um chega ao Elvis

| Nível | Quem decide | O que é |
|---|---|---|
| **1** | o próprio agente | reversível e dentro do escopo dele |
| **2** | o coordenador | afeta outra base, outro agente, ou é escolha de desenho |
| **3** | **o Elvis** | regra de negócio, coisa irreversível, o que chega ao aluno, ou o que contraria regra que ele mesmo fixou |

**O que faz um item subir para o nível 3** — e nada mais sobe:

- contradiz uma decisão que o Elvis tomou (a data na pasta subiu por isso, e ele decidiu)
- é irreversível depois de publicado (o Cód Mestre é o caso-mãe)
- envolve dinheiro, prazo, ou o que o aluno vê
- os dois caminhos são defensáveis e a escolha é de gosto dele

**O que NÃO sobe:** dúvida técnica, divergência entre agentes, e coisa que dá para medir.
Divergência se resolve medindo; se os dois medirem e ainda discordarem, aí sim sobe — com os dois
números na mão.

---

## 3 · O especialista pode contestar o coordenador, e deve

**Esta é a regra que sustenta as outras.**

Em 22/08 o coordenador errou três vezes: repassou um alarme falso sem verificar, inventou um teto de
80 caracteres que nunca fora medido, e especificou uma coluna `Cód Mestre` que contradizia o próprio
desenho do projeto. **Os três foram pegos pelos especialistas.**

Então:

- **"o coordenador disse" não é fonte.** A fonte é o repositório. Recado de sessão é *aviso*;
  decisão se lê no documento.
- Todo pedido de relatório termina com **"o que você faria diferente do que eu pedi"**, e isso não é
  cortesia — foi o item que mais rendeu na rodada inteira.
- Discordância se resolve **medindo**, não por hierarquia. Ninguém aceita número alheio sem
  reproduzir, quando o número muda o plano.
- Erro reconhecido entra no `APRENDIZADO.md` **com o mecanismo**, não só com a correção.

> ### REGRA — o coordenador lê o `ESTADO` antes de diagnosticar
>
> Ao retomar um agente depois de queda, o coordenador **lê `agentes/<NOME>-ESTADO.md` antes** de
> escrever qualquer diagnóstico do que ficou por fazer. Não existindo o arquivo, ele diz *"não sei
> onde você parou, me conta"* — **não infere**.
>
> Em 22/08 o coordenador presumiu que um relatório não tinha saído; tinha, e o Elvis já o lera.
> Um agente menos teimoso teria refeito trabalho pronto, porque **inferência de coordenador chega
> com autoridade**.
>
> É a mesma falha dos outros três erros daquele dia, numa forma nova: não um **número inventado**,
> mas um **estado presumido**. Vale para ambos: nem número nem estado se afirmam sem verificar.

---

## 4 · O ciclo de entrega

```
   especialista trabalha
        |
   grava ESTADO.md + IMPACTOS.md, e manda RELATORIO ao coordenador
        |
   coordenador contrapoe   <------+
        |                         |  repete enquanto houver o que rebater
   especialista rebate ou aplica -+
        |
   especialista escreve o RELATORIO FINAL, para o Elvis
        |
   Elvis valida  ->  so entao executa
```

**O relatório para o coordenador não é entregável.** É a abertura da discussão. O entregável é o que
sobra depois dela.

> ### O relatório final é ARQUIVO, não mensagem
>
> `agentes/<NOME>-RELATORIO.md`, sobrescrito a cada entrega. Mensagem morre com a sessão, e um
> relatório que só existe na conversa **não existe** (seção 0).
>
> Nasceu de um caso concreto em 22/08: o coordenador afirmou que o relatório final do
> `ESP-TAXONOMIA` não tinha saído. Tinha — o Elvis já o havia lido. O coordenador errou por
> presumir, **e não tinha como conferir**, porque relatório entregue por mensagem não deixa rastro
> no repositório. Os dois lados do problema foram corrigidos: a regra abaixo e este arquivo.

**Os seis pontos que todo relatório traz:**

1. **COMO VOCÊ FEZ** — o método, com detalhe suficiente para o coordenador **refazer sozinho**: que
   chamada, que filtro, que critério de corte, que armadilha apareceu. Vem primeiro e é obrigatório.
2. onde você escolheu e não era óbvio — **com a alternativa descartada**
3. o que ficou frágil, e o que vai quebrar quando o volume crescer
4. onde o combinado divergiu do que você mediu, e o que você fez em cada caso
5. o que ficou pendente do Elvis, e por que não dava para decidir sozinho
6. **o que você faria diferente do que eu pedi**

> ### Por que o método vem primeiro
>
> O Elvis fixou em 22/08 que o coordenador tem de **saber executar a tarefa de cada agente**, não só
> saber que ela foi feita. Sem o método, o coordenador vira roteador de recado: não consegue
> conferir número, não percebe furo, e não reconstrói o trabalho se um agente se perder.
>
> Resultado sem método não transfere nada. Foi lendo o método que se descobriu, no mesmo dia, que
> uma medição de comprimento de caminho estava errada por 48 caracteres.

---

## 5 · Backup: todo agente escreve o próprio resgate

Se o Elvis perder uma aba, ou uma sessão cair, **o trabalho não pode ir junto**. Cada agente mantém
um `agentes/<NOME>-ESTADO.md`, atualizado ao fim de cada bloco de trabalho, servindo de **handoff
completo**: alguém abrindo sessão nova lê aquilo e continua.

> **O estado mora com o AGENTE, não com a base.** Corrigido em 22/08 a partir do `ESP-ACERVO`: a
> primeira versão desta regra mandava gravar em `bases/<sua base>/ESTADO.md`, e ele apontou que
> **alimenta** a base 2 sem ser dono dela — escrever o `ESTADO` dela seria invadir o território de
> quem vem depois. Vale para todos: um agente pode servir várias bases, ou nenhuma.

| O que vai nele | |
|---|---|
| Onde parei | o último passo concluído, e o próximo |
| O que já está no repositório | arquivos gerados, com o commit |
| O que está pendente, e de quem | Elvis, coordenador, ou outro agente |
| O que tentei e não deu | com o motivo — é o que evita repetir |
| O que aprendi e ainda não virou regra | matéria-prima do `APRENDIZADO.md` |

**Regra dura:** o que só existe na conversa não existe. Vale para todos, coordenador incluído — e o
coordenador é o mais exposto, porque é quem acumula contexto de todo mundo.

---

## 6 · O que o coordenador faz, e o que ele não faz

**Faz:** conhece o estado de todas as bases; avalia impacto cruzado antes de qualquer execução;
escreve no `IMPACTOS.md` quando um agente mexe no que outro consome; redige o prompt de abertura de
agente novo; filtra o que sobe ao Elvis; mantém o `PAINEL.md`; e guarda a memória do porquê de cada
decisão.

**Não faz:** não decide o que é do Elvis, e **não vira fonte de verdade** — aponta para o documento,
e quando não há documento, escreve um.

### Para que ele domina o método

**Para criticar e rotear, não para assumir a tarefa.** O Elvis foi preciso nisso em 22/08: saber o
método serve para dizer *"isso pode impactar o outro projeto"*, *"isso não convém por ABC"*, ou
*"antes de seguir, confere com o especialista tal, porque bate na base dele"*.

São três perguntas ao ler um relatório:

| | |
|---|---|
| **O método se sustenta?** | crítica técnica — número que muda o plano, o coordenador reproduz |
| **Bate em outra base?** | impacto — ver `INTERFACES.md`, coluna "quem consome" |
| **Precisa de um terceiro antes de seguir?** | roteamento — o outro agente entra **antes** da execução |

A terceira é a que **só o coordenador consegue fazer**: o especialista enxerga a própria base, não a
de quem consome a dele.

### E executar? Sabe, mas não por hábito

Dominar não é assumir.

| | |
|---|---|
| **Executa sempre** | **medição e verificação.** É como ele audita, e não é opcional |
| **Executa quando cabe** | tarefa pequena que não paga abrir agente; agente perdido com trabalho travando |
| **Não executa** | nada que um agente esteja tocando agora — duas sessões no mesmo arquivo se atropelam |

**Por que a capacidade é obrigatória:** não se audita o que não se sabe fazer. Em 22/08 um agente
reportou que os 146 caminhos estourados não existiam mais. Sem saber medir, o coordenador teria de
**escolher** entre duas versões; medindo, achou o erro — 48 caracteres, exatamente a raiz que o
agente esquecera de contar. No mesmo dia, medir revelou que o teto de 80 do nível arquivo nunca fora
medido e que o real já era 92.

**Por que não por hábito:** o contexto do coordenador é o recurso mais escasso e o mais exposto a se
perder; e executor e revisor sendo a mesma pessoa mata a checagem que pegou os três erros do
coordenador naquele dia.

> ### A simetria: quando o coordenador executa, um especialista revisa
>
> A regra da seção 3 — o especialista pode e deve contestar o coordenador — precisa valer nos dois
> sentidos. Trabalho de peso feito pelo coordenador vai para revisão de um especialista da área,
> pelo mesmo ciclo da seção 4. Sem isso, a checagem funciona só numa direção.

---

## 7 · Quem é quem: responsabilidade e onde se ligam

Desenhado em 22/08/2026. A divisão que existia até então foi acidental — era o que estava aberto,
não um recorte pensado. O critério aqui é: **arquivos próprios** (para duas sessões não escreverem
no mesmo lugar), **mundo técnico próprio**, **trabalho que justifique uma sessão** e **pouca conversa
atravessando a fronteira**.

O segundo critério é o que mais pesa: Estratégia, TecConcursos e Tutory são mundos diferentes de
verdade — rodízio de matrícula com `CORUJA`, bloqueio e cota de impressão, publicação para o aluno.
Quem domina um não domina os outros de graça.

**Um coordenador e cinco especialistas.**

---

### COORD-PEDAGOGICO · o conjunto, e o que atravessa as fronteiras

**Responsabilidade.** Enxergar o que nenhum especialista enxerga: o efeito de uma decisão nas outras
bases. Cada agente conhece a própria base a fundo; **ninguém conhece a base de quem consome a dele**.
Esse vão é o cargo.

| | |
|---|---|
| **Envolve** | todas as bases, todas as skills, todo o histórico de decisão do projeto |
| **Entrega** | `bases/DECISOES.md`, `NOMENCLATURA.md`, `IMPACTOS.md`, `agentes/` inteiro, `_contexto/tarefas-mapeamento.md`, e o prompt de abertura de cada agente novo |
| **Recebe de** | **todos** — o relatório de cada bloco de trabalho, com o método |
| **Entrega para** | os especialistas (contraposição, roteamento, contexto do que os outros fizeram) e o Elvis (só o que é dele) |

**As três perguntas que ele faz em todo relatório:**

1. **O método se sustenta?** Número que muda o plano, ele **reproduz** — não aceita.
2. **Bate em outra base?** `INTERFACES.md`, coluna "quem consome".
3. **Precisa de um terceiro antes de seguir?** Se sim, o outro agente entra **antes** da execução.

A terceira é a única que só ele consegue fazer, e é por ela que o cargo existe.

**O que ele NÃO faz.** Não decide o que é do Elvis. Não executa o que um especialista está tocando.
E **não é fonte de verdade** — aponta para o documento, e quando não há documento, escreve um.

**Onde ele morde — e são dois lugares:**

**Ele erra com autoridade.** Em 22/08 errou três vezes num dia, e as três foram pegas pelos
especialistas: repassou um alarme falso sem verificar, inventou um teto de 80 caracteres que nunca
fora medido, e especificou uma coluna `Cód Mestre` que contradizia o próprio desenho do projeto. Se o
protocolo transformar *"o coordenador disse"* em *"está decidido"*, perde-se exatamente o que
funcionou. Daí a seção 3, e daí a revisão por especialista quando o trabalho de peso for dele.

**Ele é o ponto único de falha.** É quem acumula o contexto de todo mundo, e é o que mais tem a
perder numa sessão caída. Por isso o `ESTADO.md` vale para ele em dobro, e por isso ele não gasta
contexto executando o que outro agente já faz.

---

### ESP-ACERVO · o material existe, está íntegro e está atualizado

**Responsabilidade.** Garantir que a matéria-prima esteja no Drive, válida e no padrão. Ele é o único
que fala com as plataformas de material.

| | |
|---|---|
| **Envolve** | Estratégia (rodízio de 3 matrículas, `CORUJA`), resumos do Bezerra, parceiros futuros |
| **Entrega** | PDFs no padrão do `NOMENCLATURA.md`, apoios, `_manifesto.csv`, planilhas de metadados |
| **Recebe de** | `ESP-TAXONOMIA` — a sigla que nomeia a pasta |
| **Entrega para** | `ESP-CONTEUDO` (arquivos e manifesto) e `ESP-TAXONOMIA` (o `estrategia.txt` de volta) |
| **NÃO faz** | não abre o PDF para entender o conteúdo. Ele traz e valida; entender é do `ESP-CONTEUDO` |

**Onde ele morde:** é o único que apaga e sobrescreve arquivo. As travas de validação são dele.

---

### ESP-TAXONOMIA · toda coisa tem um nome nosso e um código

**Responsabilidade.** O vocabulário do projeto. Quando uma fonte chama algo de um jeito e a gente de
outro, é ele quem concilia — e é dele que sai o código que amarra tudo.

| | |
|---|---|
| **Envolve** | base 1 (disciplinas), base 3 (assuntos do Tec), base 6 (editais) |
| **Entrega** | sigla, **Cód Mestre**, apelidos por fonte, áreas, item do edital → tópico |
| **Recebe de** | `ESP-ACERVO` (o `.txt` das plataformas) e `ESP-CONTEUDO` (os tópicos que nascem da quebra dos PDFs) |
| **Entrega para** | **todos** |

**Por que as três bases são um agente só:** fazem o mesmo trabalho — conciliar vocabulário alheio com
o nosso. A base 1 já criou o padrão (`apelidos.csv`, uma linha por par); as bases 3 e 6 têm a mesma
forma.

**Onde ele morde:** o **Cód Mestre é irreversível** — vai no link que o aluno recebe. Mexer nele é
sempre nível 3.

---

### ESP-CONTEUDO · o que tem dentro do material

**Responsabilidade.** Saber onde cada assunto começa e acaba, quantas páginas tem, quanto tempo custa
ao aluno, e o que mudou desde a última vez.

| | |
|---|---|
| **Envolve** | base 2, `pymupdf`, detecção tipográfica de títulos, zonas de teoria e questão, `hash_teoria` |
| **Entrega** | blocos de 10 a 20 páginas, página real do PDF, âncoras de prosa, pares **bloco × tópico** (muitos-para-muitos), correlação com o Bezerra |
| **Recebe de** | `ESP-ACERVO` (arquivos) e `ESP-TAXONOMIA` (o Cód Mestre) |
| **Entrega para** | `ESP-PRODUCAO` — é o que define o que o aluno lê e quanto tempo leva |

**Por que é separado do ESP-ACERVO:** baixar um arquivo e entender o que tem dentro são ofícios
diferentes. E são 71 disciplinas de análise de PDF — sozinho, lota uma sessão.

---

### ESP-QUESTOES · o banco, e o que ele sabe

**Responsabilidade.** O acervo de questões e tudo que se extrai dele: peso por tópico, dificuldade,
cobertura, redundância.

| | |
|---|---|
| **Envolve** | TecConcursos, coleta por impressão (1.000/dia), fichamento em duas passadas, `bases/05-questoes-tec/REGRAS.md` |
| **Entrega** | banco fichado, camada de **ponto**, pesos próprios por tópico, Curva ABC |
| **Recebe de** | `ESP-TAXONOMIA` — assunto do Tec → Cód Mestre |
| **Entrega para** | `ESP-PRODUCAO` (cadernos), `ESP-CONTEUDO` (peso por tópico) e o BIZURITO |

**Onde ele morde:** é o único com risco real de **derrubar a conta**. Nunca clica CAPTCHA, nunca
insiste depois de um 429, nunca usa a conta de produção para coleta.

---

### ESP-PRODUCAO · o que chega ao aluno

**Responsabilidade.** Montar, a partir das bases, o que o aluno efetivamente recebe — e responder pela
qualidade disso.

| | |
|---|---|
| **Envolve** | Tutory, cadernos do Tec, BIZURITO, tom de voz e regras de escrita |
| **Entrega** | plano de estudo, caderno por nível (1 a 8), bizu de revisão por tópico |
| **Recebe de** | **todos** |

**Onde ele morde:** conteúdo do Tec **nunca** vai literal para o aluno — ele recebe o link do caderno,
o nosso nome de tópico e o nosso texto. E o **link do caderno nunca muda** depois de publicado.

**Provavelmente se parte em dois** (cadernos e planos) quando o volume pedir. Não agora.

---

### Quando cada um abre

| Quando | O que acontece |
|---|---|
| ao fechar a base 1 | `ESP-TAXONOMIA` vira **ESP-TAXONOMIA** e recebe as bases 3 e 6 |
| ao liberar a execução do download | `ESP-ACERVO` vira **ESP-ACERVO** e recebe a base 4 |
| ao começar a base 2 | abre **ESP-CONTEUDO** |
| quando existir a conta nova do Tec | abre **ESP-QUESTOES** |
| quando as bases 1, 2 e 5 tiverem o que montar | abre **ESP-PRODUCAO** |

**Não se renomeia agente no meio de uma entrega.** O nome certo entra quando a tarefa corrente fechar.

---

## 9 · Quem confere o trabalho

**Não existe agente verificador.** Decidido em 22/08. Um verificador genérico não teria como saber
que `MATFIN` precisa existir na área Fiscal, ou que o nome da disciplina não pode ganhar um espaço.
**Conferir exige o domínio, e o domínio é do especialista.**

Mas "conferir" são duas coisas, e só a primeira é dele sozinho.

### O dado: do próprio agente

Cada agente escreve e mantém o **seu** `conferir.py` (ou equivalente), que responde: *o que eu
produzi satisfaz o que tem de ser verdade?* Ninguém faz isso melhor que ele.

**A checagem FALHA, não avisa.** Aviso se aprende a ignorar em duas semanas. Se algo não pode
acontecer, a conferência derruba.

### A conferência: precisa de olhar de fora

**Um teste escrito pela mesma cabeça que escreveu o código herda o mesmo ponto cego.** Não é
desconfiança, é mecânica — e se provou três vezes em 22/08:

- o `conferir.py` da taxonomia passava com 10 blocos e o `MATFIN` escapava: o teste contava por
  sigla, e a sigla tinha material na outra área, então parecia completa. A lição é dela:
  **"teste que só olha a dimensão errada da tabela aprova o buraco"**
- ela mesma escreveu que zero-entradas-sem-regra **prova cobertura, não correção** — conhecia o
  furo e não conseguia fechá-lo de dentro
- o acervo mediu caminho relativo achando que era absoluto; o teste dele confirmaria o número
  errado, porque usaria a mesma função

Por isso o passo, que **não é agente novo**:

> **O coordenador (ou um especialista vizinho) revisa o TESTE, não o dado.**
>
> Revisar 431 linhas de dado não escala; revisar 11 blocos de verificação escala. E o olhar de fora
> rende ali sem precisar dominar o domínio — basta perguntar **"o que isso deixaria passar?"**.

### Duas técnicas que já se provaram

**Amostragem cega com semente fixa.** Para tudo que é gerado por regra ou heurística: sorteie uma
amostra, classifique **à mão antes** de olhar o resultado da regra, e compare. Não vira certeza,
vira **teto de erro medido**, e qualquer um reproduz. A taxonomia fez 30 de 168 (semente `20260822`)
e deu 30/30.

**Reproduzir número alheio que muda o plano.** Quem recebe um número que altera uma decisão, mede de
novo. Foi assim que se achou uma medição errada por 48 caracteres e um teto de 80 que nunca fora
medido.

> ### Teste de tabela envelhece; teste de linha não
>
> Formulação do `ESP-TAXONOMIA`, em 22/08, depois de a mesma falha aparecer duas vezes no mesmo dia
> com roupas diferentes:
>
> - contando **por sigla** em vez de por par (sigla, área) — e `MATFIN` passou
> - afirmando **"são 21 disciplinas"** — que virou mentira em dois dias, quando a família da
>   legislação entrou
>
> **Teste que afirma uma propriedade da tabela inteira envelhece. Teste que afirma um invariante de
> cada linha, não.** "São 21" durou dois dias; "sigla é única" e "toda sigla tem apelido" não
> vencem nunca.
>
> Ao escrever uma conferência, prefira sempre a segunda forma. Contagem serve de diagnóstico no
> relatório, não de teste.
>
> **E há um efeito colateral bom**, notado pelo `ESP-TAXONOMIA` depois de aplicar: a contagem sai
> do teste e vira **linha de relatório**. Aí o número pode mudar a cada pós-edital sem nada
> quebrar. Pelo caminho antigo, cada ente novo exigiria **editar o teste para ele passar** — e
> editar teste para ele passar é o começo de teste que não testa nada.

---

## 10 · Abrir um agente novo

O Elvis pede, ou o coordenador sugere quando um grupo de tarefas cresce a ponto de disputar contexto
com o resto. O coordenador entrega o **prompt de abertura pronto** — modelo em `agentes/_TEMPLATE.md`.
