# Mapeamento de aulas e composição de cadernos

Código que sobreviveu ao teste de aprendizado de 20 e 21/08/2026. Estava numa pasta
temporária de sessão e foi trazido para cá para não se perder no recomeço.

> **Nada aqui é skill ainda.** São as peças validadas que a skill vai usar. As decisões de
> negócio estão na memória; aqui está o que funciona na prática, com os limiares já medidos.

## A cadeia, na ordem

| Arquivo | O que faz |
|---|---|
| `mapear_generico.py` | Lê os PDFs de uma disciplina e devolve as zonas de teoria e os títulos. É a base de tudo. |
| `nivel2.py` | Acha o subtítulo entre um par de linhas roxas. Só necessário onde corpo e título têm o mesmo tamanho de fonte. |
| `caixa.py` | Title Case do projeto: palavra-chave maiúscula, ligação minúscula, sigla em caixa alta. |
| `gerar_blocos.py` | Corta a aula em blocos de 5 a 12 páginas, sempre em ponto de título. |
| `publicar_multi.py` | Escreve a planilha da base. |
| `compor_cadernos.py` | Distribui as questões de cada ponto entre os 7 níveis, priorizando cobertura. |
| `schema_fichamento.py` | Cria as abas do banco de fichamento com as colunas que o BIZURITO exige. |
| `validar_cache.py` | Reconfere o cache por amostragem. Já pegou uma regressão real. |
| `densidade.py` | Mede quanto de cada bloco é caixa de questão, por área. |

## Dados de apoio (leitura visual feita à mão)

`faixas_lidas.py` · `faixas_lidas_disc.py` · `titulos_imagem_lidos.py` — as transcrições dos
títulos que são **imagem** e não têm camada de texto. Foram 160 em Direito Administrativo e 17
em Controle Externo, lidos um a um em folhas de contato. **Não regenerar sem necessidade.**

`edital.py` — o programa de Direito Administrativo do TCDF/ANACE 2026 e o mapa aula → item.

## Ordem de execução

```bash
python mapear_generico.py "<pasta da disciplina>" "mapa_<slug>.json"
python nivel2.py            # só se a disciplina precisar
python gerar_blocos.py
python publicar_multi.py
```

## Armadilhas que já custaram retrabalho

Estão todas na memória, em `project_detector_tipografico_titulos_estrategia`. As três que mais
voltaram:

1. **Nunca testar negrito.** O flag é invertido entre safras e há títulos em `Montserrat Medium`,
   que não tem "Bold" no nome. Só o tamanho vale.
2. **A faixa pode vir numerada** (`6. LISTA DE QUESTÕES`). Remover o prefixo antes de casar,
   senão a teoria vai até a última página do arquivo.
3. **Título numerado é legítimo** (`1 - Conceitos Introdutórios`). Testar `isupper()` no
   primeiro caractere descarta todos.

## O que ainda falta

- A base de questões do TecConcursos (o fichamento). Sem ela, `compor_cadernos.py` não roda.
- A comparação bloco a bloco entre pacotes.
- Empacotar tudo isso como skill.
