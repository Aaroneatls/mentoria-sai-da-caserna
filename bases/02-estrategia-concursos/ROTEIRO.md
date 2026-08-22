# Roteiro — Base 2 - Estrategia Concursos

> **Abra este arquivo primeiro.** Ele existe para que uma sessao nova comece sabendo o que ja foi
> decidido, o que ja existe e por onde pegar. Leia junto com `../DECISOES.md` (decisoes fechadas)
> e `APRENDIZADO.md` (licoes, que crescem).

Criado em 21/08/2026, na sessao que fechou o Bloco 1 de decisoes.

## O que esta base entrega

Os **blocos de estudo** cortados dos PDFs do Estrategia: onde o aluno estuda cada topico, com a
pagina de inicio e de fim, literais do arquivo.

E a base que produz o `INICIE EM` e o `TERMINE EM` que vao para a Referencia do aluno na Tutory,
e e dela que sai a maior parte dos Cod Mestre.

## Os tres modos da skill

| Modo | O que faz | Cuidado |
|---|---|---|
| `criar` | monta do zero | escreve; conferir antes com `conferir` |
| `atualizar` | roda o diff e aplica so o que mudou | nunca sobrescrever o que nao mudou |
| `conferir` | roda as verificacoes **sem escrever nada** | e o modo padrao quando houver duvida |

O modo `conferir` nasceu de um caso real: em 21/08 foi conferindo antes de executar que se
descobriu um filtro faltando, o que teria gasto ~600 chamadas produzindo dado errado.

## Passo a passo

1. **Reconhecimento antes de construir.** Rodar a passada barata que so caracteriza o material:
   tamanho de fonte do corpo e dos titulos, vocabulario das faixas de secao, taxa de
   rasterizacao, onde a teoria comeca e acaba. **Nunca pular este passo** — foi o que mais custou
   retrabalho em 20/08.

2. **Detectar os titulos pela tipografia.** O codigo esta nesta pasta e ja foi validado em 8
   disciplinas. Ver `APRENDIZADO.md` para as tres armadilhas que mais voltaram.

3. **Cortar em blocos de ~10 paginas de teoria**, sempre em ponto de titulo, e **por zona de
   teoria** — a teoria pode voltar depois de um bloco de questoes.

4. **Nomear cada bloco** com o Nome Mestre, no padrao `assunto do edital: subtopicos`.

5. **Gerar `INICIE EM` e `TERMINE EM` literais**, com a pagina **do arquivo PDF**, nunca a
   impressa na folha nem a do sumario.

6. **Calcular o `hash_teoria`** de cada bloco. E ele que diz se dois cursos tem o mesmo conteudo,
   e o que permite compartilhar Cod Mestre entre areas.

7. **Montar a tabela de pares bloco x topico**, mesmo que 95% das linhas fiquem 1 para 1.

8. **Preencher `depende de`** (pre-requisito) por duas fontes baratas: a ordem do curso e as
   **referencias cruzadas no texto** ("conforme estudamos na aula anterior"). Padrao e **livre**;
   so marcar com evidencia.

9. **Atribuir o Cod Mestre** consumindo o contador da base 1.

10. **Publicar a planilha** e pedir conferencia do Elvis.

## O que ja existe e nao deve ser refeito

Todo o codigo validado esta nesta pasta:

| Arquivo | O que faz |
|---|---|
| `mapear_generico.py` | le os PDFs e devolve zonas de teoria e titulos. E a base de tudo |
| `nivel2.py` | acha subtitulo entre par de linhas roxas, onde corpo e titulo tem o mesmo tamanho |
| `gerar_blocos.py` | corta a aula em blocos, por zona |
| `caixa.py` | Title Case do projeto |
| `densidade.py` | mede quanto de cada bloco e caixa de questao, por area |
| `validar_cache.py` | reconfere o cache por amostragem; ja pegou uma regressao real |

E as **transcricoes feitas a mao**, caras de refazer: `faixas_lidas.py`, `faixas_lidas_disc.py` e
`titulos_imagem_lidos.py`, com 177 titulos que sao imagem e nao tem camada de texto, lidos um a
um em folhas de contato. **Nao regenerar sem necessidade.**

## Perguntas em aberto

1. **O alvo mudou de 12 para ~10 paginas.** Os 449 blocos da sessao antiga foram cortados com 12,
   entao **vao mudar**. E esperado, e confirma que o mapeamento e para refazer, nao para migrar.

2. **Auditoria Governamental tem secoes de 12 a 14 paginas sem subdivisao.** Ja foi decidido
   aceitar, porque nao ha titulo onde cortar. Com o alvo de 10, o desvio fica mais visivel.

3. **Administracao Publica precisa do detector de nivel 2**, porque corpo e titulo usam o mesmo
   tamanho de fonte.

4. **Qual curso mapear primeiro dentro da disciplina?** O Regular manda sempre; o especifico so
   completa. Mas a ordem entre Regular Fiscal e Regular Controle importa para o cruzamento.

## Sugestao de por onde comecar

Comecar por **Direito Administrativo**, por dois motivos: e onde o Elvis tem mais expertise para
validar, e e a unica disciplina onde o detector ja foi provado.

Rodar o passo 1 (reconhecimento) mesmo ja conhecendo a disciplina — o alvo mudou, e a
caracterizacao e barata.

**Nao toca no Tec.** Pode rodar em paralelo com a coleta.
