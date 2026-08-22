# Aprendizado — Base 2 — Estrategia Concursos

> Este arquivo **cresce**. Toda licao aprendida trabalhando nesta base entra aqui, com a data e
> com o custo que ela teve. Aprendizado nao se arquiva junto com o dado.

## 21/08/2026 — do teste de aprendizado

- **Titulo e o que tem fonte maior que o corpo.** Nunca testar negrito: o flag e invertido entre
  safras e ha titulos em `Montserrat Medium`, que nao tem "Bold" no nome.
- **A faixa de secao pode vir numerada** (`6. LISTA DE QUESTOES`). Sem remover o prefixo antes de
  casar, a teoria vai ate a ultima pagina do arquivo. Custou uma auditoria inteira errada: 1.224
  paginas de teoria contadas onde havia 552.
- **Titulo numerado e legitimo** (`1 - Conceitos Introdutorios`). Testar `isupper()` no primeiro
  caractere descarta todos: Administracao Publica foi de 65 para 199 titulos depois da correcao.
- **A teoria pode voltar depois das questoes.** Medir por zona, nunca supor que o arquivo e
  teoria e depois questao.
- **Titulo que e imagem nao tem camada de texto.** A hipotese de que "sempre sobra fragmento" era
  falsa. Renderizar e olhar e o unico metodo confiavel, nao o ultimo recurso.
- **Pagina e sempre a do arquivo PDF**, nunca a impressa na folha nem a do sumario.

## 22/08/2026 — a marca d'agua esta na CAMADA DE TEXTO

O PDF do Estrategia carrega, em quase toda pagina, uma linha com **CPF e nome do titular da
conta**:

```
02055447114 - Gisilene Tatianne Santos de Lima
```

Medido: **124 das 125 paginas** de "Aula 00 - Regime Juridico-Administrativo e Principios LS".

**Isso quebra o `hash_teoria` se nao for tratado.** O hash existe para dizer que dois cursos tem a
mesma teoria e portanto compartilham Cod Mestre. Com a marca dentro do texto, o mesmo conteudo
baixado por **contas diferentes** gera hashes diferentes, e a regra falha **em silencio** — o
sistema simplesmente deixa de reconhecer que sao o mesmo topico.

**A regra:** normalizar antes de qualquer processamento de texto — remover a linha de marca
(padrao `<CPF> - <Nome>`) e, em geral, **tudo que varia por conta ou por download**.

Vale para o hash, para as ancoras de prosa e para qualquer extracao. O detector de titulos por
tamanho de fonte nao sofre, porque a marca e pequena, mas as ancoras de prosa sofreriam.

**Nao invalida o hash como conceito**, so exige a normalizacao antes.

### Junto disso: o hash do ARQUIVO nao serve para nada

Descoberto pela sessao das skills de download em 22/08: o PDF vem **marcado por download**. Quatro
downloads do mesmo arquivo deram quatro hashes diferentes, com o tamanho variando ~100 bytes
(90.153 / 90.183 / 90.224 / 90.274).

Entao hash de arquivo daria **falso positivo de mudanca em toda execucao**. A assinatura de
mudanca passa a ser: **nome do arquivo no CDN** (identidade) + numero de paginas + tamanho
aproximado (tolerancia de ~1 KB) + data da capa do PDF.
