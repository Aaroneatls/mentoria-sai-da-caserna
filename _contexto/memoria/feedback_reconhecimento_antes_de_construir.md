---
name: feedback-reconhecimento-antes-de-construir
description: "Antes de construir sobre material novo, rodar uma passada barata que só caracteriza o material — evita o retrabalho de construir sobre suposição errada"
metadata:
  type: feedback
---

Definido pelo Elvis em 2026-08-21, como **forma padrão de trabalho**.

## A regra

**Sempre que entrar material novo** — disciplina, pacote, plataforma — rodar primeiro uma
passada que só **caracteriza**, sem construir nada em cima:

- tamanhos de fonte do corpo e dos títulos, e **se eles se distinguem**
- vocabulário das faixas de seção, **inclusive se vêm numeradas**
- taxa de rasterização (título que é imagem e não tem camada de texto)
- densidade e **distribuição** dos títulos (média engana; o que importa é o maior vão)
- onde a teoria começa e onde acaba

Só depois construir.

## Por que virou regra

O maior custo da sessão de 2026-08-20 **não foi decisão errada, foi retrabalho**: construir,
rodar, descobrir que o material não batia com a suposição, refazer. Três casos, todos
pegáveis por reconhecimento:

| O que quebrou | Teria sido visto por |
|---|---|
| Faixa numerada (`6. LISTA DE QUESTÕES`) inflava a teoria até o fim do arquivo | listar o vocabulário das faixas |
| Corpo e título com o mesmo tamanho em Administração Pública | histograma de fonte |
| 23% dos títulos rasterizados em Direito Administrativo | contar faixa sem texto |

## Complemento: aproveitar o aprendizado, não recomeçar do zero

Decidido junto. "Refazer pra valer" **não** é reconstruir. Mantêm-se:

- o código validado em `mapeamento/` do workspace
- as **177 transcrições** de títulos-imagem, lidas uma a uma
- as regras já registradas na memória
- as bases já publicadas

O que se refaz é o **dado**, não o método.

## Escopo de teste

Teste de aprendizado usa **uma matéria inteira**, nunca amostra parcial. Em Direito
Administrativo, porque é onde o Elvis tem expertise para validar com calma. Amostra parcial
não serve: ele precisa ver a disciplina fechada para julgar.

Ver [[project_mapeamento_8_disciplinas_resultado]] e
[[project_detector_tipografico_titulos_estrategia]].
