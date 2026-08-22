# Quem alimenta quem

> O mapa que o coordenador usa para **rotear**: ao ler um relatório, saber se aquilo bate em outra
> base e se precisa de um terceiro antes de seguir. Mantido pelo coordenador. 22/08/2026.

Sem isto, o roteamento vive na cabeça de quem está na conversa — e cabeça se perde.

---

## O mapa

| Produz | Quem consome | O que quebra se mudar sem avisar |
|---|---|---|
| **Base 1** · sigla, apelidos, áreas | bases 2, 3, 4, 6 e a Tutory | a sigla abre o Cód Mestre. Mudar sigla depois de publicado **quebra o link do aluno** |
| **Base 2** · blocos, páginas, `hash_teoria` | planos, base 4, cadernos | o plano manda o aluno para a página errada |
| **Base 3** · assunto do Tec → Cód Mestre | base 5, cadernos | a coleta traz questão de outra disciplina |
| **Base 4** · resumo do parceiro → Cód Mestre | planos, BIZURITO | o aluno recebe resumo que não é do tópico |
| **Base 5** · banco fichado, pesos | cadernos, BIZURITO, base 2 | o caderno sai desbalanceado, sem ninguém perceber |
| **Base 6** · item do edital → Cód Mestre | planos pós-edital, base 5 | o plano cobre o que não cai e omite o que cai |
| **Download** · arquivos, manifesto, `estrategia.txt` | bases 1 e 2 | a base 2 mapeia arquivo que não existe mais |

---

## Os quatro pontos sensíveis de verdade

Estes já morderam ou quase morderam. Ao ver um relatório encostar num deles, **rotear antes de
deixar seguir**.

### 1 · O Cód Mestre E O NOME DA DISCIPLINA são irreversíveis

`SIGLA-NNNN` vai no link que o aluno recebe. Renomear o tópico pode; **trocar o conteúdo dele exige
código novo**, senão as questões já publicadas perdem a correlação em silêncio.

**E desde 22/08 o `nome_canonico` da disciplina tem o mesmo estatuto**, por motivo de plataforma: a
Tutory reconhece que o aluno já estudou um assunto comparando **nome do assunto + nome da
disciplina**. Um espaço a mais e ela trata como disciplina nova — **o histórico do aluno se perde**.

Qualquer mexida em sigla, numeração ou nome canônico é nível 3. O `conferir.py` da base 1 tem um
bloco que falha se o nome divergir.

### 2 · O download e a base 1 se alimentam nos dois sentidos

A base 1 dá a **sigla** que nomeia a pasta; o download devolve o **`estrategia-plataforma.txt`** e o
`pasta_atual_no_disco` atualizado, que é o que a base 1 diffa.

> **SÃO DOIS ARQUIVOS, e confundi-los apaga uma camada inteira.** Corrigido em 22/08, depois de o
> coordenador quase mandar sobrescrever o errado:
>
> | Arquivo | Camada | Exemplo |
> |---|---|---|
> | `fontes/estrategia.txt` | **drive** — nomes de pasta | `Regular Controle \| AFO, Orçamento Público e LRF` |
> | `fontes/estrategia-plataforma.txt` | **plataforma** — nomes de curso, com id | `220866 \| 1 \| Concursos da Área Fiscal - Curso Básico de Direito Empresarial` |
>
> Existem separados porque **22 pastas correspondem a 25 cursos**: a camada de pasta perde
> informação. Escrever nomes de plataforma no primeiro deixaria **duas cópias de uma camada e zero
> da outra** — e o estrago só apareceria quando alguém precisasse da que sumiu.
>
> **Quem escreve o quê:** o download escreve **só** o `estrategia-plataforma.txt`. O que acontece
> com a camada `drive` depois de uma renomeação é do `ESP-TAXONOMIA`, que marca as linhas antigas
> como **histórico** em vez de apagar — mesma lógica da sigla aposentada.

É o único ciclo fechado do projeto, e por isso o mais fácil de quebrar: se um lado deixa de escrever,
o outro responde *"nada mudou"* com toda a confiança do mundo. **Erro silencioso, não erro ruidoso.**

### 3 · Uma entrada da fonte pode valer por duas disciplinas nossas

Já apareceu quatro vezes — e a quarta é a mais fina, porque acontece **dentro de um curso só**: o
curso **336350** tem Lei Kandir (`LTRIB`) e a Reforma (`REFTRI`) no mesmo material. Ali a separação
não é de pasta nem de curso, é **de bloco**, e sai na base 2 lendo os PDFs.

As outras três: a matéria 69 do Tec (AFO + Contabilidade Pública), a matéria 37 (Auditoria +
Controle Externo), e a pasta "Raciocinio Logico e Matematica" do Regular Fiscal (RACLOG + MATFIN).

Sempre que uma fonte junta o que a gente separa, **duas linhas, nunca uma escolhida como principal**
— senão a segunda disciplina fica órfã e ninguém sente falta, porque ela tem material na outra área
e a tabela parece completa.

### 4 · Filtrar por matéria do Tec não isola disciplina nossa

Decorre do item 3. O corte de coleta é por **assunto**, e o **dimensionamento** também: medir
"2.500 questões de AFO" pela matéria 69 conta questão de Contabilidade Pública como se fosse AFO, e
a janela de anos sai curta demais.

---

## Como usar ao ler um relatório

1. **O método se sustenta?** — crítica técnica. Número que muda o plano, o coordenador reproduz.
2. **Bate em outra base?** — olhar a coluna "quem consome" da linha correspondente.
3. **Precisa de um terceiro antes de seguir?** — se bate num dos quatro pontos acima, o outro agente
   entra na conversa **antes** da execução, não depois.

O terceiro é o que só o coordenador consegue fazer: o especialista enxerga a própria base, não a de
quem consome a dele.
