# Sistema do Caderno de Erros do Aluno

> Estado: **desenho fechado na sessão de 2026-08-20**, com pendências listadas na seção 9.
> Esta sessão é de desenho. O mapeamento das aulas e a montagem dos cadernos N1 a N7
> continuam na janela de origem. O que exigir mudança lá está na seção 8, como pedido.

---

## 1. O que o sistema faz

O aluno manda o desempenho dele. O sistema devolve:

1. um **caderno de reforço** com outras questões dos pontos que ele errou
2. o **BIZURITO** desses mesmos pontos

Personalização em cima de uma operação de massa. O produto é vendido como **extra da
mentoria**, com janela de pedidos aberta pelo Elvis e prazo de resposta de **48 horas**.

---

## 2. O fluxo fechado

```
Elvis  ->  compartilha o link curto do caderno (/s/XXXXXX)
Aluno  ->  abre, vira CÓPIA na conta dele no Tec, resolve lá
Aluno  ->  Estatísticas > filtra Período e Pasta > ordena por Pontos Fracos
           > EXPORTAR PARA PLANILHA
Aluno  ->  envia o arquivo pelo formulário, identificado pelo E-MAIL
Elvis  ->  na janela de atendimento, loga no Tec e roda o lote
Elvis  ->  devolve a prescrição: por ponto, caderno de reforço + BIZURITO
```

Nenhuma etapa de atendimento consome requisição do Tec, exceto a criação de caderno
de ponto ainda inexistente (ver seção 5).

---

## 3. O que foi verificado ao vivo no Tec (2026-08-20)

Tudo abaixo foi testado na conta `bizu.cadastros@gmail.com`, plano Avançado.

### Caderno de erros nativo
Não é botão, é filtro. Em `Filtrar questões` > aba **Opções** > bloco
`RESOLUÇÕES E ACERTOS`, com quatro chaves: remover as que acertei / errei / resolvi /
não resolvi. O caderno de erros é "remover as que acertei" + "remover as que não resolvi".

**Pegadinha:** a aba Opções fica com classe `bloqueada` (cinza, não clica) enquanto não
houver nenhum filtro ativo. Marque uma matéria primeiro. Não é limitação de plano.

**Limite dele:** devolve só as MESMAS questões que o aluno errou, pra refazer. Não busca
questão nova. É diagnóstico, não reforço. É exatamente aí que entra o nosso produto.

### Compartilhamento de caderno
O caderno tem botão **Compartilhar**, que entrega duas coisas:

```
Link curto:  https://www.tecconcursos.com.br/s/Q6rSYH
Incorporar:  <iframe src="https://www.tecconcursos.com.br/caderno/Q6rSYH">
             + https://cdn.tecconcursos.com.br/conteudo/tec-iframe/Tec-iframeResizer.js
```

O aluno abre o link curto e o caderno vira **cópia na conta dele**. Cada aluno tem conta
própria no Tec (confirmado pelo Elvis), então o desempenho fica na conta dele.

O iframe permite embutir o caderno **dentro da Tutory**. Existe, mas está fora do escopo
por ora (ver seção 7).

### Tela de Estatísticas: é a fonte do diagnóstico
`Estatísticas > Desempenho` traz o painel **Desempenho por Matéria e Assunto**:

- filtros: **Período**, Matéria, Banca, **Pasta**, Dificuldade
- ordem de exibição: Índice, Pontos Fortes, **Pontos Fracos**
- colunas: **Questões Resolvidas · Desempenho · Peso**
- tabela **em árvore**, do matéria até o assunto folha
- botões: `USAR COMO FILTRO` · `CRIAR CADERNO COM TODAS` · `CRIAR CADERNO COM ERRADAS`
  · **`EXPORTAR PARA PLANILHA`**

O filtro por **Período** é o que impede o pedido do mês 2 de repetir o do mês 1.
O filtro por **Pasta** é o que isola o nosso material do que o aluno estuda por fora.

### Desempenho por caderno, em uma requisição
```
GET /api/pastas-cadernos/{pastaId}/progresso
```
Devolve `numeroAcertos`, `numeroErros`, `porcentagemAcertos` de **todos** os cadernos da
pasta. Alternativa mais grossa (por caderno, logo por bloco) ao export por assunto.
Vale como plano B.

### Privacidade e bloqueio
- Sem sessão, a API devolve **HTTP 200 com o HTML da tela de login**. É a armadilha já
  documentada no AGENTS.md. Qualquer parser tem que checar o tipo real da resposta.
