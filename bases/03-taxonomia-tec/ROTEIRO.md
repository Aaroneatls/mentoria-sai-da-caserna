# Roteiro — Base 3 - Taxonomia do Tec

> **Abra este arquivo primeiro.** Ele existe para que uma sessao nova comece sabendo o que ja foi
> decidido, o que ja existe e por onde pegar. Leia junto com **`DECISOES.md` desta pasta**
> (so o que afeta esta base) e `APRENDIZADO.md` (licoes, que crescem). O `../DECISOES.md`
> central fica como referencia completa, para consultar quando faltar algo.

Criado em 21/08/2026, na sessao que fechou o Bloco 1 de decisoes.

## O que esta base entrega

A arvore de assuntos do TecConcursos, por materia, com id, nome e hierarquia. Serve de **palpite
inicial** para o topico mestre e de vocabulario comum com a plataforma.

Nao e veredito: a classificacao final vem de ler o enunciado.

## Os tres modos da skill

| Modo | O que faz | Cuidado |
|---|---|---|
| `criar` | monta do zero | escreve; conferir antes com `conferir` |
| `atualizar` | roda o diff e aplica so o que mudou | nunca sobrescrever o que nao mudou |
| `conferir` | roda as verificacoes **sem escrever nada** | e o modo padrao quando houver duvida |

O modo `conferir` nasceu de um caso real: em 21/08 foi conferindo antes de executar que se
descobriu um filtro faltando, o que teria gasto ~600 chamadas produzindo dado errado.

## Passo a passo

1. **Puxar a arvore por materia**: `GET /api/assuntos?materia={id}&hierarquico=true`. Uma chamada
   por materia; a de Direito Administrativo voltou com **2.755 assuntos**.

2. **Guardar id, nome e hierarquia** (`01.02.03`), preservando a estrutura.

3. **Ligar assunto do Tec -> Cod Mestre**, marcando como **palpite**, a confirmar pela leitura.

4. **Medir a taxa de concordancia** entre o palpite do Tec e o nosso enquadramento. Em 21/08, num
   teste de 199 questoes em 4 assuntos, deu **100%** — mas o teste era facil, porque os quatro
   assuntos casavam 1 para 1 com quatro blocos nossos. O teste de verdade e onde as fronteiras
   nao coincidem.

## O que ja existe e nao deve ser refeito

- O manual completo do Tec esta em `_contexto/tecconcursos.md`, com o contrato da API.
- As regras de acesso estao em `../05-questoes-tec/REGRAS.md` e **valem aqui tambem**.
- Ja se sabe que a busca do catalogo e **fuzzy (OR)**: contagem alta nao significa acerto.

## Perguntas em aberto

1. **Puxar as 146 materias da plataforma ou so as 21 nossas?** As 21 bastam, e custam 21 chamadas
   em vez de 146.

2. **A arvore muda com o tempo?** Se mudar, o modo `atualizar` precisa de um diff. Vale medir daqui
   a um mes.

## Sugestao de por onde comecar

Fazer **depois da base 1**, porque o vinculo assunto -> Cod Mestre precisa dos codigos existirem.

E barata: ~21 chamadas, uma vez so. Cabe em qualquer janela de cota.
