# O que esta base precisa saber

> Extrato de `../DECISOES.md`, so com o que afeta esta base. O arquivo central continua sendo a
> referencia completa; aqui esta o essencial, para a sessao nao gastar contexto com decisao de
> outra base.

## Antes de qualquer coisa: `REGRAS.md`

Esta na mesma pasta e **vale acima de qualquer conveniencia de execucao**.

## Os filtros da coleta

| Filtro | Valor |
|---|---|
| Area (Carreira) — Controle | **Controladorias + Tribunais de Contas**, sem Gestao Governamental |
| Area (Carreira) — Fiscal | Fiscal |
| **Escolaridade** | **so nivel superior** |
| Limpeza | `REMOVER_ANULADAS`, `REMOVER_DESATUALIZADAS`, `REMOVER_ADAPTADAS_INEDITAS` |
| Bancas | Cebraspe, FGV, FCC |
| Janela de anos | **definida materia a materia**, mirando ~2.500 questoes, teto de 10 anos |

**Filtro por Formacao nao serve:** concurso que **aceita** TI nao e concurso **de** TI.

## Area especializada: imprimir tudo e MARCAR

Nao filtrar na origem. **Imprimir tudo e separar internamente**, marcando **por concurso**, nao por
questao. A lista de concursos se monta sozinha a partir do cabecalho impresso:

```
CEBRASPE (CESPE) - AG (TCE-PE) /TCE PE/Administracao/2017
                    cargo        orgao   area          ano
```

Serve a tres usos: excluir do caderno do aluno, **excluir do caderno de erros** (reforcar no nivel
errado piora), e guardar como ativo para material especializado no futuro.

## Ouro NAO e dificuldade

Questao **facil** pode ser ouro. O rotulo `dificuldade` do Tec e enquadramento **deles**. Ouro e
alto rendimento de revisao, por tres motivos:

1. **Abrangencia** — toca varios pontos numa questao so
2. **Qualidade da resolucao** — o comentario mais completo entre as do mesmo ponto
3. **Representatividade** — quando varias repetem o modelo, a que revisa as outras

**Ouro nao se le da API**: sai do fichamento.

## A classificacao vem de LER o enunciado

O assunto do Tec e pista, nunca veredito. **Nao montar caderno para aluno em cima da classificacao
dele.**

## Parametros de tempo das questoes

| | Pre-edital | Reta final |
|---|---|---|
| Certo/errado | **2 min** | **1,5 min** |
| Multipla escolha | **3 min** | **2,5 min** |

O `tempoMedio` do Tec **nao e usado**: custa 1 requisicao por questao e a Tutory arredonda para
multiplos de 30 de qualquer jeito.

## Composicao dos cadernos

- **Cobertura manda**: antes de repetir um ponto, tocar todos os outros
- **Recencia dentro da cota do ponto**, nunca no bolo
- **Repetir entre niveis e permitido e desejado**, mas com **questao diferente** enquanto houver
  acervo — sem rodizio, dois niveis de mesmo escopo saem identicos
- **Inedita vai em caderno separado**: exige plano avancado do aluno
- **Topico sem questao**: registrar e ignorar, nunca puxar de assunto vizinho

---

**Duvida sobre algo que nao esta aqui?** Consulte `../DECISOES.md`.
**Licao aprendida nesta base?** Escreva em `APRENDIZADO.md`, nao aqui.
