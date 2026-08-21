# Memória do projeto — cópia portátil

Estes arquivos são a **memória de trabalho do Claude**, copiada para dentro do repositório para
que **qualquer assistente** (ChatGPT, Codex, ou outra sessão do Claude) consiga retomar o
trabalho sem depender da instalação local.

## Por que existe

A memória original mora em `~/.claude/projects/.../memory/`, **fora do repositório**. Quem abre
só a pasta do projeto não a enxerga. Se a máquina reinstalar, o conhecimento se perde.

## A regra

| | |
|---|---|
| Cópia de trabalho | `~/.claude/.../memory/` — é onde o Claude escreve no dia a dia |
| **Cópia portátil** | **esta pasta** — sincronizada no encerramento de cada sessão |

**Ao encerrar sessão, sincronizar as duas.** Está no checklist de encerramento do `AGENTS.md`.

## Como ler

Cada arquivo é um fato, com cabeçalho dizendo o tipo:

- `user` — quem é o Elvis, o que ele prefere
- `feedback` — correções e orientações de como trabalhar, com o porquê
- `project` — decisões e contexto do trabalho em andamento
- `reference` — ponteiros para material externo

`MEMORY.md` é o índice. Referências entre arquivos aparecem como `[[nome-do-arquivo]]`.

## Onde estão as outras fontes

| Assunto | Onde |
|---|---|
| Decisões fechadas do projeto | `bases/DECISOES.md` |
| Regras de acesso ao TecConcursos | `bases/05-questoes-tec/REGRAS.md` |
| Aprendizado por base | `bases/*/APRENDIZADO.md` |
| Lista viva de tarefas | `_contexto/tarefas-mapeamento.md` |
| Instruções do workspace | `AGENTS.md` |
