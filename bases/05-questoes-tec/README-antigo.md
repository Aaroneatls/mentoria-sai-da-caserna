# Coleta TecConcursos

Projeto **separado** do de tratamento, por decisão do Elvis em 21/08/2026. Aqui só se
constrói o banco. Fichamento, cadernos, Ouro e BIZURITO ficam no outro lado e **não tocam
no Tec**.

## Por que separar

A coleta é lenta e depende de renovação manual da verificação do Tec. Enquanto ela era parte
do mesmo trabalho, cada travada interrompia o desenho. Separada, ela roda parada esperando e
o trabalho que rende segue sem depender dela.

E separa o risco: a conta que coleta é a que apanha. A conta que **gera os cadernos** fica com
tráfego leve, e é ela que sustenta o produto, porque o link do caderno é o que vai pro aluno.

## Regras duras

1. O banco **nunca** entra no git. Fica em `dados/banco-tec/`, já no `.gitignore`.
2. Conteúdo do Tec **não sai** nas entregas: nem enunciado, nem resolução. O aluno recebe
   link de caderno, nome de tópico nosso e texto nosso.
3. O BIZURITO é **escrito**, nunca copiado da resolução.
4. A conta de produção (a dos cadernos) **nunca** é usada para coleta em massa.

## Como o limite do Tec funciona

Medido em 21/08/2026, ver `reference_tec_parametros_de_coleta` na memória:

- O balde é do **cookie**, e enche por **chamada**. Nem tempo nem espera o renovam.
- Rendeu 775 chamadas na primeira renovação, 324 na segunda, 125 na terceira: **está apertando**.
- **Desacelerar não ajuda** e chega a piorar. Rodar rápido.
- Retentar durante o bloqueio é desperdício. Parar e esperar a renovação.
- A renovação é um clique **do Elvis**, na verificação do próprio Tec. Claude não clica.

## Custo

| | Requisições |
|---|---|
| Enunciado das 5.463 | ~5.500 |
| Resolução das que interessam | ~5.500 |
| Conferir anuladas/desatualizadas (mensal) | ~150 |
| **Montar os cadernos (outro projeto)** | ~260 por disciplina |

A checagem de validade usa o truque do censo: filtro em lote por assunto devolve quem
continua válido, e quem sumiu da lista virou desatualizada. Barato o bastante pra rodar sempre.

## Arquivos

| | |
|---|---|
| `banco.py` | esquema e consultas do SQLite |
| `importar.py` | traz pro banco o que o coletor exportou por download |

O coletor em si roda no navegador, guardado em `localStorage['coletor_src']`, e exporta por
download. Rearmar é `eval(localStorage.getItem('coletor_src'))`.
