---
name: feedback_tudo_portatil_e_encerramento
description: decisao ou aprendizado que so existe na memoria do Claude nao existe; ao encerrar sessao, copiar a memoria para _contexto/memoria/ e sincronizar
metadata:
  type: feedback
---

**O Elvis pode abrir este projeto em outro assistente**, em especial o ChatGPT, e o workspace foi
montado para isso (por isso `AGENTS.md` e a fonte e `CLAUDE.md` so aponta para ele, e por isso
existe a ponte `.agents/skills`).

**Consequencia:** decisao, regra ou aprendizado que so existe dentro da memoria do Claude **nao
existe**. A memoria mora em `~/.claude/projects/.../memory/`, fora do repositorio; quem abre so a
pasta do projeto nao enxerga nada dela, e uma reinstalacao apaga tudo.

**A regra:** a memoria do Claude e **copia de trabalho**; a **fonte de verdade e o repositorio**.

| Onde escrever | O que vai |
|---|---|
| `bases/DECISOES.md` | decisoes fechadas |
| `bases/<n>/APRENDIZADO.md` | licao aprendida naquela base |
| `bases/05-questoes-tec/REGRAS.md` | regras de acesso ao Tec |
| `_contexto/tarefas-mapeamento.md` | lista viva de tarefas |
| `_contexto/memoria/` | copia portatil da memoria |

**Quando o Elvis avisar que vai encerrar, sair, dormir ou fechar o computador**, rodar o
checklist de encerramento do `AGENTS.md`, que agora inclui **copiar a memoria para
`_contexto/memoria/` antes do commit final**. O objetivo dele e explicito: se a maquina
desligar ou o sistema for reinstalado, continuar de onde parou.
