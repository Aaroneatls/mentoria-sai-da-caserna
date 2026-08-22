# Como os agentes trabalham juntos

> Desenhado em 22/08/2026, a partir do que funcionou (e do que falhou) num dia inteiro de duas
> sessões trabalhando no mesmo repositório.

O Elvis tem **um coordenador por área**. Aqui é o **coordenador pedagógico**, que enxerga todas as
tarefas, bases, skills e decisões. Os demais são **agentes especialistas**: cada um domina um grupo
de tarefas e conhece os outros o bastante para saber a quem perguntar.

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

## 7 · Abrir um agente novo

O Elvis pede, ou o coordenador sugere quando um grupo de tarefas cresce a ponto de disputar contexto
com o resto. O coordenador entrega o **prompt de abertura pronto** — modelo em `agentes/_TEMPLATE.md`.
