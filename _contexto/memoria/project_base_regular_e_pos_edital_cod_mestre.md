---
name: project-base-regular-e-pos-edital-cod-mestre
description: "Arquitetura: base por área no Curso Regular; pós-edital reaproveita o Cód Mestre do que é idêntico e só acrescenta o que falta — o Cód Mestre e o nome da disciplina são chave no Tutory"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1ec1cd8-e665-4dfb-a047-a7395dc82975
  modified: 2026-08-20T13:24:09.568Z
---

Definido pelo Elvis em 2026-08-20.

## Por que o Cód Mestre não pode mudar

Cada Cód Mestre vira um **link de estudo do aluno na plataforma Tutory**, e a plataforma guarda
esse código. Ela indexa por **dois parâmetros**:

1. **Cód Mestre** — lá se chama "assunto"
2. **Nome da disciplina**

Trocar qualquer um dos dois quebra o histórico do aluno. Por isso os dois são **chave**, não
rótulo.

## O fluxo

**A base do Curso Regular é a espinha permanente** — uma por área (Controle, Fiscal…).

Quando sai um **pós-edital**:

1. Comparar o conteúdo do pacote do concurso com o da base do regular.
2. **Conteúdo idêntico → mantém o mesmo Cód Mestre.** É a mesma teoria; toda a correlação com
   questões já fichadas continua valendo.
3. **Conteúdo que só existe no pós-edital → linha nova**, com Cód Mestre próprio, **marcado na
   numeração** para dar para identificar que é específico daquele edital.
4. Conteúdo que está no regular e o edital não cobre **não entra** naquela base específica, mas
   continua no regular.

## Nome da disciplina é canônico

Se o pós-edital chama a disciplina de um jeito e o regular de outro, **vale o nome do regular**,
desde que a aula seja a mesma. Exemplo que o Elvis deu: o regular traz
`Administração Financeira e Orçamentária` e o pós-edital pode trazer `Direito Financeiro`.

Isso precisa de uma **tabela de nomes canônicos com aliases**, que se soma à tabela de siglas já
prevista em [[project_taxonomia_codigo_mestre_e_atualizacao]].

## ⚠️ Comparar BLOCO a bloco, nunca aula a aula

Erro cometido e corrigido em 2026-08-20. Os dois cursos **fatiam o conteúdo de forma diferente**:
o TCDF quebra Agentes Públicos em 4 aulas (13 a 16); o Regular Controle junta tudo numa aula de
172 páginas de teoria.

Comparando aula com aula, a `Aula 14 do TCDF` (Provimento, vacância, estabilidade, remuneração)
pontuou **0,08** e seria classificada como **nova** — quando na verdade o Regular Controle já
cobre provimento (título na p45), estabilidade/efetividade/vitaliciedade (p153-161), remuneração
(p111-130) e aposentadoria (p148-172). Criar Cód Mestre novo ali quebraria o link do Tutory.

**A unidade de comparação é o bloco**, que é o que carrega o Cód Mestre.

Também não comparar por **número de aula**: a numeração dos dois cursos não coincide (Controle
da Administração é a Aula 13 no regular e a Aula 11 no TCDF).

## Como comparar, na prática

- **Contenção**, não Jaccard: `|A∩B| / |A|`. Jaccard pune diferença de tamanho e dá "novo" para
  conteúdo que já existe dentro de uma aula maior.
- **Fallback de prosa** para aula cujos títulos são imagem: n-gramas do texto corrido da teoria.
  Sem isso, `Responsabilidade Civil do Estado` do Regular Controle (títulos todos rasterizados)
  compara contra conjunto vazio e dá 0,00.
- `LS` e `LC` no nome do arquivo são **versão simplificada e completa do livro**, não professor.
  Nos dois cursos o autor é o mesmo (Herbert Almeida).

## Medido no caso TCDF x Regular Controle (Direito Administrativo)

15 das 21 aulas do TCDF batem com o Regular Controle (contenção 0,99-1,00). Sem correspondência
no regular: `Lei 9.784/1999`, `LGPD`, `Direitos e deveres`, `Responsabilidades — sindicância e
PAD`. E o edital do TCDF não tem item para `PPPs e Consórcios` nem `Convênios`, que existem no
regular.

Ver [[project_curso_referencia_e_aulas_faltantes]],
[[feedback_codigo_identifica_conteudo_nao_posicao]] e
[[project_arquitetura_bases_e_link_imutavel]].
