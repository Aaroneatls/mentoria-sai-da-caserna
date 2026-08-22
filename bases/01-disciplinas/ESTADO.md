# Estado — Base 1 · Disciplinas

> **Handoff completo.** Quem abrir uma sessão nova (Claude, ChatGPT, Codex, máquina nova) lê este
> arquivo e continua daqui, **sem nenhum histórico de conversa**. Agente dono:
> `agentes/ESP-DISCIPLINAS.md`.

Atualizado em 22/08/2026. Último commit desta base: **`2c46928`**.

---

## Onde parei

**A base está construída e conferida. Falta só o Elvis validar para declará-la fechada.**

O ciclo da seção 4 do `agentes/README.md` foi cumprido inteiro: construí, mandei o relatório ao
coordenador, ele contrapôs em três rodadas, apliquei o que procedia, rebati o que não procedia, e
**entreguei o relatório final ao Elvis**. Ele ainda não respondeu.

**Próximo passo:** aguardar a validação do Elvis nos três itens da seção "Pendente" abaixo. Nada
mais depende de mim. **Não refazer nada** e **não executar renomeação nenhuma**: quem renomeia pasta
é o `ESP-DOWNLOAD`, e só depois do ok do Elvis.

---

## O que já está no repositório

Tudo commitado e íntegro. `python bases/01-disciplinas/conferir.py` passa nos 10 blocos.

| Arquivo | Linhas | O que é |
|---|---|---|
| `dados/disciplinas.csv` | 21 | as siglas; transcrição literal da seção A8 de `bases/DECISOES.md` |
| `dados/apelidos.csv` | 431 | uma linha por par (sigla, fonte, nome literal), sobre 5 camadas |
| `dados/areas.csv` | 31 | uma linha por par (sigla, área), com a evidência em cada linha |
| `dados/renomear-pastas.csv` | 34 | contrato com o `ESP-DOWNLOAD`: 31 prontas, 3 pendentes |
| `fontes/tec.txt` | 146 | matérias do Tec, levantadas em 1 chamada |
| `SEM-DONA.md` | — | as órfãs em 4 baldes; **gerado**, não editar à mão |
| `conferir.py` | — | 10 blocos de validação; **não escreve nada** |
| `APRENDIZADO.md` | — | 8 lições, com o mecanismo de cada uma |
| `.claude/skills/montar-base-disciplinas/SKILL.md` | — | os 3 modos e as 7 regras que não se quebram |

**Vista** (descartável, regenerável do CSV):
`https://docs.google.com/spreadsheets/d/1a_F3RLdtj5lsLeNaOiD4YyasxfDRD9xnFN2NsUbH3pU`

### Commits desta base

```
2c46928  conferir os dois tetos do nivel disciplina, 58 e 64
d3b4781  a data desce pro nivel da disciplina (regra 9); pasta_nova -> pasta_nova_sem_data
2aa689e  a pasta da Reforma nao se resolve sozinha; a contradicao da A8 caiu
2552a28  fechar os dois furos da revisao (amostragem 30/30, MATFIN, blocos 9 e 10)
a68f08b  as cinco camadas de apelido, as areas e o relatorio de orfas
24d79e1  as 21 siglas e o mapa de renomeacao das pastas
```

---

## Como refazer, se precisar

Tudo é reproduzível. A única etapa que toca a rede é a 2.

1. `disciplinas.csv` sai da **seção A8** de `bases/DECISOES.md`. Transcrição, zero interpretação.
2. `fontes/tec.txt`: `GET /api/materias?universo=&formato=OBJETIVA`, autenticado, **1 chamada**.
   A resposta é um objeto, **não** uma lista: o array vem dentro (`Array.isArray(j) ? j : ...`).
   Vale `bases/05-questoes-tec/REGRAS.md`: 429 encerra o dia, sem retentativa, e CAPTCHA é do Elvis.
3. Conciliar as 5 camadas contra as 21. O casamento é **muitos-para-muitos nos dois sentidos**.
4. `areas.csv`: a área sai de qual Regular **de fato** tem o curso, com o `curso_id` como evidência.
5. `conferir.py` **antes** de publicar qualquer coisa.

**Validação da classificação da Tutory:** 168 entradas classificadas por regex ordenada (a 1ª regra
que casa vence, então **a ordem importa**: as regras de `local` e `lixo` vêm antes das de
disciplina, senão "Economia Regional do Pará" viraria `ECOFIN`). Conferida por **amostragem cega**:
30 sorteadas com `random.seed(20260822)`, classificadas à mão antes de olhar o resultado da regex.
**30/30.** Mesma semente reproduz a mesma amostra.

---

## Pendente, e de quem

### Do Elvis (nível 3 — nada disso é decidível por agente)

