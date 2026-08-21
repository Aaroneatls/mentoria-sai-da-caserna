---
name: feedback-nome-mestre-sintetiza-referencia-e-literal
description: "Nome Mestre é nossa taxonomia e pode sintetizar; a referência de onde estudar é literal do PDF, porque o aluno abre e tem que bater com o olho"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T10:57:46.865Z
---

Definido pelo Elvis em 2026-08-20, pensando na experiência de leitura do aluno.

## São duas informações com papéis diferentes

O aluno recebe as duas coisas, e elas **não** servem pro mesmo:

**Nome Mestre do Tópico — IDENTIFICA.** É a nossa taxonomia. Serve pra amarrar Estratégia +
Bezerra + TecConcursos + edital no mesmo assunto. É nosso, então **pode sintetizar**: encurtar
título longo demais, padronizar, normalizar a caixa.

**"Começa em" / "Vai até" — LOCALIZA.** É **literal**: exatamente como está impresso na
página, **inclusive em CAIXA ALTA**. O aluno abre o PDF na página indicada e tem que bater com
o olho. Se a gente normaliza a caixa aqui, deixa de bater com o que está lá.

Antes as duas colunas faziam a mesma coisa, e a normalização de caixa (que está certa pro Nome
Mestre) estava desalinhando 9 títulos da referência.

## Síntese é permitida na taxonomia — regra geral

Vale pra **todas** as nossas bases: Nome Mestre, aula do Estratégia, resumos do Bezerra e
assuntos do Tec. Quando o rótulo da fonte for longo ou confuso, sintetizar. Ex.:

```
impresso no PDF: "Pessoa física ou jurídica que tenha firmado parceria com o Poder Público"
Nome Mestre:     "Improbidade Administrativa: sujeito ativo — terceiros e entidades parceiras"
```

O título impresso continua registrado na coluna própria, então nada se perde.

## Caixa: uma regra só na base inteira (Elvis, 2026-08-20)

A alternância entre CAIXA ALTA e caixa baixa foi **abandonada**. Ela era um sinal meu para
distinguir faixa roxa de subtítulo, e o Elvis dispensou pelo mesmo motivo do Ctrl+F: o aluno
abre a página e vê. Duas convenções concorrendo confundem mais do que ajudam.

**A regra:** palavra-chave com inicial maiúscula, palavra de ligação em minúscula, sigla em
caixa alta. Vale para tudo — Nome Mestre, subtópicos e referência.

```
no PDF:   RESPONSABILIDADES PELA EXECUÇÃO E PELOS ENCARGOS DO CONTRATO
na base:  Responsabilidades pela Execução e pelos Encargos do Contrato
```

Isso **flexibiliza** a regra de literalidade acima: as *palavras* continuam literais, só a caixa
é normalizada. O aluno acha do mesmo jeito — caixa não atrapalha busca visual nem Ctrl+F.

**Cuidado com sigla que colide com palavra comum.** `OS`, `SEM`, `EP`, `ME`, `DL` e algarismos
romanos **não** entram na lista de siglas: "Disposições sobre os Contratos" virava
"Disposições sobre OS Contratos". Quando o título não é todo em caixa alta, um token que já
vem em maiúscula na fonte é preservado como sigla.

## Formato da referência: nomear o tópico a CONCLUIR

Escolhido pelo Elvis entre três variantes. Duas colunas, voz imperativa:

```
INICIE EM    Página 42, em “Responsabilidades pela Execução e pelos Encargos do Contrato”
TERMINE EM   Página 49, ao concluir “Direito Subjetivo do Contratado à Extinção”
```

O `TERMINE EM` nomeia o tópico que o aluno **termina**, não o que ele deve evitar. Quando o
bloco fecha a aula, acrescenta `— é o fim da teoria desta aula`.

**Sem coluna de comentário.** Avisos do tipo "título é imagem, não sai no Ctrl+F" ou "título
impresso usado sem alteração" foram removidos: é conversa minha, não indexação. **Subtópicos
tratados lista TODOS os títulos do bloco**, sem corte e sem descrição — é índice, não resumo.

## Três armadilhas na referência (medidas, não supostas)

**Título repetido na mesma aula.** Na Aula 03, `Conceito` aparece na p3 e na p17; também
`Criação e extinção`, `Regime jurídico` e `Regime de pessoal`. Se a referência diz só
`"Conceito" (p17)`, o aluno dá Ctrl+F e cai na p3. **Qualificar pela seção:**
`"Conceito" — o da seção FUNDAÇÕES PÚBLICAS`.

**Título que é imagem.** A faixa da Aula 02 p3 é rasterizada e **não sai no Ctrl+F**. A
referência avisa pra procurar com o olho.

**Dizer o tipo de marco visual.** No Estratégia a faixa roxa e o subtítulo são inconfundíveis,
então a referência diz qual procurar: `começar na faixa roxa "..."` ou
`começar no subtítulo "..."`. Isso encurta muito a busca visual do aluno.

## Resumo x Compilado de jurisprudência

**Resumo NÃO é teoria** — fica fora dos blocos de estudo.
**Compilado de jurisprudência É teoria** — entra normalmente.

Ver [[project_detector_tipografico_titulos_estrategia]] e [[feedback_nomenclatura_nome_mestre]].
