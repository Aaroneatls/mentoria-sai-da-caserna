# Briefing — Sessão "Quais materiais do Estratégia entram no mapeamento"

> Como usar: abra uma sessão nova do Claude Code neste workspace e cole a seção
> **"Prompt para colar"** abaixo. Esta sessão precisa de você por perto: exige login no
> Estratégia e o rodízio de matrícula. Não deve rodar sozinha em segundo plano.

---

## Contexto de onde isso nasceu (2026-08-20)

Estamos construindo a skill que mapeia as aulas do Estratégia em blocos de estudo, indicando ao
aluno "estude da página X, tópico A, até a página Y, tópico B". O método já funciona nos PDFs de
**aula em PDF** do Curso Regular: os títulos são achados pela tipografia (corpo de fonte maior
que o texto) e pela faixa roxa do template.

O que ainda não sabemos: **esse método vale para os outros tipos de material do Estratégia?**
O pacote traz muito mais coisa além da aula em PDF, e cada tipo tem diagramação própria.

## O que a sessão precisa responder

Para **cada tipo de material**, dizer: entra no mapeamento por página, entra de outra forma, ou
não entra.

Tipos a examinar (os que o Elvis listou, mais o que aparecer no pacote):

- Passo Estratégico
- Monitorias
- Cursivas
- Curso Estratégico
- Bizu Estratégico
- Resumos e mapas mentais (já é pendência conhecida do projeto)
- Caderno de questões / listas
- Legislação comentada, súmulas, jurisprudência
- Slides e material de videoaula

## Onde olhar

Pacote: **TCDF — Analista, Pós-Edital** (pacote completo).

⚠️ O Estratégia tem **limite de 3 produtos matriculados**. Para entrar nesse pacote é preciso
desmatricular outro. O procedimento está no `AGENTS.md`: em `/app/dashboard/assinaturas`,
`DESMATRICULAR` no que vai sair digitando `CORUJA`, depois achar o pacote desejado na aba
**PACOTES** (buscar sempre por pacote, nunca por curso), `MATRICULAR` e digitar `CORUJA` de
novo, e recarregar. É reversível.

**Antes de desmatricular qualquer coisa, checar os placeholders `.txt` daquele pacote na pasta
do Drive (aulas ainda não publicadas) e avisar o Elvis.**

Navegador: usar o **Claude Browser (embutido)**, reaproveitando a janela já aberta. Chrome real
só com autorização dele na conversa, pedida na hora.

## Regras de trabalho

- **Não precisa baixar tudo.** Dá para inspecionar na plataforma. Se precisar baixar para ver a
  diagramação, baixar para pasta temporária e apagar depois.
- **Amostra mínima: 40 itens**, espalhados entre os tipos de material — amplitude importa mais
  que profundidade.
- Se baixar, valem as travas de download do `AGENTS.md`: arquivo temporário primeiro, validar
  que o PDF começa com `%PDF-` e abre no `pypdf`, e **nunca sobrescrever arquivo bom**.
- Se levar HTTP 429, **parar e avisar o Elvis** — ver a regra de bloqueio de plataforma.
- Trabalho é de leitura e análise. Não commitar nada.

## Método sugerido para cada material examinado

1. Que tipo é (PDF de teoria, PDF de questões, vídeo, planilha, HTML na plataforma).
2. Tem faixa roxa de seção? Tem hierarquia de títulos por corpo de fonte?
3. Tem numeração de página estável, ou é material curto/fluido?
4. O aluno consegue "abrir na página X e achar o tópico"? Se não, qual seria a âncora certa
   (número da questão, nome do tópico, minutagem do vídeo)?
5. Vale a pena mapear? O material acrescenta teoria nova, ou é revisão/exercício do que já
   está na aula?

Ferramenta: `pymupdf` (já instalado). Para os PDFs, o detector tipográfico que já funciona está
descrito na memória em `project_detector_tipografico_titulos_estrategia`.

## Entrega

Gravar em `_contexto/estrategia-tipos-de-material.md`, com:

- **Uma tabela** por tipo de material: o que é, quantos itens examinados, tem estrutura de
  título?, entra no mapeamento? (sim / de outra forma / não), e por quê.
- **Seção "Como ancorar cada tipo"** — para os que entram, qual é a referência que vamos dar ao
  aluno.
- **Seção "Decisões para o Elvis"** — o que não deu para resolver sozinho.

---

## Prompt para colar na sessão nova

```
Leia o arquivo _contexto/briefing-sessao-tipos-de-material.md deste workspace e execute a
investigação descrita nele. Comece me perguntando qual pacote você deve desmatricular para
abrir vaga para o TCDF Analista Pós-Edital, e confira os placeholders .txt desse pacote na
pasta do Drive antes de mexer em qualquer matrícula. Use o navegador embutido.
```