- **Desempenho não atravessa contas.** Compartilhar o caderno leva a composição, nunca o
  desempenho. O export é o único jeito de o dado sair da conta do aluno.
- O Tec **bloqueou duas vezes** na sessão, com poucas requisições, exigindo CAPTCHA e
  novo login. Volume de crawl é o risco real, não volume de aluno.

---

## 4. A camada de ponto e os pares de reforço

O fichamento já define `Disciplina > Tópico Mestre > Ponto > Questões`
(ver `project_banco_fichamento_questoes`). O reforço se apoia inteiramente nela.

**Par de reforço é consulta, não coluna.** A lista de irmãs da questão A é "todas as
questões do ponto P, menos a A", que já está na aba **Questão x Ponto**. Guardar a lista
explicitamente obriga a reeditar todas as irmãs a cada questão nova. Manter derivada.

**A irmandade se define pelo Ponto Principal**, não por qualquer ponto tocado, senão volta
o ruído que a camada de ponto existe pra eliminar.

### Alocação: por ponto, nunca por questão errada
Errar quatro questões de prazo é um ponto fraco, não quatro. Então:

```
1. Pega as questões erradas
2. Reduz ao Ponto Principal de cada uma, sem repetição
3. Aloca as vagas POR PONTO
```

| Erros no ponto | Reforço |
|---|---|
| 1 | 2 questões |
| 2 | 3 questões |
| 3 ou mais | 4 questões, e o BIZURITO sobe pro topo da prescrição |

### Cascata de escolha das questões (sem reservar nada)
Decisão do Elvis: **não reter questão boa** pra alimentar reforço. O N1 leva as melhores.

1. questão do mesmo ponto em status `reserva` (sobrou, não foi usada)
2. questão do mesmo ponto que ele não viu
3. questão do mesmo ponto que ele viu e acertou
4. por último, a própria que ele errou

O passo 4 fica em último porque refazer a errada é o que o caderno de erros nativo do Tec
já dá de graça.

**Regra dura:** nunca completar caderno de reforço com questão de outro ponto pra bater
número. Ponto sem questão nova entrega **só BIZURITO**, e está certo. Antes de declarar
escassez, rodar a repescagem por enunciado pelo nome do instituto.

---

## 5. Operação: janela de pedidos e lote

Decisão do Elvis. Substitui tanto o atendimento em tempo real quanto a pré-fabricação
de todos os cadernos possíveis.

- Janela anunciada (ex.: dia 1 a 5 do mês). Fora dela, fechado, com aviso prévio.
- Prazo de resposta: **48 horas**.
- No dia do lote, o Elvis loga no Tec e o processamento roda de uma vez.

**Por que isso ganha das alternativas:**

| | Problema |
|---|---|
| Pré-fabricar tudo | ~400 pontos por disciplina, a maioria nunca pedida, e tudo a manter |
| Tempo real | exige o Elvis logado a qualquer hora, e o Tec bloqueia por volume atípico |
| **Janela + lote** | **agrupa, deduplica e concentra o acesso ao Tec num momento previsível** |

**A deduplicação do lote é o maior ganho.** Se 12 alunos erraram o ponto `DADM-031.P05`,
isso é **um** caderno criado e 12 links enviados. Sem o lote seriam 12 criações.

### A biblioteca se constrói sozinha
Não pré-fabricar. Criar por demanda e **guardar o link**. O primeiro aluno que errar um
ponto paga uma criação; do segundo em diante o ponto já tem link e sai de graça.

Erro se concentra (mesma lógica da Curva ABC), então depois de algumas dezenas de alunos
a biblioteca cobre quase todo pedido e o custo marginal tende a zero. O trabalho manual
**encolhe** com o tempo, em vez de crescer com o número de alunos.

---

## 6. Registro por aluno

**Chave: o e-mail** informado no formulário. Normalizar (minúsculas, sem espaço) e manter
uma coluna de apelidos pra quando o aluno digitar diferente do cadastro.

Uma aba, uma linha por prescrição:

```
Aluno(e-mail) · Data · Ponto · Caderno enviado · BIZURITO enviado · Antes · Depois
```

Serve pra duas coisas: não reenviar o mesmo caderno, e fechar o ciclo antes/depois.

---

## 7. Entrega

Fora da Tutory, por decisão do Elvis: colocar tarefa por aluno na Tutory é trabalho
manual que não compensa agora. Entrega por link, no canal de contato.

