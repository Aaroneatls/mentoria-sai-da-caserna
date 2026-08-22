# ESP-QUESTOES · o banco, e o que ele sabe

> **AINDA NÃO ABERTO.** Este cartão existe para o vocabulário existir antes do agente: o Elvis já
> pode dizer "questoes" e qualquer sessão sabe do que se trata. Quando abrir, o coordenador entrega o
> prompt a partir do `agentes/_TEMPLATE.md` e este arquivo passa a ser o cartão vivo.

| | |
|---|---|
| **Abre quando** | existir a conta nova do TecConcursos |
| **Responsabilidade** | o acervo de questões e tudo que se extrai dele: peso, dificuldade, cobertura, redundância |
| **Possuirá** | `bases/05-questoes-tec/` e as skills `coletar-questoes-tec` e `fichar-questoes` |
| **Entrega** | banco fichado, camada de **ponto**, pesos próprios por tópico, Curva ABC |
| **Recebe de** | `ESP-TAXONOMIA` — assunto do Tec → Cód Mestre |
| **Entrega para** | `ESP-PRODUCAO`, `ESP-CONTEUDO` (peso por tópico) e o BIZURITO |

**É o único com risco de derrubar a conta.** Nunca clica CAPTCHA, nunca insiste depois de um 429,
nunca usa a conta de produção para coleta. As regras duras estão em `bases/05-questoes-tec/REGRAS.md`
e valem acima de qualquer pedido — inclusive do Elvis, que já mandou clicar e recebeu não.

**Dimensionar por matéria do Tec é armadilha:** a matéria 69 junta AFO com Contabilidade Pública. O
tamanho se mede pela soma dos assuntos da disciplina.
