# Roteiro — Base 5 - Questoes do Tec

> **Abra este arquivo primeiro.** Ele existe para que uma sessao nova comece sabendo o que ja foi
> decidido, o que ja existe e por onde pegar. Leia junto com **`DECISOES.md` desta pasta**
> (so o que afeta esta base) e `APRENDIZADO.md` (licoes, que crescem). O `../DECISOES.md`
> central fica como referencia completa, para consultar quando faltar algo.

Criado em 21/08/2026, na sessao que fechou o Bloco 1 de decisoes.

## O que esta base entrega

O acervo de questoes com enunciado, alternativas e gabarito, mais a camada de **ponto** que so
existe porque alguem leu. E a base que alimenta os cadernos.

## Os tres modos da skill

| Modo | O que faz | Cuidado |
|---|---|---|
| `criar` | monta do zero | escreve; conferir antes com `conferir` |
| `atualizar` | roda o diff e aplica so o que mudou | nunca sobrescrever o que nao mudou |
| `conferir` | roda as verificacoes **sem escrever nada** | e o modo padrao quando houver duvida |

O modo `conferir` nasceu de um caso real: em 21/08 foi conferindo antes de executar que se
descobriu um filtro faltando, o que teria gasto ~600 chamadas produzindo dado errado.

## Passo a passo

1. **Ler `REGRAS.md` nesta pasta antes de tocar no Tec.** Elas valem acima de qualquer
   conveniencia de execucao.

2. **Definir a janela de anos da materia**, mirando ~2.500 questoes, teto de 10 anos, medindo pela
   **contagem** (`/api/questoes/contagem/filtros`), que custa 1 chamada e devolve so o numero.
   Claude propoe, o Elvis confirma.

3. **Criar o caderno-base** com os filtros de limpeza ligados (`REMOVER_ANULADAS`,
   `REMOVER_DESATUALIZADAS`, `REMOVER_ADAPTADAS_INEDITAS`), banca e janela de anos.

4. **Imprimir em blocos**, respeitando **1.000 questoes por dia**, com cabecalho completo, texto
   associado e **gabarito junto de cada questao**.

5. **Extrair e gravar** no banco: id, banca, ano, orgao, cargo, assunto, enunciado, alternativas,
   gabarito.

6. **Fichar**: ler o enunciado e ligar cada questao ao topico mestre e aos pontos que ela cobra.
   O assunto do Tec entra como pista, **nunca como veredito**.

7. **Compor os cadernos** por nivel, e criar no Tec **na conta de producao**.

## O que ja existe e nao deve ser refeito

| Arquivo | O que e |
|---|---|
| `REGRAS.md` | as regras de acesso, nascidas de um dia inteiro de erro |
| `historico_tec.json` | o historico medido dos bloqueios |
| `banco.py` | esquema SQLite do banco de questoes |
| `importar.py` | traz para o banco o que o coletor exportou |
| `compor.py` | compoe os cadernos por nivel, com rodizio entre eles |

E em `_arquivo/2026-08-21-aprendizado/`, de conferencia: 1.224 questoes colhidas, 5.423
classificadas por dificuldade e banca, 199 fichadas em 38 pontos.

## Perguntas em aberto

1. **O gabarito ainda nao sai junto de cada questao.** A opcao existe (`JUNTO_QUESTAO`), mas a
   extracao ainda nao pegou. **E o primeiro item a resolver**, porque sem gabarito as alternativas
   perdem metade do valor.

2. **Limpar a conta antiga:** os 5 cadernos `ZZ-COLETA`, o caderno `101395596` (banca ESAF) e a
   chave `coletor_src` do navegador.

3. **Testar criar caderno vazio.** Cairia de 5 para 3 requisicoes por caderno.

4. **As 3 melhorias de composicao** (A27) ficaram para quando o primeiro caderno real for montado:
   tamanho proporcional ao numero de pontos, ordem didatica dentro do caderno, e peso real
   mandando nos niveis 3 a 5.

## Sugestao de por onde comecar

**Nao comecar por aqui.** Depende da conta nova, que o Elvis vai criar, e o fichamento depende dos
Cod Mestre, que nascem na base 2.

Quando comecar: **Direito Administrativo**, seguindo a ordem de coleta decidida, que comeca pelas
disciplinas comuns as duas areas.

Primeiro item da sessao, antes de qualquer impressao: **resolver o gabarito**.