Evolução prevista: **página fixa por aluno** (HTML publicado no Cloudflare Pages, já no
catálogo de ferramentas), com URL imutável e imprevisível, mostrando histórico, pontos
atacados e evolução antes/depois. Sem nome de aluno na URL.

---

## 8. Pedidos para a outra janela

1. **Coluna Principal/Secundário na aba Questão x Ponto.** Uma questão de múltipla escolha
   cobra vários pontos, um por alternativa. O reforço precisa saber em qual deles o
   gabarito se decide, senão dispara reforço de assunto que o aluno domina. Em Certo/Errado
   do Cebraspe o problema quase não existe; concentra-se em FGV e FCC.
   **Tem que ser decidido na mesma passada do fichamento.** Depois exige reler questão a
   questão.

3. **Gravar o índice de acerto da comunidade** no fichamento de cada questão. Ele vem em
   `/api/questoes/{id}/desempenho`, que o fichamento **já chama**, então é uma coluna a mais,
   custo zero agora. É o que sustenta a Camada 6 da seção 12: sem ele, comparar nossos alunos
   com a comunidade exigiria varrer o Tec de novo depois, e o Tec bloqueia por volume.

2. **Nada a reservar.** O pedido anterior de reter cota de questões fora dos N1 a N7 foi
   **retirado**. Vale a cascata da seção 4.

---

## 9. Pendências

- **Colunas exatas do arquivo exportado.** A tela foi vista populada (1 resolvida), mas o
  arquivo em si não foi aberto. Confirmar antes de escrever o parser.
- **Onde a cópia do caderno cai na conta do aluno.** Se cair em "Sem classificação", o
  filtro por Pasta não isola nada e o export vem contaminado. Vira instrução de
  onboarding: criar pasta `Mentoria` e jogar os cadernos lá.
- **Cópia é retrato, não espelho.** Corrigir um caderno depois de distribuído não atualiza
  a cópia do aluno, e exige reenviar o link. Acertar antes de mandar.
- Perguntas 3 a 7 do briefing original: respondidas em sua maior parte pelas seções 5 a 7,
  menos o gatilho de periodicidade, que ficou como janela mensal anunciada.

---

## 10. Faseamento sugerido

| Fase | O quê | Custo |
|---|---|---|
| 0 | Google Form com upload de arquivo, e-mail como chave. Processamento junto com o Claude | zero código |
| 1 | Script lê a planilha, converte em pontos, monta a prescrição pronta | onde está 80% do ganho |
| 2 | Página fixa por aluno (Cloudflare Pages) | baixo, depois da aba existir |
| 3 | WhatsApp de verdade, se o volume doer | Z-API arrisca banir o número; Cloud API exige verificação de negócio e template pra iniciar conversa |

Automatizar o **processamento** antes do **transporte**. O transporte é o que parece
automação; o processamento é o que é.

---

## 11. Memórias relacionadas

`project_caderno_de_erros_do_aluno` · `project_banco_fichamento_questoes` ·
`project_cadernos_cobertura_e_composicao_propria` · `reference_tec_api_desempenho_e_filtros` ·
`project_bizu_revisao_por_topico` · `project_niveis_caderno_tec_e_pesos` ·
`project_recencia_na_selecao_de_questoes` · `feedback_bloqueio_plataforma_como_agir`

---

## 12. Retroalimentação: o agregado é pra dentro, não pro aluno

Decisão do Elvis em 2026-08-20. Gravado como **Camada 6** em
[[project_bizurito_validacao_conteudo]].

**Pra dentro (aprovado):** se muitos alunos erram o mesmo ponto, a suspeita recai sobre o
**nosso material**, não sobre eles. Vira fila de prioridade de qual BIZURITO reescrever.

**Não usar percentual cru.** São 100 alunos e a minoria manda o export. Percentual baixo pode
ser só questão difícil. O sinal é o **delta contra o índice de acerto da comunidade**, que a
API do Tec já dá em `/api/questoes/{id}/desempenho`:

- comunidade 70%, nossos alunos 30% -> o material falhou
- comunidade 30%, nossos alunos 30% -> questão difícil, material ok

Isso tira a dificuldade da conta e por isso funciona com amostra pequena. Ainda assim, exigir
um mínimo de alunos no mesmo ponto antes de reescrever.

