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

1. **Puxar a arvore por materia**: `GET /api/assuntos?materia={id}` — **SEM** `hierarquico=true`.

   > **Os dois numeros que estavam aqui estavam errados. Medido em 22/08/2026.**
   >
   > | | Dizia | E |
   > |---|---|---|
   > | assuntos de Direito Administrativo | 2.755 | **276** |
   > | chamadas para as nossas materias | ~21 | **30** |
   >
   > E `hierarquico=true` devolve **menos**, nao mais: 121 contra 276 em Direito Administrativo.
   > Ele filtra; o parametro nao serve para levantar a arvore.
   >
   > **A hierarquia nao vem aninhada.** A resposta e uma **lista plana**, e o caminho vem
   > codificado no campo `hierarquia` (`"10.05.02"`). Quem procurar `filhos` ou `children` conta
   > so o nivel 1 e acha que a arvore e rasa — foi o que aconteceu na primeira passada.

2. **Guardar id, nome e hierarquia** (`01.02.03`), preservando a estrutura.

3. **Ligar assunto do Tec -> Cod Mestre**, marcando como **palpite**, a confirmar pela leitura.

4. **Medir a taxa de concordancia** entre o palpite do Tec e o nosso enquadramento. Em 21/08, num
   teste de 199 questoes em 4 assuntos, deu **100%** — mas o teste era facil, porque os quatro
   assuntos casavam 1 para 1 com quatro blocos nossos. O teste de verdade e onde as fronteiras
   nao coincidem.

## Antes de comecar e ao terminar: `../IMPACTOS.md`

**Ao comecar:** ler `../IMPACTOS.md` e verificar se alguma base ja pronta mudou algo que esta
base usa.

**Ao terminar:** escrever la o que foi construido, **o que mudou em relacao ao decidido**, e
**qual base isso afeta**. Se uma base ja pronta precisar de ajuste por causa disto, ajustar
agora, nao depois.

As seis bases se conversam. Sem esse registro, uma muda uma regra, outra fica desatualizada, e
ninguem percebe ate o material chegar torto na mao do aluno.

## O que ja existe e nao deve ser refeito

- O manual completo do Tec esta em `_contexto/tecconcursos.md`, com o contrato da API.
- As regras de acesso estao em `../05-questoes-tec/REGRAS.md` e **valem aqui tambem**.
- Ja se sabe que a busca do catalogo e **fuzzy (OR)**: contagem alta nao significa acerto.

## Perguntas em aberto

1. ~~Puxar as 146 materias ou so as 21 nossas?~~ **Resolvido em 22/08/2026.** A pergunta misturava
   dois niveis. **Materia** e apelido e mora na base 1: as 146 custam **1 chamada** (`/api/materias`),
   nao 146. **Assunto** e taxonomia e mora aqui: custa 1 chamada por materia, e sao **30** materias
   com sigla nossa, nao 21 — `TECINF` sozinha espalha em 10.

2. **A arvore muda com o tempo?** Se mudar, o modo `atualizar` precisa de um diff. Vale medir daqui
   a um mes.

## Sugestao de por onde comecar

Fazer **depois da base 1**, porque o vinculo assunto -> Cod Mestre precisa dos codigos existirem.

**Ja foi puxada em 22/08/2026**: `dados/assuntos.csv`, 4.805 assuntos em 30 materias, profundidade
ate 6 niveis. Custou 62 chamadas (30 com o parametro errado, 30 certas, 2 de diagnostico), sem
nenhum 429. O que falta aqui e o **vinculo assunto -> Cod Mestre**, e ele depende da base 2.
