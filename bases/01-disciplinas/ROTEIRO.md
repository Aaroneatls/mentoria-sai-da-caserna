# Roteiro — Base 1 - Disciplinas

> **Abra este arquivo primeiro.** Ele existe para que uma sessao nova comece sabendo o que ja foi
> decidido, o que ja existe e por onde pegar. Leia junto com **`DECISOES.md` desta pasta**
> (so o que afeta esta base) e `APRENDIZADO.md` (licoes, que crescem). O `../DECISOES.md`
> central fica como referencia completa, para consultar quando faltar algo.

Criado em 21/08/2026, na sessao que fechou o Bloco 1 de decisoes.

## O que esta base entrega

A tabela mestra das **21 disciplinas**, com a sigla que abre todo Cod Mestre, os apelidos que
cada fonte usa para a mesma disciplina, e o contador do proximo numero livre.

E a base mais simples e a **mais critica**: sem ela nao da para numerar topico sem risco de
repetir, e o numero, uma vez publicado na Tutory, nao pode mudar nunca.

## Os tres modos da skill

| Modo | O que faz | Cuidado |
|---|---|---|
| `criar` | monta do zero | escreve; conferir antes com `conferir` |
| `atualizar` | roda o diff e aplica so o que mudou | nunca sobrescrever o que nao mudou |
| `conferir` | roda as verificacoes **sem escrever nada** | e o modo padrao quando houver duvida |

O modo `conferir` nasceu de um caso real: em 21/08 foi conferindo antes de executar que se
descobriu um filtro faltando, o que teria gasto ~600 chamadas produzindo dado errado.

## Passo a passo

1. **Criar a tabela de disciplinas** com as 21 ja decididas em `../DECISOES.md`, secao A8.
   Colunas: `sigla`, `nome_canonico`, `proximo_numero`.

2. **Criar a tabela de apelidos.** Cada fonte chama a mesma disciplina de um jeito, e e por esse
   nome que se encontra o material la dentro. Uma linha por par (disciplina, fonte, nome na fonte):

   ```
   TECINF | Estrategia Regular Controle | "Analise de Informacoes"
   TECINF | Estrategia Regular Fiscal   | "Informatica"
   TECINF | Bezerra                     | "Tecnologia"
   TECINF | Tutory (legado)             | "TECNOLOGIA DA INFORMACAO"
   ```

   **As tres fontes ja estao levantadas**, na pasta `fontes/`:

   | Arquivo | O que tem |
   |---|---|
   | `estrategia.txt` | 34 entradas dos dois Cursos Regulares |
   | `bezerra.txt` | 29 materias dos Resumos Esquematizados |
   | `tutory.txt` | as 170+ disciplinas cadastradas hoje na plataforma |

   O `tutory.txt` e o **problema, nao a solucao**: serve para levantar apelidos e para montar o
   plano de migracao (item A28).

3. **Criar a tabela de areas como LISTA**, nunca como colunas `Fiscal`/`Controle`. Uma linha por
   par (disciplina, area). E o que permite a area Legislativa entrar depois sem mexer em nada.

4. **Nao criar contador gravado.** O proximo numero de cada sigla se **deriva** do registro de
   topicos (maior usado + 1). A faixa continua sendo `0001` a `4999` para o Curso Regular e
   `5001` em diante para pos-edital, com o `5000` inexistente.

5. **Guardar em CSV**, em `dados/`, tres arquivos: `disciplinas.csv`, `apelidos.csv` e
   `areas.csv`. CSV porque qualquer IA le, o git mostra o que mudou linha a linha, e nao depende
   de ferramenta nenhuma.

6. **Publicar como planilha** para o Elvis conferir, no padrao do projeto: cabecalho na linha 10,
   dados a partir da 11, alinhamento centralizado e quebra de texto. A planilha e **vista**, o CSV
   e a fonte.

## O que ja existe e nao deve ser refeito

- A **lista das 21 disciplinas com siglas** esta fechada em `../DECISOES.md`, secao A8.
- A proposta original com o levantamento dos dois cursos esta em `proposta.md`, nesta pasta.
  **Ela esta desatualizada** (tinha 25 disciplinas); vale como registro de como se chegou la.
- O levantamento das **170 disciplinas da Tutory** foi feito em 21/08 e mostra o estado atual da
  plataforma: seis entradas para Direito Administrativo, duas diferindo por um espaco.

## Perguntas em aberto

1. **A coluna de area ficou em aberto de proposito.** As pastas dos cursos e os ciclos de estudo
   divergem: Matematica Financeira aparece junto do Raciocinio Logico na pasta do Fiscal e
   separada no ciclo. Preencher agora seria chutar. **Resolver ao abrir os PDFs na base 2.**

2. ~~Falta levantar os apelidos do Bezerra~~ **feito**: esta em `fontes/bezerra.txt`.

3. **O contador NAO se guarda, se DERIVA.** Contador gravado desincroniza: se um mapeamento
   falhar no meio, ele avanca sem os topicos existirem e some um numero. O proximo `DADM` e o
   maior numero usado mais um, lido do registro de topicos. Ate a base 2 comecar a produzir,
   todas as siglas estao em `0001`.

## Sugestao de por onde comecar

Comecar pelos passos 1 e 2 juntos, porque a tabela de apelidos e o que da utilidade imediata: e
ela que permite dizer "o que o Estrategia chama de Analise de Informacoes e o que a gente chama
de Tecnologia da Informacao".

**Nao toca no Tec.** Pode ser feita a qualquer hora, sem depender de conta nem de cota.

Tempo estimado: uma sessao curta.
