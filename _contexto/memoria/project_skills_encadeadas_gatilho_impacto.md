---
name: project_skills_encadeadas_gatilho_impacto
description: Skill de download alimenta a base 2; ao rodar `atualizar` ela avisa que as bases em cima precisam ser reprocessadas
metadata:
  type: project
---

Decidido pelo Elvis em 22/08/2026. As skills do projeto **não são independentes**: o download do
Estratégia alimenta a base 2, que alimenta o mapeamento, que alimenta os cadernos.

Por isso o modo `atualizar` de qualquer skill de download **termina perguntando** se é pra rodar
também a skill da base que consome aquele material, e já trazer os impactos.

**Why:** material atualizado sem reprocessar a base deixa a base mentindo — ela aponta para
páginas e blocos que mudaram de lugar. O erro só aparece lá na frente, num caderno com tópico
errado, quando já não dá para saber de onde veio.

**How to apply:** a máquina já existe, é o `bases/IMPACTOS.md`: toda base escreve nele o que mudou
ao terminar e lê dele ao começar. O gatilho é só a skill escrever lá e perguntar. Ver
[[project_arquitetura_bases_e_link_imutavel]] e [[feedback_lembrar_syncar_apos_skill]].

**A planilha de metadados é o contrato entre as duas.** Ela responde "o que existe" (aula,
`curso_id`, LS/LC, páginas, conferido em); a base 2 responde "o que tem dentro" (blocos, tópicos,
âncoras). A base 2 **lê a planilha** para saber o que mapear. Como planilha publicada é vista e
nunca fonte, a skill grava também um `_manifesto.csv` na pasta da disciplina: o CSV é o que a base
2 lê, a planilha é o que o Elvis lê.
