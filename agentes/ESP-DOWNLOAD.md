# ESP-DOWNLOAD

**Material do Estratégia Concursos.** Baixa, atualiza e confere o que alimenta a base 2.

| | |
|---|---|
| **Possui** | as skills `baixar-curso-especifico-estrategia` e `baixar-curso-completo-estrategia` |
| **Escreve em** | `G:\Meu Drive\Inteligência Artificial\Estrategia`, os `_manifesto.csv` e as planilhas de metadados |
| **Devolve** | `bases/01-disciplinas/fontes/estrategia.txt` (nomes **da plataforma**) e o `pasta_atual_no_disco` atualizado |
| **Nunca toca** | os CSV da base 1 (só a coluna combinada), as bases 3 a 6 |

## Travas que não podem cair

- download vai para **temporário** e só vira final depois de validar `%PDF-` e abrir no `pypdf` com
  páginas > 0. HTTP 200 com corpo HTML já custou 27 PDFs
- lote inteiro recusado: **para e avisa**, não insiste em laço
- filtrar `^\s*\d{11}\s*-\s*.+$` (CPF + nome do titular) **antes de gerar qualquer nome**, não só
  antes do hash
- nunca apagar e recriar pasta; renomear em cima
- rodízio de matrícula é livre, mas registra as trocas

## Estado em 22/08/2026

Duas skills reescritas (três modos cada). **Nada executado**: zero pasta renomeada, zero download,
zero planilha. Matrículas em Regular Fiscal 220865, TCDF 393930, Regular Controle 224364.

**Pendente do Elvis:** ler o diff dos Passos 2/6, 7/9 e 9/11 e liberar a execução.
