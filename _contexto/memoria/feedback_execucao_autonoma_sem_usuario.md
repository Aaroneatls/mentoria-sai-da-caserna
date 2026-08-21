---
name: feedback_execucao_autonoma_sem_usuario
description: "Quando o Elvis avisa que vai ficar fora da sessão por um tempo, seguir executando as tarefas sem parar pra perguntar — tomar a decisão mais razoável em cada dúvida e reportar tudo no final pra ele ratificar."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9171338f-adf6-4abf-a949-98ec12c55576
  modified: 2026-08-18T00:12:01.363Z
---

Quando o usuário disser algo como "vou sair da sessão", "volto daqui a
algumas horas", "não vou estar por perto" — e pedir pra continuar as tarefas
mesmo assim — mudar de modo: em vez de parar pra perguntar a cada dúvida,
tomar a decisão mais razoável sozinho (seguindo os padrões já estabelecidos:
convenções da skill em uso, memórias salvas, contexto da conversa) e seguir
executando.

**Why:** o usuário não vai estar disponível pra responder perguntas em tempo
real nesse período, e prefere que o trabalho continue avançando a ficar
travado esperando confirmação. Ele explicitamente prefere revisar decisões
depois a ser interrompido durante.

**How to apply:**
- Guardar um registro simples de cada dúvida/decisão não-trivial tomada
  durante a execução autônoma (o quê, qual decisão, por quê).
- Ao final da tarefa (ou quando o usuário voltar), apresentar esse resumo:
  o que foi feito + as dúvidas/decisões tomadas, pra ele ratificar ou pedir
  retificação.
- Isso vale só pro período em que ele avisou que ia ficar fora — não é uma
  licença permanente pra parar de perguntar em qualquer situação. Decisões
  realmente irreversíveis/destrutivas (apagar dado, ação financeira, etc)
  continuam exigindo cautela mesmo nesse modo — nesse caso, é melhor optar
  pela alternativa mais conservadora/reversível e registrar isso no resumo,
  em vez de arriscar.
