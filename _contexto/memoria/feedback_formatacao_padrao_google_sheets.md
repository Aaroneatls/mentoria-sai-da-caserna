---
name: feedback_formatacao_padrao_google_sheets
description: "Formatação padrão a aplicar sempre que criar ou editar uma planilha no Google Sheets: alinhamento centralizado (horizontal e vertical), quebra de texto ativada, e remoção das colunas não utilizadas."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9171338f-adf6-4abf-a949-98ec12c55576
  modified: 2026-08-18T12:33:58.549Z
---

Sempre que criar ou formatar uma planilha no Google Sheets (não Excel local —
ver [[feedback_preferencia_google_sheets_sobre_excel]]), aplicar por padrão:

1. **Alinhamento centralizado** em todo o texto — horizontal e vertical.
2. **Quebra de texto ativada** ("ajuste de texto") nas células com conteúdo
   mais longo, pra não cortar visualmente.
3. **Remover o excesso de colunas e linhas em branco, mas com cautela** —
   apagar (não só ocultar) o excedente padrão da planilha nova (geralmente
   até a coluna Z e a linha 1000), só que:
   - **Colunas:** nunca apagar uma coluna que já tenha algum dado, nem cortar
     rente à última coluna usada — deixar uma pequena margem (2-3 colunas
     vazias) depois do fim da tabela, caso precise acrescentar campo novo
     depois.
   - **Linhas:** o mesmo raciocínio — pode cortar o excesso de milhares de
     linhas em branco padrão, mas deixar uma margem de algumas dezenas de
     linhas depois do fim dos dados (não cortar rente à última linha usada),
     pra sobrar espaço pra novas aulas serem lançadas sem precisar reinserir
     linha toda vez.
4. **Largura de coluna ajustada pro conteúdo, nunca a largura padrão apertada**
   — dimensionar cada coluna pra caber o texto confortavelmente na tela sem
   parecer espremido (colunas de texto curto/rótulo mais estreitas, colunas de
   texto longo/explicação bem mais largas). Não deixar a largura genérica
   padrão do Sheets quando o conteúdo claramente não cabe nela.

**Why:** confirmado pelo Elvis em 2026-08-18, testando a primeira planilha de
metadados (Direito Administrativo). Ele fez questão de mostrar exatamente esse
padrão de formatação ao vivo antes de eu replicar pras outras disciplinas —
é o "acabamento" que ele espera em qualquer planilha entregue, não só nessa
específica.

**How to apply:** rodar essa formatação como parte do próprio script de
criação da planilha (via `gspread`/Sheets API), não como um passo manual
separado depois — always ligar `wrapStrategy: WRAP` e
`horizontalAlignment/verticalAlignment: CENTER` no range de dados, e
deletar (`deleteDimension`) as colunas sobrando além da última usada.
