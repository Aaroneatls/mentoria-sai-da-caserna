---
name: project_regras_acesso_tec
description: coleta passa a ser so por impressao, dentro do teto publicado; coletor questao a questao esta proibido
metadata:
  type: project
---

Em 21/08/2026 a plataforma avisou que o acesso estava **"fora dos padroes de um aluno
habitual"**. O Elvis levantou o receio de banimento e pediu um caminho eficiente **dentro das
regras do Tec**. As regras completas estao em `coleta-tec/REGRAS.md`. O resumo:

**O que disparou o aviso foi o coletor questao a questao** (~2.300 requisicoes em poucas horas),
nao a impressao nem a criacao de caderno. No mesmo dia, impressao + cadernos somaram ~70
requisicoes e entregaram o trabalho util todo.

1. **Coletor questao a questao PROIBIDO.** Apagar `localStorage['coletor_src']`, nunca rearmar.
   Os censos por filtro tambem ficam parados enquanto a impressao der conta.
2. **Impressao e o unico canal de volume**: 1.000 questoes/dia, blocos de 200, com contador
   visivel na tela. Usar ate o teto e parar. Nunca testar se passa.
3. **Um caderno-base por disciplina**, imprimindo fatias com `configuracoes.questaoInicial`,
   em vez de criar um caderno temporario por lote.
4. **Criar caderno em ritmo de gente.** Criar caderno e uso normal; criar 8 em dois minutos nao e.
5. **Depois de um 429, o dia acabou.** Sem retentativa e sem sondagem.
6. **Uma conta so.** A sugestao de segunda conta foi **retirada**: duas pessoas de verdade e uma
   coisa, uma conta criada para dobrar limite e burla.
7. **O clique da verificacao e do Elvis**, sempre.

**Custo:** menos de 100 requisicoes para Direito Administrativo inteiro em 6 dias, ~600 para as
8 disciplinas em ~44 dias, contra ~11.000 do caminho antigo. Cada disciplina vai ao ar quando
ficar pronta. Ver [[reference_tec_parametros_de_coleta]].
