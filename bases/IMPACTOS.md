# Impactos entre bases

> **Toda base, ao terminar, escreve aqui o que ela mexeu nas outras.** E toda base, ao comecar,
> le este arquivo para saber se alguma anterior mudou algo que ela ja usava.
>
> As seis bases se conversam. Sem este registro, a base 2 muda uma regra, a base 1 fica
> desatualizada, e ninguem percebe ate o material chegar torto na mao do aluno.

## Como usar

**Ao terminar uma base**, acrescentar uma secao com:

- o que foi construido
- **o que mudou** em relacao ao que estava decidido
- **qual base isso afeta**, e o que precisa ser ajustado la
- o que ficou pendente

**Ao comecar uma base**, ler daqui para baixo e verificar se ha ajuste pendente que a afete.

**Se uma base ja pronta precisar de ajuste**, fazer o ajuste e registrar aqui tambem. Nao deixar
para depois: base desatualizada contamina tudo que vem em cima dela.

---

## Estado das bases

| Base | Estado | Ultima revisao |
|---|---|---|
| 1 · Disciplinas | nao iniciada | — |
| 2 · Estrategia Concursos | nao iniciada | — |
| 3 · Taxonomia do Tec | nao iniciada | — |
| 4 · Materiais de parceiros | nao iniciada | — |
| 5 · Questoes do Tec | nao iniciada | — |
| 6 · Editais | nao iniciada | — |

---

## Registro

### 22/08/2026 · Sessao das skills de download do Estrategia (pre-base 2)

**O que foi construido:** piloto de levantamento do APOIO do Estrategia (resumo e mapa mental) na
disciplina Direito Constitucional do Regular Fiscal (curso 220880). 42 links, **32 arquivos
distintos** (12 resumos, 20 mapas mentais), 28 MB, presentes em 14 das 22 aulas.

**O que mudou em relacao ao que estava decidido:** descobrimos que resumo e mapa mental **nao sao
da aula, sao de cada VIDEO** dentro dela (campos `resumo` / `mapa_mental` em `videos[]`; rota
`/api/video/{videoId}/download/{tipo}`). A suposicao anterior era que estariam dentro do livro.
Desenho completo em `DECISOES.md`, secao "Apoio do Estrategia: resumo e mapa mental".

**Edicao no arquivo central:** esta sessao escreveu a secao "Apoio do Estrategia" no topo do
`bases/DECISOES.md` em 22/08/2026. Registrado aqui porque duas sessoes escrevendo no arquivo
central ao mesmo tempo perdem decisao.

**Qual base isso afeta:**

- **Base 2 (Estrategia)** — o apoio e tabela secundaria dela. A coleta acontece na fase de
  download; a correlacao apoio -> Cod Mestre fica para a fase de granularidade. Destrava o item
  A39, que estava marcado como bloqueante.
- **Base 1 (Disciplinas)** — o download vai criar, dentro de cada pasta de disciplina, uma
  subpasta de apoio. **Nenhuma pasta de disciplina existente sera renomeada, e o acento nao sera
  normalizado** (os nomes do Regular Fiscal continuam sem acento e os do Controle com acento,
  literal como estao). Se algum nome de pasta mudar em execucao futura, o diff contra
  `bases/01-disciplinas/fontes/estrategia.txt` sera registrado aqui.
- **Base 4 (Parceiros)** — a indicacao de resumo do Bezerra tem **prioridade** sobre a do
  Estrategia, e e a unica que pode ser indicada independentemente do curso de origem do bloco.

**Correcao tecnica para quem for implementar:** **hash de arquivo nao serve** nem para deduplicar
nem para detectar mudanca. O PDF do Estrategia e **marcado por download**: o mesmo arquivo baixado
4 vezes deu 4 hashes diferentes, com tamanho variando ~100 bytes. A identidade e o **nome do
arquivo no CDN**; a assinatura de mudanca deve ser **nome no CDN + n de paginas + tamanho
aproximado + data da capa do PDF**.

**Pendente:**

- confirmar o limite de caracteres da Tutory (o texto de indicacao para o aluno depende dele);
- fechar com o Elvis a convencao de pasta e o destino dos arquivos de apoio;
- estender o levantamento as demais disciplinas (~800 MB estimados no pacote inteiro).

