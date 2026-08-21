---
name: project-zonas-de-teoria-e-questao-no-pdf
description: "ALERTA: a teoria pode voltar depois de um bloco de questões no mesmo PDF — varrer o arquivo inteiro, nunca parar na primeira faixa de questões nem confiar no índice"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T12:27:59.433Z
---

Levantado pelo Elvis em 2026-08-20. **É um alerta que precisa ser checado sempre.**

## O risco

Um PDF do Estratégia pode ter esta estrutura:

```
p1-10   teoria
p11-20  questões + comentários
p40     TEORIA DE NOVO
p41+    mais questões
```

Se a skill parar na **primeira** faixa `QUESTÕES PARA FIXAÇÃO`, a teoria da p40 **some da base
inteira** e o aluno nunca recebe aquele conteúdo. Erro silencioso: nada quebra, o número só
sai menor.

**Nunca confiar no índice.** O que vale é varrer o arquivo página a página.

## Como fazer

Varrer **todas** as faixas do arquivo, do começo ao fim, e classificar cada uma:

| Classe | Faixas |
|---|---|
| Questões | `QUESTÕES`, `QUESTÕES PARA FIXAÇÃO`, `QUESTÕES COMENTADAS`, `LISTA DE QUESTÕES`, `GABARITO`, `REFERÊNCIAS` |
| Revisão | `RESUMO`, `PARA REVISAR`, `MAPAS MENTAIS`, `MAPAS E ESQUEMAS` |
| Teoria | todo o resto |

As zonas de teoria são **todas** as faixas dessa terceira classe, e todas entram no mapeamento.

Medido: das 18 aulas de Direito Administrativo, só a **Aula 16** tem teoria retomando —
`RESUMO` na p101 e `COMPILADO DE JURISPRUDÊNCIA` de p102 a p111. O código antigo acertava
**por sorte**, porque o bloco de questões daquela aula só começa na p112. A varredura dos
1.096 PDFs achou o padrão em 6,9% dos arquivos, concentrado em Contabilidade e Auditoria.

## Questão do professor no meio da teoria continua sendo teoria

Caixa `ESTA CAI NA PROVA!` (uma questão + comentário) dentro do texto teórico **não quebra o
bloco** e conta como página normal. Ela está na sequência do raciocínio, e logo depois vem
outro tópico de teoria — separar não faz sentido.

Diferente é o **bloco de questões** com faixa própria: esse fecha a zona de teoria.

## Medir densidade por ÁREA, não por página

Contar "páginas que contêm alguma questão" **infla muito**: a caixa costuma ocupar cerca de um
quinto da página, e o resto é teoria. Em Direito Administrativo isso dava **32% por página** e
**13% por área** — mais de duas vezes de diferença, e a leitura errada quase virou decisão de
reformular os blocos.

**Como medir:** a caixa é delimitada por **linhas pontilhadas** (`dashes` não vazio,
largura > 300pt). A altura entre o par de linhas dividida pela área útil da página
(y de 70 a 780) dá a fração real.

Ver [[project_detector_tipografico_titulos_estrategia]] e
[[feedback_qualidade_acima_de_economia_de_tokens]].
