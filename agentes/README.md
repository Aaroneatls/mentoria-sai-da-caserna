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

```
agentes/COORD-PEDAGOGICO.md      o coordenador
agentes/ESP-DISCIPLINAS.md       base 1
agentes/ESP-DOWNLOAD.md          material do Estratégia e dos parceiros
```

**Ao abrir conversa com um agente desconhecido**, endereçar assim:

> "Para quem tem `agentes/ESP-DOWNLOAD.md` no disco. Se não é você, ignore e me diga quem é."

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
um `ESTADO.md` na pasta da sua base, atualizado ao fim de cada bloco de trabalho, servindo de
**handoff completo**: alguém abrindo sessão nova lê aquilo e continua.

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

## 7 · Os cinco especialistas: responsabilidade e onde se ligam

Desenhado em 22/08/2026. A divisão que existia até então foi acidental — era o que estava aberto,
não um recorte pensado. O critério aqui é: **arquivos próprios** (para duas sessões não escreverem
no mesmo lugar), **mundo técnico próprio**, **trabalho que justifique uma sessão** e **pouca conversa
atravessando a fronteira**.

O segundo critério é o que mais pesa: Estratégia, TecConcursos e Tutory são mundos diferentes de
verdade — rodízio de matrícula com `CORUJA`, bloqueio e cota de impressão, publicação para o aluno.
Quem domina um não domina os outros de graça.

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
| ao fechar a base 1 | `ESP-DISCIPLINAS` vira **ESP-TAXONOMIA** e recebe as bases 3 e 6 |
| ao liberar a execução do download | `ESP-DOWNLOAD` vira **ESP-ACERVO** e recebe a base 4 |
| ao começar a base 2 | abre **ESP-CONTEUDO** |
| quando existir a conta nova do Tec | abre **ESP-QUESTOES** |
| quando as bases 1, 2 e 5 tiverem o que montar | abre **ESP-PRODUCAO** |

**Não se renomeia agente no meio de uma entrega.** O nome certo entra quando a tarefa corrente fechar.

---

## 8 · Abrir um agente novo

O Elvis pede, ou o coordenador sugere quando um grupo de tarefas cresce a ponto de disputar contexto
com o resto. O coordenador entrega o **prompt de abertura pronto** — modelo em `agentes/_TEMPLATE.md`.