| # | O quê | Por que não dava para decidir sozinho |
|---|---|---|
| **B69** | separar a pasta `Reforma Tributaria`, que guarda `LTRIB` (curso 336350) e `REFTRI` (371461, 389109) | mexe na pasta dele, e **não se resolve sozinha**: no modo `atualizar` a pasta existente fica como está |
| **B70** | os cursos 220891 e 220896 são `LTRIB` também? | regra de negócio. Metade já caiu: os dois são **genéricos** (o 220891 diz "(Todos Estados)"), então **não** são o `LTRIB-<ente>` da A8, e a contradição que eu havia levantado não existe |
| — | as **8 entradas do balde 1** do `SEM-DONA.md` | "esquecer uma disciplina" é irreversível depois de o Cód Mestre ser publicado |

Enquanto não decididas, as 3 pastas ficam **sem prefixo** no `renomear-pastas.csv`. **Sigla errada
gravada é pior que pasta sem sigla:** a sem sigla qualquer um vê que falta; a errada ninguém percebe
e ela contamina o Cód Mestre, que não pode mudar depois de publicado.

### Do ESP-DOWNLOAD (não bloqueia esta base)

1. Depois de renomear, **atualizar a coluna `pasta_atual_no_disco`** com o nome novo. Ela é
   **estado**, não histórico; sem isso o `conferir` desta base casa zero linha.
2. **Reescrever `fontes/estrategia.txt` como subproduto** de cada rodada, com os nomes **da
   plataforma**. É o que fecha o furo do `atualizar` offline (ver "o que tentei e não deu").
3. **B70:** puxar a lista de aulas dos cursos 220891 e 220896 quando estiver na plataforma.

---

## O que tentei e não deu

**1. Conferir a ementa dos cursos 220891 e 220896 pela API do Estratégia.**
`TypeError: Failed to fetch` no origin `estrategiaconcursos.com.br`, nos três ids testados. Não
insisti, por dois motivos: o cartão deste agente diz que ele **não entra no Estratégia**, e o
`ESP-DOWNLOAD` já está logado lá. Repassado como B70.
**Resolvi metade sem a API**, pelo nome do curso: "(Todos Estados)" mata a hipótese de ser local.

**2. Regenerar `fontes/estrategia.txt` lendo as pastas do Drive.** Proposta minha, **vetada com
razão** pelo coordenador. Era **circular**: as pastas vão ganhar o **nosso** prefixo de sigla, então
a base passaria a "descobrir na fonte" um nome que nós mesmos inventamos.
**Regra que ficou:** o `.txt` guarda o nome **como a plataforma mostra**, e só muda quando o
Estratégia mudar. A pasta é derivada dele, nunca fonte dele.

**3. Fechar o furo do `atualizar` offline com aviso por prazo.** Proposta minha, **retirada**: se
ninguém atualiza o `.txt`, o `atualizar` responde "nada mudou" com toda a confiança. Eu quis gravar
a data e avisar quando envelhecesse. Contraposição aceita: **aviso por prazo é alerta que se aprende
a ignorar em duas semanas**, e o furo volta com falsa segurança por cima. Ficou a solução
estrutural: quem já está logado reescreve o `.txt` como subproduto.

**4. `python3` não existe neste ambiente.** É `python` (3.12.10). E o `/tmp` do Git Bash **não** é
visível para o Python nativo do Windows: usar o scratchpad da sessão para arquivo temporário.

---

## O que aprendi e ainda não virou regra do projeto

As lições com mecanismo estão em `APRENDIZADO.md`. Aqui, só o que ainda não tem casa:

**1. Coluna cujo nome envelheceu é pior que coluna mal nomeada desde o começo**, porque ninguém
desconfia. Aconteceu com `pasta_nova`: ele dizia a verdade até a regra 9 entrar, e depois passou a
prometer o nome final quando entregava o nome final **menos a data**. Quem lesse ao pé da letra
criaria 31 pastas sem data. Candidato a regra geral de nomenclatura de coluna.

**2. Orçamento de caracteres que fecha exato fecha por coincidência.** `AFO` batia 58 de 58. Só
apareceu porque alguém somou; nenhum teste pegava. Hoje o `conferir.py` checa os dois tetos (58 e
64), mas a lição é anterior ao caso: **limite sem folga declarada é limite que vai estourar em
execução**, não em revisão.

**3. Quando um problema for resolvido, procurar onde mais ele aparece.** O caso `MATFIN` era
idêntico ao das matérias 69 e 37 do Tec, já resolvido quatro parágrafos antes no mesmo relatório, e
eu não liguei os pontos. Isso está no `APRENDIZADO.md` desta base, mas vale para o projeto inteiro.

---

## Se a base 1 for declarada fechada

Este agente vira **ESP-TAXONOMIA** e recebe também a base 3 (assuntos do Tec) e a base 6 (editais).
Ver `agentes/README.md`, seção 7. **Não se renomeia agente no meio de uma entrega.**

Parecer sobre a sequência, já alinhado com o coordenador: **puxar a árvore do Tec agora, sim**
(leitura pura, ~21 chamadas, e serve para medir se o problema de dimensionamento das matérias 69 e
37 tem mais casos). **Amarrar assunto ao Cód Mestre, só depois da base 2**, porque o tópico nasce da
teoria que o aluno lê, e o assunto do Tec é apelido que se pendura nele. Amarrar antes inverteria o
desenho.
