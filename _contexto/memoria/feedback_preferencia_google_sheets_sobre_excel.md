---
name: feedback_preferencia_google_sheets_sobre_excel
description: "Ao criar qualquer planilha, usar Google Sheets nativo (via gspread) como padrão em vez de gerar um arquivo .xlsx local — só recorrer ao Excel se o Sheets não for possível."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9171338f-adf6-4abf-a949-98ec12c55576
  modified: 2026-08-18T12:38:06.268Z
---

Quando o usuário pedir pra criar uma planilha, o padrão é gerar um **Google
Sheets nativo** (via `gspread`, usando as credenciais já configuradas em
`credenciais/google-oauth-client.json` e `credenciais/google-oauth-token.json`
— tem escopo `spreadsheets` e `drive`), não um arquivo `.xlsx` local via
`openpyxl`.

Ver também [[feedback_formatacao_padrao_google_sheets]] pra formatação padrão
a aplicar em toda planilha criada.

**Why:** confirmado pelo Elvis em 2026-08-18 — ele já tinha pedido uma
planilha de metadados (Direito Administrativo), eu gerei um `.xlsx` local
salvo dentro da pasta, e ele corrigiu: queria o arquivo já como Google Sheets
nativo, salvo direto na pasta certa do Drive (usando o ID da pasta via Drive
API, não só um arquivo solto).

**How to apply:**
- Autenticar com `google.oauth2.credentials.Credentials.from_authorized_user_file`
  usando o token em `credenciais/`, escopos `spreadsheets` + `drive`.
- Achar o ID da pasta de destino no Drive navegando a árvore de pastas por
  nome (`drive.files().list` com `mimeType = 'application/vnd.google-apps.folder'`
  e `'<parent_id>' in parents`), replicando o caminho local.
- Criar a planilha com `gc.create(titulo, folder_id=<id da pasta>)` — isso já
  posiciona o arquivo na pasta certa do Drive (aparece localmente como um
  atalho `.gsheet`, sem duplicar conteúdo).
- Se por algum motivo o Sheets não for viável (sem credencial disponível, erro
  de API), aí sim cair pro Excel local — mas isso é exceção, não padrão.

**Pegadinha confirmada em 2026-08-18 — separador de argumento de fórmula:**
as planilhas desse workspace usam locale `pt_BR` (confirmado via
`sh.locale`), que exige **`;` (ponto e vírgula) como separador de argumento
em fórmulas com mais de um argumento** (`=COUNTIF(F7:F54;">0")`), não vírgula
(`=COUNTIF(F7:F54,">0")` dá `#ERROR!`). Fórmulas de um argumento só
(`=COUNTA(A7:A54)`) funcionam com qualquer separador porque não têm separador
nenhum — por isso só os `COUNTIF` quebraram numa planilha onde `COUNTA`
funcionou. **Sempre escrever fórmulas de múltiplos argumentos com `;` desde a
criação**, e depois de qualquer `batch_update`/edição de fórmula, ler de volta
com `value_render_option='FORMATTED_VALUE'` (ou `UNFORMATTED_VALUE`) pra
conferir que não virou `#ERROR!`/`#REF!`/`#NAME?` antes de dar a planilha como
pronta — não existe `recalc.py` (LibreOffice) funcionando nesse ambiente
Windows, então essa é a forma de validar fórmula do Google Sheets aqui.