**Pro aluno (descartado).** Devolver ao aluno o percentual dele comparado à turma sai. A
amostra é pequena e o Tec já tem o botão **COMPARE-SE COM A COMUNIDADE**, com base muito
maior. Seria uma versão pior do que ele já tem de graça.

---

## 13. As perguntas 3 a 7 do briefing original, respondidas

**3. Onde roda?** **Google Forms**, confirmado por Elvis. O formulário **não será criado agora**:
ele é a parte fácil e só faz sentido depois que existir base pra responder. **A prioridade é a base
de dados, ou seja, o fichamento do Tec.** Sem ele o formulário recebe pedido e não tem o que devolver.

**4. Quantos alunos por vez?** 100 alunos na base, e a **minoria manda**. Volume baixo por
janela, o que confirma o lote manual como escolha certa por ora.

**5. O caderno fica na conta de quem?** Nasce na conta do Elvis, e vira **cópia na conta do
aluno** quando ele abre o link curto. O desempenho fica com o aluno. Escala, porque o mesmo
link serve N alunos.

**6. BIZURITO tem link fixo por aluno?** Não, e não deve ter. É **biblioteca por ponto**: o
aluno recebe os links dos pontos dele, dentre os que já existem. Um Doc por aluno multiplicaria
a manutenção por aluno e quebraria a correção centralizada.

**7. Qual o gatilho?** **Janela mensal anunciada** pelo Elvis, **no início de cada mês**, aberta
por alguns dias, com resposta em 48h. Vendida como extra da mentoria. Não é sob demanda contínua
nem automático por calendário.

---

## 14. Caminho crítico

O gargalo **não é o formulário, nem o WhatsApp, nem a página do aluno**. É a base.

```
fichamento (Questao x Ponto + Ponto Principal + indice da comunidade)
     -> sem isso, nada abaixo funciona
formulario -> lookup -> prescricao -> entrega
```

Enquanto a base não existir, o sistema recebe pedido e não tem o que devolver. Por isso os
três pedidos da seção 8 estão no caminho crítico, e os três são baratos **agora** e caros depois.

---

## 15. Estrutura real do diagnóstico (capturada em 2026-08-20)

Endpoint que alimenta a tela de Estatísticas:

```
GET /api/resolucoes/estatisticas?filtro.dataInicio=14%2F08%2F2026&filtro.dataFim=20%2F08%2F2026
```

```json
"dadosMateria": [{ "id":1, "nome":"Direito Administrativo...", "nomeAbreviado":"DAD",
  "acertos":0, "erros":1, "resolucoes":1, "peso":1.0,
  "assuntos":[{ "id":9619, "hierarquia":"14", "subTree":[{ "id":9622, "hierarquia":"14.02",
    "subTree":[{ "id":9626, "nome":"Objetivos, Fases e Formalidades (arts. 11 a 17)",
      "hierarquia":"14.02.01", "descendentes":"9626;",
      "acertos":0, "erros":1, "total":1, "peso":1.0 }]}]}]}],
"dadosEvolucao": [{ "inicio":"20/08/2026", "acertos":0, "erros":1, "resolucoes":1 }]
```

Cada assunto traz **id do Tec**, **hierarquia** (`14.02.01`) e acertos/erros na folha. O `id` é
a chave de junção com a nossa taxonomia. `dadosEvolucao` é série diária, serve pro antes/depois.

### LIMITE: o export não traz número de questão

Ele conta acertos e erros **por assunto**, e só. Assunto é a granularidade grossa que a camada
de ponto existe pra corrigir. Logo, **o export sozinho não chega no ponto**.

### Entrada corrigida: link do caderno de erradas

Na mesma tela existe o botão **CRIAR CADERNO COM ERRADAS**. Então:

```
Aluno: CRIAR CADERNO COM ERRADAS -> Compartilhar -> manda UM link
Elvis: abre o link (vira copia na conta dele) -> le a lista de questoes
       -> fichamento -> PONTO
```

Compartilhar caderno leva a **composição** (o que não atravessa contas é o desempenho). E é
menos atrito pro aluno: dois cliques e um link, sem anexar arquivo.

**Decisão:** link do caderno de erradas como entrada **principal** (chega no ponto); export da
planilha como **complemento opcional** (panorama por assunto e série de evolução).

**NÃO TESTADO:** ler a composição de um caderno compartilhado por **outra** conta. O Tec
bloqueou três vezes na sessão. É o primeiro teste da próxima janela, e o desenho da entrada
depende dele.
