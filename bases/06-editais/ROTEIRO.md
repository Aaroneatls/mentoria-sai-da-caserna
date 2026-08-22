# Roteiro — Base 6 - Editais

> **Abra este arquivo primeiro.** Ele existe para que uma sessao nova comece sabendo o que ja foi
> decidido, o que ja existe e por onde pegar. Leia junto com **`DECISOES.md` desta pasta**
> (so o que afeta esta base) e `APRENDIZADO.md` (licoes, que crescem). O `../DECISOES.md`
> central fica como referencia completa, para consultar quando faltar algo.

Criado em 21/08/2026, na sessao que fechou o Bloco 1 de decisoes.

## O que esta base entrega

O programa de cada concurso, item a item, ligado ao Cod Mestre. E a fonte que manda no
pos-edital: define o que entra e o que fica de fora.

## Os tres modos da skill

| Modo | O que faz | Cuidado |
|---|---|---|
| `criar` | monta do zero | escreve; conferir antes com `conferir` |
| `atualizar` | roda o diff e aplica so o que mudou | nunca sobrescrever o que nao mudou |
| `conferir` | roda as verificacoes **sem escrever nada** | e o modo padrao quando houver duvida |

O modo `conferir` nasceu de um caso real: em 21/08 foi conferindo antes de executar que se
descobriu um filtro faltando, o que teria gasto ~600 chamadas produzindo dado errado.

## Passo a passo

1. **Levantar os editais** que entram no escopo.

2. **Extrair item a item**, guardando o **texto literal** do edital.

3. **Ligar item -> Cod Mestre**, aceitando que um item pode cobrir varios topicos e vice-versa.

4. **Marcar os itens SEM correspondencia.** Esse e o alerta: ou falta material, ou o mapeamento
   errou.

5. **Alimentar o alerta de nomenclatura**: quando o edital chamar diferente da gente, o plano
   avisa o aluno.

## Antes de comecar e ao terminar: `../IMPACTOS.md`

**Ao comecar:** ler `../IMPACTOS.md` e verificar se alguma base ja pronta mudou algo que esta
base usa.

**Ao terminar:** escrever la o que foi construido, **o que mudou em relacao ao decidido**, e
**qual base isso afeta**. Se uma base ja pronta precisar de ajuste por causa disto, ajustar
agora, nao depois.

As seis bases se conversam. Sem esse registro, uma muda uma regra, outra fica desatualizada, e
ninguem percebe ate o material chegar torto na mao do aluno.

## O que ja existe e nao deve ser refeito

- O programa de Direito Administrativo do TCDF/ANACE 2026 e o mapa aula -> item estao em
  `../02-estrategia-concursos/edital.py`.
- Alguns PDFs de edital estao no arquivo da sessao antiga.

## Perguntas em aberto

1. **Quais editais entram?** E o item A26, ainda em aberto.

2. **Edital antigo serve para que?** Para medir peso historico e ver o que se repete, mas isso
   compete com a base de pesos que sai do fichamento. Vale decidir se compensa.

## Sugestao de por onde comecar

Fazer **por ultimo**, porque depende de decisao do Elvis sobre quais editais entram, e porque o
valor dela aparece no pos-edital.

**Nao toca no Tec.**
